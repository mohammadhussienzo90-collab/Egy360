"""
Rate Limiting Utilities
Provides decorators for rate limiting views to prevent abuse
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
import time


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    return ip


def rate_limit(requests_per_minute=10, requests_per_hour=100, key_prefix='ratelimit'):
    """
    Rate limiting decorator for views.

    Args:
        requests_per_minute: Maximum requests allowed per minute
        requests_per_hour: Maximum requests allowed per hour
        key_prefix: Prefix for cache keys (use different prefixes for different endpoints)

    Usage:
        @rate_limit(requests_per_minute=5, requests_per_hour=20, key_prefix='login')
        def login_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Only rate limit POST requests (form submissions)
            if request.method != 'POST':
                return view_func(request, *args, **kwargs)

            ip = get_client_ip(request)
            now = int(time.time())

            # Per-minute rate limiting
            minute_key = f"{key_prefix}:minute:{ip}:{now // 60}"
            minute_count = cache.get(minute_key, 0)

            if minute_count >= requests_per_minute:
                return _rate_limit_response(request, "Too many requests. Please wait a minute.")

            # Per-hour rate limiting
            hour_key = f"{key_prefix}:hour:{ip}:{now // 3600}"
            hour_count = cache.get(hour_key, 0)

            if hour_count >= requests_per_hour:
                return _rate_limit_response(request, "Too many requests. Please try again later.")

            # Increment counters
            cache.set(minute_key, minute_count + 1, 60)  # Expires in 60 seconds
            cache.set(hour_key, hour_count + 1, 3600)   # Expires in 1 hour

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator


def _rate_limit_response(request, message):
    """Return appropriate rate limit response based on request type"""
    if request.headers.get('Accept') == 'application/json' or request.content_type == 'application/json':
        return JsonResponse({
            'success': False,
            'error': message,
            'code': 'RATE_LIMITED'
        }, status=429)

    from django.contrib import messages
    messages.error(request, message)
    return render(request, 'accounts/rate_limited.html', {
        'message': message
    }, status=429)


def rate_limit_otp(requests_per_minute=3, requests_per_hour=10):
    """
    Stricter rate limiting specifically for OTP requests.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour,
        key_prefix='otp'
    )


def rate_limit_login(requests_per_minute=5, requests_per_hour=30):
    """
    Rate limiting specifically for login attempts.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour,
        key_prefix='login'
    )


def rate_limit_register(requests_per_minute=3, requests_per_hour=10):
    """
    Rate limiting specifically for registration attempts.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour,
        key_prefix='register'
    )
