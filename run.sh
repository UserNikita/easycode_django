#!/usr/bin/env bash
sleep 5
python manage.py migrate &
python manage.py collectstatic &
python manage.py runserver 0.0.0.0:8000
#gunicorn wsgi:application --bind 0.0.0.0:8000