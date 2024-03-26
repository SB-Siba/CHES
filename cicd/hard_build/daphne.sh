#!/bin/bash

echo "-------------------Woring on Daphne setup---------------------"


jenkins_dir_escaped=$(echo "$jenkins_dir$pipeline_name" | sed 's/\//\\\//g')


cd $jenkins_dir$pipeline_name/cicd/hard_build/

# delete existing celery celery_worker.conf
sudo rm -rf daphne_worker.conf

# creating new celery_worker.conf

sed -e "s/{{working_dir}}/$jenkins_dir_escaped/g" \
    -e "s/{{django_project_name}}/$django_project_name/g" \
    -e "s/{{ubuntu_user}}/$ubuntu_user_name/g" daphne_worker_template.conf > daphne_worker.conf

sudo cp -r daphne_worker.conf /etc/supervisor/conf.d/

echo "some more commands"

sudo supervisorctl update
sudo supervisorctl restart daphne
sudo supervisorctl status daphne
