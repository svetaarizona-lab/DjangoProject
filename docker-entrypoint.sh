#!/bin/sh

echo "Waiting for database..."

while ! nc -z db 5432; do
  sleep 1
done

echo "Database started"

python manage.py migrate

exec python manage.py runserver 0.0.0.0:8000