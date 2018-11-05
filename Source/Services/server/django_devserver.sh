#! /bin/bash
#pip install --no-cache-dir -r /care_adopt_backend/requirements.txt

cd /care_adopt_backend/

python -m venv backend_env

source backend_env/bin/activate

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
