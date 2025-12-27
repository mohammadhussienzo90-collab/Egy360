"""Egy360 URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Basic health check for Railway"""
    return JsonResponse({'status': 'ok'})

def debug_check(request):
    """Debug endpoint to check system status"""
    import traceback
    result = {'status': 'ok', 'checks': {}}

    # Check database
    try:
        from accommodations.models import Accommodation
        acc = Accommodation.objects.filter(is_active=True).first()
        if acc:
            result['checks']['database'] = 'ok'
            result['checks']['accommodation'] = acc.name
            result['checks']['rooms_count'] = acc.rooms.count()
            result['checks']['amenities_count'] = acc.amenities.count()
        else:
            result['checks']['database'] = 'no accommodations found'
    except Exception as e:
        result['checks']['database'] = f'error: {str(e)}'

    # Check templates
    try:
        from django.template.loader import get_template
        get_template('accommodation_detail.html')
        result['checks']['template'] = 'ok'
    except Exception as e:
        result['checks']['template'] = f'error: {str(e)}'

    # Check reviews
    try:
        from reviews.templatetags.review_tags import get_item
        result['checks']['review_tags'] = 'ok'
    except Exception as e:
        result['checks']['review_tags'] = f'error: {str(e)}'

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
