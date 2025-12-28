# payments/urls.py
"""
Payment URL Configuration

Routes:
- /payments/ - Payment info page
- /payments/checkout/<booking_id>/ - PayMob checkout page
- /payments/success/<booking_id>/ - Payment success page
- /payments/callback/ - PayMob callback/webhook handler
"""
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment info page
    path('', TemplateView.as_view(template_name='payments/list.html'), name='list'),

    # PayMob checkout flow
    path('checkout/<int:booking_id>/', views.payment_checkout, name='checkout'),
    path('success/<int:booking_id>/', views.payment_success, name='success'),

    # PayMob callback (user redirect after payment)
    path('callback/', views.paymob_callback, name='paymob_callback'),

    # Legacy Stripe webhook (kept for reference)
    # path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]