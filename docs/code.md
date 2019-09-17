# Software

## OS setup

Download [Armbian][1] Bionic image and [7-Zip][2] to extract it.

Use [Etcher][4] to flash the image onto your [SD card][3].

Boot the hardware from the SD card and use [Putty][5] to access it.

  [1]: https://www.armbian.com/nanopi-neo/
  [2]: https://www.7-zip.org/
  [3]: https://shop.sandisk.com/store/sdiskus/en_US/pd/productID.5163153100/SanDisk-Ultra-microSDXC-UHSI-Card-32GB-A1C10U1
  [4]: https://www.balena.io/etcher/
  [5]: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html

## Initial config

* login as `root` using `1234`
* change password
* new user wizard
  * password
  * skip all the questions
* `apt update`
* `DEBIAN_FRONTEND=noninteractive apt upgrade -y`
* `armbian-config`
    * System > Install > Install/Update the bootloader on SD/eMMC > Yes
    * Ok > Back
    * Personal > Hostname > type a new hostname
    * Personal > Timezone > set that too
    * Ok > Ok > Back > Exit
* `shutdown -r now` to reboot

## Usage

Use your new username and password

`sudo nano /etc/environment` to add env variables (did not use)

```
WHATEVER=something
```

example provision from other repo maybe (did not use)

```
git clone https://github.com/chrispalmeri/nanopi-neo-nodejs.git
cd nanopi-neo-nodejs
sudo ./provision.sh
```

## WiringNP install/fix

This might be because of Armbian, and I think the values are specific for H3 boards. Worked with Neo v1.3 and Neo Core v1.1

from https://github.com/friendlyarm/WiringNP

`git clone https://github.com/friendlyarm/WiringNP`

`sudo nano /etc/sys_info` to create this file

```
sunxi_platform    : Sun8iw7p1
sunxi_secure      : normal
sunxi_chipid      : 2c21020e786746240000540000000000
sunxi_chiptype    : 00000042
sunxi_batchno     : 1
sunxi_board_id    : 1(0)
```

`nano WiringNP/wiringPi/boardtype_friendlyelec.c` and replace `/sys/class/sunxi_info/sys_info` with `/etc/sys_info`

`cd WiringNP/`

`chmod 755 build`

`./build`

## GPIO

`gpio readall`

`gpio mode 3 out` enable led pin

`gpio write 3 1` turn led on

`gpio write 3 0` turn led off

`gpio mode 4 in` enable d1 input pin

### Current hardware

wPi | physical | function
--- | --- | ---
  0 |  11 | lock
  1 |  12 | door contact
  2 |  13 | reader d0
  3 |  15 | reader d1
  4 |  16 | reader led
  5 |  18 | reader buzzer
  6 |  22 | doorbell
  7 |   7 | relay out

There is nothing to set these up currently you have to manually set modes each boot

## Python

python3 is installed already

Simple script example:

`sudo nano hello-world.py`

```
#!/usr/bin/python3

print("Hello, World!");
```

`chmod +x hello-world.py`

`./hello-world.py`

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