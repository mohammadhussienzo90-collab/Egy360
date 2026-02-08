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
    path('hotels-search/', views.hotels_search, name='hotels-search'),
    path('insurance/', views.insurance, name='insurance'),
    path('deals/', views.deals, name='deals'),

    # Legal pages
    path('privacy/', views.privacy_policy, name='privacy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('affiliate-disclosure/', views.affiliate_disclosure, name='affiliate-disclosure'),
    path('cookie-policy/', views.cookie_policy, name='cookie-policy'),

    # Social media
    path('links/', views.social_links, name='social-links'),

    # Lead magnet
    path('free-egypt-guide/', views.lead_magnet_page, name='lead-magnet'),

    # Help, Careers, and Search
    path('help/', views.help_center, name='help'),
    path('careers/', views.careers, name='careers'),
    path('search/', views.search, name='search'),

    # Content seeding (admin)
    path('seed-content/', views.seed_all_content, name='seed-content'),

    # API endpoints
    path('api/newsletter/', views.newsletter_subscribe, name='newsletter-subscribe'),
    path('api/lead-magnet/', views.lead_magnet_download, name='lead-magnet-api'),
    path('api/search-autocomplete/', views.search_autocomplete, name='search-autocomplete'),
    path('api/stats/', views.get_platform_stats, name='platform-stats'),
]