#!/bin/bash
echo "y" | sudo apt-get update
echo "y" | sudo apt-get upgrade
echo "y" | sudo apt-get install python3-pip libpq-dev postgresql postgresql-contrib nginx
echo "y" | sudo apt install python3.11-venv
echo "y" | sudo apt-get install openjdk-11-jre
echo "y" | sudo apt-get update
echo "y" | sudo apt-get upgrade
echo "y" | wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -

echo "y" | sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
echo "y" | sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5BA31D57EF5975CA
echo "y" | sudo apt-get update
echo "y" | sudo apt-get install jenkins
echo "y" | sudo apt upgrade
echo "y" | sudo apt-get install git
echo "y" | sudo apt install supervisor