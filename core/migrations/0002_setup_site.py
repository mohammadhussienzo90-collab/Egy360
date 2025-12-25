# Generated migration to ensure Site is properly configured
from django.db import migrations


def setup_site(apps, schema_editor):
    """Ensure Site model is configured with correct domain"""
    Site = apps.get_model('sites', 'Site')

    # Update or create site with ID=1
    site, created = Site.objects.update_or_create(
        id=1,
        defaults={
            'domain': '360egy.com',
            'name': 'Egy360 Travel'
        }
    )


def reverse_setup_site(apps, schema_editor):
    """Reverse the site setup"""
    pass  # Don't delete, just leave as is


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_affiliate_tracking'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.RunPython(setup_site, reverse_setup_site),
    ]
