# core/middleware/__init__.py
"""
Security Middleware for Egy360

Adds Content Security Policy and other security headers.
"""

import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ContentSecurityPolicyMiddleware:
    """
    Middleware to add Content-Security-Policy headers.

    CSP helps prevent XSS attacks by specifying which sources
    of content are allowed to be loaded.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Build CSP directives
        self.csp_directives = self._build_csp()

    def _build_csp(self):
        """Build the Content Security Policy string."""

        # Base CSP directives for Egy360
        directives = {
            # Default source for anything not specified
            "default-src": ["'self'"],

            # Scripts - allow self, inline (for legacy), and trusted CDNs
            "script-src": [
                "'self'",
                "'unsafe-inline'",  # Required for inline scripts (minimize usage)
                "'unsafe-eval'",    # Required for some JS libraries (minimize usage)
                "https://www.googletagmanager.com",
                "https://www.google-analytics.com",
                "https://js.stripe.com",
                "https://tpembars.com",
                "https://cdn.travelpayouts.com",
                "https://www.travelpayouts.com",
                "https://cdnjs.cloudflare.com",
                "https://cdn.jsdelivr.net",
            ],

            # Styles - allow self, inline, and trusted CDNs
            "style-src": [
                "'self'",
                "'unsafe-inline'",  # Required for inline styles
                "https://fonts.googleapis.com",
                "https://cdnjs.cloudflare.com",
                "https://cdn.jsdelivr.net",
            ],

            # Images - allow self, data URIs, and trusted sources
            "img-src": [
                "'self'",
                "data:",
                "blob:",
                "https:",  # Allow images from HTTPS sources
                "https://res.cloudinary.com",
                "https://www.google-analytics.com",
                "https://www.googletagmanager.com",
            ],

            # Fonts - allow self and Google Fonts
            "font-src": [
                "'self'",
                "data:",
                "https://fonts.gstatic.com",
                "https://cdnjs.cloudflare.com",
            ],

            # Connect (AJAX, WebSocket, etc.)
            "connect-src": [
                "'self'",
                "https://www.google-analytics.com",
                "https://api.stripe.com",
                "https://tpembars.com",
                "https://www.travelpayouts.com",
            ],

            # Frames - allow trusted embeds
            "frame-src": [
                "'self'",
                "https://js.stripe.com",
                "https://www.youtube.com",
                "https://www.google.com",  # reCAPTCHA
                "https://tp.media",
                "https://www.travelpayouts.com",
            ],

            # Object/embed - block by default
            "object-src": ["'none'"],

            # Base URI - restrict base tag
            "base-uri": ["'self'"],

            # Form actions - allow self
            "form-action": ["'self'"],

            # Frame ancestors - who can embed us
            "frame-ancestors": ["'self'"],

            # Upgrade insecure requests
            "upgrade-insecure-requests": [],
        }

        # Allow overriding via settings
        custom_directives = getattr(settings, 'CSP_DIRECTIVES', {})
        directives.update(custom_directives)

        # Build the CSP string
        csp_parts = []
        for directive, sources in directives.items():
            if sources:
                csp_parts.append(f"{directive} {' '.join(sources)}")
            else:
                csp_parts.append(directive)

        return "; ".join(csp_parts)

    def __call__(self, request):
        response = self.get_response(request)

        # Add CSP header
        # Use Content-Security-Policy-Report-Only for testing
        # Change to Content-Security-Policy for enforcement
        csp_header = getattr(settings, 'CSP_HEADER', 'Content-Security-Policy')
        response[csp_header] = self.csp_directives

        # Add additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(self), microphone=()'

        return response


class SecurityHeadersMiddleware:
    """
    Simple middleware to add basic security headers.

    Use this if you don't need full CSP configuration.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Basic security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(self), microphone=()'

        return response
