# bookings/urls.py
from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # My bookings list
    path('', views.my_bookings, name='list'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    # Checkout flow
    path('checkout/<str:booking_type>/<int:item_id>/', views.booking_checkout, name='checkout'),

    # Booking management
    path('<int:booking_id>/', views.booking_detail, name='detail'),
    path('<int:booking_id>/confirmation/', views.booking_confirmation, name='confirmation'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel'),

    # AJAX endpoints
    path('quick-book/', views.quick_book, name='quick_book'),
]
