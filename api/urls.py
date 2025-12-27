# api/urls.py
from django.urls import path
from django.http import JsonResponse
from core.views import track_affiliate_click

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
            'track-click': '/api/track-click/',
        },
        'documentation': 'API documentation coming soon'
    })


urlpatterns = [
    path('', api_root, name='root'),
    path('track-click/', track_affiliate_click, name='track_affiliate_click'),
]