"""
Management command: setup_social_account

Creates or updates a SocialAccount from environment variables or CLI args.
Designed for Railway deployment where tokens are stored as env vars.

Usage examples:
  # Facebook (reads from env vars SOCIAL_FB_PAGE_TOKEN, SOCIAL_FB_PAGE_ID, etc.)
  python manage.py setup_social_account facebook

  # Instagram (shares Facebook credentials)
  python manage.py setup_social_account instagram

  # With explicit token override
  python manage.py setup_social_account facebook --token "EAA..."

  # Show current account status
  python manage.py setup_social_account --status
"""

import os

from django.core.management.base import BaseCommand

from social_poster.models import SocialAccount


# Environment variable mapping per platform
ENV_MAP = {
    'facebook': {
        'token': 'SOCIAL_FB_PAGE_TOKEN',
        'page_id': 'SOCIAL_FB_PAGE_ID',
        'app_id': 'SOCIAL_FACEBOOK_APP_ID',
        'app_secret': 'SOCIAL_FACEBOOK_APP_SECRET',
        'account_name': '360egy.com Facebook Page',
    },
    'instagram': {
        'token': 'SOCIAL_FB_PAGE_TOKEN',      # Same token as Facebook
        'ig_user_id': 'SOCIAL_IG_USER_ID',
        'page_id': 'SOCIAL_FB_PAGE_ID',        # Needed for IG publishing
        'app_id': 'SOCIAL_FACEBOOK_APP_ID',
        'app_secret': 'SOCIAL_FACEBOOK_APP_SECRET',
        'account_name': '360egy.com Instagram',
    },
    'pinterest': {
        'token': 'PINTEREST_ACCESS_TOKEN',
        'refresh_token': 'PINTEREST_REFRESH_TOKEN',
        'app_id': 'PINTEREST_APP_ID',
        'app_secret': 'PINTEREST_APP_SECRET',
        'board_id': 'PINTEREST_BOARD_ID',
        'account_name': '360egy Pinterest',
    },
}


class Command(BaseCommand):
    help = (
        'Create or update a SocialAccount from environment variables. '
        'Use --status to view all configured accounts.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'platform',
            nargs='?',
            choices=['facebook', 'instagram', 'pinterest'],
            help='Platform to set up.',
        )
        parser.add_argument(
            '--token',
            type=str,
            default=None,
            help='Override access token (instead of reading from env var).',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show status of all configured social accounts.',
        )

    def handle(self, *args, **options):
        if options['status']:
            return self._show_status()

        platform = options['platform']
        if not platform:
            self.stdout.write(self.style.ERROR(
                'Please specify a platform: facebook, instagram, or pinterest'
            ))
            return

        env = ENV_MAP[platform]

        # Get access token
        token = options['token'] or os.environ.get(env['token'], '')
        if not token:
            self.stdout.write(self.style.ERROR(
                f'No access token found. Set {env["token"]} env var or use --token.'
            ))
            return

        # Build platform_metadata
        metadata = {}

        if platform == 'facebook':
            metadata['page_id'] = os.environ.get(env['page_id'], '')
            metadata['app_id'] = os.environ.get(env['app_id'], '')
            metadata['app_secret'] = os.environ.get(env['app_secret'], '')
            account_id = metadata['page_id']

        elif platform == 'instagram':
            metadata['ig_user_id'] = os.environ.get(env['ig_user_id'], '')
            metadata['page_id'] = os.environ.get(env['page_id'], '')
            metadata['app_id'] = os.environ.get(env['app_id'], '')
            metadata['app_secret'] = os.environ.get(env['app_secret'], '')
            account_id = metadata['ig_user_id']

        elif platform == 'pinterest':
            metadata['board_id'] = os.environ.get(env.get('board_id', ''), '')
            metadata['app_id'] = os.environ.get(env['app_id'], '')
            metadata['app_secret'] = os.environ.get(env['app_secret'], '')
            account_id = metadata.get('board_id', '')

        # Create or update the account
        account, created = SocialAccount.objects.update_or_create(
            platform=platform,
            defaults={
                'account_name': env['account_name'],
                'account_id': account_id,
                'platform_metadata': metadata,
                'is_active': True,
            },
        )

        # Set encrypted token via the property setter
        account.access_token = token
        if platform == 'pinterest':
            refresh_tok = os.environ.get(env.get('refresh_token', ''), '')
            if refresh_tok:
                account.refresh_token = refresh_tok
        account.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(
            f'{action} {platform} account: {account.account_name}'
        ))
        self.stdout.write(f'  Account ID: {account_id or "(not set)"}')
        self.stdout.write(f'  Token: {"***" + token[-8:] if len(token) > 8 else "(set)"}')
        self.stdout.write(f'  Metadata keys: {list(metadata.keys())}')
        self.stdout.write(f'  Active: {account.is_active}')

    def _show_status(self):
        accounts = SocialAccount.objects.all()

        if not accounts.exists():
            self.stdout.write(self.style.WARNING('No social accounts configured yet.'))
            self.stdout.write('')
            self.stdout.write('To set up an account:')
            self.stdout.write('  python manage.py setup_social_account facebook --token "EAA..."')
            self.stdout.write('')
            self.stdout.write('Required env vars for Facebook/Instagram:')
            self.stdout.write('  SOCIAL_FB_PAGE_TOKEN  - Page access token')
            self.stdout.write('  SOCIAL_FB_PAGE_ID     - Facebook Page ID')
            self.stdout.write('  SOCIAL_IG_USER_ID     - Instagram Business User ID')
            self.stdout.write('  SOCIAL_FACEBOOK_APP_ID     - Facebook App ID')
            self.stdout.write('  SOCIAL_FACEBOOK_APP_SECRET - Facebook App Secret')
            return

        self.stdout.write(self.style.SUCCESS('=== Social Accounts ==='))
        for acc in accounts:
            has_token = bool(acc.access_token_encrypted)
            status_style = self.style.SUCCESS if acc.is_active and has_token else self.style.WARNING

            self.stdout.write(status_style(
                f'\n  [{acc.platform.upper()}] {acc.account_name}'
            ))
            self.stdout.write(f'    Active:    {acc.is_active}')
            self.stdout.write(f'    Token:     {"Set" if has_token else "MISSING"}')
            self.stdout.write(f'    Account ID: {acc.account_id or "(not set)"}')
            if acc.token_expiry:
                self.stdout.write(f'    Expiry:    {acc.token_expiry}')
            if acc.last_used_at:
                self.stdout.write(f'    Last used: {acc.last_used_at}')
            if acc.platform_metadata:
                self.stdout.write(f'    Metadata:  {list(acc.platform_metadata.keys())}')
