# accounts/urls.py
from django.urls import path
from django.http import JsonResponse

app_name = 'accounts'

def debug_view(request):
    """Simple debug endpoint - no imports"""
    return JsonResponse({'status': 'ok', 'app': 'accounts', 'test': 'no-views-import'})

def test_import(request):
    """Test what import is failing"""
    errors = []

    try:
        from django.contrib.auth import views as auth_views
    except Exception as e:
        errors.append(f"auth_views: {str(e)}")

    try:
        from . import views
    except Exception as e:
        errors.append(f"views: {str(e)}")

    if errors:
        return JsonResponse({'status': 'error', 'errors': errors})
    return JsonResponse({'status': 'ok', 'message': 'All imports successful'})

# Minimal urlpatterns - no views import at module level
urlpatterns = [
    path('debug/', debug_view, name='debug'),
    path('test-import/', test_import, name='test_import'),
]
