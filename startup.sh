#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Checking if database needs population..."
python manage.py populate_comprehensive_data || echo "Database already populated or error occurred"

echo "Creating superuser if needed..."
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'enzo.alihussien90@gmail.com', 'admin123'); print('Admin user ready')" || echo "Admin already exists"

echo "Starting Gunicorn..."
exec gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120
# Force redeploy
