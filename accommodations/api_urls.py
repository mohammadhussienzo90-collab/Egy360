"""
API URL Configuration for Accommodations App
API endpoints for JSON data (REST Framework)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    AccommodationTypeViewSet,
    AmenityViewSet,
    AccommodationViewSet,
    RoomViewSet,
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'types', AccommodationTypeViewSet, basename='accommodationtype')
router.register(r'amenities', AmenityViewSet, basename='amenity')
router.register(r'accommodations', AccommodationViewSet, basename='accommodation')
router.register(r'rooms', RoomViewSet, basename='room')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]

"""
Generated API URLs (accessed via /api/accommodations/):

Accommodation Types:
- GET    /api/accommodations/types/
- GET    /api/accommodations/types/{id}/

Amenities:
- GET    /api/accommodations/amenities/
- GET    /api/accommodations/amenities/{id}/

Accommodations:
- GET    /api/accommodations/accommodations/
- POST   /api/accommodations/accommodations/
- GET    /api/accommodations/accommodations/{id}/
- PUT    /api/accommodations/accommodations/{id}/
- PATCH  /api/accommodations/accommodations/{id}/
- DELETE /api/accommodations/accommodations/{id}/
- GET    /api/accommodations/accommodations/search/
- GET    /api/accommodations/accommodations/featured/
- GET    /api/accommodations/accommodations/verified/
- GET    /api/accommodations/accommodations/nearby/
- GET    /api/accommodations/accommodations/{id}/availability/
- GET    /api/accommodations/accommodations/{id}/rooms/
- GET    /api/accommodations/accommodations/{id}/images/

Rooms:
- GET    /api/accommodations/rooms/
- POST   /api/accommodations/rooms/
- GET    /api/accommodations/rooms/{id}/
- PUT    /api/accommodations/rooms/{id}/
- PATCH  /api/accommodations/rooms/{id}/
- DELETE /api/accommodations/rooms/{id}/
- GET    /api/accommodations/rooms/available/
- GET    /api/accommodations/rooms/by_accommodation/
"""