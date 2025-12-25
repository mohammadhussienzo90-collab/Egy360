"""
WSGI config for Egy360 project.
"""
import os
import sys

# Add startup logging
print(f"WSGI: Starting with Python {sys.version}", file=sys.stderr)
print(f"WSGI: Current directory: {os.getcwd()}", file=sys.stderr)
print(f"WSGI: DATABASE_URL set: {bool(os.environ.get('DATABASE_URL'))}", file=sys.stderr)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')

try:
    from django.core.wsgi import get_wsgi_application
    print("WSGI: Django import successful", file=sys.stderr)
    application = get_wsgi_application()
    print("WSGI: Application created successfully", file=sys.stderr)
except Exception as e:
    print(f"WSGI: FAILED TO START: {type(e).__name__}: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise
