#!/bin/bash

python manage.py migrate

nginx -g 'daemon off;' &

gunicorn --bind=0.0.0.0:5050 --workers=8 user_templates_api.wsgi:application
