#!/bin/bash

jenkins_dir_escaped=$(echo "$jenkins_dir$pipeline_name" | sed 's/\//\\\//g')
cd $jenkins_dir_escaped

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

if [ -d "media" ] 
then
    echo "media folder exists." 
else
    mkdir media
    sudo chmod -R 777 media
fi

if [ -d "logs" ] 
then
    echo "Log folder exists." 
else
    mkdir logs
    touch logs/error.log logs/access.log
fi

echo "user is : $USER"

sudo chmod -R 777 logs

