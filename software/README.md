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

## WiringNP fix

This might be because of Armbian, and I think the values are specific for H3 boards. Worked with Neo v1.3 and Neo Core v1.1

Start with install steps at https://github.com/friendlyarm/WiringNP

  * edit `~/WiringNP/wiringPi/boardtype_friendlyelec.c` and replace `/sys/class/sunxi_info/sys_info` with `/etc/sys_info`
  * create the file `/etc/sys_info` with this content (sudo nano)

```
sunxi_platform    : Sun8iw7p1
sunxi_secure      : normal
sunxi_chipid      : 2c21020e786746240000540000000000
sunxi_chiptype    : 00000042
sunxi_batchno     : 1
sunxi_board_id    : 1(0)
```

`./build` again probably

## GPIO

`gpio readall`

`gpio mode 3 out` enable led pin

`gpio write 3 1` turn led on

`gpio write 3 0` turn led off

`gpio mode 4 in` enable d1 input pin

### Old test board

pin | function
--- | ---
  3 | led
  2 | buzzer
  6 | lock
  4 | d1
  5 | d0
 16 | door

### Current hardware

pin | function
--- | ---
  0 | lock
  1 | door contact
  2 | reader d0
  3 | reader d1
  4 | reader led
  5 | reader buzzer
  6 | doorbell
  7 | relay out

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
