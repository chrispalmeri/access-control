# access-control

DIY door access control system with NanoPi

# Hardware

![Board picture](board/images/top.png)

[DipTrace][1] files, `gerber.zip` works with [JLCPCB][2]

Removed SVG's from repo but you can drop `gerber.zip` into [tracespace][3] to generate.

You need to plug a [NanoPi Neo Core][4] on to it

  [1]: https://diptrace.com/
  [2]: https://jlcpcb.com/
  [3]: https://tracespace.io/view/
  [4]: https://www.friendlyarm.com/index.php?route=product/product&path=69&product_id=212

These are the gpio pins that are used:

BCM | wPi | physical | function
--- | --- | --- | ---
  2 |   2 |  13 | lock
201 |   5 |  18 | door contact
  6 |   1 |  12 | reader d0
199 |  16 |  10 | reader d1
203 |   7 |   7 | reader led
198 |  15 |   8 | reader buzzer
200 |   4 |  16 | doorbell
  3 |   3 |  15 | relay out

# Software

## OS setup

Download [Armbian][1] image (Debian 10.7 "Buster") and [7-Zip][2] to extract it.

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

## Local Development

`vagrant up` for dev at http://localhost:8080
