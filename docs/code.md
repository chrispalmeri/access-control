# Software

## PHP

`apt install php`

`apt install apache2 libapache2-mod-php` cause php installs it but doesn't setup the service or something

And then also

`nano /etc/apache2/apache2.conf`

```
<FilesMatch \.php$>
SetHandler application/x-httpd-php
</FilesMatch>
```

And if it is still jacked up

`a2dismod mpm_event && a2enmod mpm_prefork && a2enmod php7.2`

`systemctl restart apache2`

Then go to `/var/www/html` and make your files

`index.php`

```
<?php
phpinfo();
```

`rm index.html`

## Notes

do you want to emulate `gpio` command for dev?

you should use some of this https://github.com/calcinai/phpi

`Access-Control-Allow-Origin` was for dev probably shouldn't stay


## Future installation

from wherever, home directory probably

`git clone`

`./provision-prod.sh`

  * this should save the working directory somewhere
  * and do whatever other setup
  * and kick off `update.sh`
  * that would copy files into /var/www/html

then api/update will know where to switch to in order to

`git pull`

`./update.sh` again