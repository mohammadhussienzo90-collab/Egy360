"""
URL Configuration for Core App
Includes affiliate tracking, SEO, and utility endpoints
"""
from django.urls import path
from . import views
from . import seo

app_name = 'core'

urlpatterns = [
    # Affiliate tracking
    path('api/track-click/', views.track_affiliate_click, name='track_affiliate_click'),

    # SEO endpoints
    path('sitemap.xml', seo.generate_sitemap, name='sitemap'),
    path('robots.txt', seo.robots_txt, name='robots'),
]
