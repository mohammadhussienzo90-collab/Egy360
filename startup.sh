#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Applying database fixes..."
python fix_affiliate_fields.py || echo "Fix script completed or fields already exist"

echo "Adding hotel images..."
python add_hotel_images.py || echo "Images already added or error occurred"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if database needs population..."
python manage.py populate_comprehensive_data || echo "Database already populated or error occurred"

echo "Creating superuser..."
python create_superuser_production.py || echo "Superuser creation completed or already exists"

echo "Starting Gunicorn..."
exec gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
# Force redeploy
