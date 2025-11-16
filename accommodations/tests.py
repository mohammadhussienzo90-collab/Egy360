"""
Management command to create test accommodations
Place in: core/management/commands/create_test_accommodations.py
Run: python manage.py create_test_accommodations
"""
from django.core.management.base import BaseCommand
from accommodations.models import Accommodation
from destinations.models import City
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates test accommodation data for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating test accommodations...')

        # Test data
        test_accommodations = [
            {
                'name': 'Pyramids View Hotel',
                'city_name': 'Giza',
                'description': 'Luxurious 5-star hotel with stunning views of the Great Pyramids. Features include rooftop restaurant, infinity pool, and spa.',
                'accommodation_type': 'hotel',
                'star_rating': 5,
                'price_per_night': Decimal('2500.00'),
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 2,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': True,
                'has_beach_access': False,
                'safety_score': 98,
                'is_verified': True,
                'is_active': True,
                'is_featured': True,
            },
            {
                'name': 'Nile Palace Resort',
                'city_name': 'Cairo',
                'description': 'Elegant riverside resort offering panoramic views of the Nile. Perfect for business and leisure travelers.',
                'accommodation_type': 'resort',
                'star_rating': 4,
                'price_per_night': Decimal('1800.00'),
                'max_guests': 3,
                'bedrooms': 1,
                'bathrooms': 1,
                'has_wifi': True,
                'has_parking': False,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': False,
                'has_beach_access': False,
                'safety_score': 95,
                'is_verified': True,
                'is_active': True,
                'is_featured': True,
            },
            {
                'name': 'Luxor Grand Hotel',
                'city_name': 'Luxor',
                'description': 'Historic luxury hotel near Valley of the Kings. Experience ancient Egyptian hospitality with modern amenities.',
                'accommodation_type': 'hotel',
                'star_rating': 5,
                'price_per_night': Decimal('3200.00'),
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 3,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': True,
                'has_beach_access': False,
                'safety_score': 97,
                'is_verified': True,
                'is_active': True,
                'is_featured': True,
            },
            {
                'name': 'Red Sea Resort',
                'city_name': 'Sharm El Sheikh',
                'description': 'Beautiful beachfront resort with world-class diving facilities. All-inclusive packages available.',
                'accommodation_type': 'resort',
                'star_rating': 4,
                'price_per_night': Decimal('2100.00'),
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 2,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': True,
                'has_beach_access': True,
                'safety_score': 93,
                'is_verified': True,
                'is_active': True,
                'is_featured': True,
            },
            {
                'name': 'Alexandria Beach Hotel',
                'city_name': 'Alexandria',
                'description': 'Comfortable beachside hotel with Mediterranean views. Great for family vacations.',
                'accommodation_type': 'hotel',
                'star_rating': 3,
                'price_per_night': Decimal('1200.00'),
                'max_guests': 3,
                'bedrooms': 1,
                'bathrooms': 1,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': False,
                'has_gym': False,
                'has_restaurant': True,
                'has_spa': False,
                'has_beach_access': True,
                'safety_score': 90,
                'is_verified': False,
                'is_active': True,
                'is_featured': False,
            },
            {
                'name': 'Aswan Oasis Resort',
                'city_name': 'Aswan',
                'description': 'Peaceful resort on the banks of the Nile. Perfect for relaxation and cultural tours.',
                'accommodation_type': 'resort',
                'star_rating': 4,
                'price_per_night': Decimal('1900.00'),
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 2,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': False,
                'has_restaurant': True,
                'has_spa': True,
                'has_beach_access': False,
                'safety_score': 94,
                'is_verified': True,
                'is_active': True,
                'is_featured': True,
            },
            {
                'name': 'Downtown Cairo Apartment',
                'city_name': 'Cairo',
                'description': 'Modern apartment in the heart of Cairo. Walking distance to Egyptian Museum.',
                'accommodation_type': 'apartment',
                'star_rating': 3,
                'price_per_night': Decimal('800.00'),
                'max_guests': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'has_wifi': True,
                'has_parking': False,
                'has_pool': False,
                'has_gym': False,
                'has_restaurant': False,
                'has_spa': False,
                'has_beach_access': False,
                'safety_score': 88,
                'is_verified': True,
                'is_active': True,
                'is_featured': False,
            },
            {
                'name': 'Dahab Beach Villa',
                'city_name': 'Dahab',
                'description': 'Private villa with private beach access. Perfect for diving enthusiasts.',
                'accommodation_type': 'villa',
                'star_rating': 4,
                'price_per_night': Decimal('2800.00'),
                'max_guests': 8,
                'bedrooms': 4,
                'bathrooms': 3,
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': False,
                'has_restaurant': False,
                'has_spa': False,
                'has_beach_access': True,
                'safety_score': 92,
                'is_verified': True,
                'is_active': True,
                'is_featured': False,
            },
            {
                'name': 'Hurghada Budget Hostel',
                'city_name': 'Hurghada',
                'description': 'Clean and friendly hostel near the beach. Great for backpackers.',
                'accommodation_type': 'hostel',
                'star_rating': 2,
                'price_per_night': Decimal('350.00'),
                'max_guests': 1,
                'bedrooms': 1,
                'bathrooms': 1,
                'has_wifi': True,
                'has_parking': False,
                'has_pool': False,
                'has_gym': False,
                'has_restaurant': False,
                'has_spa': False,
                'has_beach_access': False,
                'safety_score': 85,
                'is_verified': True,
                'is_active': True,
                'is_featured': False,
            },
            {
                'name': 'Siwa Oasis Eco Lodge',
                'city_name': 'Siwa',
                'description': 'Unique eco-friendly lodge in the beautiful Siwa Oasis. Experience desert tranquility.',
                'accommodation_type': 'hotel',
                'star_rating': 3,
                'price_per_night': Decimal('1100.00'),
                'max_guests': 2,
                'bedrooms': 1,
                'bathrooms': 1,
                'has_wifi': False,
                'has_parking': True,
                'has_pool': True,
                'has_gym': False,
                'has_restaurant': True,
                'has_spa': False,
                'has_beach_access': False,
                'safety_score': 91,
                'is_verified': True,
                'is_active': True,
                'is_featured': False,
            },
        ]

        created_count = 0
        skipped_count = 0

        for acc_data in test_accommodations:
            # Get or create city
            city_name = acc_data.pop('city_name')
            city, _ = City.objects.get_or_create(
                name=city_name,
                defaults={'country': 'Egypt', 'is_popular': True}
            )

            # Check if accommodation already exists
            if Accommodation.objects.filter(name=acc_data['name']).exists():
                self.stdout.write(
                    self.style.WARNING(f'Skipped: {acc_data["name"]} (already exists)')
                )
                skipped_count += 1
                continue

            # Create accommodation
            accommodation = Accommodation.objects.create(
                city=city,
                **acc_data
            )

            self.stdout.write(
                self.style.SUCCESS(f'Created: {accommodation.name}')
            )
            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Done! Created {created_count} accommodations, skipped {skipped_count}'
            )
        )
