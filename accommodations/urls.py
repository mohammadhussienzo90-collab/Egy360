from django.urls import path
from . import views

app_name = 'accommodations'

urlpatterns = [
    # Main search/listing
    path('', views.AccommodationSearchView.as_view(), name='search'),

    # Filter by city
    path('city/<str:city>/', views.accommodation_by_city, name='by-city'),

    # Filter by type
    path('type/<str:acc_type>/', views.accommodation_by_type, name='by-type'),

    # Detail view (must be last due to slug pattern)
    path('<slug:slug>/', views.AccommodationDetailView.as_view(), name='detail'),
]
