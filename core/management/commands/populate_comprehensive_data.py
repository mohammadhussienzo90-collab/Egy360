"""
Comprehensive Data Population for Egy360
Generates realistic Egyptian tourism data for testing and demonstration

Run with: python manage.py populate_comprehensive_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Import all models
from destinations.models import Country, City, Attraction
from accommodations.models import Accommodation, Amenity
from tours.models import Tour, TourItinerary
from blog.models import BlogPost, BlogCategory


class Command(BaseCommand):
    help = 'Populates database with comprehensive Egyptian tourism data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting comprehensive data population...'))

        # Create admin user if doesn't exist
        self.create_admin_user()

        # Create data in order of dependencies
        self.create_amenities()
        self.create_country_and_cities()
        self.create_attractions()
        self.create_accommodations()
        self.create_tours()
        self.create_blog_content()

        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] All data created successfully!'))
        self.stdout.write(self.style.SUCCESS('Summary:'))
        self.stdout.write(f'  - Cities: {City.objects.count()}')
        self.stdout.write(f'  - Attractions: {Attraction.objects.count()}')
        self.stdout.write(f'  - Accommodations: {Accommodation.objects.count()}')
        self.stdout.write(f'  - Tours: {Tour.objects.count()}')
        self.stdout.write(f'  - Blog Posts: {BlogPost.objects.count()}')

    def create_admin_user(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@egytravel360.com',
                password='admin123'  # Change this!
            )
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Admin user created (username: admin, password: admin123)'))
        else:
            self.stdout.write('[INFO] Admin user already exists')

    def create_amenities(self):
        amenities = [
            'Free WiFi', 'Swimming Pool', 'Restaurant', 'Bar', 'Spa',
            'Gym/Fitness Center', 'Airport Shuttle', 'Room Service',
            'Air Conditioning', 'Parking', 'Laundry Service', 'Concierge',
            'Business Center', 'Pet Friendly', 'Nile View', 'Garden View',
            'Rooftop Terrace', 'Hot Tub', 'Sauna', '24-Hour Front Desk'
        ]

        icon_map = {
            'Free WiFi': 'fa-wifi', 'Swimming Pool': 'fa-swimming-pool', 'Restaurant': 'fa-utensils',
            'Bar': 'fa-cocktail', 'Spa': 'fa-spa', 'Gym': 'fa-dumbbell', 'Room Service': 'fa-concierge-bell',
            'Air Conditioning': 'fa-snowflake', 'Parking': 'fa-parking', 'Airport Shuttle': 'fa-bus',
            'Beach Access': 'fa-umbrella-beach', 'Business Center': 'fa-briefcase', '24/7 Reception': 'fa-clock',
            'Laundry Service': 'fa-tshirt', 'Pet Friendly': 'fa-paw', 'Family Rooms': 'fa-home',
            'Non-Smoking Rooms': 'fa-smoking-ban', 'Safe': 'fa-lock', 'Mini Bar': 'fa-glass-martini',
            'TV': 'fa-tv', 'Balcony': 'fa-door-open', 'Kitchen': 'fa-blender', 'Hot Tub': 'fa-hot-tub',
            'Garden': 'fa-tree'
        }
        for name in amenities:
            Amenity.objects.get_or_create(name=name, defaults={'icon': icon_map.get(name, 'fa-check')})

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {len(amenities)} amenities'))

    def create_country_and_cities(self):
        # Create Egypt
        egypt, _ = Country.objects.get_or_create(
            name='Egypt',
            defaults={
                'code': 'EG',
                'description': 'Land of Pharaohs, home to ancient civilizations and modern wonders'
            }
        )

        # Major Egyptian cities
        cities_data = [
            {
                'name': 'Cairo',
                'description': 'Egypt\'s capital and largest city, home to the Pyramids of Giza and the Egyptian Museum',
                'is_popular': True,
                'latitude': 30.0444,
                'longitude': 31.2357
            },
            {
                'name': 'Luxor',
                'description': 'Ancient Thebes, the world\'s greatest open-air museum with Valley of the Kings',
                'is_popular': True,
                'latitude': 25.6872,
                'longitude': 32.6396
            },
            {
                'name': 'Aswan',
                'description': 'Beautiful Nile city known for its stunning river views and Nubian culture',
                'is_popular': True,
                'latitude': 24.0889,
                'longitude': 32.8998
            },
            {
                'name': 'Alexandria',
                'description': 'Mediterranean pearl, Egypt\'s second-largest city with rich Greco-Roman heritage',
                'is_popular': True,
                'latitude': 31.2001,
                'longitude': 29.9187
            },
            {
                'name': 'Sharm El Sheikh',
                'description': 'Red Sea resort paradise, world-class diving and beach destination',
                'is_popular': True,
                'latitude': 27.9158,
                'longitude': 34.3300
            },
            {
                'name': 'Hurghada',
                'description': 'Red Sea resort town, perfect for diving, snorkeling and water sports',
                'is_popular': True,
                'latitude': 27.2579,
                'longitude': 33.8116
            },
        ]

        for city_data in cities_data:
            City.objects.get_or_create(
                name=city_data['name'],
                country=egypt,
                defaults={
                    'slug': slugify(city_data['name']),
                    'description': city_data['description'],
                    'is_popular': city_data.get('is_popular', False),
                    'latitude': city_data.get('latitude'),
                    'longitude': city_data.get('longitude')
                }
            )

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {len(cities_data)} cities'))

    def create_attractions(self):
        attractions_data = {
            'Cairo': [
                ('Pyramids of Giza', 'The last remaining Wonder of the Ancient World', True, 5000),
                ('Egyptian Museum', 'World\'s largest collection of Pharaonic antiquities', True, 4500),
                ('Khan El Khalili', 'Historic bazaar and souk in Islamic Cairo', True, 4200),
                ('Citadel of Saladin', 'Medieval Islamic fortification with stunning mosques', True, 4000),
                ('Al-Azhar Mosque', 'One of Cairo\'s oldest mosques and Islamic university', True, 3800),
                ('Coptic Cairo', 'Historic area with ancient Christian churches', False, 3500),
                ('Cairo Tower', 'Iconic tower with panoramic city views', False, 3200),
                ('Saqqara', 'Ancient burial ground with Step Pyramid', False, 3000),
            ],
            'Luxor': [
                ('Valley of the Kings', 'Ancient pharaohs\' royal burial tombs', True, 5000),
                ('Karnak Temple', 'Massive temple complex, largest in Egypt', True, 4800),
                ('Luxor Temple', 'Stunning temple in the heart of Luxor', True, 4500),
                ('Hatshepsut Temple', 'Magnificent mortuary temple carved into cliff', True, 4300),
                ('Colossi of Memnon', 'Massive stone statues of Pharaoh Amenhotep III', True, 4000),
                ('Valley of the Queens', 'Royal tombs of queens and princes', False, 3800),
                ('Luxor Museum', 'Well-curated collection of ancient artifacts', False, 3500),
            ],
            'Aswan': [
                ('Abu Simbel', 'Magnificent rock temples of Ramesses II', True, 5000),
                ('Philae Temple', 'Beautiful island temple dedicated to Isis', True, 4500),
                ('Aswan High Dam', 'Modern engineering marvel controlling the Nile', True, 4200),
                ('Nubian Village', 'Experience authentic Nubian culture and hospitality', True, 4000),
                ('Unfinished Obelisk', 'Ancient quarry with massive incomplete obelisk', False, 3500),
                ('Elephantine Island', 'Historic island with ancient ruins', False, 3300),
            ],
            'Alexandria': [
                ('Bibliotheca Alexandrina', 'Modern tribute to ancient Library of Alexandria', True, 4500),
                ('Qaitbay Citadel', 'Historic fortress on Mediterranean coast', True, 4300),
                ('Catacombs of Kom el Shoqafa', 'Roman burial chambers blending cultures', True, 4000),
                ('Montaza Palace', 'Royal palace with beautiful gardens', True, 3800),
                ('Alexandria National Museum', 'Artifacts spanning all Egyptian eras', False, 3500),
            ],
            'Sharm El Sheikh': [
                ('Ras Mohammed National Park', 'World-renowned diving and snorkeling site', True, 4800),
                ('Naama Bay', 'Popular beach resort area with dining and nightlife', True, 4500),
                ('Blue Hole', 'Famous diving spot with unique underwater formations', True, 4300),
                ('St. Catherine\'s Monastery', 'Historic Christian monastery at Mt. Sinai', True, 4000),
            ],
            'Hurghada': [
                ('Giftun Island', 'Beautiful island for snorkeling and diving', True, 4500),
                ('Hurghada Marina', 'Modern marina with shops, restaurants and nightlife', True, 4200),
                ('Mahmya Beach', 'Pristine white sand beach on protected island', True, 4000),
            ],
        }

        total_attractions = 0
        for city_name, attractions in attractions_data.items():
            city = City.objects.get(name=city_name)
            for name, desc, is_must_see, visitors in attractions:
                Attraction.objects.get_or_create(
                    name=name,
                    city=city,
                    defaults={
                        'slug': slugify(name),
                        'description': desc,
                        'is_must_see': is_must_see,
                        'attraction_type': 'historical' if 'Pyramid' in name or 'Temple' in name else 'archaeological',
                        'address': city_name,
                        'is_family_friendly': True
                    }
                )
                total_attractions += 1

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {total_attractions} attractions'))

    def create_accommodations(self):
        # Get amenities
        all_amenities = list(Amenity.objects.all())

        accommodations_data = {
            'Cairo': [
                ('Four Seasons Hotel Cairo at Nile Plaza', 5, 'hotel', 3500, 'Luxury 5-star hotel overlooking the Nile with world-class amenities'),
                ('Marriott Mena House', 5, 'hotel', 3200, 'Historic luxury hotel with stunning Pyramids views'),
                ('The Nile Ritz-Carlton', 5, 'hotel', 3000, 'Elegant riverside luxury hotel in heart of Cairo'),
                ('Sofitel Cairo Nile El Gezirah', 5, 'hotel', 2800, 'French luxury on Gezira Island with Nile panoramas'),
                ('Kempinski Nile Hotel', 5, 'hotel', 2600, 'Modern luxury hotel with rooftop pool and spa'),
                ('Steigenberger Hotel El Tahrir', 4, 'hotel', 1800, 'Central 4-star hotel near Egyptian Museum'),
                ('Ramses Hilton', 4, 'hotel', 1600, 'Downtown hotel with Nile views and multiple dining options'),
                ('Le Meridien Pyramids', 4, 'hotel', 1400, 'Modern hotel close to the Pyramids'),
                ('Guardian Guest House', 3, 'hostel', 600, 'Budget-friendly hostel near pyramids'),
                ('Cairo City Center Hostel', 2, 'hostel', 400, 'Affordable downtown hostel for backpackers'),
                ('Zamalek Boutique Hotel', 3, 'hotel', 900, 'Charming boutique hotel in upscale Zamalek'),
                ('Cairo Pyramids Hotel', 3, 'hotel', 800, 'Budget hotel with pyramids view'),
                ('Nile View Apartment', 3, 'apartment', 1200, 'Spacious apartment with Nile views'),
                ('Garden City Suite', 3, 'apartment', 1000, 'Modern furnished apartment in Garden City'),
                ('Cairo Central Hostel', 2, 'hostel', 350, 'Social hostel with rooftop terrace'),
            ],
            'Luxor': [
                ('Sofitel Winter Palace Luxor', 5, 'hotel', 2500, 'Historic Victorian-era luxury palace on the Nile'),
                ('Hilton Luxor Resort & Spa', 5, 'hotel', 2200, 'Full-service resort with Nile views and spa'),
                ('Pavillon Winter Luxor', 4, 'hotel', 1500, 'Charming Nile-side hotel near temples'),
                ('Steigenberger Nile Palace', 4, 'hotel', 1400, 'Elegant hotel in heart of Luxor'),
                ('Sonesta St. George Hotel', 4, 'hotel', 1300, 'Nile cruise-style hotel in Luxor'),
                ('Nefertiti Hotel', 3, 'hotel', 700, 'Family-run hotel near Karnak Temple'),
                ('Bob Marley Peace Hotel', 2, 'hostel', 400, 'Budget hostel with Nile views'),
                ('Happy Land Hotel', 3, 'hotel', 600, 'Affordable hotel near Luxor Temple'),
                ('Luxor Nile Apartment', 3, 'apartment', 900, 'Modern apartment overlooking Nile'),
                ('West Bank Villa', 3, 'villa', 1800, 'Traditional villa near Valley of Kings'),
            ],
            'Aswan': [
                ('Sofitel Legend Old Cataract', 5, 'hotel', 2800, 'Legendary Victorian palace hotel on the Nile'),
                ('Movenpick Resort Aswan', 5, 'hotel', 2200, 'Island resort on Elephantine Island'),
                ('Pyramisa Isis Island Resort', 4, 'hotel', 1400, 'Island resort with lush gardens'),
                ('Basma Hotel Aswan', 4, 'hotel', 1100, 'Hillside hotel with panoramic Nile views'),
                ('Tolip Aswan Hotel', 4, 'hotel', 1000, 'Modern hotel on the Corniche'),
                ('Nubian Eco Village', 3, 'villa', 1500, 'Authentic Nubian experience in traditional village'),
                ('Anakato Nubian Houses', 3, 'villa', 1200, 'Colorful Nubian-style guesthouse'),
                ('Oscar Hotel', 3, 'hotel', 700, 'Budget hotel with rooftop terrace'),
            ],
            'Alexandria': [
                ('Four Seasons Hotel Alexandria', 5, 'hotel', 2600, 'Beachfront luxury with Mediterranean elegance'),
                ('Hilton Alexandria Corniche', 5, 'hotel', 2200, 'Waterfront hotel in city center'),
                ('Steigenberger Cecil Hotel', 4, 'hotel', 1600, 'Historic landmark hotel since 1929'),
                ('Sheraton Montazah Hotel', 4, 'hotel', 1400, 'Resort-style hotel near Montazah Palace'),
                ('Paradise Inn Le Metropole', 4, 'hotel', 1200, 'Art Deco charm on the Corniche'),
                ('Alexander The Great Hotel', 3, 'hotel', 800, 'Mid-range hotel near beaches'),
                ('Aifu Resort', 3, 'hotel', 900, 'Beach resort in Agami area'),
                ('Mediterranean Breeze Apartment', 3, 'apartment', 1100, 'Sea-view apartment'),
            ],
            'Sharm El Sheikh': [
                ('Four Seasons Resort Sharm El Sheikh', 5, 'resort', 4000, 'Ultra-luxury Red Sea resort with private beach'),
                ('Rixos Premium Seagate', 5, 'resort', 3500, 'All-inclusive ultra-luxury resort'),
                ('Movenpick Resort Sharm El Sheikh', 5, 'resort', 3200, 'Beachfront resort with excellent diving'),
                ('Sheraton Sharm Hotel', 5, 'resort', 3000, 'Large resort complex with aqua park'),
                ('Savoy Sharm El Sheikh', 5, 'resort', 2800, 'Elegant resort in Naama Bay'),
                ('Jaz Belvedere Resort', 4, 'resort', 1800, 'Family-friendly all-inclusive resort'),
                ('Tropitel Naama Bay Hotel', 4, 'resort', 1600, 'Central Naama Bay location'),
                ('Sharm Inn Amarein', 3, 'hotel', 900, 'Budget hotel near beach'),
                ('Bedouin Moon Hotel', 3, 'hotel', 800, 'Authentic Bedouin-style accommodation'),
                ('Desert Camp Sharm', 2, 'desert_camp', 600, 'Traditional Bedouin desert camp experience'),
            ],
            'Hurghada': [
                ('Steigenberger Al Dau Beach Hotel', 5, 'resort', 2800, 'Luxury all-inclusive beachfront resort'),
                ('Hilton Hurghada Resort', 5, 'resort', 2500, 'Full-service resort with private beach'),
                ('Marriott Hurghada Beach Resort', 5, 'resort', 2400, 'Family-friendly resort with aqua park'),
                ('Jaz Aquaviva Resort', 4, 'resort', 1600, 'Modern resort with diving center'),
                ('Three Corners Rihana Resort', 4, 'resort', 1400, 'All-inclusive beach resort'),
            ],
        }

        total_accommodations = 0
        for city_name, accommodations in accommodations_data.items():
            city = City.objects.get(name=city_name)
            for name, stars, acc_type, price, desc in accommodations:
                # Create accommodation
                accommodation, created = Accommodation.objects.get_or_create(
                    name=name,
                    city=city,
                    defaults={
                        'slug': slugify(name),
                        'accommodation_type': acc_type,
                        'description': desc,
                        'star_rating': stars if stars <= 5 else 5,
                        'price_per_night': Decimal(str(price)),
                        'address': f'{name}, {city_name}, Egypt',
                        'is_active': True,
                        'is_featured': stars >= 4,
                    }
                )

                if created:
                    # Add random amenities based on star rating
                    num_amenities = min(stars * 3, len(all_amenities))
                    selected_amenities = random.sample(all_amenities, num_amenities)
                    accommodation.amenities.set(selected_amenities)
                    total_accommodations += 1

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {total_accommodations} accommodations'))

    def create_tours(self):
        tours_data = [
            # Cairo Tours
            ('Pyramids and Sphinx Full Day Tour', 'cultural', 'Cairo', 1, 0, 1200,
             'Visit the Great Pyramids of Giza, Sphinx, and Solar Boat Museum',
             ['Pyramids of Giza', 'Great Sphinx', 'Solar Boat Museum', 'Lunch at local restaurant']),

            ('Egyptian Museum and Islamic Cairo', 'cultural', 'Cairo', 1, 0, 1000,
             'Explore ancient artifacts and medieval Islamic architecture',
             ['Egyptian Museum', 'Saladin Citadel', 'Mohamed Ali Mosque', 'Khan El Khalili bazaar']),

            ('Cairo Day Tour: Pyramids, Museum & Bazaar', 'cultural', 'Cairo', 1, 0, 1500,
             'Complete Cairo experience in one day',
             ['Giza Pyramids', 'Egyptian Museum', 'Khan El Khalili shopping']),

            # Luxor Tours
            ('Valley of the Kings and Karnak Temple', 'cultural', 'Luxor', 1, 0, 1500,
             'Explore ancient pharaonic tombs and massive temple complex',
             ['Valley of the Kings (3 tombs)', 'Temple of Hatshepsut', 'Colossi of Memnon', 'Karnak Temple']),

            ('Luxor Hot Air Balloon Ride', 'adventure', 'Luxor', 1, 0, 2500,
             'Sunrise balloon flight over ancient Thebes',
             ['Pre-dawn pickup', 'Hot air balloon flight (45-60 min)', 'Champagne celebration', 'Certificate']),

            ('Luxor West and East Bank Full Day', 'cultural', 'Luxor', 1, 0, 1800,
             'Complete tour of Luxor\'s ancient sites',
             ['Valley of Kings', 'Hatshepsut Temple', 'Karnak Temple', 'Luxor Temple', 'Lunch included']),

            # Aswan Tours
            ('Abu Simbel Day Trip from Aswan', 'cultural', 'Aswan', 1, 0, 2000,
             'Visit Ramesses II magnificent rock temples',
             ['Early morning departure', 'Abu Simbel Temples', 'Guided tour', 'Return to Aswan']),

            ('Philae Temple and High Dam Tour', 'cultural', 'Aswan', 1, 0, 1200,
             'Explore Aswan\'s main attractions',
             ['Aswan High Dam', 'Philae Temple by boat', 'Unfinished Obelisk']),

            ('Nubian Village Experience', 'cultural', 'Aswan', 1, 0, 800,
             'Immerse in authentic Nubian culture',
             ['Felucca ride to village', 'Nubian house visit', 'Traditional tea', 'Henna painting option']),

            # Multi-city Tours
            ('Cairo, Luxor & Aswan: 7-Day Nile Cruise', 'cruise', 'Cairo', 6, 5, 15000,
             'Complete Egypt experience with Nile cruise',
             ['Cairo sightseeing (2 days)', 'Flight to Luxor', 'Nile cruise Luxor-Aswan (4 nights)',
              'All temples included', 'Most meals included', 'Return from Aswan']),

            ('Cairo and Alexandria: 3-Day Tour', 'cultural', 'Cairo', 2, 2, 3500,
             'Explore Egypt\'s ancient and Mediterranean cities',
             ['Cairo Pyramids & Museum', 'Drive to Alexandria', 'Alexandria city tour',
              'Bibliotheca & Qaitbay', 'Return to Cairo']),

            # Red Sea Tours
            ('Ras Mohammed Diving Day Trip', 'diving', 'Sharm El Sheikh', 1, 0, 1400,
             'World-class diving at Ras Mohammed National Park',
             ['2 guided dives', 'Equipment included', 'Boat trip', 'Lunch & drinks',
              'Professional instructor', 'All levels welcome']),

            ('Sharm El Sheikh: Quad Bike Desert Safari', 'adventure', 'Sharm El Sheikh', 1, 0, 900,
             'Thrilling desert adventure and Bedouin experience',
             ['Hotel pickup', 'Quad bike ride', 'Bedouin camp visit', 'Camel ride', 'BBQ dinner', 'Star gazing']),

            ('St. Catherine Monastery and Mt. Sinai Sunrise', 'religious', 'Sharm El Sheikh', 1, 1, 1600,
             'Climb Moses Mountain for sunrise and visit historic monastery',
             ['Midnight departure', 'Mt. Sinai climb', 'Sunrise viewing', 'St. Catherine Monastery tour',
              'Breakfast', 'Return to hotel']),

            ('Hurghada: Giftun Island Snorkeling Trip', 'diving', 'Hurghada', 1, 0, 1000,
             'Snorkel pristine coral reefs at protected island',
             ['Boat trip to Giftun Island', '2 snorkeling spots', 'Lunch buffet',
              'Beach relaxation', 'Snorkeling equipment included']),

            ('Hurghada: Dolphin House Snorkeling', 'diving', 'Hurghada', 1, 0, 1200,
             'Swim with wild dolphins in their natural habitat',
             ['Dolphin House reef', 'Snorkeling with dolphins', 'Lunch on boat', 'Multiple snorkel spots']),

            # Luxury Tours
            ('Cairo Private Tour: Pyramids, Saqqara & Memphis', 'luxury', 'Cairo', 1, 0, 3500,
             'VIP private tour with Egyptologist guide',
             ['Private vehicle & guide', 'Giza Pyramids VIP access', 'Saqqara Step Pyramid',
              'Memphis ancient capital', 'Luxury lunch', 'No shopping stops']),

            # Budget Tours
            ('Cairo Budget Tour: Pyramids & Museum', 'budget', 'Cairo', 1, 0, 600,
             'Affordable group tour covering main Cairo attractions',
             ['Small group tour', 'Pyramids of Giza', 'Egyptian Museum', 'Basic lunch included']),

            ('Luxor Budget Day Tour', 'budget', 'Luxor', 1, 0, 800,
             'Affordable Luxor highlights tour',
             ['East Bank: Karnak & Luxor temples', 'West Bank: Valley of Kings', 'Group tour']),

            # Family Tours
            ('Cairo Family Adventure: Pyramids & Camel Ride', 'family', 'Cairo', 1, 0, 1800,
             'Family-friendly pyramid experience with camel rides',
             ['Pyramids exploration', 'Camel or horse ride', 'Child-friendly guide',
              'Photo opportunities', 'Ice cream stop']),
        ]

        total_tours = 0
        for (name, tour_type, departure_city, days, nights, price, desc, highlights) in tours_data:
            tour, created = Tour.objects.get_or_create(
                name=name,
                defaults={
                    'slug': slugify(name),
                    'tour_type': tour_type,
                    'departure_city': departure_city,
                    'description': desc,
                    'highlights': desc,
                    'duration_days': days,
                    'duration_nights': nights,
                    'price_per_person': Decimal(str(price)),
                    'child_discount': Decimal('20.00'),
                    'min_group_size': 2,
                    'max_group_size': 15,
                    'difficulty_level': 'easy',
                    'includes': highlights,
                    'excludes': ['Personal expenses', 'Tipping', 'Additional beverages'],
                    'is_active': True,
                    'is_featured': price >= 2000,
                }
            )

            if created and days > 1:
                # Create itinerary for multi-day tours
                for day in range(1, days + 1):
                    if day < len(highlights):
                        overnight = f'Hotel in {tour.city.name if hasattr(tour, "city") else "destination"}' if (nights > 0 and day < days) else ''
                        TourItinerary.objects.create(
                            tour=tour,
                            day=day,
                            title=f'Day {day}',
                            description=highlights[day-1] if day <= len(highlights) else f'Day {day} activities',
                            meals_included='Breakfast, Lunch' if day > 1 else 'Lunch',
                            overnight_location=overnight
                        )
                total_tours += 1

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {total_tours} tours'))

    def create_blog_content(self):
        # Create blog categories
        category_travel, _ = BlogCategory.objects.get_or_create(
            name='Travel Guides',
            slug='travel-guides',
            defaults={'description': 'Comprehensive travel guides for Egypt'}
        )

        category_hotels, _ = BlogCategory.objects.get_or_create(
            name='Hotel Reviews',
            slug='hotel-reviews',
            defaults={'description': 'Top hotel recommendations across Egypt'}
        )

        category_safety, _ = BlogCategory.objects.get_or_create(
            name='Safety & Tips',
            slug='safety-tips',
            defaults={'description': 'Safety information and travel tips'}
        )

        # Get admin user for blog posts
        admin_user = User.objects.filter(is_superuser=True).first()

        blog_posts = [
            # Top Hotels Articles
            ('Top 5 Luxury Hotels in Cairo', category_hotels, '''
# Top 5 Luxury Hotels in Cairo

Cairo offers some of the most luxurious accommodations in the Middle East. Here are our top picks:

## 1. Four Seasons Hotel Cairo at Nile Plaza

The pinnacle of luxury in Cairo, this 5-star masterpiece offers breathtaking Nile views, Michelin-quality dining, and impeccable service. Located in the heart of Cairo with easy access to all major attractions.

**Price:** From 3,500 EGP/night
**Highlights:** Nile views, rooftop pool, world-class spa

## 2. Marriott Mena House

Step into history at this legendary hotel with direct views of the Pyramids. Originally a royal hunting lodge, it combines Victorian charm with modern luxury.

**Price:** From 3,200 EGP/night
**Highlights:** Pyramid views, historic property, beautiful gardens

## 3. The Nile Ritz-Carlton

Elegant riverside luxury in the heart of downtown Cairo. Perfect for business and leisure travelers seeking refined sophistication.

**Price:** From 3,000 EGP/night
**Highlights:** Central location, executive lounge, fine dining

## 4. Sofitel Cairo Nile El Gezirah

French elegance meets Egyptian hospitality on the exclusive Gezira Island. Stunning Nile panoramas from every room.

**Price:** From 2,800 EGP/night
**Highlights:** Island location, French cuisine, elegant design

## 5. Kempinski Nile Hotel

Modern luxury hotel with contemporary design and exceptional service. The rooftop pool offers spectacular Cairo skyline views.

**Price:** From 2,600 EGP/night
**Highlights:** Rooftop pool, modern design, central location
            '''),

            ('Top 5 Hotels in Luxor: Valley of the Kings Edition', category_hotels, '''
# Top 5 Hotels in Luxor

Luxor, the world's greatest open-air museum, offers accommodation with unparalleled historical views:

## 1. Sofitel Winter Palace Luxor

The jewel of Luxor, this Victorian-era palace hotel has hosted royalty and celebrities since 1886. Pure elegance on the Nile.

**Price:** From 2,500 EGP/night
**Why stay:** Historic luxury, Nile views, regal ambiance

## 2. Hilton Luxor Resort & Spa

Full-service modern resort perfectly positioned on the Nile with views of both the ancient temples and the river.

**Price:** From 2,200 EGP/night
**Why stay:** Modern amenities, spa, temple views

## 3. Pavillon Winter Luxor

Charming boutique hotel combining French elegance with Egyptian warmth, steps from Luxor Temple.

**Price:** From 1,500 EGP/night
**Why stay:** Boutique charm, central location, personal service

## 4. Steigenberger Nile Palace

Modern comfort meets ancient history. Perfect base for exploring Luxor's treasures.

**Price:** From 1,400 EGP/night
**Why stay:** Value for money, Nile views, good location

## 5. Sonesta St. George Hotel

Unique cruise-ship styled hotel permanently docked on the Nile. Experience cruise amenities without leaving Luxor.

**Price:** From 1,300 EGP/night
**Why stay:** Unique concept, all meals included, cruise experience
            '''),

            ('Best Hotels in Aswan: Nubian Paradise', category_hotels, '''
# Best Hotels in Aswan

Aswan's serene beauty and Nubian culture create a unique hotel experience:

## 1. Sofitel Legend Old Cataract

The most legendary hotel in Egypt, this Victorian palace overlooking the Nile inspired Agatha Christie's "Death on the Nile."

**Price:** From 2,800 EGP/night
**Why stay:** Historic legend, unmatched elegance, Nile panoramas

## 2. Movenpick Resort Aswan (Elephantine Island)

Island paradise retreat on Elephantine Island. Arrive by private boat to this lush tropical oasis.

**Price:** From 2,200 EGP/night
**Why stay:** Island location, tropical gardens, tranquility

## 3. Pyramisa Isis Island Resort

Full resort experience on another Nile island, perfect for relaxation after temple tours.

**Price:** From 1,400 EGP/night
**Why stay:** Island resort, gardens, family-friendly

## 4. Nubian Eco Village

Authentic Nubian experience in a traditional village setting. Eco-friendly and culturally immersive.

**Price:** From 1,500 EGP/night
**Why stay:** Cultural authenticity, eco-friendly, unique experience

## 5. Basma Hotel Aswan

Hillside hotel with some of the best Nile views in Aswan at affordable prices.

**Price:** From 1,100 EGP/night
**Why stay:** Panoramic views, good value, central location
            '''),

            ('Sharm El Sheikh: Top 5 Red Sea Resorts', category_hotels, '''
# Top 5 Red Sea Resorts in Sharm El Sheikh

World-class beach resorts and diving destinations:

## 1. Four Seasons Resort Sharm El Sheikh

Ultra-luxury beachfront resort setting the standard for Red Sea hospitality.

**Price:** From 4,000 EGP/night
**Why stay:** Ultimate luxury, private beach, exceptional service

## 2. Rixos Premium Seagate

All-inclusive ultra-luxury with Turkish hospitality standards and gourmet dining.

**Price:** From 3,500 EGP/night
**Why stay:** All-inclusive luxury, premium dining, family-friendly

## 3. Movenpick Resort Sharm El Sheikh

Beachfront elegance with house reef for world-class diving and snorkeling.

**Price:** From 3,200 EGP/night
**Why stay:** Excellent diving, beach access, Swiss quality

## 4. Sheraton Sharm Hotel

Large resort complex with aqua park, perfect for families seeking Red Sea fun.

**Price:** From 3,000 EGP/night
**Why stay:** Aqua park, family activities, beachfront

## 5. Savoy Sharm El Sheikh

Elegant Naama Bay resort combining luxury with central location.

**Price:** From 2,800 EGP/night
**Why stay:** Naama Bay location, nightlife access, resort amenities
            '''),

            # Safety Guide
            ('Safety Tips for Foreign Tourists Visiting Egypt', category_safety, '''
# Safety Tips for Foreign Tourists Visiting Egypt

Egypt is generally safe for tourists, but following these guidelines ensures a worry-free trip:

## General Safety

### Stay in Tourist Areas
- Stick to established tourist destinations
- Use reputable hotels and tour operators
- Tourist police are present at all major sites

### Transportation Safety
- Use official taxis or ride-hailing apps (Uber, Careem)
- Avoid unmarked taxis
- For longer journeys, book through your hotel
- Trains and domestic flights are safe and reliable

### Money and Valuables
- Don't carry large amounts of cash
- Use hotel safes for passports and valuables
- ATMs are widely available in tourist areas
- Credit cards accepted at major hotels and restaurants
- Keep small bills for tips and small purchases

## Health and Hygiene

### Water and Food
- Drink only bottled water (widely available)
- Avoid ice in drinks at street vendors
- Eat at reputable restaurants
- Street food is generally safe but choose busy stalls
- Fruits that can be peeled are safest

### Sun Protection
- Egypt's sun is intense year-round
- Use high-SPF sunscreen
- Wear hat and sunglasses
- Stay hydrated (2-3 liters/day)
- Avoid midday sun (11am-3pm)

### Medical
- Bring prescription medications in original containers
- Travel insurance highly recommended
- Private hospitals in Cairo, Luxor, Aswan have good facilities
- Pharmacies ("Agzakhana") are everywhere

## Cultural Sensitivity

### Dress Code
- Egypt is conservative; dress modestly
- **Women:** Cover shoulders and knees, carry scarf for religious sites
- **Men:** Long pants preferred, shirts with sleeves
- Beach resorts more relaxed
- Respect increases when dressed appropriately

### Religious Sites
- Remove shoes when entering mosques
- Ask permission before photographing people
- Non-Muslims may not enter all mosque areas
- Friday is holy day (mosques busy)

### Social Customs
- Greetings: Handshake common (wait for women to extend hand first)
- Personal space less valued than Western countries
- "Baksheesh" (tips) expected for small services
- Haggling expected in markets (start at 50% of asking price)

## Scams to Avoid

### Common Tourist Scams
1. **Papyrus scams:** Sold as "authentic ancient" - it's modern
2. **Free tours:** Often lead to aggressive souvenir selling
3. **Taxi overcharging:** Always agree on price before starting
4. **Photo fees:** Some people charge after photo taken
5. **"Museum closed" scam:** Drivers say it's closed to take you shopping

### How to Avoid Scams
- Book tours through reputable companies
- Research typical prices beforehand
- Be polite but firm saying "No thank you"
- Don't feel obligated to buy
- Use official ticket offices

## Emergency Contacts

- **Tourist Police:** 126
- **Emergency:** 122
- **Ambulance:** 123
- **Fire:** 180

### Embassy Contacts
- Keep your embassy contact information
- Register with your embassy (optional but recommended)
- Embassies located in Cairo (Zamalek area)

## Women Travelers

### Safety for Women
- Egypt is generally safe for women travelers
- Dress modestly to minimize unwanted attention
- Ignore catcalls - don't engage
- Use women-only metro cars in Cairo (first two cars)
- Solo female travelers should be extra cautious after dark
- Join group tours if concerned about safety

## COVID-19 and Health

- Check current health requirements before travel
- Major tourist sites implement health protocols
- Masks may be required in certain locations
- Hand sanitizer widely available

## What to Pack for Safety

- **Copies** of passport and important documents
- **Emergency cash** in USD or EUR
- **Prescription medications** with doctor's note
- **First aid kit** with anti-diarrheal medication
- **Sunscreen** (expensive in Egypt)
- **Modest clothing** appropriate for religious sites
- **Universal adapter** for electronics
- **Flashlight** or headlamp
- **Reusable water bottle** with filter

## Final Tips

1. **Trust your instincts** - if something feels wrong, leave
2. **Stay connected** - get local SIM card for data
3. **Learn basic Arabic** - "Shukran" (thank you), "La shukran" (no thank you)
4. **Be patient** - things move slowly; embrace it
5. **Smile** - Egyptians are friendly and helpful
6. **Negotiate** - except in shops with price tags
7. **Enjoy** - Egypt is an incredible experience!

## Best Times to Visit

- **October-April:** Pleasant weather (20-25°C)
- **May-September:** Very hot (35-45°C) but fewer tourists
- **Ramadan:** Restaurants closed during day, festive evenings

Egypt welcomes millions of tourists annually, and the vast majority have wonderful, safe experiences. Following these guidelines helps ensure you'll be one of them!

**Welcome to Egypt - Ahlan wa Sahlan!**
            '''),

            # Other guides
            ('Complete Guide to Nile Cruises: Everything You Need to Know', category_travel, '''
# Complete Guide to Nile Cruises

Experience Egypt's ancient wonders from the comfort of a luxury Nile cruise ship.

## Why Choose a Nile Cruise?

- Visit multiple temples without packing/unpacking
- All meals included
- Expert Egyptologist guides
- Scenic Nile views
- Relaxation between site visits

## Popular Routes

### Luxor to Aswan (4 days/3 nights)
The classic cruise covering Egypt's greatest ancient sites.

### Aswan to Luxor (4 days/3 nights)
Same route in reverse, starting from peaceful Aswan.

### Extended Cruises (7+ days)
Include Cairo, with more time at each site.

## What's Included

- All meals (breakfast, lunch, dinner)
- Guided tours to temples
- Onboard entertainment
- Swimming pool
- Sun deck

## Best Time to Go

- **October-April:** Ideal weather
- **December-February:** Peak season (book early)
- **Summer:** Hot but cheaper rates

## Pricing

- **Budget cruises:** 5,000-8,000 EGP
- **Mid-range:** 10,000-15,000 EGP
- **Luxury:** 20,000+ EGP

## What to Pack

- Comfortable walking shoes
- Sun protection
- Modest clothing for temples
- Camera
- Medications
- Light jacket for evenings

Book your Nile cruise through Egy360 for best rates and verified operators!
            '''),
        ]

        total_posts = 0
        for title, category, content in blog_posts:
            post, created = BlogPost.objects.get_or_create(
                title=title,
                defaults={
                    'slug': slugify(title),
                    'content': content,
                    'excerpt': content[:300] if len(content) > 300 else content,
                    'category': category,
                    'author': admin_user,
                    'status': 'published',
                    'published_at': datetime.now(),
                }
            )
            if created:
                total_posts += 1

        self.stdout.write(self.style.SUCCESS(f'[SUCCESS] Created {total_posts} blog posts'))
