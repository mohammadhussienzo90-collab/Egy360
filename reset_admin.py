#!/usr/bin/env python
"""
Reset admin password using Django
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Simple approach - just update the password using Django ORM
# But this won't work because we can't connect locally

# Instead, let's just print the properly hashed password
password = "Egypt360Admin"
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
print("=" * 70)
