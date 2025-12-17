# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Bookings
    path('bookings/', views.my_bookings, name='bookings'),
    path('bookings/<int:booking_id>/', views.booking_detail, name='booking-detail'),
    path('bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel-booking'),

    # Reviews
    path('reviews/', views.my_reviews, name='reviews'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
