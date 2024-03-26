#!/bin/bash

sudo apt-get update
sudo apt-get install -y build-essential
sudo apt install python3.11-dev
sudo apt-get install -y libpq-dev

echo "--------------------------------Install POSTGRES--------------------------"
sudo apt install postgresql postgresql-contrib
echo "--------------------------------DONE Install POSTGRES--------------------------"

echo "--------------------------------Creating Database --------------------------"
sudo -u postgres psql -c "CREATE DATABASE $database_name"
echo "--------------------------------Creating Database Done--------------------------"

echo "--------------------------------Changing User's Password --------------------------"
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '$postgres_password'"
echo "--------------------------------Done User's Password --------------------------"

echo "--------------------------------Granting All permission to user --------------------------"
sudo -u postgres psql -c  "GRANT ALL PRIVILEGES ON DATABASE hvp TO postgres"
echo "--------------------------------Done Granting All permission to user --------------------------"