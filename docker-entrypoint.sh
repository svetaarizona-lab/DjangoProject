#!/bin/sh

echo "Waiting for database..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

python manage.py migrate

python manage.py collectstatic --noinput

exec gunicorn shopbook.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3