"""Egy360 URL Configuration"""
import os
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
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist

    result = {'status': 'checking'}

    # Check DEBUG setting
    from django.conf import settings
    result['DEBUG'] = settings.DEBUG
    result['DEBUG_env'] = os.environ.get('DEBUG', 'not set')

    # Check database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        result['database'] = 'connected'
    except Exception as e:
        result['database'] = f'error: {str(e)}'

    # Check tours
    try:
        from tours.models import Tour
        result['tours_count'] = Tour.objects.count()
        result['active_tours'] = Tour.objects.filter(is_active=True).count()
    except Exception as e:
        result['tours_error'] = str(e)

    # Check accommodations
    try:
        from accommodations.models import Accommodation
        result['accommodations_count'] = Accommodation.objects.count()
        result['active_accommodations'] = Accommodation.objects.filter(is_active=True).count()
    except Exception as e:
        result['accommodations_error'] = str(e)

    # Check templates exist
    templates_to_check = ['base.html', 'tour_listing.html', 'accommodation_search.html',
                          'includes/travelpayouts_widgets.html']
    result['templates'] = {}
    for tpl in templates_to_check:
        try:
            get_template(tpl)
            result['templates'][tpl] = 'found'
        except TemplateDoesNotExist:
            result['templates'][tpl] = 'NOT FOUND'
        except Exception as e:
            result['templates'][tpl] = f'error: {str(e)}'

    # Test rendering tours template with context
    try:
        from tours.models import Tour
        from django.template import Context
        template = get_template('tour_listing.html')
        tours = Tour.objects.filter(is_active=True)[:5]
        # Just check that we can access tour properties
        if tours:
            first_tour = tours[0]
            result['sample_tour'] = {
                'name': first_tour.name,
                'has_tour_type': hasattr(first_tour, 'tour_type'),
                'has_get_tour_type_display': hasattr(first_tour, 'get_tour_type_display'),
            }
    except Exception as e:
        result['template_render_error'] = f'{type(e).__name__}: {str(e)}'

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
