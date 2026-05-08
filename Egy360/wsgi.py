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

    # Health check bypass
    if path in ['/health/', '/health', '/healthz/', '/healthz']:
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
            ('Content-Length', '15'),
        ])
        return [b'{"status":"ok"}']

    # Setup admin bypass - creates admin user directly
    if path in ['/setup-admin/', '/setup-admin']:
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
            body = f"{msg}<br>User: admin360<br>Pass: Egy360Admin2026!<br><a href='/admin/'>Go to Admin</a>"
            start_response('200 OK', [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body))),
            ])
            return [body.encode()]
        except Exception as e:
            body = f"Error: {str(e)}"
            start_response('500 OK', [
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(body))),
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
