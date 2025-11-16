from django.urls import path
from . import views

app_name = 'accommodations'

urlpatterns = [
    path('', views.AccommodationSearchView.as_view(), name='search'),
    path('<slug:slug>/', views.AccommodationDetailView.as_view(), name='detail'),
]