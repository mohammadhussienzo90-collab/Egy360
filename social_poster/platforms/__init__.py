"""
Platform client registry for the Egy360 social poster.

Usage::

    from social_poster.platforms import get_client

    client = get_client(social_account)
    result = client.publish_with_retry(caption, image_url, link_url)
"""
from .base import BasePlatformClient, PlatformError, RateLimitError, TokenExpiredError
from .facebook import FacebookClient
from .instagram import InstagramClient
from .pinterest import PinterestClient

_CLIENT_MAP = {
    "pinterest": PinterestClient,
    "facebook": FacebookClient,
    "instagram": InstagramClient,
}


def get_client(social_account):
    """
    Return the appropriate platform client for the given account.

    Parameters
    ----------
    social_account : social_poster.models.SocialAccount
        A model instance with a ``platform`` field (e.g. ``"pinterest"``).

    Returns
    -------
    BasePlatformClient
        An initialised client ready to publish.

    Raises
    ------
    ValueError
        If the account's platform is not supported.
    """
    platform = social_account.platform
    client_cls = _CLIENT_MAP.get(platform)
    if client_cls is None:
        supported = ", ".join(sorted(_CLIENT_MAP))
        raise ValueError(
            f"Unknown platform '{platform}'. Supported platforms: {supported}."
        )
    return client_cls(social_account)


__all__ = [
    "get_client",
    "BasePlatformClient",
    "PlatformError",
    "RateLimitError",
    "TokenExpiredError",
    "PinterestClient",
    "FacebookClient",
    "InstagramClient",
]
