"""
API URL Configuration for Tours App
API endpoints for JSON data (REST Framework)
Path: tours/api_urls.py
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create API router
router = DefaultRouter()

# Register viewsets
router.register(r'tours', api_views.TourViewSet, basename='tour')
router.register(r'categories', api_views.TourCategoryViewSet, basename='tour-category')
router.register(r'operators', api_views.TourOperatorViewSet, basename='tour-operator')

# URL patterns
urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
]

"""
Generated API URLs (accessed via /api/tours/):

Tours:
- GET    /api/tours/tours/
- POST   /api/tours/tours/
- GET    /api/tours/tours/{id}/
- PUT    /api/tours/tours/{id}/
- PATCH  /api/tours/tours/{id}/
- DELETE /api/tours/tours/{id}/

Categories:
- GET    /api/tours/categories/
- GET    /api/tours/categories/{id}/

Operators:
- GET    /api/tours/operators/
- GET    /api/tours/operators/{id}/
"""