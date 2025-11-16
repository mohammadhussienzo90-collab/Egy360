web: gunicorn Egy360.wsgi --log-file - --workers 3 --timeout 120
worker: celery -A Egy360 worker --loglevel=info
beat: celery -A Egy360 beat --loglevel=info
