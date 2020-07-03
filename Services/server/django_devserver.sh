#! /bin/bash

echo Creating Virtual Environment

cd /care_adopt_backend/

python -m venv backend_env

source backend_env/bin/activate

echo Installing requirements
pip install -r requirements.txt

echo Running server on port 8000
python manage.py migrate --noinput

echo Running celery
celery worker -A care_adopt_backend -D -l info
celery beat -A care_adopt_backend --detach -l info

echo Start rebuild
echo "y" | python manage.py rebuild_index

echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$ADMIN_USER', '$ADMIN_PASS')" | python manage.py shell
python manage.py runserver 0.0.0.0:8000