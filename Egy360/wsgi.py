"""WSGI config for Egy360 project."""
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    """WSGI application with health check bypass"""
    path = environ.get('PATH_INFO', '')
    if path in ['/health/', '/health', '/healthz/', '/healthz']:
        start_response('200 OK', [
            ('Content-Type', 'application/json'),
            ('Content-Length', '15'),
        ])
        return [b'{"status":"ok"}']
    return _application(environ, start_response)
