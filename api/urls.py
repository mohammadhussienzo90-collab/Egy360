# api/urls.py
from django.urls import path
from django.http import JsonResponse

app_name = 'api'


def api_root(request):
    """API root endpoint listing available endpoints"""
    return JsonResponse({
        'status': 'ok',
        'version': '1.0',
        'message': 'Welcome to Egy360 API',
        'endpoints': {
            'health': '/health/',
            'accommodations': '/accommodations/',
            'tours': '/tours/',
            'destinations': '/destinations/',
            'blog': '/blog/',
        },
        'documentation': 'API documentation coming soon'
    })


urlpatterns = [
    path('', api_root, name='root'),
]