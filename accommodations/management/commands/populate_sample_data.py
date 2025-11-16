from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify
from decimal import Decimal
from datetime import date, timedelta
import random

from destinations.models import Country, City, Attraction
from accommodations.models import (
    AccommodationType, Amenity, Accommodation, Room
)
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Populates database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Starting data population...'))

        try:
            with transaction.atomic():
                self.create_countries_and_cities()
                self.create_attractions()
                self.create_accommodation_types_and_amenities()
                self.create_accommodations()

            self.stdout.write(self.style.SUCCESS('✅ Data population completed!'))
            self.print_summary()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
            import traceback
            traceback.print_exc()
            raise

    def create_countries_and_cities(self):
        """Create Egypt and major cities"""
        self.stdout.write('Creating countries and cities...')

        self.egypt, _ = Country.objects.get_or_create(
            code='EG',
            defaults={
                'name': 'Egypt',
                'flag_emoji': '🇪🇬',
                'description': 'Land of the Pharaohs'
            }
        )

        cities_data = [
            {'name': 'Cairo', 'latitude': Decimal('30.0444'), 'longitude': Decimal('31.2357'), 'is_popular': True,
             'population': 20000000},
            {'name': 'Giza', 'latitude': Decimal('30.0131'), 'longitude': Decimal('31.2089'), 'is_popular': True,
             'population': 8000000},
            {'name': 'Luxor', 'latitude': Decimal('25.6872'), 'longitude': Decimal('32.6396'), 'is_popular': True,
             'population': 500000},
            {'name': 'Aswan', 'latitude': Decimal('24.0889'), 'longitude': Decimal('32.8998'), 'is_popular': True,
             'population': 300000},
            {'name': 'Hurghada', 'latitude': Decimal('27.2579'), 'longitude': Decimal('33.8116'), 'is_popular': True,
             'population': 250000},
            {'name': 'Alexandria', 'latitude': Decimal('31.2001'), 'longitude': Decimal('29.9187'), 'is_popular': True,
             'population': 5000000},
        ]

        self.cities = {}
        for city_data in cities_data:
            city, _ = City.objects.get_or_create(
                name=city_data['name'],
                country=self.egypt,
                defaults=city_data
            )
            self.cities[city_data['name']] = city

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(self.cities)} cities'))

    def create_attractions(self):
        """Create attractions"""
        self.stdout.write('Creating attractions...')

        attractions = [
            {'name': 'Great Pyramid', 'city': 'Giza', 'category': 'monument', 'entry_fee': Decimal('240'),
             'average_rating': 4.9, 'total_reviews': 1500},
            {'name': 'Egyptian Museum', 'city': 'Cairo', 'category': 'museum', 'entry_fee': Decimal('200'),
             'average_rating': 4.7, 'total_reviews': 850},
            {'name': 'Karnak Temple', 'city': 'Luxor', 'category': 'temple', 'entry_fee': Decimal('220'),
             'average_rating': 4.9, 'total_reviews': 1200},
        ]

        for attr in attractions:
            city = attr.pop('city')
            Attraction.objects.get_or_create(
                name=attr['name'],
                city=self.cities[city],
                defaults={'description': f"Famous {attr['category']}", **attr}
            )

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {len(attractions)} attractions'))

    def create_accommodation_types_and_amenities(self):
        """Create types and amenities"""
        self.stdout.write('Creating types and amenities...')

        self.acc_types = {}
        for name in ['Hotel', 'Apartment', 'Hostel', 'Villa']:
            acc_type, _ = AccommodationType.objects.get_or_create(name=name)
            self.acc_types[name] = acc_type

        self.amenities = []
        for name in ['Free WiFi', 'Swimming Pool', 'Free Parking', 'Air Conditioning', 'Restaurant']:
            amenity, _ = Amenity.objects.get_or_create(name=name)
            self.amenities.append(amenity)

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created types and amenities'))

    def create_accommodations(self):
        """Create accommodations"""
        self.stdout.write('Creating accommodations...')

        acc_data = [
            {'name': 'Pyramids View Hotel', 'city': 'Giza', 'type': 'Hotel', 'star': 5, 'price': 3500, 'rooms': 120},
            {'name': 'Mena House Hotel', 'city': 'Giza', 'type': 'Hotel', 'star': 5, 'price': 4500, 'rooms': 160},
            {'name': 'Nile Riverside Resort', 'city': 'Cairo', 'type': 'Hotel', 'star': 4, 'price': 1800, 'rooms': 80},
            {'name': 'Cairo City Apartment', 'city': 'Cairo', 'type': 'Apartment', 'star': 3, 'price': 800,
             'rooms': 30},
            {'name': 'Downtown Hostel', 'city': 'Cairo', 'type': 'Hostel', 'star': 2, 'price': 350, 'rooms': 20},
            {'name': 'Luxor Palace Hotel', 'city': 'Luxor', 'type': 'Hotel', 'star': 5, 'price': 2800, 'rooms': 90},
            {'name': 'Aswan Nubian Resort', 'city': 'Aswan', 'type': 'Hotel', 'star': 4, 'price': 1600, 'rooms': 60},
            {'name': 'Red Sea Beach Resort', 'city': 'Hurghada', 'type': 'Hotel', 'star': 5, 'price': 3200,
             'rooms': 200},
            {'name': 'Alexandria Palace', 'city': 'Alexandria', 'type': 'Hotel', 'star': 4, 'price': 1900,
             'rooms': 100},
            {'name': 'Budget Inn Cairo', 'city': 'Cairo', 'type': 'Hostel', 'star': 1, 'price': 250, 'rooms': 15},
        ]

        count = 0
        for data in acc_data:
            if Accommodation.objects.filter(name=data['name']).exists():
                continue

            acc = Accommodation.objects.create(
                name=data['name'],
                city=self.cities[data['city']],
                accommodation_type=self.acc_types[data['type']],
                description=f"Great {data['type'].lower()} in {data['city']}",
                address=f"123 Main St, {data['city']}",
                phone_number='+20 2 1234 5678',
                email=f"info@{slugify(data['name'])}.com",
                star_rating=data['star'],
                price_per_night=Decimal(str(data['price'])),
                total_rooms=data['rooms'],
                max_guests=data['rooms'] * 2,
                average_rating=4.5,
                total_reviews=100,
                is_verified=True,
                safety_score=90
            )

            for amenity in self.amenities:
                acc.amenities.add(amenity)

            # Create 3 sample rooms
            for i in range(3):
                Room.objects.create(
                    accommodation=acc,
                    room_number=f"{100 + i}",
                    room_type='double',
                    capacity=2,
                    price_per_night=Decimal(str(data['price'])),
                    description="Comfortable room",
                    is_available=True
                )

            count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {count} accommodations'))

    def print_summary(self):
        """Print summary"""
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write(self.style.SUCCESS('📊 DATA SUMMARY'))
        self.stdout.write('=' * 50)
        self.stdout.write(f'Countries: {Country.objects.count()}')
        self.stdout.write(f'Cities: {City.objects.count()}')
        self.stdout.write(f'Accommodations: {Accommodation.objects.count()}')
        self.stdout.write(f'Rooms: {Room.objects.count()}')
        self.stdout.write('\n✅ Visit http://localhost:8000/accommodations/')