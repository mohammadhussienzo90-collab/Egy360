# accommodations/management/commands/populate_with_images.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accommodations.models import Accommodation
from tours.models import Tour


class Command(BaseCommand):
    help = 'Populate database with sample data including images'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate sample data with images...')

        # Get or create a user
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@egy360.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()

        # Clear existing data
        Accommodation.objects.all().delete()
        Tour.objects.all().delete()

        # Create Accommodations with images
        self.stdout.write('Creating accommodations with images...')
        accommodations_data = [
            {
                'name': 'Nile Luxury Hotel Cairo',
                'slug': 'nile-luxury-hotel-cairo',
                'city': 'Cairo',
                'accommodation_type': 'hotel',
                'description': 'Luxurious 5-star hotel overlooking the Nile River with panoramic views of Cairo',
                'address': 'Corniche El Nile, Downtown Cairo',
                'price_per_night': 150.00,
                'main_image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',
            },
            {
                'name': 'Pyramids View Resort',
                'slug': 'pyramids-view-resort',
                'city': 'Giza',
                'accommodation_type': 'resort',
                'description': 'Unique resort with stunning views of the Pyramids of Giza',
                'address': 'Pyramids Road, Giza',
                'price_per_night': 120.00,
                'main_image': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',
            },
            {
                'name': 'Luxor Temple Boutique Hotel',
                'slug': 'luxor-temple-boutique-hotel',
                'city': 'Luxor',
                'accommodation_type': 'hotel',
                'description': 'Charming boutique hotel steps away from Luxor Temple',
                'address': 'Corniche Street, Luxor',
                'price_per_night': 90.00,
                'main_image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80',
            },
            {
                'name': 'Red Sea Beach Resort',
                'slug': 'red-sea-beach-resort',
                'city': 'Hurghada',
                'accommodation_type': 'resort',
                'description': 'All-inclusive beach resort with private beach and diving center',
                'address': 'Safaga Road, Hurghada',
                'price_per_night': 180.00,
                'main_image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80',
            },
            {
                'name': 'Nubian Heritage Aswan',
                'slug': 'nubian-heritage-aswan',
                'city': 'Aswan',
                'accommodation_type': 'guesthouse',
                'description': 'Authentic Nubian guesthouse offering cultural experiences',
                'address': 'Elephantine Island, Aswan',
                'price_per_night': 60.00,
                'main_image': 'https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&q=80',
            },
            {
                'name': 'Mediterranean Pearl',
                'slug': 'mediterranean-pearl',
                'city': 'Alexandria',
                'accommodation_type': 'hotel',
                'description': 'Elegant seafront hotel with Mediterranean views',
                'address': 'Corniche Road, Alexandria',
                'price_per_night': 110.00,
                'main_image': 'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&q=80',
            },
        ]

        for acc_data in accommodations_data:
            acc = Accommodation.objects.create(**acc_data)
            self.stdout.write(self.style.SUCCESS(f'✓ {acc.name}'))

        # Create Tours with images (removed city and category)
        self.stdout.write('\nCreating tours with images...')
        tours_data = [
            {
                'name': 'Pyramids of Giza Tour',
                'slug': 'pyramids-giza-tour',
                'description': 'Explore the Great Pyramids and Sphinx with expert guide',
                'duration_days': 1,
                'price_per_person': 75.00,
                'max_group_size': 15,
                'difficulty_level': 'easy',
                'main_image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800&q=80',
            },
            {
                'name': 'Valley of the Kings',
                'slug': 'valley-of-kings',
                'description': 'Visit ancient pharaoh tombs and temples',
                'duration_days': 1,
                'price_per_person': 85.00,
                'max_group_size': 12,
                'difficulty_level': 'moderate',
                'main_image': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80',
            },
            {
                'name': 'Red Sea Diving',
                'slug': 'red-sea-diving',
                'description': 'Discover underwater coral reefs and marine life',
                'duration_days': 1,
                'price_per_person': 95.00,
                'max_group_size': 10,
                'difficulty_level': 'moderate',
                'main_image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80',
            },
            {
                'name': 'Nile Felucca Cruise',
                'slug': 'nile-felucca-cruise',
                'description': 'Sail on traditional Egyptian boat at sunset',
                'duration_days': 1,
                'price_per_person': 45.00,
                'max_group_size': 8,
                'difficulty_level': 'easy',
                'main_image': 'https://images.unsplash.com/photo-1569969356570-96e8d07c73a6?w=800&q=80',
            },
            {
                'name': 'Alexandria Walking Tour',
                'slug': 'alexandria-walking-tour',
                'description': 'Walk through Mediterranean history and culture',
                'duration_days': 1,
                'price_per_person': 65.00,
                'max_group_size': 15,
                'difficulty_level': 'easy',
                'main_image': 'https://images.unsplash.com/photo-1549144511-f099e773c147?w=800&q=80',
            },
            {
                'name': 'Abu Simbel Temples',
                'slug': 'abu-simbel-temples',
                'description': 'Marvel at Ramses II massive rock temples',
                'duration_days': 1,
                'price_per_person': 120.00,
                'max_group_size': 20,
                'difficulty_level': 'easy',
                'main_image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80',
            },
        ]

        for tour_data in tours_data:
            tour = Tour.objects.create(**tour_data)
            self.stdout.write(self.style.SUCCESS(f'✓ {tour.name}'))

        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('✅ SUCCESSFULLY CREATED!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS(f'✓ {Accommodation.objects.count()} accommodations with images'))
        self.stdout.write(self.style.SUCCESS(f'✓ {Tour.objects.count()} tours with images'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Visit your website to see beautiful images!'))