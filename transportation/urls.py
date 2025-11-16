# transportation/urls.py
from django.urls import path
from . import views

app_name = 'transportation'

urlpatterns = [
    path('', views.TransportationListView.as_view(), name='list'),
    path('<int:pk>/', views.TransportationDetailView.as_view(), name='detail'),
    path('<int:pk>/book/', views.book_transport, name='book'),
]