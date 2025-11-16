"""
populate_sample_data.py - Create sample data for Egy360 platform
Run this script to populate the database with sample data
"""

import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment FIRST before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

# NOW we can import Django modules
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from destinations.models import Country, City, Attraction, TravelGuide
from accommodations.models import Accommodation, Room, Amenity
from tours.models import Tour, TourItinerary
from transportation.models import TransportationService, Driver
from blog.models import BlogCategory, BlogPost
from reviews.models import Review

print("=" * 60)
print("   POPULATING SAMPLE DATA FOR EGY360")
print("=" * 60)

# Create Users
print("\n📱 Creating sample users...")
users = []
user_data = [
    {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
    {'username': 'traveler1', 'email': 'traveler1@example.com', 'first_name': 'Mike', 'last_name': 'Johnson'},
]

for data in user_data:
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name']
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        users.append(user)
        print(f"✅ Created user: {user.username}")

# Create Country
print("\n🌍 Creating country...")
egypt, created = Country.objects.get_or_create(
    code='EG',
    defaults={
        'name': 'Egypt',
        'description': 'Land of the Pharaohs, home to ancient wonders and modern marvels',
        'flag_emoji': '🇪🇬'
    }
)
if created:
    print("✅ Created country: Egypt")

# Create Cities
print("\n🏙️ Creating cities...")
cities_data = [
    {
        'name': 'Cairo',
        'slug': 'cairo',
        'description': 'The capital city of Egypt, home to the Great Pyramids and the Sphinx',
        'population': 20000000,
        'best_time_to_visit': 'October to April',
        'is_popular': True,
        'is_capital': True,
        'has_airport': True
    },
    {
        'name': 'Luxor',
        'slug': 'luxor',
        'description': 'Ancient city of Thebes, home to Valley of the Kings and Karnak Temple',
        'population': 500000,
        'best_time_to_visit': 'October to April',
        'is_popular': True,
        'has_airport': True
    },
    {
        'name': 'Hurghada',
        'slug': 'hurghada',
        'description': 'Red Sea resort town famous for diving and beach activities',
        'population': 250000,
        'best_time_to_visit': 'Year-round',
        'is_popular': True,
        'has_airport': True
    },
    {
        'name': 'Alexandria',
        'slug': 'alexandria',
        'description': 'Mediterranean port city with Greco-Roman landmarks',
        'population': 5000000,
        'best_time_to_visit': 'March to November',
        'is_popular': True,
        'has_airport': True
    },
    {
        'name': 'Aswan',
        'slug': 'aswan',
        'description': 'Nubian city on the Nile, gateway to Abu Simbel',
        'population': 300000,
        'best_time_to_visit': 'October to April',
        'is_popular': True,
        'has_airport': True
    }
]

cities = []
for data in cities_data:
    city, created = City.objects.get_or_create(
        slug=data['slug'],
        country=egypt,
        defaults=data
    )
    cities.append(city)
    if created:
        print(f"✅ Created city: {city.name}")

# Create Attractions
print("\n🏛️ Creating attractions...")
attractions_data = [
    {
        'city': cities[0],  # Cairo
        'name': 'Great Pyramids of Giza',
        'slug': 'pyramids-giza',
        'attraction_type': 'historical',
        'description': 'The last surviving Wonder of the Ancient World',
        'address': 'Giza Plateau, Cairo',
        'admission_fee': Decimal('20.00'),
        'visit_duration': '3-4 hours',
        'is_unesco': True,
        'is_must_see': True
    },
    {
        'city': cities[0],  # Cairo
        'name': 'Egyptian Museum',
        'slug': 'egyptian-museum',
        'attraction_type': 'museum',
        'description': 'Home to the largest collection of ancient Egyptian artifacts',
        'address': 'Tahrir Square, Cairo',
        'admission_fee': Decimal('15.00'),
        'visit_duration': '2-3 hours',
        'is_must_see': True
    },
    {
        'city': cities[1],  # Luxor
        'name': 'Valley of the Kings',
        'slug': 'valley-kings',
        'attraction_type': 'archaeological',
        'description': 'Royal burial ground for pharaohs including Tutankhamun',
        'address': 'West Bank, Luxor',
        'admission_fee': Decimal('25.00'),
        'visit_duration': '3-4 hours',
        'is_unesco': True,
        'is_must_see': True
    },
    {
        'city': cities[1],  # Luxor
        'name': 'Karnak Temple',
        'slug': 'karnak-temple',
        'attraction_type': 'historical',
        'description': 'Largest ancient religious site in the world',
        'address': 'East Bank, Luxor',
        'admission_fee': Decimal('20.00'),
        'visit_duration': '2-3 hours',
        'is_unesco': True,
        'is_must_see': True
    },
    {
        'city': cities[4],  # Aswan
        'name': 'Abu Simbel Temples',
        'slug': 'abu-simbel',
        'attraction_type': 'historical',
        'description': 'Massive rock-cut temples built by Ramesses II',
        'address': 'Abu Simbel, Aswan',
        'admission_fee': Decimal('30.00'),
        'visit_duration': '2-3 hours',
        'is_unesco': True,
        'is_must_see': True
    }
]

for data in attractions_data:
    attraction, created = Attraction.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        print(f"✅ Created attraction: {attraction.name}")

# Create Amenities
print("\n🏨 Creating hotel amenities...")
amenities_list = [
    {'name': 'WiFi', 'icon': 'fa-wifi'},
    {'name': 'Swimming Pool', 'icon': 'fa-swimming-pool'},
    {'name': 'Restaurant', 'icon': 'fa-utensils'},
    {'name': 'Gym', 'icon': 'fa-dumbbell'},
    {'name': 'Spa', 'icon': 'fa-spa'},
    {'name': 'Parking', 'icon': 'fa-parking'},
    {'name': 'Airport Shuttle', 'icon': 'fa-shuttle-van'},
    {'name': 'Bar', 'icon': 'fa-glass-martini'},
]

amenities = []
for data in amenities_list:
    amenity, created = Amenity.objects.get_or_create(
        name=data['name'],
        defaults={'icon': data['icon']}
    )
    amenities.append(amenity)
    if created:
        print(f"✅ Created amenity: {amenity.name}")

# Create Accommodations
print("\n🏨 Creating accommodations...")
accommodations_data = [
    {
        'name': 'Pyramids View Hotel',
        'slug': 'pyramids-view-hotel',
        'accommodation_type': 'hotel',
        'description': 'Luxury hotel with stunning views of the Great Pyramids',
        'city': 'Cairo',
        'address': 'Pyramid Road, Giza, Cairo',
        'star_rating': 5,
        'total_rooms': 200,
        'price_per_night': Decimal('150.00'),
        'is_featured': True,
        'is_verified': True,
        'average_rating': Decimal('4.5')
    },
    {
        'name': 'Nile Palace Resort',
        'slug': 'nile-palace-resort',
        'accommodation_type': 'resort',
        'description': 'Elegant resort on the banks of the Nile River',
        'city': 'Luxor',
        'address': 'East Bank, Luxor',
        'star_rating': 5,
        'total_rooms': 150,
        'price_per_night': Decimal('200.00'),
        'is_featured': True,
        'is_verified': True,
        'average_rating': Decimal('4.7')
    },
    {
        'name': 'Red Sea Beach Resort',
        'slug': 'red-sea-beach-resort',
        'accommodation_type': 'resort',
        'description': 'Beachfront resort with world-class diving facilities',
        'city': 'Hurghada',
        'address': 'Sheraton Road, Hurghada',
        'star_rating': 4,
        'total_rooms': 300,
        'price_per_night': Decimal('120.00'),
        'is_featured': True,
        'is_verified': True,
        'average_rating': Decimal('4.3')
    },
    {
        'name': 'Budget Cairo Hostel',
        'slug': 'budget-cairo-hostel',
        'accommodation_type': 'hostel',
        'description': 'Affordable accommodation in the heart of Cairo',
        'city': 'Cairo',
        'address': 'Downtown Cairo',
        'star_rating': 2,
        'total_rooms': 20,
        'price_per_night': Decimal('25.00'),
        'is_verified': True,
        'average_rating': Decimal('4.0')
    }
]

for data in accommodations_data:
    accommodation, created = Accommodation.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        # Add amenities
        accommodation.amenities.set(random.sample(amenities, random.randint(3, 6)))
        print(f"✅ Created accommodation: {accommodation.name}")

        # Create rooms for the accommodation
        room_types = ['single', 'double', 'suite', 'family']
        for room_type in random.sample(room_types, 2):
            Room.objects.create(
                accommodation=accommodation,
                room_type=room_type,
                name=f"{room_type.title()} Room",
                description=f"Comfortable {room_type} room with modern amenities",
                max_occupancy=2 if room_type in ['single', 'double'] else 4,
                beds='1 King' if room_type == 'single' else '2 Queens',
                base_price=accommodation.price_per_night * Decimal('1.2') if room_type == 'suite' else accommodation.price_per_night,
                total_rooms=10,
                available_rooms=8
            )

# Create Tours
print("\n🚌 Creating tours...")
tours_data = [
    {
        'name': 'Pyramids & Sphinx Day Tour',
        'slug': 'pyramids-sphinx-day-tour',
        'tour_type': 'cultural',
        'description': 'Full day tour to the Great Pyramids, Sphinx, and Saqqara',
        'highlights': 'Visit the Great Pyramids, See the Sphinx, Explore Saqqara Step Pyramid',
        'duration_days': 1,
        'duration_nights': 0,
        'departure_city': 'Cairo',
        'price_per_person': Decimal('75.00'),
        'max_group_size': 15,
        'is_featured': True,
        'average_rating': Decimal('4.6')
    },
    {
        'name': 'Nile River Cruise - 3 Days',
        'slug': 'nile-cruise-3-days',
        'tour_type': 'cruise',
        'description': 'Luxury cruise from Aswan to Luxor with guided tours',
        'highlights': 'Philae Temple, Kom Ombo, Edfu Temple, Valley of the Kings',
        'duration_days': 3,
        'duration_nights': 2,
        'departure_city': 'Aswan',
        'price_per_person': Decimal('450.00'),
        'max_group_size': 30,
        'is_featured': True,
        'average_rating': Decimal('4.8')
    },
    {
        'name': 'Desert Safari Adventure',
        'slug': 'desert-safari',
        'tour_type': 'adventure',
        'description': 'Exciting desert safari with quad biking and Bedouin dinner',
        'highlights': 'Quad biking, Camel riding, Bedouin dinner, Star gazing',
        'duration_days': 1,
        'duration_nights': 0,
        'departure_city': 'Hurghada',
        'price_per_person': Decimal('85.00'),
        'max_group_size': 20,
        'is_featured': True,
        'average_rating': Decimal('4.4')
    },
    {
        'name': 'Red Sea Diving Experience',
        'slug': 'red-sea-diving',
        'tour_type': 'diving',
        'description': 'Discover the underwater wonders of the Red Sea',
        'highlights': 'Two dive sites, Professional instructor, Equipment included',
        'duration_days': 1,
        'duration_nights': 0,
        'departure_city': 'Hurghada',
        'price_per_person': Decimal('120.00'),
        'max_group_size': 8,
        'average_rating': Decimal('4.7')
    }
]

for data in tours_data:
    tour, created = Tour.objects.get_or_create(
        slug=data['slug'],
        defaults={
            **data,
            'destinations': ['Cairo', 'Giza'] if 'pyramids' in data['slug'] else ['Luxor', 'Aswan'],
            'includes': ['Professional guide', 'Transportation', 'Entrance fees', 'Lunch'],
            'excludes': ['Personal expenses', 'Tips', 'Travel insurance'],
            'languages': ['English', 'Arabic', 'Spanish', 'French']
        }
    )
    if created:
        print(f"✅ Created tour: {tour.name}")

        # Create itinerary for multi-day tours
        if tour.duration_days > 1:
            for day in range(1, tour.duration_days + 1):
                TourItinerary.objects.create(
                    tour=tour,
                    day=day,
                    title=f"Day {day} Adventure",
                    description=f"Exciting activities planned for day {day}",
                    meals_included="Breakfast, Lunch" if day > 1 else "Lunch",
                    overnight_location="Cruise Ship" if 'cruise' in tour.slug else "Hotel"
                )

# Create Transportation Services
print("\n🚗 Creating transportation services...")
transport_data = [
    {
        'name': 'Cairo Airport Transfer',
        'slug': 'cairo-airport-transfer',
        'service_type': 'airport_transfer',
        'description': 'Professional airport transfer service with meet & greet',
        'vehicle_model': 'Toyota Camry',
        'max_passengers': 4,
        'max_luggage': 3,
        'fixed_price': Decimal('40.00'),
        'is_available': True
    },
    {
        'name': 'Luxury Private Car Service',
        'slug': 'luxury-private-car',
        'service_type': 'private_car',
        'description': 'Premium car service with professional driver',
        'vehicle_model': 'Mercedes E-Class',
        'max_passengers': 4,
        'max_luggage': 4,
        'price_per_hour': Decimal('60.00'),
        'has_wifi': True,
        'is_available': True
    },
    {
        'name': 'Desert Safari Bus',
        'slug': 'desert-safari-bus',
        'service_type': 'bus',
        'description': 'Comfortable bus for desert tours and excursions',
        'vehicle_model': 'Mercedes Sprinter',
        'max_passengers': 15,
        'max_luggage': 15,
        'price_per_hour': Decimal('100.00'),
        'is_available': True
    }
]

for data in transport_data:
    service, created = TransportationService.objects.get_or_create(
        slug=data['slug'],
        defaults=data
    )
    if created:
        print(f"✅ Created transport service: {service.name}")

# Create Drivers
print("\n👨‍✈️ Creating drivers...")
drivers_data = [
    {
        'name': 'Ahmed Hassan',
        'phone': '+201234567890',
        'email': 'ahmed@example.com',
        'license_number': 'EG123456',
        'years_experience': 10,
        'languages_spoken': ['Arabic', 'English'],
        'is_verified': True,
        'average_rating': Decimal('4.8')
    },
    {
        'name': 'Mohamed Ali',
        'phone': '+201234567891',
        'email': 'mohamed@example.com',
        'license_number': 'EG123457',
        'years_experience': 8,
        'languages_spoken': ['Arabic', 'English', 'German'],
        'is_verified': True,
        'average_rating': Decimal('4.6')
    }
]

for data in drivers_data:
    driver, created = Driver.objects.get_or_create(
        license_number=data['license_number'],
        defaults=data
    )
    if created:
        print(f"✅ Created driver: {driver.name}")

# Create Blog Categories and Posts
print("\n📝 Creating blog content...")
categories_data = [
    {'name': 'Travel Tips', 'slug': 'travel-tips'},
    {'name': 'Culture & History', 'slug': 'culture-history'},
    {'name': 'Food & Cuisine', 'slug': 'food-cuisine'},
    {'name': 'Adventures', 'slug': 'adventures'},
    {'name': 'Travel Guides', 'slug': 'travel-guides'}
]

categories = []
for data in categories_data:
    category, created = BlogCategory.objects.get_or_create(
        slug=data['slug'],
        defaults={'name': data['name']}
    )
    categories.append(category)
    if created:
        print(f"✅ Created blog category: {category.name}")

# Create Blog Posts
blog_posts_data = [
    {
        'title': '10 Things You Must Know Before Visiting Egypt',
        'slug': '10-things-before-egypt',
        'category': categories[0],  # Travel Tips
        'excerpt': 'Essential tips for first-time visitors to Egypt, from visa requirements to cultural etiquette.',
        'content': '''Egypt is an amazing destination with rich history and culture. Here are the essential things you need to know before your visit...
        
        1. Visa Requirements: Most visitors need a visa, which can be obtained on arrival or online.
        2. Best Time to Visit: October to April offers the most comfortable weather.
        3. Currency: Egyptian Pound (EGP) is the local currency.
        4. Language: Arabic is the official language, but English is widely spoken in tourist areas.
        5. Dress Code: Modest clothing is recommended, especially when visiting religious sites.
        6. Tipping: Baksheesh (tipping) is customary for many services.
        7. Safety: Egypt is generally safe for tourists, but stay aware of your surroundings.
        8. Transportation: Use registered taxis or ride-sharing apps for safe travel.
        9. Bargaining: Haggling is expected in markets and souks.
        10. Respect Local Customs: Be respectful of Islamic traditions and practices.''',
        'is_published': True,
        'is_featured': True
    },
    {
        'title': 'The Ultimate Guide to Egyptian Street Food',
        'slug': 'egyptian-street-food-guide',
        'category': categories[2],  # Food & Cuisine
        'excerpt': 'Discover the delicious world of Egyptian street food, from koshari to falafel.',
        'content': '''Egyptian street food is a culinary adventure you won\'t want to miss. From savory to sweet, the streets of Egypt offer amazing flavors...
        
        Popular dishes include:
        - Koshari: The national dish mixing rice, pasta, lentils, and crispy onions
        - Falafel (Ta\'ameya): Made with fava beans instead of chickpeas
        - Ful Medames: Slow-cooked fava beans, a breakfast staple
        - Shawarma: Rotating meat served in pita
        - Om Ali: Delicious bread pudding dessert''',
        'is_published': True
    },
    {
        'title': 'Exploring the Valley of the Kings: A Complete Guide',
        'slug': 'valley-kings-guide',
        'category': categories[1],  # Culture & History
        'excerpt': 'Everything you need to know about visiting the Valley of the Kings in Luxor.',
        'content': '''The Valley of the Kings is one of Egypt\'s most remarkable archaeological sites. Home to 63 discovered tombs, including that of Tutankhamun...
        
        Key highlights:
        - Tomb of Tutankhamun (KV62)
        - Tomb of Ramesses II (KV7)
        - Tomb of Seti I (KV17)
        - Best visited early morning to avoid crowds
        - Photography requires additional ticket''',
        'is_published': True,
        'is_featured': True
    },
    {
        'title': 'Red Sea Diving: Best Spots in Hurghada',
        'slug': 'red-sea-diving-spots',
        'category': categories[3],  # Adventures
        'excerpt': 'Discover the best diving spots in Hurghada and the Red Sea.',
        'content': '''The Red Sea offers some of the world\'s best diving with crystal clear waters and vibrant marine life...
        
        Top diving spots:
        - Giftun Island: Beautiful coral reefs
        - Abu Nuhas: Famous wreck diving site
        - Dolphin House: Swim with dolphins
        - Careless Reef: Stunning wall dives
        - Best visibility: June to August''',
        'is_published': True
    }
]

# Get admin user for blog posts
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.first()

for data in blog_posts_data:
    post_data = data.copy()
    post_data['author'] = admin_user
    blog_post, created = BlogPost.objects.get_or_create(
        slug=data['slug'],
        defaults=post_data
    )
    if created:
        blog_post.published_at = datetime.now()
        blog_post.save()
        print(f"✅ Created blog post: {blog_post.title}")

# Create Sample Reviews
print("\n⭐ Creating sample reviews...")
review_texts = [
    "Amazing experience! Would definitely recommend.",
    "Great service and wonderful tour guide.",
    "Excellent value for money. Very professional.",
    "Beautiful location and friendly staff.",
    "Unforgettable experience! Exceeded expectations."
]

# Create reviews for accommodations
for accommodation in Accommodation.objects.all()[:3]:
    for i in range(2):
        Review.objects.create(
            content_type=ContentType.objects.get_for_model(Accommodation),
            object_id=accommodation.id,
            user=random.choice(User.objects.all()),
            rating=random.randint(4, 5),
            title=f"Great stay at {accommodation.name}",
            comment=random.choice(review_texts),
            is_verified=True
        )

print("✅ Created sample reviews")

print("\n" + "=" * 60)
print("   ✅ SAMPLE DATA POPULATION COMPLETE!")
print("=" * 60)
print("\nSummary of created data:")
print(f"  • Users: {User.objects.count()}")
print(f"  • Cities: {City.objects.count()}")
print(f"  • Attractions: {Attraction.objects.count()}")
print(f"  • Accommodations: {Accommodation.objects.count()}")
print(f"  • Tours: {Tour.objects.count()}")
print(f"  • Transportation Services: {TransportationService.objects.count()}")
print(f"  • Drivers: {Driver.objects.count()}")
print(f"  • Blog Posts: {BlogPost.objects.count()}")
print(f"  • Reviews: {Review.objects.count()}")

print("\n🎉 Your Egy360 platform now has sample data!")
print("\nYou can login to the admin panel to manage this data.")
print("Sample user accounts created:")
print("  Username: john_doe | Password: password123")
print("  Username: jane_smith | Password: password123")
print("  Username: traveler1 | Password: password123")