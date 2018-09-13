#! /bin/bash
#pip install --no-cache-dir -r /care_adopt_backend/requirements.txt

cd /care_adopt_backend/

source my_env/bin/activate

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
