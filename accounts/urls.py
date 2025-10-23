# FILE: accounts/urls.py
# ============================================================
"""
URL Routing for Accounts App

This file maps URLs to views for all user-related endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Create router for automatic CRUD endpoints
router = DefaultRouter()

# Register the UserViewSet with the router
# This automatically creates all CRUD endpoints
router.register(r'users', UserViewSet, basename='user')

# URL patterns for accounts app
urlpatterns = [
    path('', include(router.urls)),
]

# ============================================================
# WHAT THIS CREATES
# ============================================================
"""
When included in main urls.py as:
    path('api/v1/', include('accounts.urls'))

The following endpoints are automatically created:

LIST & CREATE:
  GET /api/v1/users/
  POST /api/v1/users/

RETRIEVE, UPDATE, DELETE:
  GET /api/v1/users/{id}/
  PUT /api/v1/users/{id}/
  PATCH /api/v1/users/{id}/
  DELETE /api/v1/users/{id}/

CUSTOM ACTIONS (from @action decorators in views):
  POST /api/v1/users/register/
  POST /api/v1/users/login/
  GET /api/v1/users/me/
  PUT /api/v1/users/me/
  POST /api/v1/users/password_change/
  POST /api/v1/users/upload_profile_picture/
  GET /api/v1/users/provider_info/

HOW IT WORKS:
1. DefaultRouter examines UserViewSet
2. Finds all @action decorators
3. Automatically creates URLs for them
4. No manual URL mapping needed!
"""