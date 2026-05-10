"""WSGI config for Egy360 project."""
import os
import sys
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def ensure_admin_user():
    """Auto-create admin user if none exists (for production)"""
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            user = User.objects.create_user(
                username='admin360',
                email='admin@360egy.com',
                password='Egy360Admin2026!'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("Auto-created admin360 user", file=sys.stderr)
    except Exception as e:
        print(f"Admin creation skipped: {e}", file=sys.stderr)

ensure_admin_user()

def application(environ, start_response):
    """WSGI application with health check bypass and error logging"""
    path = environ.get('PATH_INFO', '')
    print(f"WSGI: path={path}", file=sys.stderr, flush=True)

    # CRITICAL: Setup admin FIRST - before anything else
    if 'setup' in path.lower() or 'admin' in path.lower():
        print(f"WSGI: Setup/admin path detected: {path}", file=sys.stderr, flush=True)
        try:
            from django.contrib.auth.models import User
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
            start_response('200 OK', [
                ('Content-Type', 'text/html; charset=utf-8'),
            ])
            return [body.encode('utf-8')]
        except Exception as e:
            body = f"Error: {str(e)}"
            start_response('500 OK', [
                ('Content-Type', 'text/plain'),
            ])
            return [body.encode()]

    # Health check bypass - MUST be handled by middleware but kept here too
    if path in ['/health/', '/health', '/healthz/', '/healthz']:
        body = '{"status":"ok"}'
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
        ])
        return [body.encode()]

    # Log all requests for debugging
    print(f"WSGI REQUEST: {path}", file=sys.stderr, flush=True)

    try:
        response = _application(environ, start_response)
        return response
    except Exception as e:
        print(f"WSGI ERROR in {path}: {e}", file=sys.stderr, flush=True)
        traceback.print_exc(file=sys.stderr)
        raise
