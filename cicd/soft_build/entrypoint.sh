#!/bin/bash

echo "creating python env"

if [ -d "env" ] 
then
    echo "Python virtual environment exists." 
else
    python3 -m venv env
fi

source env/bin/activate

echo "upgrade pip"
python3 -m pip install --upgrade pip

pip3 install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

echo "restarting celery"
sudo supervisorctl restart all
echo "running server reload"

sudo systemctl daemon-reload & sudo systemctl restart gunicorn & sudo systemctl restart nginx
