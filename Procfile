release: python manage.py migrate --noinput
web: gunicorn Egy360.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
