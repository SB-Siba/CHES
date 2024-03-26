#!/bin/bash

sudo apt-get install -y redis-server
echo "redis install done"

sudo apt-get install supervisor
echo "supervisor install done"


jenkins_dir_escaped=$(echo "$jenkins_dir$pipeline_name" | sed 's/\//\\\//g')


cd $jenkins_dir$pipeline_name/cicd/hard_build/

# delete existing celery celery_worker.conf
sudo rm -rf celery_worker.conf

# creating new celery_worker.conf

sed -e "s/{{working_dir}}/$jenkins_dir_escaped/g" \
    -e "s/{{django_project_name}}/$django_project_name/g" \
    -e "s/{{ubuntu_user}}/$ubuntu_user_name/g" celery_worker_template.conf > celery_worker.conf

sudo cp -r celery_worker.conf /etc/supervisor/conf.d/

echo "some more commands"

sudo systemctl status supervisor

sudo supervisorctl update
sudo supervisorctl restart celery-default
sudo supervisorctl status celery-default