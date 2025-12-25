"""Egy360 URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    """Basic health check for Railway"""
    return JsonResponse({'status': 'ok'})

def test_login_template(request):
    """Test rendering login template"""
    try:
        from django.template.loader import get_template
        from django.shortcuts import render
        template = get_template('accounts/login.html')
        return render(request, 'accounts/login.html', {'form': None})
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        })

urlpatterns = [
    path('test-login/', test_login_template, name='test-login'),
    path('health/', health_check, name='health'),
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
