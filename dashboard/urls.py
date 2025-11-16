# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('reviews/', views.my_reviews, name='my_reviews'),
    path('settings/', views.settings_view, name='settings'),
]