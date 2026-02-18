"""
Facebook Graph API v19.0 client for the Egy360 social poster.

Endpoints used
--------------
* POST  /{page_id}/feed           -- publish a link post to a page
* GET   /oauth/access_token       -- exchange for a long-lived token
* GET   /me                       -- validate credentials
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


class FacebookClient(BasePlatformClient):
    """Publish link posts to a Facebook Page via the Graph API."""

    # ------------------------------------------------------------------
    # publish_post
    # ------------------------------------------------------------------

    def publish_post(self, caption, image_url, link_url, **kwargs):
        """
        Create a link post on the configured Facebook Page.

        Parameters
        ----------
        caption : str
            The post message body.
        image_url : str
            Not directly used (Facebook scrapes OG image from the link),
            but accepted for interface consistency.
        link_url : str
            The URL to share (with UTM params).
        **kwargs :
            ``hashtags`` -- string of hashtags to append to the message.
            ``page_id`` -- override the default page from metadata.

        Returns
        -------
        dict
            ``{"platform_post_id": "...", "post_url": "..."}``.
        """
        page_id = kwargs.get("page_id") or self.metadata.get("page_id")
        if not page_id:
            raise PlatformError(
                "page_id is required in platform_metadata for Facebook.",
                platform="facebook",
            )

        hashtags = kwargs.get("hashtags", "")
        message = f"{caption}\n\n{hashtags}".strip() if hashtags else caption

        payload = {
            "message": message,
            "link": link_url,
            "access_token": self.access_token,
        }

        response = requests.post(
            f"{API_BASE}/{page_id}/feed",
            data=payload,
            timeout=TIMEOUT,
        )

        self._handle_errors(response)

        data = response.json()
        post_id = data.get("id", "")
        # Facebook post IDs have the form "pageId_postId".
        post_url = f"https://www.facebook.com/{post_id}" if post_id else ""

        logger.info("Facebook post created: %s", post_id)
        return {
            "platform_post_id": post_id,
            "post_url": post_url,
        }

    # ------------------------------------------------------------------
    # refresh_access_token
    # ------------------------------------------------------------------

    def refresh_access_token(self):
        """
        Exchange the current short-lived token for a long-lived one.

        Facebook Page tokens obtained via a long-lived *user* token are
        already long-lived and do not expire.  This method supports the
        ``fb_exchange_token`` grant for cases where a short-lived token
        needs to be upgraded.

        Returns
        -------
        dict
            ``{"access_token": "...", "expires_in": ...}``.
        """
        app_id = self.metadata.get("app_id")
        app_secret = self.metadata.get("app_secret")
        if not app_id or not app_secret:
            raise PlatformError(
                "app_id and app_secret are required in platform_metadata "
                "for Facebook token exchange.",
                platform="facebook",
            )

        response = requests.get(
            f"{API_BASE}/oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": app_id,
                "client_secret": app_secret,
                "fb_exchange_token": self.access_token,
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

        logger.info("Facebook access token refreshed successfully.")
        return {
            "access_token": new_token,
            "expires_in": expires_in,
        }

    # ------------------------------------------------------------------
    # validate_credentials
    # ------------------------------------------------------------------

    def validate_credentials(self):
        """
        Verify the token by calling ``GET /me``.

        Returns
        -------
        bool
        """
        try:
            response = requests.get(
                f"{API_BASE}/me",
                params={"access_token": self.access_token},
                timeout=TIMEOUT,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _handle_errors(self, response):
        """Raise an appropriate exception for non-2xx responses."""
        if response.ok:
            return

        status = response.status_code
        try:
            body = response.json()
        except ValueError:
            body = response.text

        # Facebook wraps errors in {"error": {"message": ..., "code": ...}}
        error_obj = body.get("error", {}) if isinstance(body, dict) else {}
        fb_code = error_obj.get("code")

        # Rate limiting (code 4 = app-level, code 32 = page-level).
        if status == 429 or fb_code in (4, 32):
            raise RateLimitError(
                f"Facebook rate limit hit: {body}",
                platform="facebook",
                status_code=status,
                response_body=body,
            )

        # Expired or invalid token (code 190).
        if fb_code == 190 or status == 401:
            raise TokenExpiredError(
                f"Facebook token expired or invalid: {body}",
                platform="facebook",
                status_code=status,
                response_body=body,
            )

        raise PlatformError(
            f"Facebook API error ({status}): {body}",
            platform="facebook",
            status_code=status,
            response_body=body,
        )
