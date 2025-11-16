# payments/urls.py
from django.urls import path
from django.views.generic import TemplateView

app_name = 'payments'

urlpatterns = [
    path('', TemplateView.as_view(template_name='payments/list.html'), name='list'),
]