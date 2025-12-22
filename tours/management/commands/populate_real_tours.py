# tours/management/commands/populate_real_tours.py
"""
Populate database with REAL Egyptian tours
Actual tour experiences available in Egypt
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tours.models import Tour, TourItinerary
from decimal import Decimal
import json


class Command(BaseCommand):
    help = 'Populate database with real Egyptian tours'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing tours before adding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing tours...')
            Tour.objects.all().delete()

        self.stdout.write('Adding real Egyptian tours...')

        tours = [
            # PYRAMIDS & CAIRO TOURS
            {
                'name': 'Pyramids of Giza, Sphinx & Egyptian Museum Full Day Tour',
                'tour_type': 'cultural',
                'description': 'Explore the last remaining wonder of the ancient world! Visit the Great Pyramids of Giza, the mysterious Sphinx, and the world-renowned Egyptian Museum housing King Tutankhamun\'s treasures. Includes expert Egyptologist guide, lunch, and all entrance fees.',
                'highlights': 'Great Pyramid of Khufu, Sphinx, Valley Temple, Egyptian Museum, Tutankhamun exhibits, Mummy Room',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Cairo',
                'destinations': ['Giza', 'Cairo'],
                'price_per_person': Decimal('75.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 15,
                'includes': ['Hotel pickup and drop-off', 'Air-conditioned vehicle', 'Egyptologist guide', 'Entrance fees', 'Lunch', 'Bottled water'],
                'excludes': ['Gratuities', 'Personal expenses', 'Camel rides (optional)'],
                'languages': ['English', 'Spanish', 'French', 'German', 'Italian'],
                'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800',
                'is_featured': True,
            },
            {
                'name': 'Grand Egyptian Museum VIP Tour',
                'tour_type': 'cultural',
                'description': 'Be among the first to explore the brand new Grand Egyptian Museum (GEM), the largest archaeological museum in the world! See the complete Tutankhamun collection, the Grand Staircase, and artifacts never displayed before.',
                'highlights': 'Grand Egyptian Museum, Complete Tutankhamun collection, Khufu Solar Boat, Ramses II statue, Ancient artifacts',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Cairo',
                'destinations': ['Giza'],
                'price_per_person': Decimal('95.00'),
                'difficulty_level': 'easy',
                'min_group_size': 1,
                'max_group_size': 10,
                'includes': ['Hotel pickup and drop-off', 'Skip-the-line entrance', 'Private Egyptologist', 'Lunch at museum restaurant'],
                'excludes': ['Gratuities', 'Additional food and drinks'],
                'languages': ['English', 'Arabic', 'French', 'Spanish'],
                'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800',
                'is_featured': True,
            },
            {
                'name': 'Cairo Islamic & Coptic Heritage Walking Tour',
                'tour_type': 'cultural',
                'description': 'Discover 1,400 years of religious history in Cairo. Explore the ancient Coptic quarter with the Hanging Church, walk through medieval Islamic Cairo including Al-Azhar Mosque, and browse the legendary Khan El Khalili bazaar.',
                'highlights': 'Hanging Church, Ben Ezra Synagogue, Al-Azhar Mosque, Khan El Khalili, Islamic Cairo streets',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Cairo',
                'destinations': ['Cairo'],
                'price_per_person': Decimal('45.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 12,
                'includes': ['Expert guide', 'Entrance fees', 'Traditional Egyptian tea', 'Walking tour'],
                'excludes': ['Hotel transfers', 'Lunch', 'Shopping purchases'],
                'languages': ['English', 'Arabic'],
                'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800',
                'is_featured': False,
            },
            # LUXOR TOURS
            {
                'name': 'Luxor Full Day Tour: Valley of Kings, Hatshepsut & Karnak',
                'tour_type': 'cultural',
                'description': 'Experience the ancient capital of Egypt! Visit the famous Valley of the Kings where Tutankhamun was buried, the stunning Temple of Hatshepsut, and the massive Karnak Temple complex. A must-do for history lovers.',
                'highlights': 'Valley of the Kings, Temple of Hatshepsut, Colossi of Memnon, Karnak Temple, Luxor Temple',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Luxor',
                'destinations': ['Luxor'],
                'price_per_person': Decimal('85.00'),
                'difficulty_level': 'moderate',
                'min_group_size': 2,
                'max_group_size': 15,
                'includes': ['Hotel pickup', 'Air-conditioned vehicle', 'Egyptologist guide', 'All entrance fees', 'Lunch', 'Water'],
                'excludes': ['Gratuities', 'Photography tickets inside tombs'],
                'languages': ['English', 'Spanish', 'French', 'German'],
                'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800',
                'is_featured': True,
            },
            {
                'name': 'Luxor Hot Air Balloon Sunrise Experience',
                'tour_type': 'adventure',
                'description': 'Soar over the ancient temples and tombs of Luxor at sunrise! This magical hot air balloon ride offers breathtaking views of the Valley of the Kings, Hatshepsut Temple, and the Nile River as the sun rises.',
                'highlights': 'Sunrise flight, Valley of Kings aerial view, Nile River panorama, Hatshepsut Temple from above, Photo opportunities',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Luxor',
                'destinations': ['Luxor'],
                'price_per_person': Decimal('120.00'),
                'difficulty_level': 'easy',
                'min_group_size': 1,
                'max_group_size': 20,
                'includes': ['Hotel pickup (4:30 AM)', 'Balloon flight (45-60 min)', 'Flight certificate', 'Tea/coffee after landing'],
                'excludes': ['Gratuities', 'Breakfast', 'Video recording'],
                'languages': ['English', 'Arabic'],
                'image_url': 'https://images.unsplash.com/photo-1507608616759-54f48f0af0ee?w=800',
                'is_featured': True,
            },
            # NILE CRUISES
            {
                'name': '4-Night Nile Cruise: Luxor to Aswan',
                'tour_type': 'cruise',
                'description': 'Sail the legendary Nile River from Luxor to Aswan on a luxury cruise ship. Visit all major temples including Karnak, Edfu, Kom Ombo, and Philae. All-inclusive with gourmet meals and nightly entertainment.',
                'highlights': 'Karnak Temple, Edfu Temple, Kom Ombo Temple, Philae Temple, Aswan High Dam, Felucca ride',
                'duration_days': 5,
                'duration_nights': 4,
                'departure_city': 'Luxor',
                'destinations': ['Luxor', 'Edfu', 'Kom Ombo', 'Aswan'],
                'price_per_person': Decimal('650.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 150,
                'includes': ['4 nights accommodation', 'Full board meals', 'Sightseeing with guide', 'Entrance fees', 'Entertainment', 'Felucca ride in Aswan'],
                'excludes': ['Flights', 'Drinks', 'Gratuities', 'Optional tours'],
                'languages': ['English', 'German', 'French', 'Spanish', 'Italian'],
                'image_url': 'https://images.unsplash.com/photo-1553913861-c0c5f9c7d221?w=800',
                'is_featured': True,
            },
            {
                'name': '7-Night Luxury Nile Cruise: Cairo to Aswan',
                'tour_type': 'luxury',
                'description': 'The ultimate Nile experience! Sail from Cairo to Aswan on a 5-star luxury vessel. Visit every major temple along the way, enjoy gourmet dining, and relax in absolute comfort as ancient Egypt unfolds before you.',
                'highlights': 'All Nile temples, Tell el-Amarna, Dendera, Abydos, Valley of Kings, Abu Simbel option',
                'duration_days': 8,
                'duration_nights': 7,
                'departure_city': 'Cairo',
                'destinations': ['Cairo', 'Minya', 'Luxor', 'Edfu', 'Aswan'],
                'price_per_person': Decimal('2200.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 50,
                'includes': ['7 nights luxury cabin', 'All meals and drinks', 'All excursions', 'Private Egyptologist', 'Butler service'],
                'excludes': ['International flights', 'Visa', 'Travel insurance', 'Abu Simbel flight'],
                'languages': ['English', 'French', 'German'],
                'image_url': 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800',
                'is_featured': True,
            },
            # ASWAN & ABU SIMBEL
            {
                'name': 'Abu Simbel Day Trip from Aswan',
                'tour_type': 'cultural',
                'description': 'Visit the awe-inspiring temples of Abu Simbel, carved into the mountainside by Ramses II. These UNESCO World Heritage temples were relocated in a massive international effort to save them from the Aswan Dam.',
                'highlights': 'Great Temple of Ramses II, Temple of Nefertari, Lake Nasser views, UNESCO heritage site',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Aswan',
                'destinations': ['Abu Simbel'],
                'price_per_person': Decimal('95.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 40,
                'includes': ['Hotel pickup (3:00 AM)', 'Air-conditioned bus', 'Egyptologist guide', 'Entrance fees', 'Breakfast box'],
                'excludes': ['Lunch', 'Gratuities', 'Drinks'],
                'languages': ['English', 'Spanish', 'French'],
                'image_url': 'https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800',
                'is_featured': True,
            },
            {
                'name': 'Aswan Highlights: Philae Temple, High Dam & Nubian Village',
                'tour_type': 'cultural',
                'description': 'Explore the best of Aswan! Visit the beautiful Philae Temple dedicated to Isis, see the engineering marvel of the High Dam, and experience authentic Nubian culture in a traditional village.',
                'highlights': 'Philae Temple, Aswan High Dam, Unfinished Obelisk, Nubian Village, Traditional lunch',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Aswan',
                'destinations': ['Aswan'],
                'price_per_person': Decimal('65.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 15,
                'includes': ['Hotel pickup', 'All entrance fees', 'Boat to Philae', 'Nubian lunch', 'Expert guide'],
                'excludes': ['Gratuities', 'Drinks', 'Shopping'],
                'languages': ['English', 'Arabic', 'French'],
                'image_url': 'https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800',
                'is_featured': False,
            },
            # RED SEA ADVENTURES
            {
                'name': 'Red Sea Diving: Full Day with 2 Dives',
                'tour_type': 'diving',
                'description': 'Explore the stunning underwater world of the Red Sea! This full-day diving trip includes two dives at premier sites with crystal clear waters, colorful coral reefs, and abundant marine life.',
                'highlights': 'Two dive sites, Coral reefs, Tropical fish, Professional instruction, Equipment included',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Hurghada',
                'destinations': ['Red Sea'],
                'price_per_person': Decimal('85.00'),
                'difficulty_level': 'moderate',
                'min_group_size': 2,
                'max_group_size': 12,
                'includes': ['Two dives', 'All equipment', 'PADI instructor', 'Lunch on boat', 'Soft drinks'],
                'excludes': ['Certification course', 'Underwater photos', 'Gratuities'],
                'languages': ['English', 'German', 'Russian'],
                'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
                'is_featured': True,
            },
            {
                'name': 'Snorkeling Trip to Giftun Island',
                'tour_type': 'adventure',
                'description': 'Escape to the pristine Giftun Island National Park! Enjoy snorkeling in crystal-clear waters, relax on white sandy beaches, and spot dolphins on the way. Perfect for families and non-divers.',
                'highlights': 'Giftun Island, Snorkeling spots, Beach time, Dolphin watching, Lunch buffet',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Hurghada',
                'destinations': ['Giftun Island'],
                'price_per_person': Decimal('45.00'),
                'difficulty_level': 'easy',
                'min_group_size': 1,
                'max_group_size': 50,
                'includes': ['Boat trip', 'Snorkeling equipment', 'National park fees', 'Lunch buffet', 'Soft drinks'],
                'excludes': ['Photos', 'Gratuities', 'Beach chairs'],
                'languages': ['English', 'German', 'Russian', 'Polish'],
                'image_url': 'https://images.unsplash.com/photo-1582967788606-a171c1080cb0?w=800',
                'is_featured': False,
            },
            {
                'name': 'Desert Safari & Bedouin BBQ Experience',
                'tour_type': 'desert',
                'description': 'Adventure into the Eastern Desert! Ride quad bikes through stunning desert landscapes, visit a Bedouin camp, watch the sunset over the mountains, and enjoy a traditional BBQ dinner under the stars.',
                'highlights': 'Quad biking, Bedouin village, Camel ride, Sunset views, BBQ dinner, Stargazing',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Hurghada',
                'destinations': ['Eastern Desert'],
                'price_per_person': Decimal('55.00'),
                'difficulty_level': 'moderate',
                'min_group_size': 2,
                'max_group_size': 30,
                'includes': ['Hotel pickup', 'Quad bike', 'Bedouin tea', 'Camel ride', 'BBQ dinner', 'Traditional show'],
                'excludes': ['Photos', 'Gratuities', 'Alcohol'],
                'languages': ['English', 'German', 'Russian'],
                'image_url': 'https://images.unsplash.com/photo-1547234935-80c7145ec969?w=800',
                'is_featured': False,
            },
            # SINAI TOURS
            {
                'name': 'Mount Sinai Sunrise Hike',
                'tour_type': 'religious',
                'description': 'Climb the sacred Mount Sinai where Moses received the Ten Commandments. Begin the trek at midnight, reach the summit for a spectacular sunrise, then visit St. Catherine\'s Monastery, one of the world\'s oldest.',
                'highlights': 'Mount Sinai summit, Sunrise views, St. Catherine Monastery, Burning Bush site, Ancient icons',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Sharm El Sheikh',
                'destinations': ['Mount Sinai', 'St. Catherine'],
                'price_per_person': Decimal('75.00'),
                'difficulty_level': 'challenging',
                'min_group_size': 2,
                'max_group_size': 20,
                'includes': ['Hotel pickup (10 PM)', 'Bedouin guide', 'Monastery visit', 'Breakfast', 'Hot drinks at summit'],
                'excludes': ['Camel ride up (optional)', 'Gratuities'],
                'languages': ['English', 'Arabic'],
                'image_url': 'https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800',
                'is_featured': True,
            },
            {
                'name': 'Ras Mohammed National Park Snorkeling',
                'tour_type': 'adventure',
                'description': 'Discover Egypt\'s premier marine park! Ras Mohammed offers some of the best snorkeling in the world with pristine coral walls, tropical fish, and the famous Shark Reef. A must-do from Sharm El Sheikh.',
                'highlights': 'Ras Mohammed Park, Shark Reef, Yolanda Reef, Mangroves, Magic Lake',
                'duration_days': 1,
                'duration_nights': 0,
                'departure_city': 'Sharm El Sheikh',
                'destinations': ['Ras Mohammed'],
                'price_per_person': Decimal('55.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 40,
                'includes': ['Hotel pickup', 'Park entrance', 'Snorkeling equipment', 'Lunch', 'Guide'],
                'excludes': ['Underwater camera', 'Gratuities'],
                'languages': ['English', 'Russian', 'German'],
                'image_url': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800',
                'is_featured': False,
            },
            # MULTI-DAY PACKAGES
            {
                'name': '10-Day Ultimate Egypt Tour: Cairo, Luxor, Aswan & Abu Simbel',
                'tour_type': 'cultural',
                'description': 'The complete Egyptian experience! Visit all major sites from the Pyramids to Abu Simbel, cruise the Nile in style, and experience the best of ancient and modern Egypt with expert guides.',
                'highlights': 'Pyramids & Sphinx, Egyptian Museum, Luxor temples, Nile cruise, Abu Simbel, Aswan',
                'duration_days': 10,
                'duration_nights': 9,
                'departure_city': 'Cairo',
                'destinations': ['Cairo', 'Luxor', 'Aswan', 'Abu Simbel'],
                'price_per_person': Decimal('1850.00'),
                'difficulty_level': 'moderate',
                'min_group_size': 2,
                'max_group_size': 16,
                'includes': ['All accommodations', 'Domestic flights', 'Nile cruise', 'All meals', 'Expert Egyptologist', 'All entrance fees'],
                'excludes': ['International flights', 'Visa', 'Travel insurance', 'Gratuities'],
                'languages': ['English', 'Spanish', 'French'],
                'image_url': 'https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800',
                'is_featured': True,
            },
            {
                'name': '5-Day Cairo & Alexandria Discovery',
                'tour_type': 'cultural',
                'description': 'Explore Egypt\'s two great cities! Discover Cairo\'s ancient wonders including the Pyramids and Egyptian Museum, then journey to Alexandria to see Greco-Roman ruins, the modern library, and Mediterranean charm.',
                'highlights': 'Pyramids, Egyptian Museum, Citadel, Alexandria Library, Catacombs, Qaitbay Citadel',
                'duration_days': 5,
                'duration_nights': 4,
                'departure_city': 'Cairo',
                'destinations': ['Cairo', 'Alexandria'],
                'price_per_person': Decimal('550.00'),
                'difficulty_level': 'easy',
                'min_group_size': 2,
                'max_group_size': 15,
                'includes': ['4-star hotels', 'Daily breakfast', 'All transfers', 'Egyptologist guide', 'Entrance fees'],
                'excludes': ['Lunches and dinners', 'Gratuities', 'Personal expenses'],
                'languages': ['English', 'Arabic', 'French'],
                'image_url': 'https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800',
                'is_featured': False,
            },
        ]

        created_count = 0
        updated_count = 0

        for tour_data in tours:
            # Generate unique slug
            base_slug = slugify(tour_data['name'])
            slug = base_slug
            counter = 1
            while Tour.objects.filter(slug=slug).exclude(name=tour_data['name']).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            tour, created = Tour.objects.update_or_create(
                name=tour_data['name'],
                defaults={
                    'slug': slug,
                    'tour_type': tour_data['tour_type'],
                    'description': tour_data['description'],
                    'highlights': tour_data['highlights'],
                    'duration_days': tour_data['duration_days'],
                    'duration_nights': tour_data['duration_nights'],
                    'departure_city': tour_data['departure_city'],
                    'destinations': tour_data['destinations'],
                    'price_per_person': tour_data['price_per_person'],
                    'difficulty_level': tour_data['difficulty_level'],
                    'min_group_size': tour_data['min_group_size'],
                    'max_group_size': tour_data['max_group_size'],
                    'includes': tour_data['includes'],
                    'excludes': tour_data['excludes'],
                    'languages': tour_data['languages'],
                    'image_url': tour_data['image_url'],
                    'is_featured': tour_data['is_featured'],
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  Created: {tour.name}')
            else:
                updated_count += 1
                self.stdout.write(f'  Updated: {tour.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count} tours, updated {updated_count} tours.'
        ))
        self.stdout.write(self.style.WARNING(
            '\nRun "python manage.py populate_tour_affiliate_urls" to add booking links!'
        ))
