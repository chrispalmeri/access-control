#!/bin/bash

# be running as root
if [ $UID != 0 ]; then
    echo "This script needs to be run as root." >&2
    exit 1
fi

# Update and install software
apt-get update
apt-get install -y gpiod python3-libgpiod python3-aiohttp sqlite3
# gpiod was already newest version btw on fresh install

# variables
dir=$(cd $(dirname $0); pwd)
user=$(logname)
app="doorctl"

# allow vagrant to override the directory with argument
if [ $1 ] && [ -d $1 ]; then
  dir=$1
fi

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
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    pin TEXT,
    card INTEGER,
    facility INTEGER
);

INSERT INTO users (name, pin)
SELECT 'Admin', '1234'
WHERE NOT EXISTS (SELECT * FROM users);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    time TEXT,
    channel TEXT,
    message TEXT
);
EOF

# add a group for gpio access
groupadd -f gpio

# add yourself to the group
# you have to log out and back in though
usermod -a -G gpio $user

# create udev rule to allow group access to gpio
# definitley need to reboot
cat > /etc/udev/rules.d/99-custom.rules << EOF
SUBSYSTEM=="gpio", GROUP="gpio", MODE="0660"
EOF

# setup systemd service and port
cat > /etc/systemd/system/$app.socket << EOF
[Unit]
Description=$app socket

[Socket]
ListenStream=80
EOF

cat > /etc/systemd/system/$app.service << EOF
[Unit]
Description=$app service
After=network.target
Requires=$app.socket

[Service]
User=$user
ExecStart=/usr/bin/python3 $dir/code/serve.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable $app

if [ $1 ] && [ -d $1 ]; then
    # you could make this uniform for vagrant/hardware
    # reboot = vagrant reload after initial vagrant up
    # and fix service start via additional "always" provisioner
    # also additional provisioner could show the status message on reload/resume

    # cause in vagrant shared folder is the holdup, causes service not to start
    sed -i 's/WantedBy=multi-user.target/WantedBy=vagrant.mount/' /etc/systemd/system/$app.service
    systemctl daemon-reload

    # start it
    systemctl start $app

    if systemctl is-active $app &> /dev/null; then
        echo -e ">>> $app service is \e[32mUP\e[0m"
    else
        echo -e ">>> $app service is \e[31mDOWN\e[0m"
    fi
else
    # if running with real gpio you will need permissions and udev reloaded
    echo "You should reboot now"
fi
