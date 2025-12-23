#!/bin/bash
set -e

echo "Clearing Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "Running migrations..."
python manage.py migrate --noinput

echo "Setting up site domain for OAuth..."
python manage.py setup_site || echo "Site setup completed or error occurred"

echo "Fixing database schema and populating images..."
python manage.py fix_and_populate_images || echo "Database fix completed or already applied"

echo "Running standalone image population script..."
python populate_images_production.py || echo "Image population completed or error occurred"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if database needs population..."
python manage.py populate_comprehensive_data || echo "Database already populated or error occurred"

echo "Populating real Egyptian hotels..."
python manage.py populate_real_hotels || echo "Real hotels population completed or error occurred"

echo "Populating real Egyptian tours..."
python manage.py populate_real_tours || echo "Real tours population completed or error occurred"

echo "Populating blog content..."
python populate_blog_content.py || echo "Blog content population completed or error occurred"

echo "Populating affiliate URLs for accommodations..."
python manage.py populate_affiliate_urls || echo "Accommodation affiliate URLs completed or error occurred"

echo "Populating affiliate URLs for tours..."
python manage.py populate_tour_affiliate_urls || echo "Tour affiliate URLs completed or error occurred"

echo "Creating SEO blog posts..."
python manage.py create_seo_posts || echo "SEO blog posts completed or error occurred"

echo "Creating superuser..."
python create_superuser_production.py || echo "Superuser creation completed or already exists"

echo "Starting Gunicorn..."
exec gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
# Force redeploy - Dec 23 2024 - Security fixes and contact page
