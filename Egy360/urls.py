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
    except Exception as e:
        result['tours_error'] = str(e)

    # Check accommodations table
    try:
        from accommodations.models import Accommodation
        acc_count = Accommodation.objects.count()
        result['accommodations_count'] = acc_count
    except Exception as e:
        result['accommodations_error'] = str(e)

    # Check if we can render the tour template context
    try:
        from tours.views import TourListView
        from django.test import RequestFactory
        factory = RequestFactory()
        request_test = factory.get('/tours/')
        view = TourListView()
        view.request = request_test
        view.object_list = view.get_queryset()
        context = view.get_context_data()
        result['tour_context_keys'] = list(context.keys())
    except Exception as e:
        result['tour_context_error'] = f'{type(e).__name__}: {str(e)}'
        result['tour_context_traceback'] = traceback.format_exc()

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
