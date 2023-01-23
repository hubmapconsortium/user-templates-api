#!/bin/bash

python manage.py migrate

# python manage.py qcluster

uvicorn --lifespan off --host 0.0.0.0 --port 5050 --workers 8 user_templates_api.asgi:application
