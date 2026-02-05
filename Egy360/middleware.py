from django.http import HttpResponse
import traceback
import sys

class HealthCheckMiddleware:
    """Handle health check before any other middleware - bypasses all Django checks"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Use WSGI environ directly to avoid triggering Django's host validation
        path = request.META.get('PATH_INFO', '')
        if path in ['/health/', '/health', '/healthz', '/healthz/']:
            return HttpResponse('{"status":"ok","version":"v5-middleware"}', content_type='application/json', status=200)
        return self.get_response(request)


class ErrorLoggingMiddleware:
    """Log all errors to stdout for debugging"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print(f"ERROR in {request.path}: {e}", file=sys.stderr, flush=True)
            traceback.print_exc(file=sys.stderr)
            raise

    def process_exception(self, request, exception):
        print(f"EXCEPTION in {request.path}: {exception}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        return None
