"""
API URL Configuration for EGY360
Place this file in: api/api_urls.py (the api folder you have)
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your API views when ready
# from accommodations.views import AccommodationViewSet
# from tours.views import TourViewSet

router = DefaultRouter()

# Register viewsets when ready
# router.register(r'accommodations', AccommodationViewSet, basename='accommodation')
# router.register(r'tours', TourViewSet, basename='tour')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),

    # Add specific endpoints here as needed
]