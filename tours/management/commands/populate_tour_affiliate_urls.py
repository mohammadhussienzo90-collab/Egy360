"""
Management command to populate affiliate URLs for all tours.

Travelpayouts Marker ID: 477897

This creates Viator deep links through Travelpayouts for tour searches.
Viator offers 8% commission on tour bookings.
"""

from django.core.management.base import BaseCommand
from tours.models import Tour
from urllib.parse import quote_plus


TRAVELPAYOUTS_MARKER = '477897'

# Tour type to Viator category mapping
TOUR_TYPE_VIATOR_CATEGORY = {
    'cultural': 'cultural-historical',
    'adventure': 'adventure',
    'desert': 'desert-tours',
    'cruise': 'cruises-water-tours',
    'diving': 'water-sports',
    'religious': 'cultural-historical',
    'luxury': 'private-tours',
    'budget': 'day-trips',
}

# Egyptian cities with Viator destination IDs
CITY_VIATOR_IDS = {
    'cairo': 'd782',
    'luxor': 'd5413',
    'aswan': 'd5414',
    'hurghada': 'd5462',
    'sharm el sheikh': 'd5431',
    'alexandria': 'd5410',
    'giza': 'd782',  # Part of Cairo
}


class Command(BaseCommand):
    help = 'Populate affiliate URLs for all tours'

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
        """Normalize city name for lookups"""
        return city_name.lower().strip().replace(', egypt', '')

    def get_viator_destination_id(self, city_name):
        """Get Viator destination ID for a city"""
        city_key = self.get_city_key(city_name)
        for key, dest_id in CITY_VIATOR_IDS.items():
            if key in city_key or city_key in key:
                return dest_id
        return 'd782'  # Default to Cairo

    def generate_viator_search_url(self, tour):
        """
        Generate Viator affiliate search URL through Travelpayouts.

        Format: Travelpayouts redirect to Viator search
        """
        city_key = self.get_city_key(tour.departure_city)
        dest_id = self.get_viator_destination_id(tour.departure_city)

        # URL-encode the tour name for search
        search_query = quote_plus(tour.name)

        # Travelpayouts Viator affiliate link
        # Campaign ID 97 is for Viator tours
        viator_url = (
            f"https://tp.media/click?"
            f"shmarker={TRAVELPAYOUTS_MARKER}&"
            f"pression_mode=fix&"
            f"trs=262019&"
            f"campaign_id=97&"
            f"searchType=1&"
            f"city=Egypt&"
            f"q={search_query}"
        )

        return viator_url

    def generate_travelpayouts_tours_url(self, tour):
        """
        Generate Travelpayouts tours URL as fallback.
        """
        city_key = self.get_city_key(tour.departure_city)
        search_query = quote_plus(f"{tour.name} Egypt")

        # Generic Travelpayouts tours link
        url = (
            f"https://tp.media/click?"
            f"shmarker={TRAVELPAYOUTS_MARKER}&"
            f"pression_mode=fix&"
            f"trs=262019&"
            f"campaign_id=97&"
            f"searchType=1&"
            f"city={quote_plus(tour.departure_city)},Egypt"
        )

        return url

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        overwrite = options['overwrite']

        tours = Tour.objects.all()
        total = tours.count()
        updated = 0
        skipped = 0

        self.stdout.write(f"\nProcessing {total} tours...")
        self.stdout.write(f"Travelpayouts Marker: {TRAVELPAYOUTS_MARKER}")
        self.stdout.write(f"Dry run: {dry_run}")
        self.stdout.write(f"Overwrite existing: {overwrite}\n")

        for tour in tours:
            # Check if already has affiliate URL
            has_affiliate = bool(tour.viator_url or tour.travelpayouts_url)

            if has_affiliate and not overwrite:
                skipped += 1
                if options['verbosity'] >= 2:
                    self.stdout.write(f"  SKIP: {tour.name} (already has URL)")
                continue

            # Generate affiliate URLs
            viator_url = self.generate_viator_search_url(tour)
            tp_url = self.generate_travelpayouts_tours_url(tour)

            if dry_run:
                self.stdout.write(
                    f"  [DRY RUN] {tour.name} ({tour.departure_city})\n"
                    f"    -> Viator: {viator_url[:70]}...\n"
                    f"    -> TP: {tp_url[:70]}..."
                )
            else:
                # Update the tour
                tour.viator_url = viator_url
                tour.travelpayouts_url = tp_url

                # Set commission rate (Viator is typically 8%)
                if tour.commission_rate == 0:
                    tour.commission_rate = 8.0

                tour.save()

                self.stdout.write(
                    self.style.SUCCESS(f"  OK: {tour.name} ({tour.departure_city})")
                )

            updated += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(f"Total tours: {total}")
        self.stdout.write(f"Updated: {updated}")
        self.stdout.write(f"Skipped: {skipped}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nThis was a dry run. Run without --dry-run to apply changes.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"\nSuccessfully updated {updated} tours with affiliate URLs!")
            )

        # Show sample URLs
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("Sample affiliate URLs generated:\n")

        for tour in Tour.objects.all()[:3]:
            url = tour.viator_url if not dry_run else self.generate_viator_search_url(tour)
            self.stdout.write(f"\n{tour.name} ({tour.departure_city}):")
            self.stdout.write(f"  {url}")
