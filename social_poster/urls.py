from django.urls import path
from . import views

app_name = 'social_poster'

urlpatterns = [
    path('status/', views.queue_status, name='queue_status'),
    path('generate/', views.trigger_generation, name='trigger_generation'),
]
