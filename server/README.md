## Launch an AWS EC2 instance

## Install and update needed packages:

  `sudo apt-get update`
  
  `sudo apt-get install apache2`
  
  `sudo apt-get install libapache2-mod-wsgi`
  
  `sudo apt-get install python-pip`
  
  `sudo pip install flask`
  
## Clone this repo to home directory and link it 
  `git clone https://github.com/kjaanhold/verbIQ.git`
  
  `sudo ln -sT ~/verbIQ /var/www/html/flaskapp`
  
## Add the following block after to 
`/etc/apache2/sites-enabled/000-default.conf` after
`DocumentRoot /var/www/html` line

 ```{shell}
  WSGIDaemonProcess flaskapp threads=5
  WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

  <Directory flaskapp>
      WSGIProcessGroup flaskapp
      WSGIApplicationGroup %{GLOBAL}
      Order deny,allow
      Allow from all
  </Directory>
  ```
  
## Restart the server with new configs 
  `sudo apachectl restart`
