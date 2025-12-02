from django.core.management.base import BaseCommand
from django.db import connection
from accommodations.models import Accommodation


class Command(BaseCommand):
    help = 'Force-fix database schema and populate accommodation images'

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.WARNING("FIXING DATABASE SCHEMA AND POPULATING IMAGES"))
        self.stdout.write("=" * 70)

        # Step 1: Fix database schema
        self.stdout.write("\n1. Checking database schema...")

        # Detect database type
        db_engine = connection.settings_dict['ENGINE']
        is_postgres = 'postgresql' in db_engine

        with connection.cursor() as cursor:
            # Check if columns exist - different queries for PostgreSQL vs SQLite
            existing_columns = []

            if is_postgres:
                cursor.execute("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='accommodations_accommodation'
                    AND column_name IN ('image_url', 'booking_com_id', 'agoda_url', 'expedia_url', 'tripadvisor_url')
                """)
                existing_columns = [row[0] for row in cursor.fetchall()]
            else:
                # SQLite - use PRAGMA
                cursor.execute("PRAGMA table_info(accommodations_accommodation)")
                existing_columns = [row[1] for row in cursor.fetchall()]

            self.stdout.write(f"   Database: {'PostgreSQL' if is_postgres else 'SQLite'}")
            self.stdout.write(f"   Found {len(existing_columns)} columns")

            # Add missing columns
            columns_to_add = {
                'image_url': 'VARCHAR(500)',
                'booking_com_id': 'VARCHAR(100)',
                'agoda_url': 'VARCHAR(500)',
                'expedia_url': 'VARCHAR(500)',
                'tripadvisor_url': 'VARCHAR(500)'
            }

            for col_name, col_type in columns_to_add.items():
                if col_name not in existing_columns:
                    self.stdout.write(f"   Adding column: {col_name}")
                    try:
                        cursor.execute(f"""
                            ALTER TABLE accommodations_accommodation
                            ADD COLUMN {col_name} {col_type} NULL
                        """)
                        self.stdout.write(self.style.SUCCESS(f"   [OK] Added {col_name}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"   [ERROR] Error adding {col_name}: {e}"))
                else:
                    self.stdout.write(f"   [OK] Column {col_name} already exists")
        
        # Step 2: Populate images
        self.stdout.write("\n2. Populating accommodation images...")
        
        # High-quality hotel images from Unsplash
        hotel_images = [
            'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400',  # Luxury hotel
            'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400',  # Hotel lobby
            'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400',  # Beach resort
            'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400',  # Modern hotel
            'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400',  # Hotel exterior
            'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400',  # Pool hotel
            'https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400',  # Resort
            'https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400',  # Boutique hotel
            'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400',  # City hotel
            'https://images.unsplash.com/photo-1571003123894-1f0594d2b5d9?w=400',  # Hotel room
        ]
        
        accommodations = Accommodation.objects.all()
        updated_count = 0
        
        for i, acc in enumerate(accommodations):
            if not acc.image_url:
                # Cycle through images
                image_url = hotel_images[i % len(hotel_images)]
                acc.image_url = image_url
                acc.save(update_fields=['image_url'])
                updated_count += 1
                self.stdout.write(f"   [OK] {acc.name}: {image_url}")

        self.stdout.write(self.style.SUCCESS(f"\n[OK] Updated {updated_count} accommodations with images"))
        self.stdout.write(self.style.SUCCESS(f"[OK] Total accommodations: {accommodations.count()}"))
        
        self.stdout.write("\n" + "=" * 70)
        self.stdout.write(self.style.SUCCESS("DATABASE FIX AND IMAGE POPULATION COMPLETE!"))
        self.stdout.write("=" * 70)
