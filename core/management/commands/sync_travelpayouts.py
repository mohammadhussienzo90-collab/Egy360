"""
Daily Travelpayouts sync command.

This command updates all affiliate URLs and logs the results.
Designed to run as a scheduled cron job (daily at 3 AM).

Usage:
    python manage.py sync_travelpayouts
    python manage.py sync_travelpayouts --force

Railway Cron: 0 3 * * *
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from django.db.models import Q
from io import StringIO
import traceback


class Command(BaseCommand):
    help = 'Sync all Travelpayouts affiliate URLs and log results'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update all URLs (overwrite existing)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--no-log',
            action='store_true',
            help='Do not create DataSyncLog entry',
        )

    def handle(self, *args, **options):
        from core.models import DataSyncLog
        from accommodations.models import Accommodation
        from tours.models import Tour

        force = options['force']
        dry_run = options['dry_run']
        no_log = options['no_log']

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("TRAVELPAYOUTS DAILY SYNC")
        self.stdout.write(f"Started at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write("=" * 60 + "\n")

        # Create sync log entry
        sync_log = None
        if not no_log and not dry_run:
            sync_log = DataSyncLog.objects.create(
                sync_type='travelpayouts',
                status='running',
                details={
                    'force': force,
                    'started_by': 'management_command'
                }
            )

        errors = []
        acc_before = 0
        acc_after = 0
        tours_before = 0
        tours_after = 0

        try:
            # =================================================================
            # ACCOMMODATION AFFILIATE URLs
            # =================================================================
            self.stdout.write(self.style.HTTP_INFO("[1/2] Updating Accommodation Affiliate URLs..."))

            # Count accommodations with affiliate URLs before
            acc_before = Accommodation.objects.exclude(
                Q(booking_com_url='') | Q(booking_com_url__isnull=True)
            ).count()

            # Capture output
            out = StringIO()
            try:
                if force:
                    call_command('populate_affiliate_urls', '--overwrite', stdout=out, verbosity=0)
                else:
                    call_command('populate_affiliate_urls', stdout=out, verbosity=0)
            except Exception as e:
                errors.append(f"Accommodation URL update failed: {str(e)}")
                self.stdout.write(self.style.ERROR(f"  Error: {e}"))

            # Count after
            acc_after = Accommodation.objects.exclude(
                Q(booking_com_url='') | Q(booking_com_url__isnull=True)
            ).count()

            acc_updated = acc_after - acc_before if not force else acc_after
            self.stdout.write(f"  Accommodations with affiliate URLs: {acc_after}")
            self.stdout.write(f"  New URLs added: {max(0, acc_updated)}")

            # =================================================================
            # TOUR AFFILIATE URLs
            # =================================================================
            self.stdout.write(self.style.HTTP_INFO("\n[2/2] Updating Tour Affiliate URLs..."))

            # Count tours with affiliate URLs before
            tours_before = Tour.objects.exclude(
                Q(viator_url='') | Q(viator_url__isnull=True),
                Q(travelpayouts_url='') | Q(travelpayouts_url__isnull=True)
            ).count()

            # Capture output
            out = StringIO()
            try:
                if force:
                    call_command('populate_tour_affiliate_urls', '--overwrite', stdout=out, verbosity=0)
                else:
                    call_command('populate_tour_affiliate_urls', stdout=out, verbosity=0)
            except Exception as e:
                errors.append(f"Tour URL update failed: {str(e)}")
                self.stdout.write(self.style.ERROR(f"  Error: {e}"))

            # Count after
            tours_after = Tour.objects.exclude(
                Q(viator_url='') | Q(viator_url__isnull=True),
                Q(travelpayouts_url='') | Q(travelpayouts_url__isnull=True)
            ).count()

            tours_updated = tours_after - tours_before if not force else tours_after
            self.stdout.write(f"  Tours with affiliate URLs: {tours_after}")
            self.stdout.write(f"  New URLs added: {max(0, tours_updated)}")

        except Exception as e:
            errors.append(f"Sync failed: {str(e)}\n{traceback.format_exc()}")
            self.stdout.write(self.style.ERROR(f"\nCritical error: {e}"))

        # =================================================================
        # UPDATE SYNC LOG
        # =================================================================
        if sync_log:
            total_processed = Accommodation.objects.count() + Tour.objects.count()
            total_updated = (acc_after - acc_before) + (tours_after - tours_before)

            sync_log.records_processed = total_processed
            sync_log.records_updated = max(0, total_updated) if not force else (acc_after + tours_after)
            sync_log.records_failed = len(errors)
            sync_log.errors = [{'message': e, 'timestamp': timezone.now().isoformat()} for e in errors]
            sync_log.details.update({
                'accommodations_with_urls': acc_after,
                'tours_with_urls': tours_after,
                'force_update': force,
            })

            if errors:
                sync_log.mark_complete('partial' if (acc_after > 0 or tours_after > 0) else 'failed')
            else:
                sync_log.mark_complete('success')

        # =================================================================
        # SUMMARY
        # =================================================================
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("SYNC COMPLETE")
        self.stdout.write("=" * 60)

        self.stdout.write(f"\nCompleted at: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.stdout.write(f"Accommodations with affiliate URLs: {acc_after}")
        self.stdout.write(f"Tours with affiliate URLs: {tours_after}")

        if errors:
            self.stdout.write(self.style.WARNING(f"\nErrors encountered: {len(errors)}"))
            for error in errors:
                self.stdout.write(f"  - {error[:100]}")
        else:
            self.stdout.write(self.style.SUCCESS("\nSync completed successfully!"))

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY RUN] No changes were made."))

        self.stdout.write("")
