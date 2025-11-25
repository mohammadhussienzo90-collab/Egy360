#!/usr/bin/env python
"""
Script to add hotel images from Unsplash to all accommodations
Run with: python add_hotel_images.py
"""
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings_production')
django.setup()

from accommodations.models import Accommodation

# Curated Unsplash hotel images (high quality, commercial use allowed)
HOTEL_IMAGES = [
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",  # Luxury hotel exterior
    "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",  # Hotel lobby
    "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80",  # Hotel room
    "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80",  # Resort pool
    "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",  # Beach resort
    "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",  # Boutique hotel
    "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=800&q=80",  # Hotel facade
    "https://images.unsplash.com/photo-1587874895560-4bcc8cee3d95?w=800&q=80",  # Modern hotel
    "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=800&q=80",  # Elegant hotel room
    "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80",  # Luxury suite
    "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800&q=80",  # Hotel pool view
    "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=800&q=80",  # Rooftop terrace
    "https://images.unsplash.com/photo-1596436889106-be35e843f974?w=800&q=80",  # Historic hotel
    "https://images.unsplash.com/photo-1559599238-1fd4f0e1c9e5?w=800&q=80",  # Resort exterior
    "https://images.unsplash.com/photo-1512918728675-ed5a9ecdebfd?w=800&q=80",  # Beachfront hotel
    "https://images.unsplash.com/photo-1455587734955-081b22074882?w=800&q=80",  # Hotel entrance
    "https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=800&q=80",  # Luxury bedroom
    "https://images.unsplash.com/photo-1584132915807-fd1f5fbc078f?w=800&q=80",  # Hotel balcony
    "https://images.unsplash.com/photo-1549294413-26f195200c16?w=800&q=80",  # Modern suite
    "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=800&q=80",  # Resort pool area
]

# Egypt-specific images for context
EGYPT_HOTEL_IMAGES = [
    "https://images.unsplash.com/photo-1539768942893-daf53e448371?w=800&q=80",  # Nile view
    "https://images.unsplash.com/photo-1572252009286-268acec5ca0a?w=800&q=80",  # Egyptian architecture
    "https://images.unsplash.com/photo-1553913861-c0fddf2619ee?w=800&q=80",  # Desert resort
    "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80",  # Red Sea resort
    "https://images.unsplash.com/photo-1583037189850-1921ae7c6c22?w=800&q=80",  # Cairo hotel view
]

def assign_images():
    """Assign images to hotels based on location and type"""
    accommodations = Accommodation.objects.filter(image_url='')

    if not accommodations.exists():
        print("✅ All accommodations already have images!")
        return

    print(f"Found {accommodations.count()} accommodations without images")

    # Combine all images
    all_images = HOTEL_IMAGES + EGYPT_HOTEL_IMAGES

    updated_count = 0
    for accommodation in accommodations:
        # Assign image based on hotel characteristics
        if 'nile' in accommodation.name.lower() or 'cairo' in accommodation.city.lower():
            # Prioritize Nile/Cairo images
            image_pool = EGYPT_HOTEL_IMAGES + HOTEL_IMAGES
        elif 'beach' in accommodation.name.lower() or 'red sea' in accommodation.description.lower():
            # Beach/resort images
            image_pool = [img for img in HOTEL_IMAGES if any(word in img for word in ['beach', 'pool', 'resort'])] + HOTEL_IMAGES
        elif accommodation.star_rating and accommodation.star_rating >= 4:
            # Luxury images for 4-5 star hotels
            image_pool = HOTEL_IMAGES[:10] + EGYPT_HOTEL_IMAGES
        else:
            # General pool
            image_pool = all_images

        # Assign random image from pool
        accommodation.image_url = random.choice(image_pool)
        accommodation.save()
        updated_count += 1
        print(f"✅ Updated: {accommodation.name} - {accommodation.city}")

    print(f"\n🎉 Successfully added images to {updated_count} accommodations!")
    print("Images are from Unsplash (free for commercial use)")

if __name__ == '__main__':
    print("Adding hotel images from Unsplash...\n")
    assign_images()
