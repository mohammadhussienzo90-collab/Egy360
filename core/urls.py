"""
URL Configuration for Core App
Includes affiliate tracking and utility endpoints
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Affiliate tracking
    path('api/track-click/', views.track_affiliate_click, name='track_affiliate_click'),
]
