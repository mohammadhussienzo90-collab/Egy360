from django.http import HttpResponse

class HealthCheckMiddleware:
    """Handle health check before any other middleware - bypasses all Django checks"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Use WSGI environ directly to avoid triggering Django's host validation
        path = request.META.get('PATH_INFO', '')
        if path in ['/health/', '/health', '/healthz', '/healthz/']:
            return HttpResponse('{"status":"ok"}', content_type='application/json', status=200)
        return self.get_response(request)
