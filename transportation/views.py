# transportation/views.py
import sys
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import TransportationService, Driver, TransportBooking


class TransportationListView(ListView):
    model = TransportationService
    template_name = 'transportation/list.html'
    context_object_name = 'services'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        # Auto-seed if no services exist (Railway ephemeral storage fix)
        try:
            if TransportationService.objects.count() == 0:
                print("AUTO-SEED TRANSPORT: No services found, seeding now...", file=sys.stderr)
                self._auto_seed_transport()
                print(f"AUTO-SEED TRANSPORT: Completed. Total: {TransportationService.objects.count()}", file=sys.stderr)
        except Exception as e:
            print(f"AUTO-SEED TRANSPORT ERROR: {str(e)}", file=sys.stderr)
        return super().dispatch(request, *args, **kwargs)

    def _auto_seed_transport(self):
        """Auto-seed transportation services when database is empty."""
        services_data = [
            {
                'name': 'Cairo Airport Private Transfer',
                'slug': 'cairo-airport-private-transfer',
                'service_type': 'airport_transfer',
                'description': 'Comfortable private transfer between Cairo International Airport (CAI) and any hotel in Cairo or Giza. Meet & greet service with name board at arrivals. Available 24/7 with flight tracking.',
                'vehicle_model': 'Mercedes Vito / Toyota Hiace',
                'max_passengers': 6,
                'max_luggage': 6,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 35.00,
                'average_rating': 4.85,
                'total_reviews': 2450,
            },
            {
                'name': 'Luxor Airport Transfer',
                'slug': 'luxor-airport-transfer',
                'service_type': 'airport_transfer',
                'description': 'Private transfer between Luxor International Airport and hotels on the East or West Bank. Includes meet & greet and luggage assistance.',
                'vehicle_model': 'Toyota Corolla / Hyundai Accent',
                'max_passengers': 3,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 20.00,
                'average_rating': 4.70,
                'total_reviews': 890,
            },
            {
                'name': 'Hurghada Airport Transfer',
                'slug': 'hurghada-airport-transfer',
                'service_type': 'airport_transfer',
                'description': 'Private airport transfer to any resort in Hurghada, El Gouna, Makadi Bay, or Sahl Hasheesh. Available 24/7 with flight monitoring.',
                'vehicle_model': 'Hyundai H-1 / Toyota Hiace',
                'max_passengers': 7,
                'max_luggage': 7,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 25.00,
                'average_rating': 4.75,
                'total_reviews': 1200,
            },
            {
                'name': 'Cairo Full-Day Private Car & Driver',
                'slug': 'cairo-full-day-private-car',
                'service_type': 'private_car',
                'description': 'Explore Cairo at your own pace with a private car and professional English-speaking driver. Visit Pyramids, museums, markets — you set the itinerary. Up to 10 hours.',
                'vehicle_model': 'Mercedes E-Class / Hyundai Sonata',
                'max_passengers': 4,
                'max_luggage': 2,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'price_per_hour': 12.00,
                'fixed_price': 80.00,
                'average_rating': 4.90,
                'total_reviews': 3100,
            },
            {
                'name': 'Cairo to Luxor Private Transfer',
                'slug': 'cairo-to-luxor-private-transfer',
                'service_type': 'private_car',
                'description': 'Comfortable long-distance private transfer from Cairo to Luxor with experienced driver. Includes rest stops. Great alternative to flights for those who want to see the countryside.',
                'vehicle_model': 'Toyota Fortuner / Hyundai Tucson',
                'max_passengers': 4,
                'max_luggage': 4,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 250.00,
                'average_rating': 4.65,
                'total_reviews': 420,
            },
            {
                'name': 'Cairo to Alexandria Day Trip Car',
                'slug': 'cairo-to-alexandria-day-trip-car',
                'service_type': 'private_car',
                'description': 'Private car with driver for a day trip from Cairo to Alexandria (2.5h each way). Explore the Bibliotheca, Catacombs, Citadel, and enjoy fresh seafood on the Mediterranean.',
                'vehicle_model': 'Hyundai Sonata / Toyota Camry',
                'max_passengers': 4,
                'max_luggage': 2,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 120.00,
                'average_rating': 4.80,
                'total_reviews': 780,
            },
            {
                'name': 'Luxor to Aswan Private Transfer',
                'slug': 'luxor-to-aswan-private-transfer',
                'service_type': 'private_car',
                'description': 'Private transfer from Luxor to Aswan (3h drive). Optional stops at Edfu Temple and Kom Ombo Temple along the way.',
                'vehicle_model': 'Toyota Hiace / Hyundai H-1',
                'max_passengers': 6,
                'max_luggage': 6,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 90.00,
                'average_rating': 4.70,
                'total_reviews': 560,
            },
            {
                'name': 'VIP Luxury Limousine Service',
                'slug': 'vip-luxury-limousine-cairo',
                'service_type': 'limousine',
                'description': 'Premium luxury limousine service in Cairo for VIP transfers, business meetings, or special occasions. Professional chauffeur, complimentary water and refreshments.',
                'vehicle_model': 'Mercedes S-Class / BMW 7 Series',
                'max_passengers': 3,
                'max_luggage': 3,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': False,
                'price_per_hour': 40.00,
                'fixed_price': 200.00,
                'average_rating': 4.95,
                'total_reviews': 350,
            },
            {
                'name': 'Sharm El Sheikh Airport Transfer',
                'slug': 'sharm-airport-transfer',
                'service_type': 'airport_transfer',
                'description': 'Private transfer between Sharm El Sheikh Airport and any resort in Naama Bay, Shark Bay, Ras Um Sid, or Nabq Bay. 24/7 service with flight tracking.',
                'vehicle_model': 'Hyundai H-1 / Toyota Hiace',
                'max_passengers': 6,
                'max_luggage': 6,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 25.00,
                'average_rating': 4.80,
                'total_reviews': 950,
            },
            {
                'name': 'Group Minivan — Cairo Sightseeing',
                'slug': 'group-minivan-cairo-sightseeing',
                'service_type': 'minivan',
                'description': 'Spacious minivan with driver for groups and families touring Cairo. Perfect for Pyramids, Egyptian Museum, Coptic Cairo, and Khan El-Khalili. Full day up to 10 hours.',
                'vehicle_model': 'Toyota Hiace Grand / Mercedes Viano',
                'max_passengers': 10,
                'max_luggage': 8,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'price_per_hour': 15.00,
                'fixed_price': 100.00,
                'average_rating': 4.85,
                'total_reviews': 670,
            },
            {
                'name': 'Cairo to Hurghada Private Transfer',
                'slug': 'cairo-to-hurghada-private-transfer',
                'service_type': 'private_car',
                'description': 'Private car transfer from Cairo to Hurghada Red Sea resorts (5-6h drive). Comfortable vehicle with rest stops. Ideal for travelers who prefer road trips.',
                'vehicle_model': 'Toyota Fortuner / Hyundai Tucson',
                'max_passengers': 4,
                'max_luggage': 4,
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_child_seat': True,
                'fixed_price': 180.00,
                'average_rating': 4.60,
                'total_reviews': 340,
            },
            {
                'name': 'Aswan Abu Simbel Return Transfer',
                'slug': 'aswan-abu-simbel-transfer',
                'service_type': 'private_car',
                'description': 'Early morning private transfer from Aswan to Abu Simbel temples and return. Departs 3:00 AM, 3h each way. Includes waiting time at the temples.',
                'vehicle_model': 'Toyota Land Cruiser / Hyundai Tucson',
                'max_passengers': 4,
                'max_luggage': 2,
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_child_seat': False,
                'fixed_price': 130.00,
                'average_rating': 4.75,
                'total_reviews': 880,
            },
        ]

        for data in services_data:
            TransportationService.objects.update_or_create(
                slug=data['slug'],
                defaults=data,
            )

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        service_type = self.request.GET.get('type')
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        return queryset


class TransportationDetailView(DetailView):
    model = TransportationService
    template_name = 'transportation/detail.html'
    context_object_name = 'service'


def book_transport(request, pk):
    service = get_object_or_404(TransportationService, pk=pk)
    return render(request, 'transportation/booking.html', {'service': service})
