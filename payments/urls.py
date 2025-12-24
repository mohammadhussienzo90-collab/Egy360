# payments/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'payments'

urlpatterns = [
    path('', TemplateView.as_view(template_name='payments/list.html'), name='list'),
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
]