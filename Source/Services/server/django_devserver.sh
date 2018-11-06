#! /bin/bash

echo Creating Virtual Environment

cd /care_adopt_backend/

python -m venv backend_env

source backend_env/bin/activate

echo Installing requirements
pip install -r requirements.txt

echo Running server on port 8000
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000