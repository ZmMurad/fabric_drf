#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
celery -A mailing_service worker --detach --loglevel=info --logfile=logs/celery.log
gunicorn -b 0.0.0.0:8000 mailing_service.wsgi:application

exec "$@"
