web: python manage.py migrate --noinput && gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
