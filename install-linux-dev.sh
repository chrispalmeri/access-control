#!/bin/bash

# be running as root
if [[ $EUID != 0 ]]; then
  echo "This script needs to be run as root." >&2
  exit 1
fi

# Update and install software
apt-get update
apt-get install -y apache2 sqlite3 php libapache2-mod-php php-curl php-sqlite3

# setup variables to use below
serve="$(pwd)/www"

# navigate to door-control/ in browser
if ! grep -q "127.0.0.1   door-control" /etc/hosts; then 
    echo "127.0.0.1   door-control" >> /etc/hosts
fi

# Add new Apache .conf file
cat > /etc/apache2/sites-available/door-control.conf << EOF
<VirtualHost *:80>
    ServerName door-control

    DocumentRoot $serve

    <Directory $serve>
        Options -Indexes +FollowSymLinks -MultiViews
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Enable site, mod rewrite, and restart Apache
a2ensite door-control
a2enmod rewrite
systemctl restart apache2
