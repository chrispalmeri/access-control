#!/bin/bash

# be running as root
if [[ $EUID != 0 ]]; then
    echo "This script needs to be run as root." >&2
    exit 1
fi

# Update and install software
apt-get update
apt-get install -y apache2 sqlite3 php libapache2-mod-php php-curl php-sqlite3

# setup the database
dir="$(pwd)"
user="$(logname)"

if [ ! -d $dir/db ]; then
    mkdir $dir/db
    chown $user:www-data $dir/db
fi

if [ ! -f $dir/db/database.db ]; then
    touch $dir/db/database.db
    chown $user:www-data $dir/db/database.db
    chmod 664 $dir/db/database.db
fi

sqlite3 $dir/db/database.db << EOF
CREATE TABLE IF NOT EXISTS "users" (
    "id" INTEGER NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "pin" TEXT,
    "card" INTEGER,
    "facility" INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "events" (
    "id" INTEGER NOT NULL UNIQUE,
    "message" TEXT NOT NULL,
    "data" TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
);
EOF

#---------------
# following is not necessary since creating db above instead of in php
# but might be the solution for software update by www-data

# https://superuser.com/questions/1123235/give-a-group-write-permission-to-a-folder
# assign the www directory to www-data group
# give group write permission
# and the 's' makes new files use same group
#chgrp -R www-data www
#chmod -R g+ws www

# you have to log out and back in though
# this is so your user is in www-data group
# and isn't locked out of new files created by www-data
#usermod -a -G www-data "$(logname)"

#---------------

# setup navigating to door-control/ in browser
if ! grep -q "127.0.0.1   door-control" /etc/hosts; then 
    echo "127.0.0.1   door-control" >> /etc/hosts
fi

# apache and php errors are left in /var/log/apache2/error.log

# Add new Apache .conf file
cat > /etc/apache2/sites-available/door-control.conf << EOF
<VirtualHost *:80>
    ServerName door-control

    DocumentRoot $dir/www

    <Directory $dir/www>
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
