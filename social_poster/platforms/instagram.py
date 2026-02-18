"""
Instagram Graph API client for the Egy360 social poster.

Instagram publishing goes through the Facebook Graph API and requires
a two-step container flow:

1. POST /{ig_user_id}/media        -- create a media container
2. POST /{ig_user_id}/media_publish -- publish the container

Endpoints used
--------------
* POST  /{ig_user_id}/media          -- create media container
* POST  /{ig_user_id}/media_publish  -- publish container
* GET   /refresh_access_token        -- refresh a long-lived IG token
* GET   /{ig_user_id}                -- validate credentials
"""
import logging

import requests

from .base import (
    BasePlatformClient,
    PlatformError,
    RateLimitError,
    TokenExpiredError,
)

logger = logging.getLogger(__name__)

API_BASE = "https://graph.facebook.com/v19.0"
TIMEOUT = 30  # seconds


class InstagramClient(BasePlatformClient):
    """Publish image posts to Instagram via the Facebook Graph API."""

    # ------------------------------------------------------------------
    # publish_post
    # ------------------------------------------------------------------

    def publish_post(self, caption, image_url, link_url, **kwargs):
        """
        Publish an image post through the two-step container flow.

        Parameters
        ----------
        caption : str
            Post caption text.
        image_url : str
            Public URL of the image to post.
        link_url : str
            Not directly embedded (Instagram does not support link posts),
            but appended to the caption for visibility.
        **kwargs :
            ``hashtags`` -- string of hashtags to append to the caption.
            ``ig_user_id`` -- override the default IG user from metadata.

        Returns
        -------
        dict
            ``{"platform_post_id": "...", "post_url": "..."}``.
        """
        ig_user_id = kwargs.get("ig_user_id") or self.metadata.get("ig_user_id")
        if not ig_user_id:
            raise PlatformError(
                "ig_user_id is required in platform_metadata for Instagram.",
                platform="instagram",
            )

        hashtags = kwargs.get("hashtags", "")
        full_caption = f"{caption}\n\n{hashtags}".strip() if hashtags else caption

        # Step 1 -- create media container.
        container_response = requests.post(
            f"{API_BASE}/{ig_user_id}/media",
            data={
                "image_url": image_url,
                "caption": full_caption,
                "access_token": self.access_token,
            },
            timeout=TIMEOUT,
        )
        self._handle_errors(container_response)

        container_data = container_response.json()
        creation_id = container_data.get("id")
        if not creation_id:
            raise PlatformError(
                f"Instagram media container creation returned no id: {container_data}",
                platform="instagram",
            )

        # Step 2 -- publish the container.
        publish_response = requests.post(
            f"{API_BASE}/{ig_user_id}/media_publish",
            data={
                "creation_id": creation_id,
                "access_token": self.access_token,
            },
            timeout=TIMEOUT,
        )
        self._handle_errors(publish_response)

        publish_data = publish_response.json()
        media_id = publish_data.get("id", "")

        # Attempt to fetch the permalink / shortcode for a nice URL.
        post_url = self._get_permalink(media_id)

        logger.info("Instagram post created: %s", media_id)
        return {
            "platform_post_id": media_id,
            "post_url": post_url,
        }

    # ------------------------------------------------------------------
    # refresh_access_token
    # ------------------------------------------------------------------

    def refresh_access_token(self):
        """
        Refresh a long-lived Instagram token.

        Uses the ``ig_refresh_token`` grant type via
        ``GET /refresh_access_token``.

        Returns
        -------
        dict
            ``{"access_token": "...", "expires_in": ...}``.
        """
        response = requests.get(
            f"{API_BASE}/refresh_access_token",
            params={
                "grant_type": "ig_refresh_token",
                "access_token": self.access_token,
            },
            timeout=TIMEOUT,
        )

        self._handle_errors(response)

        data = response.json()
        new_token = data.get("access_token", "")
        expires_in = data.get("expires_in")

        # Persist the new token.
        self.access_token = new_token
        self.account.access_token = new_token
        if expires_in is not None:
            from django.utils import timezone
            from datetime import timedelta
            self.account.token_expiry = timezone.now() + timedelta(seconds=expires_in)
        self.account.save(update_fields=["access_token_encrypted", "token_expiry", "updated_at"])

        logger.info("Instagram access token refreshed successfully.")
        return {
            "access_token": new_token,
            "expires_in": expires_in,
        }

    # ------------------------------------------------------------------
    # validate_credentials
    # ------------------------------------------------------------------

    def validate_credentials(self):
        """
        Verify credentials by fetching the IG user profile.

        Returns
        -------
        bool
        """
        ig_user_id = self.metadata.get("ig_user_id")
        if not ig_user_id:
            return False

        try:
            response = requests.get(
                f"{API_BASE}/{ig_user_id}",
                params={
                    "fields": "id,username",
                    "access_token": self.access_token,
                },
                timeout=TIMEOUT,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_permalink(self, media_id):
        """
        Fetch the permalink for a published media object.

        Falls back to a generic Instagram URL if the request fails.
        """
        if not media_id:
            return ""

        try:
            response = requests.get(
                f"{API_BASE}/{media_id}",
                params={
                    "fields": "permalink,shortcode",
                    "access_token": self.access_token,
                },
                timeout=TIMEOUT,
            )
            if response.ok:
                data = response.json()
                permalink = data.get("permalink")
                if permalink:
                    return permalink
                shortcode = data.get("shortcode")
                if shortcode:
                    return f"https://www.instagram.com/p/{shortcode}/"
        except requests.RequestException:
            pass

        return f"https://www.instagram.com/"

    def _handle_errors(self, response):
        """Raise an appropriate exception for non-2xx responses."""
        if response.ok:
            return

        status = response.status_code
        try:
            body = response.json()
        except ValueError:
            body = response.text

        error_obj = body.get("error", {}) if isinstance(body, dict) else {}
        fb_code = error_obj.get("code")

        # Rate limiting (code 4 = app-level, code 32 = page-level).
        if status == 429 or fb_code in (4, 32):
            raise RateLimitError(
                f"Instagram rate limit hit: {body}",
                platform="instagram",
                status_code=status,
                response_body=body,
            )

        # Expired or invalid token (code 190).
        if fb_code == 190 or status == 401:
            raise TokenExpiredError(
                f"Instagram token expired or invalid: {body}",
                platform="instagram",
                status_code=status,
                response_body=body,
            )

        raise PlatformError(
            f"Instagram API error ({status}): {body}",
            platform="instagram",
            status_code=status,
            response_body=body,
        )
