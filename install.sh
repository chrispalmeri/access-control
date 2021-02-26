#!/bin/bash

# be running as root
if [[ $EUID != 0 ]]; then
    echo "This script needs to be run as root." >&2
    exit 1
fi

# Update and install software
apt-get update
apt-get install -y micro sqlite3 gpiod python3-libgpiod python3-aiohttp

# variables
dir="$(pwd)"
user="$(logname)"

# setup the database
if [ ! -d $dir/db ]; then
    mkdir $dir/db
    chown $user:$user $dir/db
fi

if [ ! -f $dir/db/database.db ]; then
    touch $dir/db/database.db
    chown $user:$user $dir/db/database.db
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

# add a group for gpio access
groupadd -f gpio
chgrp gpio /dev/gpiochip* # this might be lost on reboot
chmod g+rw /dev/gpiochip* # this might be lost on reboot

# you have to log out and back in though
usermod -a -G gpio "$(logname)"
