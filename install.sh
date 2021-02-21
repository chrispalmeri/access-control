#!/bin/bash

# be running as root
if [[ $EUID != 0 ]]; then
    echo "This script needs to be run as root." >&2
    exit 1
fi

# setup variables to use below
# to switch to shared folder when vagrant
build=/home/www-data/door-control
serve=/srv/door-control

if [[ $1 ]]; then
    build=/vagrant
    serve=/vagrant
fi

# Timezone
timedatectl set-timezone America/Chicago

# Update and install software
apt-get update
apt-get install -y git apache2 sqlite3 php libapache2-mod-php php-curl php-sqlite3 ufw

# need to stop apache while modifying the user
systemctl stop apache2

# give www-data a proper home directory
# that's the user php will run commands as
# want it to have a place to put stuff
# where it has permission to `git pull` later
mkdir -p /home/www-data
chown www-data:www-data /home/www-data
usermod -d /home/www-data www-data

# clone repo as www-data, check if exists first
if [[ -d /home/www-data/door-control ]]; then
    cd /home/www-data/door-control
    #sudo -u www-data git fetch
    #if [[ $(sudo -u www-data git rev-parse HEAD) != $(sudo -u www-data git rev-parse @{u}) ]]; then
        # sudo -u www-data git reset --hard
        sudo -u www-data git pull
    #fi
else
    sudo -u www-data git clone https://github.com/chrispalmeri/access-control.git /home/www-data/door-control
fi

# copy www to www
rsync -av --delete --delete-excluded --include='php/***' --include='python/***' --include='www/***' --filter 'protect database.db' --exclude='*' /home/www-data/door-control/ /srv/door-control/

# Make a log directory
mkdir -p $build/.log

# Add another PHP .ini to be parsed after the defaults
cat > /etc/php/7.3/apache2/conf.d/90-custom.ini << EOF
date.timezone = America/Chicago
error_log = $build/.log/php-error.log
EOF

# Overwrite default Apache .conf file
cat > /etc/apache2/sites-available/000-default.conf << EOF
<VirtualHost *:80>
    ServerName example.com

    DocumentRoot $serve/www

    <Directory $serve/www>
        Options -Indexes +FollowSymLinks -MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog $build/.log/apache-error.log
    CustomLog $build/.log/apache-access.log combined
</VirtualHost>
EOF

# Add placeholder env config file
cat > /etc/apache2/conf-available/env.conf << EOF
SetEnv FOO ""
SetEnv BAR ""
EOF

# Enable mod rewrite, env config, and restart Apache
a2enmod rewrite
a2enconf env
systemctl restart apache2

# Enable firewall
ufw allow ssh
ufw allow http
ufw allow https
ufw --force enable
