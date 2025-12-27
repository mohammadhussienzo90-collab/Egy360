# api/urls.py
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from core.views import track_affiliate_click
from payments.views import PaymentViewSet, PaymentMethodViewSet, PaymentRefundViewSet

app_name = 'api'

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payment-methods', PaymentMethodViewSet, basename='payment-method')
router.register(r'refunds', PaymentRefundViewSet, basename='refund')


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
            'payments': '/api/payments/',
            'payment-methods': '/api/payment-methods/',
            'refunds': '/api/refunds/',
        },
        'documentation': 'API documentation coming soon'
    })


urlpatterns = [
    path('', api_root, name='root'),
    path('track-click/', track_affiliate_click, name='track_affiliate_click'),
] + router.urls