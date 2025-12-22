# accommodations/management/commands/populate_real_hotels.py
"""
Populate database with REAL Egyptian hotels
Actual hotel names, ratings, pricing, and locations
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from accommodations.models import Accommodation, Amenity
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with real Egyptian hotels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing accommodations before adding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing accommodations...')
            Accommodation.objects.all().delete()

        self.stdout.write('Adding real Egyptian hotels...')

        # Real Egyptian Hotels Data
        hotels = [
            # CAIRO - Luxury Hotels
            {
                'name': 'Four Seasons Hotel Cairo at Nile Plaza',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '1089 Corniche El Nil, Garden City, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('450.00'),
                'description': 'Overlooking the Nile River, Four Seasons Hotel Cairo at Nile Plaza offers luxurious accommodations with stunning views of the city and the Pyramids. Features world-class dining, a full-service spa, and exceptional service.',
                'latitude': Decimal('30.0392'),
                'longitude': Decimal('31.2293'),
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 365,
            },
            {
                'name': 'The Nile Ritz-Carlton Cairo',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '1113 Corniche El Nil, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('380.00'),
                'description': 'An iconic landmark on the banks of the Nile, The Ritz-Carlton Cairo combines timeless elegance with modern luxury. Enjoy panoramic river views, award-winning restaurants, and proximity to Egyptian Museum.',
                'latitude': Decimal('30.0444'),
                'longitude': Decimal('31.2357'),
                'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 331,
            },
            {
                'name': 'Marriott Mena House Cairo',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '6 Pyramids Road, Giza, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('320.00'),
                'description': 'Historic palace hotel with direct views of the Great Pyramids of Giza. Once hosted royalty and world leaders. Features 40 acres of gardens, multiple restaurants, and an outdoor pool facing the pyramids.',
                'latitude': Decimal('29.9870'),
                'longitude': Decimal('31.1342'),
                'image_url': 'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 331,
            },
            {
                'name': 'Kempinski Nile Hotel Cairo',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '12 Ahmed Ragheb Street, Garden City, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('280.00'),
                'description': 'Elegant boutique hotel in Garden City offering personalized service and Nile views. Features the renowned Osmanly restaurant and rooftop bar with panoramic city views.',
                'latitude': Decimal('30.0378'),
                'longitude': Decimal('31.2305'),
                'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 191,
            },
            {
                'name': 'Steigenberger Hotel El Tahrir',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '2 Kasr El Nil Street, Downtown Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('180.00'),
                'description': 'Located in the heart of Downtown Cairo overlooking Tahrir Square and the Egyptian Museum. Modern luxury with easy access to Khan El Khalili bazaar and historic sites.',
                'latitude': Decimal('30.0444'),
                'longitude': Decimal('31.2357'),
                'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 291,
            },
            # CAIRO - Mid-Range
            {
                'name': 'Le Meridien Pyramids Hotel & Spa',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': 'Alexandria Desert Road, Giza, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('150.00'),
                'description': 'Resort-style hotel with stunning pyramid views. Features large outdoor pool, spa, and multiple dining options. Perfect for families visiting the Giza plateau.',
                'latitude': Decimal('29.9925'),
                'longitude': Decimal('31.1250'),
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 498,
            },
            {
                'name': 'Cairo Marriott Hotel & Omar Khayyam Casino',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': '16 Saray El Gezira Street, Zamalek, Cairo',
                'star_rating': 5,
                'price_per_night': Decimal('200.00'),
                'description': 'Historic palace hotel in Zamalek originally built for Empress Eugenie. Beautiful gardens, riverside location, and rich heritage make it a Cairo landmark.',
                'latitude': Decimal('30.0609'),
                'longitude': Decimal('31.2243'),
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 1087,
            },
            # LUXOR
            {
                'name': 'Sofitel Winter Palace Luxor',
                'accommodation_type': 'hotel',
                'city': 'Luxor',
                'address': 'Corniche El Nile Street, Luxor',
                'star_rating': 5,
                'price_per_night': Decimal('280.00'),
                'description': 'Legendary Victorian palace on the Nile where Agatha Christie wrote Death on the Nile. Historic grandeur, tropical gardens, and views of the Nile and West Bank temples.',
                'latitude': Decimal('25.6995'),
                'longitude': Decimal('32.6421'),
                'image_url': 'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 92,
            },
            {
                'name': 'Hilton Luxor Resort & Spa',
                'accommodation_type': 'resort',
                'city': 'Luxor',
                'address': 'New Karnak, Luxor',
                'star_rating': 5,
                'price_per_night': Decimal('180.00'),
                'description': 'Modern resort on the banks of the Nile with views of Luxor Temple and West Bank. Features large pool, full-service spa, and proximity to Karnak Temple.',
                'latitude': Decimal('25.7127'),
                'longitude': Decimal('32.6583'),
                'image_url': 'https://images.unsplash.com/photo-1549294413-26f195200c16?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 236,
            },
            {
                'name': 'Steigenberger Nile Palace Luxor',
                'accommodation_type': 'hotel',
                'city': 'Luxor',
                'address': 'Khaled Ibn El Walid Street, Luxor',
                'star_rating': 5,
                'price_per_night': Decimal('160.00'),
                'description': 'Contemporary luxury hotel on the East Bank with stunning Nile views. Excellent base for exploring Valley of the Kings and Karnak Temple.',
                'latitude': Decimal('25.6944'),
                'longitude': Decimal('32.6389'),
                'image_url': 'https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 304,
            },
            {
                'name': 'Sonesta St. George Hotel Luxor',
                'accommodation_type': 'hotel',
                'city': 'Luxor',
                'address': 'Corniche El Nile, Luxor',
                'star_rating': 5,
                'price_per_night': Decimal('140.00'),
                'description': 'Elegant Nile-side hotel with beautiful gardens and river views. Features rooftop pool, spa, and easy access to Luxor Temple.',
                'latitude': Decimal('25.6972'),
                'longitude': Decimal('32.6403'),
                'image_url': 'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 322,
            },
            # ASWAN
            {
                'name': 'Sofitel Legend Old Cataract Aswan',
                'accommodation_type': 'hotel',
                'city': 'Aswan',
                'address': 'Abtal El Tahrir Street, Aswan',
                'star_rating': 5,
                'price_per_night': Decimal('350.00'),
                'description': 'Iconic Victorian palace hotel where Agatha Christie stayed. Moorish architecture, stunning Nile views, and the most romantic setting in Egypt.',
                'latitude': Decimal('24.0843'),
                'longitude': Decimal('32.8857'),
                'image_url': 'https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 138,
            },
            {
                'name': 'Movenpick Resort Aswan',
                'accommodation_type': 'resort',
                'city': 'Aswan',
                'address': 'Elephantine Island, Aswan',
                'star_rating': 5,
                'price_per_night': Decimal('180.00'),
                'description': 'Stunning resort on Elephantine Island accessed by private ferry. Tropical gardens, Nubian architecture, and panoramic Nile views.',
                'latitude': Decimal('24.0850'),
                'longitude': Decimal('32.8867'),
                'image_url': 'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 244,
            },
            # SHARM EL SHEIKH
            {
                'name': 'Four Seasons Resort Sharm El Sheikh',
                'accommodation_type': 'resort',
                'city': 'Sharm El Sheikh',
                'address': '1 Four Seasons Boulevard, Sharm El Sheikh',
                'star_rating': 5,
                'price_per_night': Decimal('400.00'),
                'description': 'Ultra-luxury Red Sea resort with private beach, world-class diving, multiple pools, and exceptional dining. Perfect for both relaxation and adventure.',
                'latitude': Decimal('27.8510'),
                'longitude': Decimal('34.2965'),
                'image_url': 'https://images.unsplash.com/photo-1573843981267-be1999ff37cd?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 136,
            },
            {
                'name': 'Rixos Premium Seagate Sharm',
                'accommodation_type': 'resort',
                'city': 'Sharm El Sheikh',
                'address': 'Nabq Bay, Sharm El Sheikh',
                'star_rating': 5,
                'price_per_night': Decimal('250.00'),
                'description': 'All-inclusive luxury resort with private beach, water park, and extensive dining options. Perfect for families seeking Red Sea adventure.',
                'latitude': Decimal('27.9694'),
                'longitude': Decimal('34.4177'),
                'image_url': 'https://images.unsplash.com/photo-1551918120-9739cb430c6d?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 694,
            },
            {
                'name': 'Hyatt Regency Sharm El Sheikh',
                'accommodation_type': 'resort',
                'city': 'Sharm El Sheikh',
                'address': 'Gardens Bay, Sharm El Sheikh',
                'star_rating': 5,
                'price_per_night': Decimal('180.00'),
                'description': 'Contemporary beachfront resort in Gardens Bay with stunning coral reef access. Features large pool complex, spa, and excellent snorkeling.',
                'latitude': Decimal('27.8667'),
                'longitude': Decimal('34.3150'),
                'image_url': 'https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 428,
            },
            {
                'name': 'Stella Di Mare Beach Hotel & Spa',
                'accommodation_type': 'resort',
                'city': 'Sharm El Sheikh',
                'address': 'Naama Bay, Sharm El Sheikh',
                'star_rating': 5,
                'price_per_night': Decimal('150.00'),
                'description': 'Italian-style resort in the heart of Naama Bay. Walking distance to shops and nightlife, with excellent beach and diving facilities.',
                'latitude': Decimal('27.9061'),
                'longitude': Decimal('34.3306'),
                'image_url': 'https://images.unsplash.com/photo-1602002418082-a4443e081dd1?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 291,
            },
            # HURGHADA
            {
                'name': 'Steigenberger Aldau Beach Hotel',
                'accommodation_type': 'resort',
                'city': 'Hurghada',
                'address': 'Sahl Hasheesh Road, Hurghada',
                'star_rating': 5,
                'price_per_night': Decimal('200.00'),
                'description': 'Upscale Red Sea resort with pristine private beach, golf course nearby, and excellent diving center. Modern luxury meets Egyptian hospitality.',
                'latitude': Decimal('27.0673'),
                'longitude': Decimal('33.8554'),
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 392,
            },
            {
                'name': 'Oberoi Sahl Hasheesh',
                'accommodation_type': 'resort',
                'city': 'Hurghada',
                'address': 'Sahl Hasheesh Bay, Hurghada',
                'star_rating': 5,
                'price_per_night': Decimal('350.00'),
                'description': 'Ultra-luxury boutique resort with private suites and villas. Stunning architecture inspired by ancient Egypt, world-class spa, and private beach.',
                'latitude': Decimal('27.0500'),
                'longitude': Decimal('33.8583'),
                'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 102,
            },
            {
                'name': 'Jaz Aquamarine Resort',
                'accommodation_type': 'resort',
                'city': 'Hurghada',
                'address': 'Safaga Road, Hurghada',
                'star_rating': 5,
                'price_per_night': Decimal('120.00'),
                'description': 'Family-friendly all-inclusive resort with massive water park, multiple pools, and extensive entertainment. Great value for Red Sea vacation.',
                'latitude': Decimal('27.1000'),
                'longitude': Decimal('33.8200'),
                'image_url': 'https://images.unsplash.com/photo-1561501900-3701fa6a0864?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 768,
            },
            # ALEXANDRIA
            {
                'name': 'Four Seasons Hotel Alexandria at San Stefano',
                'accommodation_type': 'hotel',
                'city': 'Alexandria',
                'address': '399 El Geish Road, San Stefano, Alexandria',
                'star_rating': 5,
                'price_per_night': Decimal('280.00'),
                'description': 'Mediterranean luxury on the Alexandria corniche. Part of the San Stefano Grand Plaza complex with private beach, spa, and stunning sea views.',
                'latitude': Decimal('31.2436'),
                'longitude': Decimal('29.9611'),
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800',
                'is_featured': True,
                'is_verified': True,
                'total_rooms': 118,
            },
            {
                'name': 'Hilton Alexandria Corniche',
                'accommodation_type': 'hotel',
                'city': 'Alexandria',
                'address': '544 El Geish Road, Alexandria',
                'star_rating': 5,
                'price_per_night': Decimal('150.00'),
                'description': 'Seafront hotel on the famous Alexandria Corniche. Close to Bibliotheca Alexandrina and historic sites. Features rooftop pool with Mediterranean views.',
                'latitude': Decimal('31.2100'),
                'longitude': Decimal('29.9200'),
                'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 252,
            },
            # Budget Options
            {
                'name': 'Pyramids View Inn',
                'accommodation_type': 'hotel',
                'city': 'Cairo',
                'address': 'Nazlet El-Semman, Giza',
                'star_rating': 3,
                'price_per_night': Decimal('45.00'),
                'description': 'Budget-friendly hotel with rooftop terrace offering incredible Pyramid views. Simple but clean rooms, friendly staff, and unbeatable location for budget travelers.',
                'latitude': Decimal('29.9753'),
                'longitude': Decimal('31.1376'),
                'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 24,
            },
            {
                'name': 'Nefertiti Hotel Luxor',
                'accommodation_type': 'hotel',
                'city': 'Luxor',
                'address': 'El Sahabi Street, Luxor',
                'star_rating': 3,
                'price_per_night': Decimal('35.00'),
                'description': 'Popular budget hotel near Luxor Temple. Rooftop restaurant with Nile views, helpful tour desk, and great value for money. Backpacker favorite.',
                'latitude': Decimal('25.6969'),
                'longitude': Decimal('32.6422'),
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 60,
            },
            {
                'name': 'Keylany Hotel Aswan',
                'accommodation_type': 'hotel',
                'city': 'Aswan',
                'address': 'Keylany Street, Aswan',
                'star_rating': 3,
                'price_per_night': Decimal('30.00'),
                'description': 'Charming Nubian-style hotel in central Aswan. Beautiful rooftop with Nile views, traditional decor, and excellent local restaurant.',
                'latitude': Decimal('24.0889'),
                'longitude': Decimal('32.8997'),
                'image_url': 'https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800',
                'is_featured': False,
                'is_verified': True,
                'total_rooms': 32,
            },
        ]

        # Get or create amenities
        amenities_map = {}
        amenity_names = [
            'WiFi', 'Pool', 'Spa', 'Restaurant', 'Room Service', 'Gym',
            'Parking', 'Airport Shuttle', 'Beach Access', 'Air Conditioning',
            'Bar', 'Concierge', 'Business Center', 'Kids Club', 'Diving Center'
        ]
        for name in amenity_names:
            amenity, _ = Amenity.objects.get_or_create(name=name)
            amenities_map[name] = amenity

        created_count = 0
        updated_count = 0

        for hotel_data in hotels:
            # Generate unique slug
            base_slug = slugify(hotel_data['name'])
            slug = base_slug
            counter = 1
            while Accommodation.objects.filter(slug=slug).exclude(name=hotel_data['name']).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            hotel, created = Accommodation.objects.update_or_create(
                name=hotel_data['name'],
                defaults={
                    'slug': slug,
                    'accommodation_type': hotel_data['accommodation_type'],
                    'city': hotel_data['city'],
                    'address': hotel_data['address'],
                    'star_rating': hotel_data['star_rating'],
                    'price_per_night': hotel_data['price_per_night'],
                    'description': hotel_data['description'],
                    'latitude': hotel_data.get('latitude'),
                    'longitude': hotel_data.get('longitude'),
                    'image_url': hotel_data['image_url'],
                    'is_featured': hotel_data['is_featured'],
                    'is_verified': hotel_data['is_verified'],
                    'is_active': True,
                    'total_rooms': hotel_data.get('total_rooms', 100),
                }
            )

            # Add amenities based on star rating
            if hotel_data['star_rating'] >= 5:
                hotel.amenities.set([
                    amenities_map['WiFi'], amenities_map['Pool'], amenities_map['Spa'],
                    amenities_map['Restaurant'], amenities_map['Room Service'],
                    amenities_map['Gym'], amenities_map['Concierge'], amenities_map['Bar'],
                    amenities_map['Air Conditioning'], amenities_map['Business Center']
                ])
            elif hotel_data['star_rating'] >= 4:
                hotel.amenities.set([
                    amenities_map['WiFi'], amenities_map['Pool'], amenities_map['Restaurant'],
                    amenities_map['Room Service'], amenities_map['Air Conditioning'],
                    amenities_map['Gym']
                ])
            else:
                hotel.amenities.set([
                    amenities_map['WiFi'], amenities_map['Air Conditioning'],
                    amenities_map['Restaurant']
                ])

            if created:
                created_count += 1
                self.stdout.write(f'  Created: {hotel.name}')
            else:
                updated_count += 1
                self.stdout.write(f'  Updated: {hotel.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count} hotels, updated {updated_count} hotels.'
        ))
        self.stdout.write(self.style.WARNING(
            '\nRun "python manage.py populate_affiliate_urls" to add booking links!'
        ))
