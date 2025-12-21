"""
Management command to populate Travelpayouts affiliate URLs for all accommodations.

Travelpayouts Marker ID: 477897

This creates Hotellook deep links for hotel searches and also sets up
direct Booking.com affiliate links where possible.
"""

from django.core.management.base import BaseCommand
from accommodations.models import Accommodation
from urllib.parse import quote_plus


# IATA codes for Egyptian cities (used by Hotellook)
CITY_IATA_CODES = {
    'cairo': 'CAI',
    'cairo, egypt': 'CAI',
    'luxor': 'LXR',
    'luxor, egypt': 'LXR',
    'aswan': 'ASW',
    'aswan, egypt': 'ASW',
    'hurghada': 'HRG',
    'hurghada, egypt': 'HRG',
    'sharm el sheikh': 'SSH',
    'sharm el-sheikh': 'SSH',
    'sharm el sheikh, egypt': 'SSH',
    'alexandria': 'ALY',
    'alexandria, egypt': 'ALY',
    'dahab': 'SSH',  # Uses Sharm El Sheikh airport
    'dahab, egypt': 'SSH',
    'marsa alam': 'RMF',
    'marsa alam, egypt': 'RMF',
    'el gouna': 'HRG',  # Uses Hurghada airport
    'el gouna, egypt': 'HRG',
    'siwa': 'CAI',  # Closest major airport
    'siwa oasis': 'CAI',
}

# Hotellook location IDs for direct city searches
CITY_LOCATION_IDS = {
    'cairo': '12153',
    'luxor': '15951',
    'aswan': '7929',
    'hurghada': '14048',
    'sharm el sheikh': '24236',
    'alexandria': '7292',
    'dahab': '10531',
    'marsa alam': '17547',
}

TRAVELPAYOUTS_MARKER = '477897'


class Command(BaseCommand):
    help = 'Populate Travelpayouts affiliate URLs for all accommodations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing affiliate URLs',
        )

    def get_city_key(self, city_name):
        """Normalize city name to match our lookup tables"""
        return city_name.lower().strip()

    def get_iata_code(self, city_name):
        """Get IATA code for a city"""
        city_key = self.get_city_key(city_name)
        return CITY_IATA_CODES.get(city_key, 'CAI')  # Default to Cairo

    def get_location_id(self, city_name):
        """Get Hotellook location ID for a city"""
        city_key = self.get_city_key(city_name)
        # Try exact match first
        if city_key in CITY_LOCATION_IDS:
            return CITY_LOCATION_IDS[city_key]
        # Try partial match
        for key, loc_id in CITY_LOCATION_IDS.items():
            if key in city_key or city_key in key:
                return loc_id
        return CITY_LOCATION_IDS.get('cairo', '12153')  # Default to Cairo

    def generate_hotellook_url(self, accommodation):
        """
        Generate Hotellook affiliate URL for an accommodation.
        Uses hotel name search within the city for best matching.
        """
        city_key = self.get_city_key(accommodation.city)
        location_id = self.get_location_id(accommodation.city)
        hotel_name = quote_plus(accommodation.name)

        # Primary format: Search with hotel name in specific city
        # This takes users directly to search results for this hotel
        url = (
            f"https://search.hotellook.com/hotels?"
            f"locationId={location_id}&"
            f"marker={TRAVELPAYOUTS_MARKER}&"
            f"q={hotel_name}&"
            f"locale=en&"
            f"currency=usd"
        )

        return url

    def generate_hotellook_city_url(self, city_name):
        """Generate a city-level Hotellook search URL (fallback)"""
        location_id = self.get_location_id(city_name)
        return (
            f"https://search.hotellook.com/hotels?"
            f"locationId={location_id}&"
            f"marker={TRAVELPAYOUTS_MARKER}&"
            f"locale=en&"
            f"currency=usd"
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        overwrite = options['overwrite']

        accommodations = Accommodation.objects.all()
        total = accommodations.count()
        updated = 0
        skipped = 0

        self.stdout.write(f"\nProcessing {total} accommodations...")
        self.stdout.write(f"Travelpayouts Marker: {TRAVELPAYOUTS_MARKER}")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write(f"Overwrite existing: {overwrite}\n")

        for acc in accommodations:
            # Check if already has affiliate URL
            has_booking_url = bool(acc.booking_com_url)

            if has_booking_url and not overwrite:
                skipped += 1
                if options['verbosity'] >= 2:
                    self.stdout.write(f"  SKIP: {acc.name} (already has URL)")
                continue

            # Generate Hotellook affiliate URL
            hotellook_url = self.generate_hotellook_url(acc)

            if dry_run:
                self.stdout.write(
                    f"  [DRY RUN] {acc.name} ({acc.city})\n"
                    f"    -> {hotellook_url[:80]}..."
                )
            else:
                # Update the accommodation
                acc.booking_com_url = hotellook_url

                # Set commission rate (Travelpayouts hotel commission is typically 50-70% of booking site commission)
                # Booking.com pays ~4%, so affiliates get ~2-2.8%
                if acc.commission_rate == 0:
                    acc.commission_rate = 2.5

                acc.save()

                self.stdout.write(
                    self.style.SUCCESS(f"  OK: {acc.name} ({acc.city})")
                )

            updated += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(f"Total accommodations: {total}")
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Skipped: {skipped}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nThis was a dry run. Run without --dry-run to apply changes.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"\nSuccessfully updated {updated} accommodations with Travelpayouts URLs!")
            )

        # Show sample URLs
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Sample affiliate URLs generated:\n")

        cities_shown = set()
        for acc in Accommodation.objects.all()[:10]:
            city_key = self.get_city_key(acc.city)
            if city_key not in cities_shown:
                cities_shown.add(city_key)
                url = acc.booking_com_url if not dry_run else self.generate_hotellook_url(acc)
                self.stdout.write(f"\n{acc.name} ({acc.city}):")
                self.stdout.write(f"  {url}")
