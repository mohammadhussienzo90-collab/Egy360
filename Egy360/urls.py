# FILE: Egy360/urls.py (main project URLs)
# ============================================================
"""
Main URL Configuration for Egy360 Project

This file wires up all app URLs and creates the complete API structure.

API Structure:
- /api/token/ - JWT token endpoints
- /api/v1/accounts/ - User management
- /api/v1/destinations/ - Cities, attractions, guides
- /api/v1/accommodations/ - Hotels, rooms
- /api/v1/tours/ - Tours, operators, schedules
- /api/v1/transportation/ - Routes, companies (coming soon)
- /api/v1/reviews/ - Reviews and ratings (coming soon)
- /api/v1/blog/ - Blog posts, comments (coming soon)
- /api/v1/bookings/ - Bookings (coming soon)
- /admin/ - Django admin panel
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Import all viewsets from each app
from accounts.views import UserViewSet
from destinations.views import CountryViewSet, CityViewSet, AttractionViewSet, TravelGuideViewSet
from accommodations.views import AccommodationViewSet, RoomViewSet
from tours.views import TourCategoryViewSet, TourOperatorViewSet, TourViewSet, TourScheduleViewSet

# Create a single router for all viewsets
router = DefaultRouter()

# ============================================================
# ACCOUNTS
# ============================================================
router.register(r'accounts/users', UserViewSet, basename='user')

# ============================================================
# DESTINATIONS
# ============================================================
router.register(r'destinations/countries', CountryViewSet, basename='country')
router.register(r'destinations/cities', CityViewSet, basename='city')
router.register(r'destinations/attractions', AttractionViewSet, basename='attraction')
router.register(r'destinations/guides', TravelGuideViewSet, basename='guide')

# ============================================================
# ACCOMMODATIONS
# ============================================================
router.register(r'accommodations/accommodations', AccommodationViewSet, basename='accommodation')
router.register(r'accommodations/rooms', RoomViewSet, basename='room')

# ============================================================
# TOURS
# ============================================================
router.register(r'tours/categories', TourCategoryViewSet, basename='tour-category')
router.register(r'tours/operators', TourOperatorViewSet, basename='tour-operator')
router.register(r'tours/tours', TourViewSet, basename='tour')
router.register(r'tours/schedules', TourScheduleViewSet, basename='tour-schedule')

# ============================================================
# MAIN URL PATTERNS
# ============================================================
urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API v1 with all routed endpoints
    path('api/v1/', include(router.urls)),

    # Django Rest Framework browsable API login
    path('api-auth/', include('rest_framework.urls')),

    # Add this to your main urls.py
    path('api/v1/blog/', include('blog.urls')),
    ]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ============================================================
# API ENDPOINTS CREATED
# ============================================================
"""
Authentication:
  POST /api/token/ - Get JWT access and refresh tokens
  POST /api/token/refresh/ - Refresh expired access token

Accounts:
  POST /api/v1/accounts/users/register/ - Register new user
  POST /api/v1/accounts/users/login/ - Login user
  GET /api/v1/accounts/users/me/ - Get current user profile
  PUT /api/v1/accounts/users/me/ - Update profile
  POST /api/v1/accounts/users/password_change/ - Change password

Destinations:
  GET /api/v1/destinations/countries/ - List countries
  GET /api/v1/destinations/cities/ - List cities
  GET /api/v1/destinations/attractions/ - List attractions
  GET /api/v1/destinations/guides/ - List travel guides

Accommodations:
  GET /api/v1/accommodations/accommodations/ - List accommodations
  POST /api/v1/accommodations/accommodations/ - Create accommodation
  GET /api/v1/accommodations/accommodations/{id}/ - Get details
  POST /api/v1/accommodations/accommodations/{id}/verify/ - Verify (admin)
  GET /api/v1/accommodations/rooms/ - List rooms

Tours:
  GET /api/v1/tours/categories/ - List tour categories
  GET /api/v1/tours/operators/ - List tour operators
  POST /api/v1/tours/operators/ - Create operator
  GET /api/v1/tours/operators/{id}/ - Get operator details
  POST /api/v1/tours/operators/{id}/verify/ - Verify operator (admin)
  GET /api/v1/tours/tours/ - List tours
  POST /api/v1/tours/tours/ - Create tour
  GET /api/v1/tours/tours/{id}/ - Get tour details
  GET /api/v1/tours/schedules/ - List tour schedules
  POST /api/v1/tours/schedules/ - Create schedule

Admin Panel:
  /admin/ - Django admin interface

Filtering Examples:
  GET /api/v1/tours/tours/?city=1&category=1&difficulty_level=easy
  GET /api/v1/tours/tours/?search=pyramid&ordering=-average_rating
  GET /api/v1/tours/schedules/?tour=1&is_available=true
  GET /api/v1/tours/operators/?is_verified=true&is_safe=true
"""