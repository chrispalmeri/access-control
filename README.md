# doorctl

DIY door access control system with NanoPi

Software part is very much unfinished

<!--

order spare inventory parts

board changes:
  put 12V at the top, move lock?
  you meant to widen lock trace
  you could make the JLCJLC text bigger
  and the github text
  any way to get the resistor designators readable? smaller?
  upsidedown ethernet kinda bugs me

www
    view log
    add codes

python
  update docs
  sqlite
  systemd
  totp

-->

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

Name | Physical | libgpiod | Type | Description
---  | ---      | ---      | ---  | ---
PA1  | 22       | 1        | OUT  | lock
PG8  | 16       | 200      | OUT  | relay out
PG9  | 18       | 201      | OUT  | reader led
PA6  | 12       | 6        | OUT  | reader buzzer
PA3  | 15       | 3        | IN   | reader d0
PG11 | 7        | 203      | IN   | reader d1
PG6  | 8        | 198      | IN   | door contact
PG7  | 10       | 199      | IN   | doorbell

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

Check [task-board][1] readme for better instructions that also apply to this.

Run python with `python3 code/serve.py`

Or now

`sudo systemctl restart doorctl`

  [1]: https://github.com/chrispalmeri/task-board
