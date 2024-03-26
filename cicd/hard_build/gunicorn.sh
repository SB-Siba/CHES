#!/bin/bash

# entering to folder where the gunicorn socket and service is located
cd $jenkins_dir$pipeline_name/cicd/hard_build/gunicorn_setup_files/

# copying to inside /etc/systemd/system/
sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/


echo "$USER"
echo "$PWD"



sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

sudo systemctl status gunicorn.socket

file /run/gunicorn.sock

sudo journalctl -u gunicorn.socket
sudo systemctl status gunicorn


curl --unix-socket /run/gunicorn.sock localhost # it will return html code
sudo systemctl status gunicorn  # check status
sudo systemctl daemon-reload
sudo systemctl restart gunicorn