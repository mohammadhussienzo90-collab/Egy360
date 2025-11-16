# reviews/urls.py
from django.urls import path
from django.views.generic import TemplateView

app_name = 'reviews'

urlpatterns = [
    path('', TemplateView.as_view(template_name='reviews/list.html'), name='list'),
]