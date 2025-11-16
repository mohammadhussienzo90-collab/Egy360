# destinations/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Country, City, Attraction, TravelGuide
from .serializers import (
    CountrySerializer, 
    CitySerializer, 
    AttractionSerializer, 
    TravelGuideSerializer
)

# Template Views
class CityListView(ListView):
    model = City
    template_name = 'destinations/list.html'
    context_object_name = 'destinations'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country__name__icontains=country)
        return queryset.filter(is_popular=True)

def destinations_list(request):
    cities = City.objects.filter(is_popular=True)
    attractions = Attraction.objects.filter(is_must_see=True)[:6]
    context = {
        'cities': cities,
        'attractions': attractions
    }
    return render(request, 'destinations/list.html', context)

def city_detail(request, slug):
    city = get_object_or_404(City, slug=slug)
    attractions = city.attractions.all()
    guides = city.guides.filter(is_published=True)
    context = {
        'city': city,
        'attractions': attractions,
        'guides': guides
    }
    return render(request, 'destinations/city_detail.html', context)

def attraction_detail(request, slug):
    attraction = get_object_or_404(Attraction, slug=slug)
    context = {
        'attraction': attraction
    }
    return render(request, 'destinations/attraction_detail.html', context)

# API Views
class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        popular = self.queryset.filter(is_popular=True)
        serializer = self.get_serializer(popular, many=True)
        return Response(serializer.data)

class AttractionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attraction.objects.all()
    serializer_class = AttractionSerializer
    
    @action(detail=False, methods=['get'])
    def must_see(self, request):
        must_see = self.queryset.filter(is_must_see=True)
        serializer = self.get_serializer(must_see, many=True)
        return Response(serializer.data)

class TravelGuideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TravelGuide.objects.filter(is_published=True)
    serializer_class = TravelGuideSerializer