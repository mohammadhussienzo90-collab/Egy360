# destinations/management/commands/load_sample_data.py
"""
Django Management Command to Load Sample Data (CORRECTED)

Usage: python manage.py load_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from destinations.models import Country, City, Attraction
from accommodations.models import AccommodationType, Amenity, Accommodation, Room
from tours.models import TourCategory, TourOperator, Tour, TourSchedule
from payments.models import PaymentMethod
from decimal import Decimal
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🚀 Starting to load sample data...'))

        # 1. Create Users
        self.create_users()

        # 2. Create Destinations
        self.create_destinations()

        # 3. Create Accommodations
        self.create_accommodations()

        # 4. Create Tours
        self.create_tours()

        # 5. Create Payment Methods
        self.create_payment_methods()

        self.stdout.write(self.style.SUCCESS('✅ Sample data loaded successfully!'))
        self.stdout.write(self.style.SUCCESS('📊 Summary:'))
        self.stdout.write(f'   - Users: {User.objects.count()}')
        self.stdout.write(f'   - Cities: {City.objects.count()}')
        self.stdout.write(f'   - Attractions: {Attraction.objects.count()}')
        self.stdout.write(f'   - Accommodations: {Accommodation.objects.count()}')
        self.stdout.write(f'   - Tours: {Tour.objects.count()}')

    def create_users(self):
        import secrets
        import string

        def generate_password(length=16):
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            return ''.join(secrets.choice(alphabet) for _ in range(length))

        self.stdout.write('👤 Creating users...')

        # Admin user
        if not User.objects.filter(username='admin').exists():
            password = generate_password()
            User.objects.create_superuser(
                username='admin',
                email='admin@egy360.com',
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('   ✓ Admin user created')
            self.stdout.write(self.style.WARNING(f'     Password: {password}'))

        # Tourist user (sample data - uses random password)
        if not User.objects.filter(username='tourist').exists():
            password = generate_password()
            User.objects.create_user(
                username='tourist',
                email='tourist@example.com',
                password=password,
                first_name='John',
                last_name='Tourist'
            )
            self.stdout.write('   ✓ Tourist user created')

        # Provider user (sample data - uses random password)
        if not User.objects.filter(username='provider').exists():
            password = generate_password()
            User.objects.create_user(
                username='provider',
                email='provider@example.com',
                password=password,
                first_name='Ahmed',
                last_name='Provider'
            )
            self.stdout.write('   ✓ Provider user created')

    def create_destinations(self):
        self.stdout.write('🗺️ Creating destinations...')

        # Create Egypt - only use fields that exist
        egypt, _ = Country.objects.get_or_create(
            name='Egypt',
            defaults={
                'code': 'EG',
                'description': 'Land of Pharaohs and ancient wonders'
            }
        )

        # Create Cities
        cities_data = [
            {
                'name': 'Cairo',
                'description': 'The capital of Egypt, home to the Pyramids and bustling city life',
                'population': 20000000,
                'is_popular': True,
                'best_time_to_visit': 'October to April'
            },
            {
                'name': 'Luxor',
                'description': 'Ancient city with magnificent temples and tombs',
                'population': 500000,
                'is_popular': True,
                'best_time_to_visit': 'October to April'
            },
            {
                'name': 'Aswan',
                'description': 'Beautiful Nile city with stunning sunsets',
                'population': 300000,
                'is_popular': True,
                'best_time_to_visit': 'October to April'
            },
            {
                'name': 'Alexandria',
                'description': 'Mediterranean coastal city with rich history',
                'population': 5000000,
                'is_popular': True,
                'best_time_to_visit': 'April to November'
            }
        ]

        cities = {}
        for city_data in cities_data:
            city, _ = City.objects.get_or_create(
                name=city_data['name'],
                country=egypt,
                defaults=city_data
            )
            cities[city_data['name']] = city
            self.stdout.write(f'   ✓ City: {city.name}')

        # Create Attractions
        attractions_data = [
            {
                'city': cities['Cairo'],
                'name': 'Great Pyramids of Giza',
                'description': 'Ancient wonders of the world, including the Great Pyramid and Sphinx',
                'category': 'historical',
                'entry_fee': Decimal('200.00'),
                'is_free': False
            },
            {
                'city': cities['Cairo'],
                'name': 'Egyptian Museum',
                'description': 'Home to the treasures of Tutankhamun and ancient artifacts',
                'category': 'museum',
                'entry_fee': Decimal('180.00'),
                'is_free': False
            },
            {
                'city': cities['Luxor'],
                'name': 'Karnak Temple',
                'description': 'Massive temple complex dedicated to Amun-Ra',
                'category': 'historical',
                'entry_fee': Decimal('300.00'),
                'is_free': False
            },
            {
                'city': cities['Aswan'],
                'name': 'Abu Simbel Temples',
                'description': 'Rock-cut temples of Ramses II relocated above Lake Nasser',
                'category': 'historical',
                'entry_fee': Decimal('250.00'),
                'is_free': False
            }
        ]

        for attr_data in attractions_data:
            Attraction.objects.get_or_create(
                name=attr_data['name'],
                city=attr_data['city'],
                defaults=attr_data
            )
            self.stdout.write(f'   ✓ Attraction: {attr_data["name"]}')

    def create_accommodations(self):
        self.stdout.write('🏨 Creating accommodations...')

        # Create Accommodation Types
        hotel_type, _ = AccommodationType.objects.get_or_create(
            name='Hotel',
            defaults={'description': 'Traditional hotel accommodation'}
        )

        hostel_type, _ = AccommodationType.objects.get_or_create(
            name='Hostel',
            defaults={'description': 'Budget-friendly shared accommodation'}
        )

        # Create Amenities
        amenities_list = ['WiFi', 'Swimming Pool', 'Restaurant', 'Gym', 'Spa', 'Parking']
        amenities = {}
        for amenity_name in amenities_list:
            amenity, _ = Amenity.objects.get_or_create(
                name=amenity_name,
                defaults={'icon': '✓'}
            )
            amenities[amenity_name] = amenity

        # Get Cairo
        cairo = City.objects.get(name='Cairo')
        provider = User.objects.get(username='provider')

        # Create Accommodations
        accommodations_data = [
            {
                'name': 'Pyramids View Hotel',
                'accommodation_type': hotel_type,
                'city': cairo,
                'owner': provider,
                'description': 'Luxury 5-star hotel with stunning pyramid views from all rooms',
                'address': 'Al Haram, Giza, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('1500.00'),
                'total_rooms': 50,
                'is_verified': True
            },
            {
                'name': 'Downtown Cairo Hotel',
                'accommodation_type': hotel_type,
                'city': cairo,
                'owner': provider,
                'description': 'Modern 4-star hotel in the heart of downtown Cairo',
                'address': 'Tahrir Square, Downtown, Cairo',
                'star_rating': 4,
                'price_per_night': Decimal('800.00'),
                'total_rooms': 30,
                'is_verified': True
            },
            {
                'name': 'Cairo Backpackers Hostel',
                'accommodation_type': hostel_type,
                'city': cairo,
                'owner': provider,
                'description': 'Budget-friendly hostel perfect for backpackers and solo travelers',
                'address': 'Tahrir Square, Cairo',
                'star_rating': 3,
                'price_per_night': Decimal('200.00'),
                'total_rooms': 20,
                'is_verified': True
            }
        ]

        for acc_data in accommodations_data:
            acc, created = Accommodation.objects.get_or_create(
                name=acc_data['name'],
                defaults=acc_data
            )

            if created:
                # Add amenities
                acc.amenities.add(amenities['WiFi'], amenities['Restaurant'])
                if acc.star_rating >= 4:
                    acc.amenities.add(amenities['Swimming Pool'], amenities['Gym'])
                if acc.star_rating >= 5:
                    acc.amenities.add(amenities['Spa'])

                # Create Rooms
                for i in range(1, 6):  # Create 5 rooms per accommodation
                    Room.objects.create(
                        accommodation=acc,
                        room_number=f'{i}01',
                        room_type='standard' if i <= 3 else 'deluxe',
                        capacity=2 if i <= 3 else 4,
                        num_beds=1 if i <= 3 else 2,
                        bed_type='queen',
                        size_sqm=25 if i <= 3 else 40,
                        price_per_night=acc.price_per_night,
                        is_available=True
                    )

            self.stdout.write(f'   ✓ Accommodation: {acc.name} (5 rooms)')

    def create_tours(self):
        self.stdout.write('🎫 Creating tours...')

        # Create Tour Categories
        cultural, _ = TourCategory.objects.get_or_create(
            name='Cultural',
            defaults={'description': 'Cultural and historical experiences'}
        )

        adventure, _ = TourCategory.objects.get_or_create(
            name='Adventure',
            defaults={'description': 'Adventure and outdoor activities'}
        )

        # Create Tour Operator
        provider = User.objects.get(username='provider')
        cairo = City.objects.get(name='Cairo')
        luxor = City.objects.get(name='Luxor')

        operator, _ = TourOperator.objects.get_or_create(
            name='Egypt Tours Co.',
            defaults={
                'owner': provider,
                'description': 'Professional tour operator with 20 years experience',
                'is_verified': True
            }
        )

        # Create Tours
        tours_data = [
            {
                'title': 'Pyramids & Egyptian Museum Day Tour',
                'operator': operator,
                'category': cultural,
                'city': cairo,
                'description': 'Full day guided tour to Giza Pyramids, Sphinx, and Egyptian Museum with expert Egyptologist guide',
                'duration_hours': 8,
                'price_per_person': Decimal('800.00'),
                'max_participants': 15,
                'includes_transport': True,
                'includes_meals': True
            },
            {
                'title': 'Luxor Temples Full Day Tour',
                'operator': operator,
                'category': cultural,
                'city': luxor,
                'description': 'Visit Karnak Temple and Luxor Temple with guided tour and lunch',
                'duration_hours': 10,
                'price_per_person': Decimal('1200.00'),
                'max_participants': 20,
                'includes_transport': True,
                'includes_meals': True
            },
            {
                'title': 'Nile River Dinner Cruise',
                'operator': operator,
                'category': adventure,
                'city': cairo,
                'description': 'Evening dinner cruise on the Nile with traditional entertainment and buffet dinner',
                'duration_hours': 3,
                'price_per_person': Decimal('500.00'),
                'max_participants': 50,
                'includes_transport': False,
                'includes_meals': True
            }
        ]

        for tour_data in tours_data:
            tour, created = Tour.objects.get_or_create(
                title=tour_data['title'],
                defaults=tour_data
            )

            if created:
                # Create schedules for next 7 days
                for i in range(7):
                    date = datetime.now().date() + timedelta(days=i + 1)
                    TourSchedule.objects.create(
                        tour=tour,
                        start_date=date,
                        start_time='09:00:00',
                        available_spots=tour.max_participants,
                        is_available=True
                    )

            self.stdout.write(f'   ✓ Tour: {tour.title}')

    def create_payment_methods(self):
        self.stdout.write('💳 Creating payment methods...')

        methods = [
            {
                'name': 'Credit Card',
                'method_type': 'card',
                'description': 'Pay securely with credit or debit card',
                'is_active': True
            },
            {
                'name': 'Cash on Arrival',
                'method_type': 'cash',
                'description': 'Pay with cash when you arrive',
                'is_active': True
            },
            {
                'name': 'Bank Transfer',
                'method_type': 'bank_transfer',
                'description': 'Direct bank transfer to our account',
                'is_active': True
            }
        ]

        for method_data in methods:
            PaymentMethod.objects.get_or_create(
                name=method_data['name'],
                defaults=method_data
            )
            self.stdout.write(f'   ✓ Payment Method: {method_data["name"]}')