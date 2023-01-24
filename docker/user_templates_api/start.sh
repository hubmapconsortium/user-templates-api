#!/bin/bash

python manage.py migrate

gunicorn --bind=0.0.0.0:5001 --workers=8 user_templates_api.wsgi:application
