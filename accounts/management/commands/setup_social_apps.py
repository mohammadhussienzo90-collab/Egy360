"""
Management command to setup social authentication providers.
Usage:
    python manage.py setup_social_apps --provider google --client-id YOUR_ID --secret YOUR_SECRET
    python manage.py setup_social_apps --provider facebook --client-id YOUR_ID --secret YOUR_SECRET
    python manage.py setup_social_apps --provider apple --client-id YOUR_ID --secret YOUR_SECRET
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = 'Setup social authentication providers (Google, Facebook, Apple)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--provider',
            type=str,
            required=True,
            choices=['google', 'facebook', 'apple'],
            help='OAuth provider name'
        )
        parser.add_argument(
            '--client-id',
            type=str,
            required=True,
            help='OAuth Client ID (or App ID for Facebook)'
        )
        parser.add_argument(
            '--secret',
            type=str,
            required=True,
            help='OAuth Client Secret (or App Secret for Facebook)'
        )
        parser.add_argument(
            '--key',
            type=str,
            default='',
            help='Additional key (for Apple: Team ID)'
        )

    def handle(self, *args, **options):
        provider = options['provider']
        client_id = options['client_id']
        secret = options['secret']
        key = options['key']

        # Get or create the site
        site = Site.objects.get(id=1)

        # Provider display names
        provider_names = {
            'google': 'Google',
            'facebook': 'Facebook',
            'apple': 'Apple',
        }

        # Check if app already exists
        existing = SocialApp.objects.filter(provider=provider).first()
        if existing:
            existing.client_id = client_id
            existing.secret = secret
            existing.key = key
            existing.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated {provider_names[provider]} OAuth app')
            )
        else:
            app = SocialApp.objects.create(
                provider=provider,
                name=provider_names[provider],
                client_id=client_id,
                secret=secret,
                key=key,
            )
            app.sites.add(site)
            self.stdout.write(
                self.style.SUCCESS(f'Created {provider_names[provider]} OAuth app')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\nCallback URL: https://360egy.com/auth/{provider}/login/callback/')
        )
