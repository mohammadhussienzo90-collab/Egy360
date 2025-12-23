# core/management/commands/setup_site.py
"""
Set up Django Site with the correct domain for allauth
"""
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Set up Django Site with the correct domain'

    def handle(self, *args, **options):
        domain = '360egy.com'
        name = 'Egy360 - Egypt Travel Platform'

        site, created = Site.objects.update_or_create(
            id=1,
            defaults={
                'domain': domain,
                'name': name,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created site: {domain}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Updated site: {domain}'))
