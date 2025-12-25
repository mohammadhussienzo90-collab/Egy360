"""Egy360 URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

@csrf_exempt
def health_check(request):
    """Basic health check for Railway"""
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def debug_check(request):
    """Diagnostic endpoint to debug 500 errors"""
    import traceback
    result = {'status': 'checking'}

    # Check database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        result['database'] = 'connected'
    except Exception as e:
        result['database'] = f'error: {str(e)}'

    # Check tours table
    try:
        from tours.models import Tour
        tour_count = Tour.objects.count()
        result['tours_count'] = tour_count
        active_tours = Tour.objects.filter(is_active=True).count()
        result['active_tours'] = active_tours
    except Exception as e:
        result['tours_error'] = str(e)

    # Check accommodations table
    try:
        from accommodations.models import Accommodation
        acc_count = Accommodation.objects.count()
        result['accommodations_count'] = acc_count
        active_acc = Accommodation.objects.filter(is_active=True).count()
        result['active_accommodations'] = active_acc
    except Exception as e:
        result['accommodations_error'] = str(e)

    # Test using Django test client for full request cycle
    try:
        from django.test import Client
        client = Client()
        resp = client.get('/tours/')
        result['tours_page_status'] = resp.status_code
        if resp.status_code != 200:
            result['tours_page_content'] = resp.content.decode()[:1000]
    except Exception as e:
        result['tours_page_error'] = f'{type(e).__name__}: {str(e)}'
        result['tours_page_traceback'] = traceback.format_exc()

    try:
        from django.test import Client
        client = Client()
        resp = client.get('/accommodations/')
        result['accommodations_page_status'] = resp.status_code
        if resp.status_code != 200:
            result['accommodations_page_content'] = resp.content.decode()[:1000]
    except Exception as e:
        result['accommodations_page_error'] = f'{type(e).__name__}: {str(e)}'
        result['accommodations_page_traceback'] = traceback.format_exc()

    result['status'] = 'complete'
    return JsonResponse(result)

urlpatterns = [
    path('health/', health_check, name='health'),
    path('debug/', debug_check, name='debug'),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accommodations/', include('accommodations.urls')),
    path('tours/', include('tours.urls')),
    path('destinations/', include('destinations.urls')),
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
    path('payments/', include('payments.urls')),
    path('transportation/', include('transportation.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
