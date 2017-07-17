# 1. Launch an AWS EC2 instance

# 2. Install and update needed packages:

  `sudo apt-get update`
  
  `sudo apt-get install apache2`
  
  `sudo apt-get install libapache2-mod-wsgi`
  
  `sudo apt-get install python-pip`
  
  `sudo pip install flask`
  
# 3. Clone this repo to home directory 
  `git clone https://github.com/kjaanhold/verbIQ.git`
  
# 4. Link to directory 
`sudo ln -sT ~/verbIQ /var/www/html/flaskapp`

# 5. Add the following block just after the DocumentRoot /var/www/html line

 `WSGIDaemonProcess flaskapp threads=5
  WSGIScriptAlias / /var/www/html/flaskapp/flaskapp.wsgi

  <Directory flaskapp>
      WSGIProcessGroup flaskapp
      WSGIApplicationGroup %{GLOBAL}
      Order deny,allow
      Allow from all
  </Directory>`
  
  # 6. Restart the server with new configs 
  `sudo apachectl restart`
