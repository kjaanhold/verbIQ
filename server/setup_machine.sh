#!/bin/bash

# install libraries
sudo apt-get update
sudo apt-get install -y apache2
sudo apt-get install -y libapache2-mod-wsgi
sudo apt-get install -y python-pip
sudo pip install -y flask

# link the repo
sudo ln -sT ~/verbIQ/server /var/www/html/flaskapp

# change site config file
sudo mv /home/ubuntu/verbIQ/server/000-default.conf /etc/apache2/sites-enabled/

# restart the server
sudo apachectl restart

# create the DB
python createDB.py