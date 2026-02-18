"""
Management command: refresh_social_tokens

Refreshes OAuth access tokens for social accounts that are expiring
soon (within 24 hours) or all active accounts when --force is used.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone

from social_poster.models import SocialAccount, SocialPostLog
from social_poster.platforms import get_client


class Command(BaseCommand):
    help = (
        'Refresh expiring OAuth tokens for active social accounts. '
        'By default only refreshes tokens expiring within 24 hours; '
        'use --force to refresh all active accounts.'
    )

    # ------------------------------------------------------------------
    # Arguments
    # ------------------------------------------------------------------
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Refresh tokens for ALL active accounts, not just expiring ones.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview which accounts would be refreshed without making changes.',
        )

    # ------------------------------------------------------------------
    # Main handler
    # ------------------------------------------------------------------
    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN -- no tokens will be refreshed.\n'))

        accounts = SocialAccount.objects.filter(is_active=True)

        total_checked = 0
        total_refreshed = 0
        total_skipped = 0
        total_errors = 0

        # Create audit log (unless dry-run)
        log = None
        if not dry_run:
            log = SocialPostLog.objects.create(
                log_type='refresh',
                status='running',
                details={'force': force},
            )

        for account in accounts:
            total_checked += 1

            # Decide whether this account needs a refresh
            needs_refresh = force or account.token_expires_soon
            if not needs_refresh:
                total_skipped += 1
                self.stdout.write(
                    f'[{account.platform}] {account.account_name} -- '
                    f'token OK, skipping.'
                )
                continue

            if dry_run:
                expiry_str = (
                    account.token_expiry.strftime('%Y-%m-%d %H:%M')
                    if account.token_expiry else 'no expiry set'
                )
                self.stdout.write(
                    f'  [DRY RUN] [{account.platform}] {account.account_name} -- '
                    f'would refresh (expires: {expiry_str})'
                )
                total_refreshed += 1
                continue

            try:
                client = get_client(account)
                token_data = client.refresh_access_token()

                # Update account with new tokens
                if isinstance(token_data, dict):
                    if 'access_token' in token_data:
                        account.access_token = token_data['access_token']
                    if 'refresh_token' in token_data:
                        account.refresh_token = token_data['refresh_token']
                    if 'token_expiry' in token_data:
                        account.token_expiry = token_data['token_expiry']
                    elif 'expires_in' in token_data:
                        account.token_expiry = timezone.now() + timezone.timedelta(
                            seconds=int(token_data['expires_in'])
                        )
                else:
                    # If the client returns a raw token string
                    account.access_token = str(token_data)

                account.save()

                total_refreshed += 1
                self.stdout.write(self.style.SUCCESS(
                    f'[{account.platform}] {account.account_name} -- token refreshed '
                    f'(new expiry: {account.token_expiry})'
                ))

            except Exception as exc:
                total_errors += 1
                msg = (
                    f'[{account.platform}] {account.account_name} -- '
                    f'refresh failed: {exc}'
                )
                self.stdout.write(self.style.ERROR(msg))
                if log:
                    log.add_error(msg)

        # Finalise audit log
        if log:
            log.posts_processed = total_checked
            log.posts_succeeded = total_refreshed
            log.posts_failed = total_errors
            final_status = 'success'
            if total_errors and total_refreshed:
                final_status = 'partial'
            elif total_errors and not total_refreshed:
                final_status = 'failed'
            log.mark_complete(status=final_status)

        # Print summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== Token Refresh Summary ==='))
        self.stdout.write(f'  Accounts checked:  {total_checked}')
        self.stdout.write(f'  Skipped (OK):      {total_skipped}')
        self.stdout.write(self.style.SUCCESS(f'  Refreshed:         {total_refreshed}'))
        if total_errors:
            self.stdout.write(self.style.ERROR(f'  Errors:            {total_errors}'))
        else:
            self.stdout.write(f'  Errors:            {total_errors}')
