#!/bin/bash

cd $jenkins_dir$pipeline_name/cicd/hard_build

# deleteing existing myproject.config
sudo rm -rf myproject.conf

# creating a new myproject.cong file passing dynamic variables in same dir


sed -e "s/{{ip_address}}/$ip_address/g" \
    -e "s/{{domain_name}}/$domain_name/g" nginx_template.conf > myproject.conf

# deleteing default project
sudo rm -rf /etc/nginx/sites-available/default
sudo rm -rf /etc/nginx/sites-enabled/default


# delteing existing myproject file from sites-available & sites-enabled
sudo rm -rf /etc/nginx/sites-available/myproject
sudo rm -rf /etc/nginx/sites-enabled/myproject


sudo cp -rf myproject.conf /etc/nginx/sites-available/myproject
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

# ssl configuration

# cd $jenkins_dir$pipeline_name/cicd/hard_build/ssl
# sudo cp -rf bundle.cer /etc/nginx/sites-available/
# sudo cp -rf hv_ssl.key /etc/nginx/sites-available/
# echo "cer and private.key has been moved"


sudo nginx -t

sudo ufw allow 'Nginx Full'
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx has been started"

sudo systemctl status nginx
