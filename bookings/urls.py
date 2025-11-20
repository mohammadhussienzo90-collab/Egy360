# bookings/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', TemplateView.as_view(template_name='bookings/list.html'), name='list'),
    path('checkout/', views.booking_checkout, name='checkout'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='confirmation'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel'),
]