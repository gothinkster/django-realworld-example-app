#!/bin/bash


sed -i "s/DEBUG = True/DEBUG = $DRF_DEBUG_MODE/g" conduit/settings.py
sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = '$DRF_ALLOWED_HOSTS'.split(',')/g" conduit/settings.py

python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000