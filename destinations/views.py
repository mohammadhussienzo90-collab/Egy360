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
    # Auto-seed if no cities exist (Railway ephemeral storage fix)
    import sys
    try:
        if City.objects.count() == 0:
            print("AUTO-SEED DESTINATIONS: No cities found, seeding now...", file=sys.stderr)
            _auto_seed_destinations()
            print(f"AUTO-SEED DESTINATIONS: Completed. Total cities: {City.objects.count()}", file=sys.stderr)
    except Exception as e:
        print(f"AUTO-SEED DESTINATIONS ERROR: {str(e)}", file=sys.stderr)

    cities = City.objects.filter(is_popular=True)
    attractions = Attraction.objects.filter(is_must_see=True)[:6]
    context = {
        'cities': cities,
        'attractions': attractions
    }
    return render(request, 'destinations/list.html', context)


def _auto_seed_destinations():
    """Auto-seed destinations when database is empty"""
    # Create Egypt country
    egypt, _ = Country.objects.get_or_create(
        code='EGY',
        defaults={
            'name': 'Egypt',
            'description': 'The land of pharaohs, pyramids, and ancient wonders.',
            'flag_emoji': '🇪🇬'
        }
    )

    cities_data = [
        {
            'name': 'Cairo',
            'slug': 'cairo',
            'description': 'Cairo, the capital of Egypt, is a sprawling metropolis where ancient history meets modern life. Home to the iconic Pyramids of Giza and the Sphinx, Cairo offers world-class museums, vibrant bazaars, and rich cultural heritage spanning over 5,000 years.',
            'population': 21000000,
            'is_popular': True,
            'is_capital': True,
            'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Pyramids of Giza', 'slug': 'pyramids-of-giza', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The last surviving Wonder of the Ancient World. These magnificent structures have stood for over 4,500 years.',
                 'admission_fee': 200, 'visit_duration': '3-4 hours', 'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800'},
                {'name': 'Egyptian Museum', 'slug': 'egyptian-museum', 'type': 'museum', 'is_must_see': True,
                 'description': 'Home to the world\'s largest collection of ancient Egyptian artifacts, including Tutankhamun\'s treasures.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800'},
                {'name': 'Khan El-Khalili Bazaar', 'slug': 'khan-el-khalili', 'type': 'market', 'is_must_see': True,
                 'description': 'Cairo\'s famous 14th-century bazaar. Shop for spices, jewelry, and experience authentic Egyptian culture.',
                 'admission_fee': 0, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800'},
            ]
        },
        {
            'name': 'Luxor',
            'slug': 'luxor',
            'description': 'Luxor is the world\'s greatest open-air museum. Once ancient Thebes, capital of the pharaohs, Luxor houses the Valley of the Kings, Karnak Temple, and countless treasures.',
            'population': 500000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'October to March',
            'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=1200',
            'attractions': [
                {'name': 'Valley of the Kings', 'slug': 'valley-of-kings', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The royal burial ground of Egypt\'s pharaohs for 500 years. Over 60 tombs including Tutankhamun\'s.',
                 'admission_fee': 300, 'visit_duration': '3-4 hours', 'image_url': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800'},
                {'name': 'Karnak Temple', 'slug': 'karnak-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'The largest ancient religious complex in the world. 2,000 years of construction by generations of pharaohs.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800'},
            ]
        },
        {
            'name': 'Aswan',
            'slug': 'aswan',
            'description': 'Aswan is Egypt\'s sunniest southern city, known for beautiful Nile scenery, Nubian culture, and gateway to Abu Simbel. Felucca sailing at sunset is a must.',
            'population': 300000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'October to April',
            'image_url': 'https://images.unsplash.com/photo-1587974928442-77dc3e0dba72?w=1200',
            'attractions': [
                {'name': 'Abu Simbel Temples', 'slug': 'abu-simbel', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'Ramesses II\'s magnificent rock-cut temples, relocated in a UNESCO engineering marvel.',
                 'admission_fee': 300, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1600697395453-e89e8a097d3a?w=800'},
                {'name': 'Philae Temple', 'slug': 'philae-temple', 'type': 'archaeological', 'is_unesco': True, 'is_must_see': True,
                 'description': 'Beautiful island temple dedicated to goddess Isis, rescued from the rising waters of the Aswan Dam.',
                 'admission_fee': 200, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
            ]
        },
        {
            'name': 'Hurghada',
            'slug': 'hurghada',
            'description': 'Hurghada is Egypt\'s premier Red Sea resort destination. World-class diving, beautiful beaches, all-inclusive resorts, and year-round sunshine.',
            'population': 250000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1200',
            'attractions': [
                {'name': 'Giftun Islands', 'slug': 'giftun-islands', 'type': 'natural', 'is_must_see': True,
                 'description': 'Protected marine park with pristine beaches, crystal-clear waters, and excellent snorkeling.',
                 'admission_fee': 100, 'visit_duration': 'Full day', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
            ]
        },
        {
            'name': 'Sharm El Sheikh',
            'slug': 'sharm-el-sheikh',
            'description': 'Sharm El Sheikh sits at the tip of the Sinai Peninsula, offering world-famous diving at Ras Mohammed National Park and luxury resorts.',
            'population': 100000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'Year-round, best March to May',
            'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=1200',
            'attractions': [
                {'name': 'Ras Mohammed National Park', 'slug': 'ras-mohammed', 'type': 'natural', 'is_must_see': True,
                 'description': 'World-renowned marine park with spectacular diving, shark reef, and pristine coral walls.',
                 'admission_fee': 100, 'visit_duration': 'Full day', 'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800'},
            ]
        },
        {
            'name': 'Alexandria',
            'slug': 'alexandria',
            'description': 'Alexandria, Egypt\'s Mediterranean jewel, was founded by Alexander the Great. Known for the legendary ancient library and beautiful Corniche.',
            'population': 5000000,
            'is_popular': True,
            'has_airport': True,
            'best_time_to_visit': 'March to May, September to November',
            'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=1200',
            'attractions': [
                {'name': 'Bibliotheca Alexandrina', 'slug': 'bibliotheca-alexandrina', 'type': 'modern', 'is_must_see': True,
                 'description': 'Modern tribute to the ancient Library of Alexandria. Stunning architecture and cultural center.',
                 'admission_fee': 70, 'visit_duration': '2-3 hours', 'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800'},
            ]
        },
    ]

    for city_data in cities_data:
        attractions = city_data.pop('attractions', [])
        city, _ = City.objects.update_or_create(
            slug=city_data['slug'],
            defaults={**city_data, 'country': egypt}
        )

        for attr_data in attractions:
            Attraction.objects.update_or_create(
                slug=attr_data['slug'],
                defaults={
                    'city': city,
                    'name': attr_data['name'],
                    'attraction_type': attr_data['type'],
                    'description': attr_data['description'],
                    'address': f"{attr_data['name']}, {city.name}, Egypt",
                    'admission_fee': attr_data.get('admission_fee', 0),
                    'visit_duration': attr_data.get('visit_duration', '1-2 hours'),
                    'is_unesco': attr_data.get('is_unesco', False),
                    'is_must_see': attr_data.get('is_must_see', False),
                    'image_url': attr_data.get('image_url', ''),
                    'average_rating': 4.5,
                    'total_reviews': 150,
                }
            )

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