"""
URL Configuration for Home App
Handles main pages and utility endpoints
"""

from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    # Health check for Railway
    path('health/', views.health_check, name='health'),

    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('flights/', views.flights, name='flights'),
    path('insurance/', views.insurance, name='insurance'),
    path('deals/', views.deals, name='deals'),

    # Legal pages
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),

    # API endpoints
    path('api/newsletter/', views.newsletter_subscribe, name='newsletter-subscribe'),
    path('api/search-autocomplete/', views.search_autocomplete, name='search-autocomplete'),
    path('api/stats/', views.get_platform_stats, name='platform-stats'),
]