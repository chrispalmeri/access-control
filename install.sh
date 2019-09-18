#!/bin/bash

# had to sudo chown -R www-data:www-data /var/www/html

if [[ ! $(id -u) == 0 ]]; then
  echo "This script needs to be run as root." >&2
  exit 1
fi

cd /var/tmp

if [[ ! -d access-control ]]; then
  echo ">>> Clone the app"
  sudo -u www-data git clone https://github.com/chrispalmeri/access-control.git
  cd access-control
else
  cd access-control
  git fetch
  if [[ $(git rev-parse HEAD) != $(git rev-parse @{u}) ]]; then
    echo ">>> Update the app"
    git pull
  else
    echo ">>> Already up to date"
  fi
fi

sudo -u www-data rsync -av --delete code/ /var/www/html