"""
Egy360 URL Configuration - Complete Version
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def homepage_view(request):
    """Render the main homepage template"""
    return render(request, 'home.html')

urlpatterns = [
    # Homepage
    path('', homepage_view, name='homepage'),

    # Admin
    path('admin/', admin.site.urls),

    # Home app (about, contact, FAQ, newsletter, etc.)
    path('', include('home.urls')),

    # Main apps
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

    # API endpoints
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)