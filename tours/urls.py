from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    # Main listing
    path('', views.TourListView.as_view(), name='list'),

    # Filter by type
    path('type/<str:tour_type>/', views.tour_by_type, name='by-type'),

    # Filter by destination
    path('destination/<str:destination>/', views.tour_by_destination, name='by-destination'),

    # Booking endpoint
    path('<slug:slug>/book/', views.book_tour, name='book'),

    # Detail view (must be last due to slug pattern)
    path('<slug:slug>/', views.TourDetailView.as_view(), name='detail'),
]
