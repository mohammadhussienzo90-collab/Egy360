#!/bin/bash
# Startup script for Railway deployment
# Don't use set -e as we want to continue even if some commands fail

echo "=== Starting Egy360 Deployment ==="

echo "1. Running migrations..."
python manage.py migrate --noinput || { echo "Migration failed"; exit 1; }

echo "2. Creating cache table..."
python manage.py createcachetable 2>/dev/null || echo "Cache table already exists or not needed"

echo "3. Setting up site domain..."
python manage.py setup_site 2>/dev/null || echo "Site setup skipped"

echo "4. Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed"; exit 1; }

echo "5. Running data population (optional steps)..."
python manage.py fix_and_populate_images 2>/dev/null || true
python manage.py populate_comprehensive_data 2>/dev/null || true
python manage.py populate_real_hotels 2>/dev/null || true
python manage.py populate_real_tours 2>/dev/null || true
python manage.py populate_transportation 2>/dev/null || true
python manage.py populate_affiliate_urls 2>/dev/null || true
python manage.py populate_tour_affiliate_urls 2>/dev/null || true
python manage.py create_seo_posts 2>/dev/null || true

echo "6. Creating superuser..."
python create_superuser_production.py 2>/dev/null || echo "Superuser exists or creation skipped"

echo "=== Starting Gunicorn Server ==="
exec gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
