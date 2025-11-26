#!/usr/bin/env python
"""
Create superuser for production - to be run on Railway server
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings_production')
django.setup()

from django.contrib.auth.models import User

# Delete existing admin if exists
User.objects.filter(username='admin').delete()

# Create new admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@360egy.com',
    password='Egypt360Admin'
)

print("=" * 70)
print("✅ SUPERUSER CREATED SUCCESSFULLY!")
print("=" * 70)
print(f"Username: {admin.username}")
print(f"Email: {admin.email}")
print(f"Password: Egypt360Admin")
print(f"Login URL: https://360egy.com/admin/")
print("=" * 70)
