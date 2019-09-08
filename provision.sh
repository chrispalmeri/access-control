#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

# Timezone
cp /usr/share/zoneinfo/America/Chicago /etc/localtime

apt-get update
apt-get install -y php

# Make a log directory
mkdir -p /vagrant/.logs

# Add another PHP .ini to be parsed after the defaults
cat > /etc/php/7.2/apache2/conf.d/99-custom.ini << EOF
error_log = /vagrant/.logs/php-error.log
EOF

# Overwrite default Apache .conf file
cat > /etc/apache2/sites-available/000-default.conf << EOF
<VirtualHost *:80>
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options -Indexes
        AllowOverride All
        Header set Access-Control-Allow-Origin "*"
    </Directory>

    ErrorLog /vagrant/.logs/apache-error.log
    CustomLog /vagrant/.logs/apache-access.log combined
</VirtualHost>
EOF

# Enable mod rewrite and restart Apache
a2enmod rewrite
# might need a2enmod headers too
systemctl restart apache2

rm /var/www/html/index.html
