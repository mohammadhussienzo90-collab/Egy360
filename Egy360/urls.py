"""Egy360 URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Basic health check for Railway"""
    return JsonResponse({'status': 'ok', 'version': 'v3-debug'})

def debug_check(request):
    """Debug endpoint to check system status"""
    import sys
    result = {'status': 'ok', 'version': 'v2', 'checks': {}}

    # Step 1: Basic check
    result['checks']['step1_basic'] = 'ok'

    # Step 2: Check database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        result['checks']['step2_db_connection'] = 'ok'
    except Exception as e:
        result['checks']['step2_db_connection'] = str(e)
        return JsonResponse(result)

    # Step 3: Check model import
    try:
        from accommodations.models import Accommodation
        result['checks']['step3_model_import'] = 'ok'
    except Exception as e:
        result['checks']['step3_model_import'] = str(e)
        return JsonResponse(result)

    # Step 4: Check query
    try:
        count = Accommodation.objects.count()
        result['checks']['step4_query'] = f'ok - {count} accommodations'
    except Exception as e:
        result['checks']['step4_query'] = str(e)
        return JsonResponse(result)

    # Step 5: Check template
    try:
        from django.template.loader import get_template
        t = get_template('accommodation_detail.html')
        result['checks']['step5_template'] = 'ok'
    except Exception as e:
        result['checks']['step5_template'] = str(e)
        return JsonResponse(result)

    # Step 6: Check review tags
    try:
        from reviews.templatetags.review_tags import get_item
        result['checks']['step6_review_tags'] = 'ok'
    except Exception as e:
        result['checks']['step6_review_tags'] = str(e)

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
    path('auth/', include('allauth.urls')),  # Social auth URLs
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
