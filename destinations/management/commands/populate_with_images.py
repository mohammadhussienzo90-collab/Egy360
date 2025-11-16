# destinations/management/commands/populate_with_images.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta
from destinations.models import Destination
from accommodations.models import Accommodation
from tours.models import Tour
from transportation.models import TransportationService


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
            self.stdout.write(self.style.SUCCESS(f'Created admin user'))

        # Clear existing data
        self.stdout.write('Clearing existing sample data...')
        Destination.objects.all().delete()
        Accommodation.objects.all().delete()
        Tour.objects.all().delete()
        TransportationService.objects.all().delete()

        # Create Destinations with images
        self.stdout.write('Creating destinations with images...')
        destinations_data = [
            {
                'name': 'Cairo',
                'slug': 'cairo',
                'description': 'The capital city of Egypt, home to the iconic Pyramids of Giza, the Sphinx, and the Egyptian Museum. Experience the bustling streets of Islamic Cairo and Khan el-Khalili bazaar.',
                'country': 'Egypt',
                'region': 'Greater Cairo',
                'featured_image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80',
                'latitude': 30.0444,
                'longitude': 31.2357,
            },
            {
                'name': 'Luxor',
                'slug': 'luxor',
                'description': 'Known as the world\'s greatest open-air museum. Home to the Valley of the Kings, Karnak Temple, and Luxor Temple. A must-visit for history enthusiasts.',
                'country': 'Egypt',
                'region': 'Upper Egypt',
                'featured_image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800&q=80',
                'latitude': 25.6872,
                'longitude': 32.6396,
            },
            {
                'name': 'Hurghada',
                'slug': 'hurghada',
                'description': 'A stunning Red Sea resort town famous for its beautiful beaches, world-class diving spots, and vibrant coral reefs. Perfect for water sports and relaxation.',
                'country': 'Egypt',
                'region': 'Red Sea',
                'featured_image': 'https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80',
                'latitude': 27.2579,
                'longitude': 33.8116,
            },
            {
                'name': 'Aswan',
                'slug': 'aswan',
                'description': 'A serene Nile city known for Philae Temple, Abu Simbel temples, and traditional Nubian culture. Experience tranquil felucca rides on the Nile.',
                'country': 'Egypt',
                'region': 'Upper Egypt',
                'featured_image': 'https://images.unsplash.com/photo-1572252009467-c0c921e7e603?w=800&q=80',
                'latitude': 24.0889,
                'longitude': 32.8998,
            },
            {
                'name': 'Alexandria',
                'slug': 'alexandria',
                'description': 'Egypt\'s Mediterranean gem with rich Greco-Roman history. Visit the Bibliotheca Alexandrina, Citadel of Qaitbay, and enjoy fresh seafood by the sea.',
                'country': 'Egypt',
                'region': 'Mediterranean Coast',
                'featured_image': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80',
                'latitude': 31.2001,
                'longitude': 29.9187,
            },
        ]

        destinations = {}
        for dest_data in destinations_data:
            dest = Destination.objects.create(**dest_data)
            destinations[dest.name] = dest
            self.stdout.write(self.style.SUCCESS(f'Created destination: {dest.name}'))

        # Create Accommodations with images
        self.stdout.write('Creating accommodations with images...')
        accommodations_data = [
            {
                'name': 'Nile Luxury Hotel Cairo',
                'destination': destinations['Cairo'],
                'accommodation_type': 'hotel',
                'description': 'Luxurious 5-star hotel overlooking the Nile River with panoramic views of Cairo. Features elegant rooms, rooftop pool, and world-class dining.',
                'address': 'Corniche El Nile, Downtown Cairo',
                'stars': 5,
                'price_per_night': 150.00,
                'main_image': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': True,
                'safety_score': 95,
                'is_verified': True,
                'check_in_time': '14:00:00',
                'check_out_time': '12:00:00',
            },
            {
                'name': 'Pyramids View Resort',
                'destination': destinations['Cairo'],
                'accommodation_type': 'resort',
                'description': 'Unique resort with stunning views of the Pyramids of Giza. Experience ancient wonders from your room balcony.',
                'address': 'Pyramids Road, Giza',
                'stars': 4,
                'price_per_night': 120.00,
                'main_image': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'safety_score': 92,
                'is_verified': True,
                'check_in_time': '15:00:00',
                'check_out_time': '11:00:00',
            },
            {
                'name': 'Luxor Temple Boutique Hotel',
                'destination': destinations['Luxor'],
                'accommodation_type': 'hotel',
                'description': 'Charming boutique hotel steps away from Luxor Temple. Traditional Egyptian décor with modern amenities.',
                'address': 'Corniche Street, Luxor',
                'stars': 4,
                'price_per_night': 90.00,
                'main_image': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_restaurant': True,
                'safety_score': 90,
                'is_verified': True,
                'check_in_time': '14:00:00',
                'check_out_time': '12:00:00',
            },
            {
                'name': 'Red Sea Beach Resort Hurghada',
                'destination': destinations['Hurghada'],
                'accommodation_type': 'resort',
                'description': 'All-inclusive beach resort with private beach, multiple pools, water sports, and diving center. Perfect for families and couples.',
                'address': 'Safaga Road, Hurghada',
                'stars': 5,
                'price_per_night': 180.00,
                'main_image': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'has_spa': True,
                'has_beach_access': True,
                'safety_score': 96,
                'is_verified': True,
                'check_in_time': '15:00:00',
                'check_out_time': '12:00:00',
            },
            {
                'name': 'Nubian Heritage Aswan',
                'destination': destinations['Aswan'],
                'accommodation_type': 'guesthouse',
                'description': 'Authentic Nubian guesthouse offering cultural experiences, traditional meals, and warm hospitality on the Nile.',
                'address': 'Elephantine Island, Aswan',
                'stars': 3,
                'price_per_night': 60.00,
                'main_image': 'https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&q=80',
                'has_wifi': True,
                'has_parking': False,
                'has_restaurant': True,
                'safety_score': 88,
                'is_verified': True,
                'check_in_time': '13:00:00',
                'check_out_time': '11:00:00',
            },
            {
                'name': 'Mediterranean Pearl Alexandria',
                'destination': destinations['Alexandria'],
                'accommodation_type': 'hotel',
                'description': 'Elegant seafront hotel with Mediterranean views, fresh seafood restaurant, and easy access to historical sites.',
                'address': 'Corniche Road, Alexandria',
                'stars': 4,
                'price_per_night': 110.00,
                'main_image': 'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&q=80',
                'has_wifi': True,
                'has_parking': True,
                'has_pool': True,
                'has_gym': True,
                'has_restaurant': True,
                'safety_score': 91,
                'is_verified': True,
                'check_in_time': '14:00:00',
                'check_out_time': '12:00:00',
            },
        ]

        for acc_data in accommodations_data:
            acc = Accommodation.objects.create(**acc_data)
            self.stdout.write(self.style.SUCCESS(f'Created accommodation: {acc.name}'))

        # Create Tours with images
        self.stdout.write('Creating tours with images...')
        tours_data = [
            {
                'name': 'Pyramids of Giza Full Day Tour',
                'destination': destinations['Cairo'],
                'slug': 'pyramids-giza-full-day-tour',
                'description': 'Explore the last remaining wonder of the ancient world! Visit the Great Pyramid of Khufu, Khafre, Menkaure, and the mysterious Sphinx. Includes camel ride and Egyptian lunch.',
                'duration_days': 1,
                'price_per_person': 75.00,
                'max_group_size': 15,
                'difficulty_level': 'easy',
                'category': 'cultural',
                'main_image': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800&q=80',
                'includes_meals': True,
                'includes_transport': True,
                'includes_guide': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 95,
            },
            {
                'name': 'Valley of the Kings Explorer',
                'destination': destinations['Luxor'],
                'slug': 'valley-of-kings-explorer',
                'description': 'Journey into the ancient burial grounds of pharaohs. Visit King Tut\'s tomb, Temple of Hatshepsut, and Colossi of Memnon. Full-day guided tour with lunch.',
                'duration_days': 1,
                'price_per_person': 85.00,
                'max_group_size': 12,
                'difficulty_level': 'moderate',
                'category': 'historical',
                'main_image': 'https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80',
                'includes_meals': True,
                'includes_transport': True,
                'includes_guide': True,
                'includes_tickets': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 93,
            },
            {
                'name': 'Red Sea Diving Adventure',
                'destination': destinations['Hurghada'],
                'slug': 'red-sea-diving-adventure',
                'description': 'Discover the underwater paradise of the Red Sea. Two-dive trip to pristine coral reefs teeming with marine life. All equipment included, suitable for beginners.',
                'duration_days': 1,
                'price_per_person': 95.00,
                'max_group_size': 10,
                'difficulty_level': 'moderate',
                'category': 'adventure',
                'main_image': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80',
                'includes_meals': True,
                'includes_transport': True,
                'includes_guide': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 97,
            },
            {
                'name': 'Nile Felucca Sunset Cruise',
                'destination': destinations['Aswan'],
                'slug': 'nile-felucca-sunset-cruise',
                'description': 'Sail on a traditional Egyptian felucca at sunset. Peaceful journey on the Nile with views of Aswan\'s islands and ancient ruins. Includes refreshments and Nubian music.',
                'duration_days': 1,
                'price_per_person': 45.00,
                'max_group_size': 8,
                'difficulty_level': 'easy',
                'category': 'nature',
                'main_image': 'https://images.unsplash.com/photo-1569969356570-96e8d07c73a6?w=800&q=80',
                'includes_transport': True,
                'includes_guide': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 90,
            },
            {
                'name': 'Alexandria Historical Walking Tour',
                'destination': destinations['Alexandria'],
                'slug': 'alexandria-historical-walking-tour',
                'description': 'Walk through history in Egypt\'s Mediterranean jewel. Visit Bibliotheca Alexandrina, Citadel of Qaitbay, Catacombs, and Montazah Palace. Includes seafood lunch.',
                'duration_days': 1,
                'price_per_person': 65.00,
                'max_group_size': 15,
                'difficulty_level': 'easy',
                'category': 'cultural',
                'main_image': 'https://images.unsplash.com/photo-1549144511-f099e773c147?w=800&q=80',
                'includes_meals': True,
                'includes_transport': True,
                'includes_guide': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 92,
            },
            {
                'name': 'Abu Simbel Temples Day Trip',
                'destination': destinations['Aswan'],
                'slug': 'abu-simbel-temples-day-trip',
                'description': 'Marvel at Ramses II\'s massive rock temples at Abu Simbel. Early morning departure to witness sunrise at these magnificent UNESCO World Heritage sites.',
                'duration_days': 1,
                'price_per_person': 120.00,
                'max_group_size': 20,
                'difficulty_level': 'easy',
                'category': 'historical',
                'main_image': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80',
                'includes_transport': True,
                'includes_guide': True,
                'includes_tickets': True,
                'is_private': False,
                'is_verified': True,
                'safety_score': 94,
            },
        ]

        for tour_data in tours_data:
            tour = Tour.objects.create(**tour_data)
            self.stdout.write(self.style.SUCCESS(f'Created tour: {tour.name}'))

        # Create Transportation Services with images
        self.stdout.write('Creating transportation services with images...')
        transportation_data = [
            {
                'name': 'Cairo Airport Premium Transfer',
                'slug': 'cairo-airport-premium-transfer',
                'service_type': 'airport_transfer',
                'description': 'Luxurious private transfer from Cairo International Airport to your hotel. Professional driver, meet & greet service, complimentary water.',
                'vehicle_brand': 'Mercedes',
                'vehicle_model': 'E-Class',
                'year': 2023,
                'max_passengers': 3,
                'max_luggage': 3,
                'fixed_price': 45.00,
                'main_image': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&q=80',
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_insurance': True,
                'is_verified': True,
                'safety_score': 98,
            },
            {
                'name': 'Private City Tour Car',
                'slug': 'private-city-tour-car',
                'service_type': 'private_car',
                'description': 'Comfortable sedan for private city tours and sightseeing. Air-conditioned with experienced driver-guide. Perfect for exploring Cairo attractions.',
                'vehicle_brand': 'Toyota',
                'vehicle_model': 'Camry',
                'year': 2022,
                'max_passengers': 4,
                'max_luggage': 2,
                'price_per_hour': 25.00,
                'main_image': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&q=80',
                'has_ac': True,
                'has_wifi': False,
                'has_gps': True,
                'has_insurance': True,
                'is_verified': True,
                'safety_score': 95,
            },
            {
                'name': 'Family Minivan Service',
                'slug': 'family-minivan-service',
                'service_type': 'minivan',
                'description': 'Spacious minivan ideal for families and groups. Comfortable seating for 7 passengers with ample luggage space. Air-conditioned with entertainment system.',
                'vehicle_brand': 'Hyundai',
                'vehicle_model': 'H1',
                'year': 2023,
                'max_passengers': 7,
                'max_luggage': 5,
                'price_per_hour': 35.00,
                'main_image': 'https://images.unsplash.com/photo-1527786356703-4b100091cd2c?w=800&q=80',
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_insurance': True,
                'is_verified': True,
                'safety_score': 96,
            },
            {
                'name': 'Luxury Limousine Service',
                'slug': 'luxury-limousine-service',
                'service_type': 'limousine',
                'description': 'Executive limousine service for VIP transfers and special occasions. Premium comfort with leather seats, climate control, and professional chauffeur.',
                'vehicle_brand': 'BMW',
                'vehicle_model': '7 Series',
                'year': 2024,
                'max_passengers': 3,
                'max_luggage': 3,
                'price_per_hour': 65.00,
                'main_image': 'https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&q=80',
                'has_ac': True,
                'has_wifi': True,
                'has_gps': True,
                'has_insurance': True,
                'is_verified': True,
                'safety_score': 99,
            },
            {
                'name': 'Budget Taxi Service',
                'slug': 'budget-taxi-service',
                'service_type': 'taxi',
                'description': 'Affordable taxi service for short trips around the city. Metered rates, clean vehicles, and friendly drivers. Available 24/7.',
                'vehicle_brand': 'Peugeot',
                'vehicle_model': '301',
                'year': 2021,
                'max_passengers': 4,
                'max_luggage': 2,
                'price_per_km': 2.50,
                'main_image': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=800&q=80',
                'has_ac': True,
                'has_gps': True,
                'has_insurance': True,
                'is_verified': True,
                'safety_score': 90,
            },
        ]

        for trans_data in transportation_data:
            trans = TransportationService.objects.create(**trans_data)
            self.stdout.write(self.style.SUCCESS(f'Created transportation: {trans.name}'))

        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('✅ Sample data with images created successfully!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS(f'Created {Destination.objects.count()} destinations'))
        self.stdout.write(self.style.SUCCESS(f'Created {Accommodation.objects.count()} accommodations'))
        self.stdout.write(self.style.SUCCESS(f'Created {Tour.objects.count()} tours'))
        self.stdout.write(
            self.style.SUCCESS(f'Created {TransportationService.objects.count()} transportation services'))
        self.stdout.write(self.style.SUCCESS('\n🎉 Your website now has beautiful images!'))