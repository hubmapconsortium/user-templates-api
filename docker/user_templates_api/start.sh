#!/bin/bash

python manage.py migrate

uvicorn --lifespan off --host 0.0.0.0 --port 5001 --workers 8 user_templates_api.asgi:application
