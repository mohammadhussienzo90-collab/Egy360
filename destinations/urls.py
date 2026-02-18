# destinations/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'destinations'

# API Router
router = DefaultRouter()
router.register(r'api/countries', views.CountryViewSet)
router.register(r'api/cities', views.CityViewSet)
router.register(r'api/attractions', views.AttractionViewSet)
router.register(r'api/guides', views.TravelGuideViewSet)

urlpatterns = [
    # Template Views
    path('', views.destinations_list, name='list'),
    path('city/<slug:slug>/', views.city_detail, name='city_detail'),
    path('attraction/<slug:slug>/', views.attraction_detail, name='attraction_detail'),

    # API URLs
    path('', include(router.urls)),

    # Short-form city URL (must be last to avoid matching api/attraction prefixes)
    path('<slug:slug>/', views.city_detail, name='city_detail_short'),
]