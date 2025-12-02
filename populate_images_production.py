#!/usr/bin/env python
"""
Standalone script to populate accommodation images on production.
Can be run via: railway run python populate_images_production.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings')
django.setup()

from accommodations.models import Accommodation

# High-quality hotel images from Unsplash
hotel_images = [
    'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',
    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400',
    'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400',
    'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400',
    'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400',
    'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400',
    'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400',
    'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400',
    'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400',
    'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400',
]

print("=" * 70)
print("POPULATING ACCOMMODATION IMAGES")
print("=" * 70)

accommodations = Accommodation.objects.all()
updated_count = 0

for i, acc in enumerate(accommodations):
    try:
        # Always set image_url, even if it exists (to ensure all have images)
        image_url = hotel_images[i % len(hotel_images)]
        acc.image_url = image_url
        acc.save(update_fields=['image_url'])
        updated_count += 1
        print(f"[{updated_count}/{accommodations.count()}] {acc.name}: {image_url}")
    except Exception as e:
        print(f"[ERROR] Failed to update {acc.name}: {e}")

print()
print("=" * 70)
print(f"SUCCESS! Updated {updated_count} out of {accommodations.count()} accommodations")
print("=" * 70)
