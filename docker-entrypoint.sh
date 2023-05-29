#!/bin/sh

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Make database migrations"
python manage.py makemigrations

echo "Apply database migrations"
python manage.py migrate

echo "Run initial_script.py"
python ./utils/initial_script.py

gunicorn --bind 0.0.0.0:8080 delivery_service.wsgi:application
