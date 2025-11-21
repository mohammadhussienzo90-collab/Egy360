#!/usr/bin/env python
"""
One-time script to add affiliate fields to accommodations table
Run this with: railway run python fix_affiliate_fields.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Egy360.settings_production')
django.setup()

from django.db import connection

def add_affiliate_fields():
    with connection.cursor() as cursor:
        # Check if fields exist
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='accommodations_accommodation'
            AND column_name='booking_com_url';
        """)

        if cursor.fetchone():
            print("✅ Affiliate fields already exist!")
            return

        print("Adding affiliate fields...")

        # Add all affiliate fields
        fields_to_add = [
            ("booking_com_id", "VARCHAR(100)"),
            ("booking_com_url", "VARCHAR(500)"),
            ("agoda_url", "VARCHAR(500)"),
            ("hotels_com_url", "VARCHAR(500)"),
            ("direct_booking_url", "VARCHAR(500)"),
            ("commission_rate", "DECIMAL(5,2) DEFAULT 0"),
            ("total_bookings", "INTEGER DEFAULT 0"),
            ("total_commission_earned", "DECIMAL(10,2) DEFAULT 0"),
        ]

        for field_name, field_type in fields_to_add:
            try:
                cursor.execute(f"""
                    ALTER TABLE accommodations_accommodation
                    ADD COLUMN {field_name} {field_type};
                """)
                print(f"✅ Added {field_name}")
            except Exception as e:
                print(f"⚠️  {field_name}: {e}")

        print("\n🎉 Affiliate fields added successfully!")
        print("You can now add Booking.com links in the admin panel!")

if __name__ == '__main__':
    add_affiliate_fields()
