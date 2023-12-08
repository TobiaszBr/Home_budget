#!/bin/bash

export PYTHONPATH="$PYTHONPATH:/home_budget/report_pdf"
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL
python manage.py runserver 0.0.0.0:8000
