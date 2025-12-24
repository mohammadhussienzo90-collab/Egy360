# core/throttling.py
"""
Custom API Throttle Classes for Egy360

Provides granular rate limiting for different API endpoints.
"""

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class PaymentRateThrottle(UserRateThrottle):
    """
    Strict rate limiting for payment-related endpoints.
    Only authenticated users should access these.
    """
    scope = 'payment'


class BookingRateThrottle(UserRateThrottle):
    """
    Rate limiting for booking-related endpoints.
    """
    scope = 'booking'


class BurstRateThrottle(AnonRateThrottle):
    """
    Prevents burst requests from anonymous users.
    More restrictive than the default anon rate.
    """
    rate = '10/minute'


class SustainedRateThrottle(AnonRateThrottle):
    """
    Long-term rate limiting for anonymous users.
    """
    rate = '100/hour'


class SearchRateThrottle(AnonRateThrottle):
    """
    Rate limiting for search endpoints to prevent scraping.
    """
    rate = '30/minute'


class ContactRateThrottle(AnonRateThrottle):
    """
    Rate limiting for contact form and messaging endpoints.
    """
    rate = '5/minute'
