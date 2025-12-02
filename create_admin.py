#!/usr/bin/env python
"""
Create a new admin user
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

print(f"✅ Created superuser: {admin.username}")
print(f"✅ Password: Egypt360Admin")
print(f"✅ Login at: https://360egy.com/admin/")
