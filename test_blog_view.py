#!/usr/bin/env python
"""Test script to debug blog view issues"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client

print("="*60)
print("ENDPOINT DEBUG TEST")
print("="*60)

client = Client()

# Test various endpoints
endpoints = [
    '/health/',
    '/debug/',
    '/seed/?key=egy360seed',
    '/blog/',
]

for endpoint in endpoints:
    try:
        response = client.get(endpoint, follow=True)
        status = response.status_code
        length = len(response.content)
        print(f"\n{endpoint}")
        print(f"  Status: {status}")
        print(f"  Length: {length}")
        if status >= 400:
            content_preview = response.content.decode()[:300]
            print(f"  Preview: {content_preview}")
    except Exception as e:
        print(f"\n{endpoint}")
        print(f"  ERROR: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
