#!/bin/bash

# install libraries
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y apache2
sudo apt-get install -y libapache2-mod-wsgi
sudo apt-get install -y python-pip
sudo apt-get install -y postgresql postgresql-contrib libpq-dev
sudo pip install flask
sudo pip install sqlalchemy
sudo pip install psycopg2 Flask-SQLAlchemy Flask-Migrate
sudo pip install flask_sqlalchemy
sudo pip install flask_script
sudo pip install flask_migrate

# link the repo
sudo ln -sT ~/verbIQ/server /var/www/html/flaskapp

# change site config file
sudo mv /home/ubuntu/verbIQ/server/000-default.conf /etc/apache2/sites-enabled/

# restart the server
sudo apachectl restart

# create the DB
python ~/verbIQ/server/createDB.py
