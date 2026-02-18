"""
Abstract base class for social media platform API clients.

Each platform client inherits from BasePlatformClient and implements
publish_post, refresh_access_token, and validate_credentials.
"""
import logging
import time
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class PlatformError(Exception):
    """Base exception for all platform API errors."""

    def __init__(self, message, platform=None, status_code=None, response_body=None):
        self.platform = platform
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class RateLimitError(PlatformError):
    """Raised when the platform returns a 429 Too Many Requests response."""

    def __init__(self, message, retry_after=None, **kwargs):
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class TokenExpiredError(PlatformError):
    """Raised when the access token has expired or been revoked."""
    pass


# ---------------------------------------------------------------------------
# Base client
# ---------------------------------------------------------------------------

class BasePlatformClient(ABC):
    """
    Abstract base for platform-specific API clients.

    Parameters
    ----------
    social_account : social_poster.models.SocialAccount
        A model instance whose ``.access_token`` property returns the
        already-decrypted token string and whose ``.platform_metadata``
        attribute is a dict of platform-specific configuration
        (board_id, page_id, ig_user_id, app_id, app_secret, etc.).
    """

    MAX_RETRIES = 3
    BASE_DELAY = 2  # seconds

    def __init__(self, social_account):
        self.account = social_account
        self.access_token = social_account.access_token
        self.metadata = social_account.platform_metadata or {}

    # ------------------------------------------------------------------
    # Abstract interface -- every subclass must implement these
    # ------------------------------------------------------------------

    @abstractmethod
    def publish_post(self, caption, image_url, link_url, **kwargs):
        """
        Publish a single post to the platform.

        Returns
        -------
        dict
            Must contain at least ``platform_post_id`` and ``post_url``.
        """

    @abstractmethod
    def refresh_access_token(self):
        """
        Refresh the access token using the platform's OAuth flow.

        Returns
        -------
        dict
            Must contain at least ``access_token`` and optionally
            ``expires_in`` (seconds).
        """

    @abstractmethod
    def validate_credentials(self):
        """
        Verify that the current credentials are still valid.

        Returns
        -------
        bool
            ``True`` if the credentials check succeeds.
        """

    # ------------------------------------------------------------------
    # Retry wrapper with exponential back-off
    # ------------------------------------------------------------------

    def publish_with_retry(self, caption, image_url, link_url, **kwargs):
        """
        Call ``publish_post`` with automatic retry logic.

        * **RateLimitError** -- waits ``retry_after`` seconds (or the
          exponential back-off delay) then retries.
        * **TokenExpiredError** -- refreshes the token once, updates
          ``self.access_token``, and retries.
        * **PlatformError** (generic) -- retries with exponential
          back-off up to ``MAX_RETRIES`` times.

        Returns
        -------
        dict
            The successful response from ``publish_post``.

        Raises
        ------
        PlatformError
            If all retry attempts are exhausted.
        """
        last_exception = None
        token_refreshed = False

        for attempt in range(self.MAX_RETRIES):
            try:
                return self.publish_post(caption, image_url, link_url, **kwargs)

            except RateLimitError as exc:
                last_exception = exc
                wait = exc.retry_after if exc.retry_after else self._backoff_delay(attempt)
                logger.warning(
                    "Rate-limited by %s (attempt %d/%d). Waiting %.1fs.",
                    self.account.platform, attempt + 1, self.MAX_RETRIES, wait,
                )
                time.sleep(wait)

            except TokenExpiredError as exc:
                last_exception = exc
                if token_refreshed:
                    logger.error(
                        "Token refresh already attempted for %s. Giving up.",
                        self.account.platform,
                    )
                    raise
                logger.info(
                    "Token expired for %s. Refreshing and retrying.",
                    self.account.platform,
                )
                refresh_data = self.refresh_access_token()
                self.access_token = refresh_data.get("access_token", self.access_token)
                token_refreshed = True
                # Retry immediately after refresh -- don't sleep.

            except PlatformError as exc:
                last_exception = exc
                wait = self._backoff_delay(attempt)
                logger.warning(
                    "Platform error from %s (attempt %d/%d): %s. Waiting %.1fs.",
                    self.account.platform, attempt + 1, self.MAX_RETRIES, exc, wait,
                )
                time.sleep(wait)

        # All retries exhausted.
        raise PlatformError(
            f"All {self.MAX_RETRIES} publish attempts failed for "
            f"{self.account.platform}: {last_exception}",
            platform=self.account.platform,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _backoff_delay(self, attempt):
        """Return an exponential back-off delay: BASE_DELAY * 2^attempt."""
        return self.BASE_DELAY * (2 ** attempt)
