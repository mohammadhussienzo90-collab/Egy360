"""
Management command to validate data quality across all models.
Checks for missing required fields, invalid URLs, orphaned records, etc.
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from accommodations.models import Accommodation, Room
from tours.models import Tour, TourBooking
from destinations.models import City, Attraction
from bookings.models import Booking
import re


class Command(BaseCommand):
    help = 'Validate data quality across all models and report issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix issues where possible',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show all checked items, not just issues',
        )

    def validate_url(self, url):
        """Basic URL validation"""
        if not url:
            return False
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(url))

    def handle(self, *args, **options):
        fix_issues = options['fix']
        verbose = options['verbose']

        issues = []
        fixes = []

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("DATA VALIDATION REPORT")
        self.stdout.write("=" * 60 + "\n")

        # =================================================================
        # ACCOMMODATIONS
        # =================================================================
        self.stdout.write(self.style.HTTP_INFO("\n[ACCOMMODATIONS]"))

        accommodations = Accommodation.objects.all()
        acc_count = accommodations.count()
        self.stdout.write(f"Total accommodations: {acc_count}")

        # Check for missing required fields
        missing_name = accommodations.filter(Q(name='') | Q(name__isnull=True)).count()
        missing_city = accommodations.filter(Q(city='') | Q(city__isnull=True)).count()
        missing_price = accommodations.filter(Q(price_per_night__isnull=True) | Q(price_per_night=0)).count()
        missing_image = accommodations.filter(Q(image_url='') | Q(image_url__isnull=True)).count()
        missing_affiliate = accommodations.filter(Q(booking_com_url='') | Q(booking_com_url__isnull=True)).count()

        if missing_name:
            issues.append(f"Accommodations missing name: {missing_name}")
        if missing_city:
            issues.append(f"Accommodations missing city: {missing_city}")
        if missing_price:
            issues.append(f"Accommodations with no price: {missing_price}")
        if missing_image:
            issues.append(f"Accommodations missing image_url: {missing_image}")
        if missing_affiliate:
            issues.append(f"Accommodations missing affiliate URL: {missing_affiliate}")

        # Check for invalid URLs
        invalid_image_urls = 0
        invalid_affiliate_urls = 0
        for acc in accommodations:
            if acc.image_url and not self.validate_url(acc.image_url):
                invalid_image_urls += 1
            if acc.booking_com_url and not self.validate_url(acc.booking_com_url):
                invalid_affiliate_urls += 1

        if invalid_image_urls:
            issues.append(f"Accommodations with invalid image URLs: {invalid_image_urls}")
        if invalid_affiliate_urls:
            issues.append(f"Accommodations with invalid affiliate URLs: {invalid_affiliate_urls}")

        self.stdout.write(f"  - Missing name: {missing_name}")
        self.stdout.write(f"  - Missing city: {missing_city}")
        self.stdout.write(f"  - No price set: {missing_price}")
        self.stdout.write(f"  - Missing image: {missing_image}")
        self.stdout.write(f"  - Missing affiliate URL: {missing_affiliate}")
        self.stdout.write(f"  - Invalid image URLs: {invalid_image_urls}")
        self.stdout.write(f"  - Invalid affiliate URLs: {invalid_affiliate_urls}")

        # =================================================================
        # TOURS
        # =================================================================
        self.stdout.write(self.style.HTTP_INFO("\n[TOURS]"))

        tours = Tour.objects.all()
        tour_count = tours.count()
        self.stdout.write(f"Total tours: {tour_count}")

        # Check for missing required fields
        tours_missing_name = tours.filter(Q(name='') | Q(name__isnull=True)).count()
        tours_missing_price = tours.filter(Q(price_per_person__isnull=True) | Q(price_per_person=0)).count()
        tours_missing_image = tours.filter(Q(image_url='') | Q(image_url__isnull=True)).count()
        tours_missing_affiliate = tours.filter(
            Q(viator_url='') | Q(viator_url__isnull=True),
            Q(travelpayouts_url='') | Q(travelpayouts_url__isnull=True)
        ).count()

        if tours_missing_name:
            issues.append(f"Tours missing name: {tours_missing_name}")
        if tours_missing_price:
            issues.append(f"Tours with no price: {tours_missing_price}")
        if tours_missing_image:
            issues.append(f"Tours missing image: {tours_missing_image}")
        if tours_missing_affiliate:
            issues.append(f"Tours missing affiliate URL: {tours_missing_affiliate}")

        self.stdout.write(f"  - Missing name: {tours_missing_name}")
        self.stdout.write(f"  - No price set: {tours_missing_price}")
        self.stdout.write(f"  - Missing image: {tours_missing_image}")
        self.stdout.write(f"  - Missing affiliate URL: {tours_missing_affiliate}")

        # =================================================================
        # DESTINATIONS
        # =================================================================
        self.stdout.write(self.style.HTTP_INFO("\n[DESTINATIONS]"))

        cities = City.objects.all()
        city_count = cities.count()
        self.stdout.write(f"Total cities: {city_count}")

        cities_missing_image = cities.filter(Q(image_url='') | Q(image_url__isnull=True)).count()
        cities_missing_description = cities.filter(Q(description='') | Q(description__isnull=True)).count()

        if cities_missing_image:
            issues.append(f"Cities missing image: {cities_missing_image}")
        if cities_missing_description:
            issues.append(f"Cities missing description: {cities_missing_description}")

        self.stdout.write(f"  - Missing image: {cities_missing_image}")
        self.stdout.write(f"  - Missing description: {cities_missing_description}")

        attractions = Attraction.objects.all()
        attraction_count = attractions.count()
        self.stdout.write(f"Total attractions: {attraction_count}")

        # =================================================================
        # BOOKINGS
        # =================================================================
        self.stdout.write(self.style.HTTP_INFO("\n[BOOKINGS]"))

        bookings = Booking.objects.all()
        booking_count = bookings.count()
        self.stdout.write(f"Total bookings: {booking_count}")

        # Check for orphaned bookings (if content_type pattern is used)
        # Note: This depends on your booking model structure

        # =================================================================
        # ROOMS
        # =================================================================
        self.stdout.write(self.style.HTTP_INFO("\n[ROOMS]"))

        rooms = Room.objects.all()
        room_count = rooms.count()
        self.stdout.write(f"Total rooms: {room_count}")

        # Check for rooms with no accommodation
        orphaned_rooms = rooms.filter(accommodation__isnull=True).count()
        if orphaned_rooms:
            issues.append(f"Orphaned rooms (no accommodation): {orphaned_rooms}")
            self.stdout.write(f"  - Orphaned rooms: {orphaned_rooms}")

        # =================================================================
        # SUMMARY
        # =================================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("SUMMARY")
        self.stdout.write("=" * 60)

        if issues:
            self.stdout.write(self.style.WARNING(f"\nFound {len(issues)} issues:\n"))
            for i, issue in enumerate(issues, 1):
                self.stdout.write(f"  {i}. {issue}")
        else:
            self.stdout.write(self.style.SUCCESS("\nNo data quality issues found!"))

        # =================================================================
        # DATA STATISTICS
        # =================================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("DATA STATISTICS")
        self.stdout.write("=" * 60)

        self.stdout.write(f"\nAccommodations: {acc_count}")
        self.stdout.write(f"Tours: {tour_count}")
        self.stdout.write(f"Cities: {city_count}")
        self.stdout.write(f"Attractions: {attraction_count}")
        self.stdout.write(f"Rooms: {room_count}")
        self.stdout.write(f"Bookings: {booking_count}")

        # Accommodations with affiliate URLs
        with_affiliate = accommodations.exclude(
            Q(booking_com_url='') | Q(booking_com_url__isnull=True)
        ).count()
        self.stdout.write(f"\nAccommodations with affiliate URLs: {with_affiliate}/{acc_count} ({100*with_affiliate//max(acc_count,1)}%)")

        # Tours with affiliate URLs
        tours_with_affiliate = tours.exclude(
            Q(viator_url='') | Q(viator_url__isnull=True),
            Q(travelpayouts_url='') | Q(travelpayouts_url__isnull=True)
        ).count()
        self.stdout.write(f"Tours with affiliate URLs: {tours_with_affiliate}/{tour_count} ({100*tours_with_affiliate//max(tour_count,1)}%)")

        self.stdout.write("\n")

        if fix_issues:
            self.stdout.write(self.style.HTTP_INFO("\nAttempting to fix issues...\n"))
            # Run affiliate URL population
            from django.core.management import call_command

            self.stdout.write("Populating missing accommodation affiliate URLs...")
            call_command('populate_affiliate_urls', verbosity=0)

            self.stdout.write("Populating missing tour affiliate URLs...")
            call_command('populate_tour_affiliate_urls', verbosity=0)

            self.stdout.write(self.style.SUCCESS("\nFix commands executed. Run validation again to check results."))
