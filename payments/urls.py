# payments/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'payments'

urlpatterns = [
    path('', TemplateView.as_view(template_name='payments/list.html'), name='list'),
    path('checkout/<int:booking_id>/', views.payment_checkout, name='checkout'),
    path('success/<int:booking_id>/', views.payment_success, name='success'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]