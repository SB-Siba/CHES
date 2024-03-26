#!/bin/bash


source env/bin/activate

python manage.py migrate
python manage.py collectstatic --noinput

echo "restarting celery"
sudo supervisorctl restart all
echo "running server reload"

sudo systemctl daemon-reload & sudo systemctl restart gunicorn & sudo systemctl restart nginx
