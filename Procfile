web: gunicorn wsgi.wsgi --timeout 3000 --keep-alive 200 --log-file - 
worker: celery -A apps.helpers worker -l info -B