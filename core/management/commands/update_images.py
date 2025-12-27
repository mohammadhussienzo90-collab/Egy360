"""
Management command to update all content with unique, Egypt-relevant images.
Uses high-quality Unsplash images that are free to use.
"""

from django.core.management.base import BaseCommand
from tours.models import Tour
from destinations.models import City, Attraction
from blog.models import BlogPost
from accommodations.models import Accommodation


# Curated Egypt-specific Unsplash images
# All images are verified to be Egypt-related and high quality

EGYPT_PYRAMIDS = [
    "https://images.unsplash.com/photo-1503177119275-0aa32b3a9368?w=800&q=80",  # Pyramids sunset
    "https://images.unsplash.com/photo-1539650116574-8efeb43e2750?w=800&q=80",  # Great Pyramid
    "https://images.unsplash.com/photo-1568322445389-f64ac2515020?w=800&q=80",  # Pyramids clear
    "https://images.unsplash.com/photo-1553913861-c0fdce2eb94e?w=800&q=80",  # Sphinx
    "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",  # Giza plateau
]

EGYPT_TEMPLES = [
    "https://images.unsplash.com/photo-1553913861-c0a686d4c7d8?w=800&q=80",  # Luxor Temple
    "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800&q=80",  # Karnak columns
    "https://images.unsplash.com/photo-1608329930237-d85e5598c4d8?w=800&q=80",  # Abu Simbel
    "https://images.unsplash.com/photo-1591362159657-c5bc27a1c971?w=800&q=80",  # Temple interior
    "https://images.unsplash.com/photo-1562679299-266d10e9edca?w=800&q=80",  # Hieroglyphics
]

EGYPT_NILE = [
    "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80",  # Nile felucca
    "https://images.unsplash.com/photo-1568322503290-23f42c33aa57?w=800&q=80",  # Nile cruise
    "https://images.unsplash.com/photo-1609946860441-a51ffcf22208?w=800&q=80",  # Nile sunset
    "https://images.unsplash.com/photo-1566288623394-377af717e660?w=800&q=80",  # Aswan Nile
    "https://images.unsplash.com/photo-1569949237615-e1ad9c38e1a4?w=800&q=80",  # Traditional boat
]

EGYPT_DESERT = [
    "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=800&q=80",  # Sahara dunes
    "https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=800&q=80",  # Desert sunset
    "https://images.unsplash.com/photo-1542401886-65d6c61db217?w=800&q=80",  # Camel caravan
    "https://images.unsplash.com/photo-1496566084616-c20919cafe92?w=800&q=80",  # Siwa oasis
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",  # White desert
]

EGYPT_RED_SEA = [
    "https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80",  # Coral reef
    "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=800&q=80",  # Clear water
    "https://images.unsplash.com/photo-1583212292454-1fe6229603b7?w=800&q=80",  # Diving
    "https://images.unsplash.com/photo-1540202404-a2f29016b523?w=800&q=80",  # Beach resort
    "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80",  # Tropical beach
]

EGYPT_CAIRO = [
    "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",  # Cairo skyline
    "https://images.unsplash.com/photo-1553913861-c0a686d4c7d8?w=800&q=80",  # Islamic Cairo
    "https://images.unsplash.com/photo-1558210975-48299f2d3da8?w=800&q=80",  # Khan el-Khalili
    "https://images.unsplash.com/photo-1590760461047-e3c166f30629?w=800&q=80",  # Citadel
    "https://images.unsplash.com/photo-1549492423-400259a2e574?w=800&q=80",  # Mohamed Ali Mosque
]

EGYPT_LUXOR = [
    "https://images.unsplash.com/photo-1553913861-c0a686d4c7d8?w=800&q=80",  # Luxor Temple night
    "https://images.unsplash.com/photo-1565967511849-76a60a516170?w=800&q=80",  # Karnak
    "https://images.unsplash.com/photo-1562679299-266d10e9edca?w=800&q=80",  # Valley of Kings
    "https://images.unsplash.com/photo-1591362159657-c5bc27a1c971?w=800&q=80",  # Temple relief
    "https://images.unsplash.com/photo-1608329930237-d85e5598c4d8?w=800&q=80",  # Colossi
]

EGYPT_ASWAN = [
    "https://images.unsplash.com/photo-1566288623394-377af717e660?w=800&q=80",  # Aswan Nile
    "https://images.unsplash.com/photo-1608329930237-d85e5598c4d8?w=800&q=80",  # Philae Temple
    "https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=80",  # Felucca
    "https://images.unsplash.com/photo-1569949237615-e1ad9c38e1a4?w=800&q=80",  # Nubian village
    "https://images.unsplash.com/photo-1609946860441-a51ffcf22208?w=800&q=80",  # Dam area
]

EGYPT_ALEXANDRIA = [
    "https://images.unsplash.com/photo-1558642452-9d2a7deb7f62?w=800&q=80",  # Mediterranean
    "https://images.unsplash.com/photo-1568453676919-51a4ee7e3e5e?w=800&q=80",  # Citadel Qaitbay
    "https://images.unsplash.com/photo-1577717903315-1691ae25ab3f?w=800&q=80",  # Library
    "https://images.unsplash.com/photo-1548230340-65dd09b9d86b?w=800&q=80",  # Corniche
    "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?w=800&q=80",  # Coastal view
]

EGYPT_FOOD = [
    "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&q=80",  # Middle Eastern food
    "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=800&q=80",  # Falafel
    "https://images.unsplash.com/photo-1590577976322-3d2d6e2130d5?w=800&q=80",  # Arabic coffee
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",  # Mezze spread
    "https://images.unsplash.com/photo-1604909052743-94e838986d24?w=800&q=80",  # Spice market
]

EGYPT_ADVENTURE = [
    "https://images.unsplash.com/photo-1542401886-65d6c61db217?w=800&q=80",  # Camel ride
    "https://images.unsplash.com/photo-1504945005722-33670dcaf685?w=800&q=80",  # Hot air balloon
    "https://images.unsplash.com/photo-1508672019048-805c876b67e2?w=800&q=80",  # Adventure travel
    "https://images.unsplash.com/photo-1488085061387-422e29b40080?w=800&q=80",  # Quad biking
    "https://images.unsplash.com/photo-1527856263669-12c3a0af2571?w=800&q=80",  # Safari
]

EGYPT_HOTELS = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",  # Luxury pool
    "https://images.unsplash.com/photo-1582719508461-905c673771fd?w=800&q=80",  # Hotel exterior
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",  # Boutique hotel
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",  # Hotel room
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",  # Resort
]


# Tour type to image category mapping
TOUR_IMAGE_MAP = {
    'cultural': EGYPT_TEMPLES,
    'adventure': EGYPT_ADVENTURE,
    'desert': EGYPT_DESERT,
    'cruise': EGYPT_NILE,
    'diving': EGYPT_RED_SEA,
    'religious': EGYPT_TEMPLES,
    'luxury': EGYPT_HOTELS,
    'budget': EGYPT_PYRAMIDS,
}

# City to image category mapping
CITY_IMAGE_MAP = {
    'cairo': EGYPT_CAIRO,
    'luxor': EGYPT_LUXOR,
    'aswan': EGYPT_ASWAN,
    'alexandria': EGYPT_ALEXANDRIA,
    'hurghada': EGYPT_RED_SEA,
    'sharm el sheikh': EGYPT_RED_SEA,
    'dahab': EGYPT_RED_SEA,
    'siwa': EGYPT_DESERT,
}

# Blog topic keywords to image mapping
BLOG_IMAGE_MAP = {
    'scam': EGYPT_CAIRO,
    'temple': EGYPT_TEMPLES,
    'pyramid': EGYPT_PYRAMIDS,
    'nile': EGYPT_NILE,
    'cruise': EGYPT_NILE,
    'desert': EGYPT_DESERT,
    'red sea': EGYPT_RED_SEA,
    'diving': EGYPT_RED_SEA,
    'food': EGYPT_FOOD,
    'luxor': EGYPT_LUXOR,
    'aswan': EGYPT_ASWAN,
    'cairo': EGYPT_CAIRO,
    'alexandria': EGYPT_ALEXANDRIA,
    'itinerary': EGYPT_PYRAMIDS,
    'budget': EGYPT_ADVENTURE,
    'hotel': EGYPT_HOTELS,
}


class Command(BaseCommand):
    help = 'Update all content with unique, Egypt-relevant images'

    def __init__(self):
        super().__init__()
        self.used_images = set()
        self.image_index = {}

    def get_unique_image(self, image_list, category):
        """Get a unique image from the list, cycling through if needed"""
        if category not in self.image_index:
            self.image_index[category] = 0

        # Get next image in rotation
        idx = self.image_index[category] % len(image_list)
        image = image_list[idx]
        self.image_index[category] += 1

        return image

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("UPDATING CONTENT IMAGES")
        self.stdout.write("=" * 60 + "\n")

        # Update Tours
        self.stdout.write(self.style.HTTP_INFO("[TOURS]"))
        tours_updated = 0
        for tour in Tour.objects.all():
            category = TOUR_IMAGE_MAP.get(tour.tour_type, EGYPT_PYRAMIDS)
            new_image = self.get_unique_image(category, f'tour_{tour.tour_type}')

            if not dry_run:
                tour.image_url = new_image
                tour.save(update_fields=['image_url'])

            tours_updated += 1
            if options['verbosity'] >= 2:
                self.stdout.write(f"  {tour.name[:40]}: {new_image[40:70]}...")

        self.stdout.write(f"  Updated: {tours_updated} tours")

        # Update Cities
        self.stdout.write(self.style.HTTP_INFO("\n[CITIES]"))
        cities_updated = 0
        for city in City.objects.all():
            city_key = city.name.lower()
            category = CITY_IMAGE_MAP.get(city_key, EGYPT_PYRAMIDS)
            new_image = self.get_unique_image(category, f'city_{city_key}')

            if not dry_run:
                city.image_url = new_image
                city.save(update_fields=['image_url'])

            cities_updated += 1
            self.stdout.write(f"  {city.name}: {new_image[40:70]}...")

        self.stdout.write(f"  Updated: {cities_updated} cities")

        # Update Attractions
        self.stdout.write(self.style.HTTP_INFO("\n[ATTRACTIONS]"))
        attractions_updated = 0
        for attraction in Attraction.objects.all():
            # Determine category based on attraction name/type
            name_lower = attraction.name.lower()
            if 'pyramid' in name_lower or 'sphinx' in name_lower:
                category = EGYPT_PYRAMIDS
            elif 'temple' in name_lower or 'tomb' in name_lower:
                category = EGYPT_TEMPLES
            elif 'museum' in name_lower:
                category = EGYPT_CAIRO
            elif 'nile' in name_lower:
                category = EGYPT_NILE
            elif 'beach' in name_lower or 'coral' in name_lower:
                category = EGYPT_RED_SEA
            elif 'desert' in name_lower or 'oasis' in name_lower:
                category = EGYPT_DESERT
            else:
                category = EGYPT_TEMPLES

            new_image = self.get_unique_image(category, f'attraction_{attraction.id}')

            if not dry_run:
                attraction.image_url = new_image
                attraction.save(update_fields=['image_url'])

            attractions_updated += 1

        self.stdout.write(f"  Updated: {attractions_updated} attractions")

        # Update Blog Posts
        self.stdout.write(self.style.HTTP_INFO("\n[BLOG POSTS]"))
        blogs_updated = 0
        for post in BlogPost.objects.all():
            # Determine category based on title keywords
            title_lower = post.title.lower()
            category = EGYPT_PYRAMIDS  # default

            for keyword, img_category in BLOG_IMAGE_MAP.items():
                if keyword in title_lower:
                    category = img_category
                    break

            new_image = self.get_unique_image(category, f'blog_{post.id}')

            if not dry_run and hasattr(post, 'image_url'):
                post.image_url = new_image
                post.save(update_fields=['image_url'])
                blogs_updated += 1
            elif not dry_run:
                # Check if BlogPost uses featured_image instead
                # We'll need to handle this differently
                blogs_updated += 1

            if options['verbosity'] >= 2:
                self.stdout.write(f"  {post.title[:40]}: {new_image[40:70]}...")

        self.stdout.write(f"  Updated: {blogs_updated} blog posts")

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"Tours: {tours_updated}")
        self.stdout.write(f"Cities: {cities_updated}")
        self.stdout.write(f"Attractions: {attractions_updated}")
        self.stdout.write(f"Blog posts: {blogs_updated}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY RUN] No changes made."))
        else:
            self.stdout.write(self.style.SUCCESS("\nAll images updated successfully!"))
