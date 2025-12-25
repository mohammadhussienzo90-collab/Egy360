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

urlpatterns = [
    path('health/', health_check, name='health'),
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
