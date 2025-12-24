"""
Management command to populate initial data for Egy360
Run with: python manage.py populate_initial_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from destinations.models import Destination
from accommodations.models import Accommodation, Room, Amenity
from tours.models import Tour, TourCategory
import random


class Command(BaseCommand):
    help = 'Populate initial data for Egy360'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')

        # Create superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            import secrets
            import string
            # Generate secure random password
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(secrets.choice(alphabet) for _ in range(16))

            User.objects.create_superuser(
                username='admin',
                email='admin@egy360.com',
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superuser created'))
            self.stdout.write(self.style.WARNING(f'  Password: {password}'))
            self.stdout.write(self.style.WARNING('  Save this password securely!'))

        # Create destinations
        destinations_data = [
            {'name': 'Cairo', 'country': 'Egypt', 'description': 'The capital city with pyramids and museums'},
            {'name': 'Giza', 'country': 'Egypt', 'description': 'Home to the Great Pyramids'},
            {'name': 'Luxor', 'country': 'Egypt', 'description': 'Ancient Thebes with Valley of Kings'},
            {'name': 'Aswan', 'country': 'Egypt', 'description': 'Beautiful Nile views and Nubian culture'},
            {'name': 'Alexandria', 'country': 'Egypt', 'description': 'Mediterranean coastal city'},
            {'name': 'Sharm El Sheikh', 'country': 'Egypt', 'description': 'Red Sea resort paradise'},
            {'name': 'Hurghada', 'country': 'Egypt', 'description': 'Beach resort and diving destination'},
            {'name': 'Dahab', 'country': 'Egypt', 'description': 'Backpacker haven with great diving'},
            {'name': 'Marsa Alam', 'country': 'Egypt', 'description': 'Pristine beaches and marine life'},
            {'name': 'Siwa Oasis', 'country': 'Egypt', 'description': 'Desert oasis with unique culture'},
        ]

        for dest_data in destinations_data:
            destination, created = Destination.objects.get_or_create(
                name=dest_data['name'],
                defaults={
                    'country': dest_data['country'],
                    'description': dest_data['description'],
                    'slug': slugify(dest_data['name']),
                    'is_popular': True,
                }
            )
            if created:
                self.stdout.write(f'  Created destination: {destination.name}')

        self.stdout.write(self.style.SUCCESS('✓ Destinations created'))

        # Create amenities
        amenities_list = [
            'WiFi', 'Swimming Pool', 'Air Conditioning', 'Parking', 'Restaurant',
            'Room Service', 'Gym', 'Spa', 'Bar', 'Airport Shuttle',
            'Pet Friendly', 'Non-Smoking Rooms', 'Family Rooms', 'Laundry',
            'Safe', 'Elevator', 'Heating', 'Breakfast Included', '24-Hour Front Desk'
        ]

        amenities = []
        for amenity_name in amenities_list:
            amenity, created = Amenity.objects.get_or_create(
                name=amenity_name,
                defaults={'icon': f'fa-{slugify(amenity_name)}'}
            )
            amenities.append(amenity)
            if created:
                self.stdout.write(f'  Created amenity: {amenity.name}')

        self.stdout.write(self.style.SUCCESS('✓ Amenities created'))

        # Create sample accommodations
        accommodations_data = [
            {
                'name': 'Pyramids View Hotel',
                'city': 'Giza',
                'accommodation_type': 'hotel',
                'price_per_night': 120,
                'description': 'Luxury hotel with stunning pyramid views'
            },
            {
                'name': 'Nile Plaza Hotel',
                'city': 'Cairo',
                'accommodation_type': 'hotel',
                'price_per_night': 85,
                'description': 'Modern hotel in the heart of Cairo'
            },
            {
                'name': 'Red Sea Resort',
                'city': 'Sharm El Sheikh',
                'accommodation_type': 'resort',
                'price_per_night': 200,
                'description': 'All-inclusive beach resort'
            },
            {
                'name': 'Luxor Temple Guest House',
                'city': 'Luxor',
                'accommodation_type': 'guesthouse',
                'price_per_night': 45,
                'description': 'Cozy guesthouse near ancient temples'
            },
            {
                'name': 'Alexandria Beach Apartment',
                'city': 'Alexandria',
                'accommodation_type': 'apartment',
                'price_per_night': 60,
                'description': 'Sea view apartment with kitchen'
            },
        ]

        for acc_data in accommodations_data:
            accommodation, created = Accommodation.objects.get_or_create(
                name=acc_data['name'],
                defaults={
                    'slug': slugify(acc_data['name']),
                    'description': acc_data['description'],
                    'accommodation_type': acc_data['accommodation_type'],
                    'address': f"123 Main St, {acc_data['city']}",
                    'city': acc_data['city'],
                    'state': 'Egypt',
                    'country': 'Egypt',
                    'price_per_night': acc_data['price_per_night'],
                    'max_guests': random.randint(2, 6),
                    'num_bedrooms': random.randint(1, 4),
                    'num_bathrooms': random.randint(1, 3),
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                    'latitude': 30.0444 + random.uniform(-5, 5),
                    'longitude': 31.2357 + random.uniform(-5, 5),
                }
            )

            if created:
                # Add random amenities
                random_amenities = random.sample(amenities, random.randint(5, 10))
                accommodation.amenities.set(random_amenities)

                # Create rooms for hotels
                if accommodation.accommodation_type == 'hotel':
                    for i in range(1, random.randint(3, 6)):
                        Room.objects.create(
                            accommodation=accommodation,
                            room_type=random.choice(['single', 'double', 'suite']),
                            room_number=f"{100 + i}",
                            price_per_night=accommodation.price_per_night * random.uniform(0.8, 1.5),
                            max_occupancy=random.randint(1, 4),
                            size_sqm=random.randint(20, 60),
                            is_available=True
                        )

                self.stdout.write(f'  Created accommodation: {accommodation.name}')

        self.stdout.write(self.style.SUCCESS('✓ Accommodations created'))

        # Create tour categories
        categories_data = [
            'Historical Tours',
            'Adventure Tours',
            'Desert Safari',
            'Nile Cruises',
            'Diving & Snorkeling',
            'Cultural Experiences',
            'Day Trips',
            'Multi-Day Tours'
        ]

        categories = []
        for cat_name in categories_data:
            category, created = TourCategory.objects.get_or_create(
                name=cat_name,
                defaults={
                    'slug': slugify(cat_name),
                    'description': f'Experience the best {cat_name.lower()} in Egypt'
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'  Created category: {category.name}')

        self.stdout.write(self.style.SUCCESS('✓ Tour categories created'))

        # Create sample tours
        tours_data = [
            {
                'title': 'Pyramids and Sphinx Day Tour',
                'category': 'Historical Tours',
                'duration_days': 1,
                'price_per_person': 65,
                'description': 'Visit the Great Pyramids of Giza and the Sphinx'
            },
            {
                'title': '3-Day Nile Cruise Luxor to Aswan',
                'category': 'Nile Cruises',
                'duration_days': 3,
                'price_per_person': 450,
                'description': 'Luxury cruise along the Nile with temple visits'
            },
            {
                'title': 'Red Sea Diving Experience',
                'category': 'Diving & Snorkeling',
                'duration_days': 1,
                'price_per_person': 120,
                'description': 'Discover amazing underwater life in the Red Sea'
            },
            {
                'title': 'Sahara Desert Safari Adventure',
                'category': 'Desert Safari',
                'duration_days': 2,
                'price_per_person': 280,
                'description': 'Camp under the stars in the Sahara Desert'
            },
            {
                'title': 'Valley of Kings and Queens Tour',
                'category': 'Historical Tours',
                'duration_days': 1,
                'price_per_person': 85,
                'description': 'Explore ancient Egyptian royal tombs'
            },
        ]

        for tour_data in tours_data:
            category = TourCategory.objects.get(name=tour_data['category'])
            tour, created = Tour.objects.get_or_create(
                title=tour_data['title'],
                defaults={
                    'slug': slugify(tour_data['title']),
                    'description': tour_data['description'],
                    'category': category,
                    'duration_days': tour_data['duration_days'],
                    'duration_nights': max(0, tour_data['duration_days'] - 1),
                    'price_per_person': tour_data['price_per_person'],
                    'max_group_size': random.randint(10, 30),
                    'min_group_size': random.randint(2, 5),
                    'is_active': True,
                    'is_featured': random.choice([True, False]),
                    'is_private_tour': random.choice([True, False]),
                    'is_group_tour': True,
                    'difficulty_level': random.choice(['easy', 'moderate', 'challenging']),
                    'languages': 'English, Arabic, German, French',
                    'highlights': 'Amazing experience\nProfessional guides\nAll inclusive',
                    'included': 'Transportation\nGuide\nEntrance fees\nLunch',
                    'excluded': 'Personal expenses\nTips',
                }
            )

            if created:
                # Add destinations
                dest_names = random.sample(['Cairo', 'Giza', 'Luxor', 'Aswan'], random.randint(1, 2))
                for dest_name in dest_names:
                    dest = Destination.objects.get(name=dest_name)
                    tour.destinations.add(dest)

                self.stdout.write(f'  Created tour: {tour.title}')

        self.stdout.write(self.style.SUCCESS('✓ Tours created'))

        self.stdout.write(self.style.SUCCESS('\n✅ All initial data populated successfully!'))
        self.stdout.write(self.style.WARNING('\n⚠️  Default admin credentials:'))
        self.stdout.write('    Username: admin')
        self.stdout.write('    Password: admin123456')
        self.stdout.write(self.style.WARNING('    Please change these immediately!'))