#!/usr/bin/env python
"""
Reset admin password using Django - reads password from environment or generates one
Usage: ADMIN_PASSWORD=your_password python reset_admin.py
"""
import os
import secrets
import string
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


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

hashed = make_password(password)

print("=" * 70)
print("ADMIN PASSWORD RESET - SQL COMMAND")
print("=" * 70)
print("\nCopy this ENTIRE SQL command and run it in Railway Data tab:\n")
print("-" * 70)
print(f"""
UPDATE auth_user
SET password = '{hashed}'
WHERE username = 'admin';
""")
print("-" * 70)
print("\nAfter running the SQL command, login with:")
print("URL: https://360egy.com/admin/")
print("Username: admin")
print(f"Password: {password}")
print("")
print("⚠️  IMPORTANT: Save this password securely!")
print("    Clear your terminal history after saving the password.")
print("=" * 70)
