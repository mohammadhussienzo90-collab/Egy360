from django.http import HttpResponse
from django.contrib.auth.models import User
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
            return HttpResponse('{"status":"ok","version":"v6-middleware"}', content_type='application/json', status=200)

        # Setup admin endpoint - create/reset admin user
        if path.startswith('/setup-admin') or path.startswith('/setupadmin') or path.startswith('/admin-setup'):
            try:
                user, created = User.objects.get_or_create(
                    username='admin360',
                    defaults={
                        'email': 'admin@360egy.com',
                        'is_staff': True,
                        'is_superuser': True,
                    }
                )
                user.set_password('Egy360Admin2026!')
                user.save()
                msg = "Admin created!" if created else "Admin password reset!"
                body = f"""<!DOCTYPE html>
<html><body>
<h1>{msg}</h1>
<p>Username: <strong>admin360</strong></p>
<p>Password: <strong>Egy360Admin2026!</strong></p>
<p><a href="/admin/">Click here to go to Admin</a></p>
</body></html>"""
                return HttpResponse(body, content_type='text/html; charset=utf-8', status=200)
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
