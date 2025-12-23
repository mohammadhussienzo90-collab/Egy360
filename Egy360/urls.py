"""
Egy360 URL Configuration - Complete Version
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from home.views import home as homepage_view
from core.sitemaps import sitemaps

urlpatterns = [
    # SEO - Sitemap and Robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots_txt'),

    # Homepage (uses home app's home view for dynamic content)
    path('', homepage_view, name='homepage'),

    # Admin
    path('admin/', admin.site.urls),

    # Home app (about, contact, FAQ, newsletter, etc.)
    path('', include('home.urls')),

    # Main apps
    path('accommodations/', include('accommodations.urls')),
    path('tours/', include('tours.urls')),
    path('destinations/', include('destinations.urls')),
    path('accounts/', include('allauth.urls')),  # Social auth URLs - must come first
    path('accounts/', include('accounts.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
    path('payments/', include('payments.urls')),
    path('transportation/', include('transportation.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),

    # API endpoints
    path('api/', include('api.urls')),

    # Core app (affiliate tracking, etc.)
    path('', include('core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'home.views.error_404'
handler500 = 'home.views.error_500'
handler403 = 'home.views.error_403'