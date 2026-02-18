"""
Pinterest API v5 client for the Egy360 social poster.

Endpoints used
--------------
* POST   /v5/pins              -- create a pin
* POST   /v5/oauth/token       -- refresh an access token
* GET    /v5/user_account      -- validate credentials
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

API_BASE = "https://api.pinterest.com/v5"
TIMEOUT = 30  # seconds


class PinterestClient(BasePlatformClient):
    """Publish pins to a Pinterest board via the v5 REST API."""

    # ------------------------------------------------------------------
    # publish_post
    # ------------------------------------------------------------------

    def publish_post(self, caption, image_url, link_url, **kwargs):
        """
        Create a new pin.

        Parameters
        ----------
        caption : str
            Pin description text.
        image_url : str
            Public URL of the image to attach.
        link_url : str
            Destination URL (with UTM params) when the pin is clicked.
        **kwargs :
            ``title`` -- optional pin title (truncated to 100 chars).
            ``board_id`` -- override the default board from metadata.

        Returns
        -------
        dict
            ``{"platform_post_id": "...", "post_url": "..."}``.
        """
        board_id = kwargs.get("board_id") or self.metadata.get("board_id")
        if not board_id:
            raise PlatformError(
                "board_id is required in platform_metadata for Pinterest.",
                platform="pinterest",
            )

        title = kwargs.get("title", "")[:100]

        payload = {
            "board_id": board_id,
            "title": title,
            "description": caption,
            "link": link_url,
            "media_source": {
                "source_type": "image_url",
                "url": image_url,
            },
        }

        response = requests.post(
            f"{API_BASE}/pins",
            json=payload,
            headers=self._auth_headers(),
            timeout=TIMEOUT,
        )

        self._handle_errors(response)

        data = response.json()
        pin_id = data.get("id", "")
        post_url = f"https://www.pinterest.com/pin/{pin_id}/"

        logger.info("Pinterest pin created: %s", pin_id)
        return {
            "platform_post_id": pin_id,
            "post_url": post_url,
        }

    # ------------------------------------------------------------------
    # refresh_access_token
    # ------------------------------------------------------------------

    def refresh_access_token(self):
        """
        Exchange the refresh token for a new access token.

        Uses HTTP Basic auth with ``app_id:app_secret`` from
        ``platform_metadata``.

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
                "for Pinterest token refresh.",
                platform="pinterest",
            )

        refresh_token = self.account.refresh_token
        if not refresh_token:
            raise TokenExpiredError(
                "No refresh token available for Pinterest account.",
                platform="pinterest",
            )

        response = requests.post(
            f"{API_BASE}/oauth/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(app_id, app_secret),
            timeout=TIMEOUT,
        )

        self._handle_errors(response)

        data = response.json()
        new_token = data.get("access_token", "")
        expires_in = data.get("expires_in")

        # Persist the new token back to the model.
        self.access_token = new_token
        self.account.access_token = new_token
        if expires_in is not None:
            from django.utils import timezone
            from datetime import timedelta
            self.account.token_expiry = timezone.now() + timedelta(seconds=expires_in)
        self.account.save(update_fields=["access_token_encrypted", "token_expiry", "updated_at"])

        logger.info("Pinterest access token refreshed successfully.")
        return {
            "access_token": new_token,
            "expires_in": expires_in,
        }

    # ------------------------------------------------------------------
    # validate_credentials
    # ------------------------------------------------------------------

    def validate_credentials(self):
        """
        Check that the current token is valid by hitting ``/v5/user_account``.

        Returns
        -------
        bool
        """
        try:
            response = requests.get(
                f"{API_BASE}/user_account",
                headers=self._auth_headers(),
                timeout=TIMEOUT,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _auth_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _handle_errors(self, response):
        """Raise an appropriate exception for non-2xx responses."""
        if response.ok:
            return

        status = response.status_code
        try:
            body = response.json()
        except ValueError:
            body = response.text

        if status == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                f"Pinterest rate limit hit: {body}",
                retry_after=int(retry_after) if retry_after else None,
                platform="pinterest",
                status_code=status,
                response_body=body,
            )

        if status == 401:
            raise TokenExpiredError(
                f"Pinterest token expired or invalid: {body}",
                platform="pinterest",
                status_code=status,
                response_body=body,
            )

        raise PlatformError(
            f"Pinterest API error ({status}): {body}",
            platform="pinterest",
            status_code=status,
            response_body=body,
        )
