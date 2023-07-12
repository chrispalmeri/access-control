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

# setup the database directory
if [ ! -d $dir/db ]; then
    mkdir $dir/db
    chown $user:$user $dir/db
fi

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

# setup ssl directory
if [ ! -d $dir/ssl ]; then
    mkdir $dir/ssl
    chown $user:$user $dir/ssl
fi

# generate self signed cert
openssl req  -x509 -newkey rsa:4096 -sha256 -days 3650 \
    -out ../ssl/cert.pem -keyout ../ssl/key.pem -nodes \
    -subj "/C=US/O=Door Controller/CN=doorctl-dev" \
    -addext "subjectAltName = DNS:doorctl-dev, IP:192.168.1.187" \
    -addext "keyUsage = critical, digitalSignature, keyEncipherment" \
    -addext "extendedKeyUsage = critical, serverAuth"

# change ownership of cert
chown $user:$user $dir/ssl/cert.pem
chown $user:$user $dir/ssl/key.pem

# setup systemd service and port
# explicitly IPv4
cat > /etc/systemd/system/$app.socket << EOF
[Unit]
Description=$app socket

[Socket]
ListenStream=0.0.0.0:443
EOF

cat > /etc/systemd/system/$app.service << EOF
[Unit]
Description=$app service
After=network.target
Requires=$app.socket

[Service]
User=$user
ExecStart=/usr/bin/python3 $dir/backend/serve.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable $app

# you will need permissions and udev reloaded for gpio
echo "You should reboot now"
