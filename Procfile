web: python manage.py collectstatic --noinput && gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
