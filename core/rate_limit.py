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


def rate_limit_password_reset(requests_per_minute=3, requests_per_hour=10):
    """
    Rate limiting specifically for password reset requests.
    """
    return rate_limit(
        requests_per_minute=requests_per_minute,
        requests_per_hour=requests_per_hour,
        key_prefix='password_reset'
    )


# ==============================================================================
# ACCOUNT LOCKOUT
# ==============================================================================

class AccountLockout:
    """
    Track failed login attempts and lock accounts temporarily.

    Usage:
        lockout = AccountLockout()

        # Check if locked before attempting login
        if lockout.is_locked(username, ip):
            return "Account locked"

        # After failed login
        lockout.record_failure(username, ip)

        # After successful login
        lockout.clear_failures(username, ip)
    """

    MAX_FAILURES = 5  # Lock after 5 failed attempts
    LOCKOUT_DURATION = 900  # 15 minutes lockout
    FAILURE_WINDOW = 300  # Track failures within 5 minutes

    def __init__(self, max_failures=None, lockout_duration=None, failure_window=None):
        self.max_failures = max_failures or self.MAX_FAILURES
        self.lockout_duration = lockout_duration or self.LOCKOUT_DURATION
        self.failure_window = failure_window or self.FAILURE_WINDOW

    def _get_key(self, identifier, key_type):
        """Generate cache key for tracking"""
        return f"lockout:{key_type}:{identifier}"

    def is_locked(self, username=None, ip=None):
        """
        Check if account or IP is locked.
        Returns tuple (is_locked, remaining_seconds, reason)
        """
        # Check username lockout
        if username:
            lock_key = self._get_key(username, 'lock')
            lock_time = cache.get(lock_key)
            if lock_time:
                remaining = lock_time - int(time.time())
                if remaining > 0:
                    return True, remaining, 'account'

        # Check IP lockout
        if ip:
            lock_key = self._get_key(ip, 'lock')
            lock_time = cache.get(lock_key)
            if lock_time:
                remaining = lock_time - int(time.time())
                if remaining > 0:
                    return True, remaining, 'ip'

        return False, 0, None

    def record_failure(self, username=None, ip=None):
        """
        Record a failed login attempt.
        Returns tuple (attempts, is_now_locked)
        """
        now = int(time.time())
        total_attempts = 0

        # Track by username
        if username:
            fail_key = self._get_key(username, 'failures')
            failures = cache.get(fail_key, [])

            # Remove old failures outside the window
            failures = [f for f in failures if f > now - self.failure_window]
            failures.append(now)

            cache.set(fail_key, failures, self.failure_window)
            total_attempts = max(total_attempts, len(failures))

            if len(failures) >= self.max_failures:
                self._lock_account(username)

        # Track by IP
        if ip:
            fail_key = self._get_key(ip, 'failures')
            failures = cache.get(fail_key, [])

            failures = [f for f in failures if f > now - self.failure_window]
            failures.append(now)

            cache.set(fail_key, failures, self.failure_window)
            total_attempts = max(total_attempts, len(failures))

            if len(failures) >= self.max_failures:
                self._lock_ip(ip)

        is_locked = total_attempts >= self.max_failures
        return total_attempts, is_locked

    def _lock_account(self, username):
        """Lock an account"""
        lock_key = self._get_key(username, 'lock')
        unlock_time = int(time.time()) + self.lockout_duration
        cache.set(lock_key, unlock_time, self.lockout_duration)

    def _lock_ip(self, ip):
        """Lock an IP address"""
        lock_key = self._get_key(ip, 'lock')
        unlock_time = int(time.time()) + self.lockout_duration
        cache.set(lock_key, unlock_time, self.lockout_duration)

    def clear_failures(self, username=None, ip=None):
        """Clear failure records after successful login"""
        if username:
            cache.delete(self._get_key(username, 'failures'))
            cache.delete(self._get_key(username, 'lock'))
        if ip:
            cache.delete(self._get_key(ip, 'failures'))

    def get_remaining_attempts(self, username=None, ip=None):
        """Get remaining login attempts before lockout"""
        max_attempts = 0
        now = int(time.time())

        if username:
            fail_key = self._get_key(username, 'failures')
            failures = cache.get(fail_key, [])
            failures = [f for f in failures if f > now - self.failure_window]
            max_attempts = max(max_attempts, len(failures))

        if ip:
            fail_key = self._get_key(ip, 'failures')
            failures = cache.get(fail_key, [])
            failures = [f for f in failures if f > now - self.failure_window]
            max_attempts = max(max_attempts, len(failures))

        return self.max_failures - max_attempts


# Global instance for easy use
account_lockout = AccountLockout()


def with_account_lockout(view_func):
    """
    Decorator to add account lockout protection to login views.

    Usage:
        @with_account_lockout
        def login_view(request):
            ...
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return view_func(request, *args, **kwargs)

        ip = get_client_ip(request)
        username = request.POST.get('username', '')

        # Check if locked
        is_locked, remaining, reason = account_lockout.is_locked(username, ip)
        if is_locked:
            minutes = remaining // 60
            message = f"Account locked due to too many failed attempts. Try again in {minutes + 1} minutes."
            return _rate_limit_response(request, message)

        # Execute view
        response = view_func(request, *args, **kwargs)

        # Check if login failed (user still not authenticated after POST)
        if request.method == 'POST' and not request.user.is_authenticated:
            attempts, now_locked = account_lockout.record_failure(username, ip)

            if now_locked:
                from django.contrib import messages
                messages.warning(request,
                    f"Account has been locked for {account_lockout.lockout_duration // 60} minutes "
                    "due to too many failed login attempts."
                )
            elif attempts > 2:
                remaining = account_lockout.max_failures - attempts
                from django.contrib import messages
                messages.warning(request,
                    f"Warning: {remaining} login attempt(s) remaining before account lockout."
                )

        return response

    return wrapper
