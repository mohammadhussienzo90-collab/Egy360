#!/bin/bash
set -e

echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Fixing database schema and populating images..."
python manage.py fix_and_populate_images || echo "Database fix completed or already applied"

echo "Running standalone image population script..."
python populate_images_production.py || echo "Image population completed or error occurred"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if database needs population..."
python manage.py populate_comprehensive_data || echo "Database already populated or error occurred"

echo "Creating superuser..."
python create_superuser_production.py || echo "Superuser creation completed or already exists"

echo "Starting Gunicorn..."
exec gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
# Force redeploy - Dec 2 2025 - fix images
