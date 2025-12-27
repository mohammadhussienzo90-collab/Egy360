#!/usr/bin/env python
"""Startup script for Railway deployment"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

def run_migrations():
    """Run database migrations"""
    from django.core.management import call_command
    print("Running migrations...")
    call_command('migrate', '--noinput')
    print("Migrations complete.")

def ensure_site_exists():
    """Ensure the default Site object exists for django-allauth"""
    from django.contrib.sites.models import Site
    try:
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={'domain': '360egy.com', 'name': 'Egy360'}
        )
        if not created:
            site.domain = '360egy.com'
            site.name = 'Egy360'
            site.save()
        print(f"Site configured: {site.domain}")
    except Exception as e:
        print(f"Warning: Could not configure site: {e}")

if __name__ == '__main__':
    run_migrations()
    ensure_site_exists()
    print("Startup complete!")
