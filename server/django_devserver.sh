#! /bin/bash
python /care_adopt_backend/manage.py migrate --noinput
python /care_adopt_backend/manage.py runserver 0.0.0.0:8000
