#!/usr/bin/env python
"""
Create a new admin user - reads password from environment variable
"""
import os
import sys
import secrets
import string
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings_production')
django.setup()

from django.contrib.auth.models import User


def generate_secure_password(length=16):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


# Get password from environment or generate a secure one
password = os.environ.get('ADMIN_PASSWORD')

if not password:
    password = generate_secure_password()
    print("⚠️  No ADMIN_PASSWORD environment variable set.")
    print("    Generated a secure random password.")

# Delete existing admin if exists
User.objects.filter(username='admin').delete()

# Create new admin
admin = User.objects.create_superuser(
    username='admin',
    email='admin@360egy.com',
    password=password
)

print("=" * 70)
print("✅ Created superuser successfully!")
print("=" * 70)
print(f"Username: {admin.username}")
print(f"Email: {admin.email}")
print(f"Password: {password}")
print("")
print("⚠️  IMPORTANT: Save this password securely and delete it from terminal history!")
print("    Login at: https://360egy.com/admin/")
print("=" * 70)
