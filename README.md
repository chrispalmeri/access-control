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

python
  update docs
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

Download [Armbian][5] Bullseye image, use [Etcher][6] to flash the image onto your [SD card][7].

Boot the hardware from the SD card, check your router to find the IP address, and use [Putty][8] to access it.

  [5]: https://www.armbian.com/nanopi-neo/
  [6]: https://www.balena.io/etcher/
  [7]: https://shop.sandisk.com/store/sdiskus/en_US/pd/productID.5163153100/SanDisk-Ultra-microSDXC-UHSI-Card-32GB-A1C10U1
  [8]: https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html

## Initial config

* login as `root` with password `1234`
* enter new password twice
* pick `1` for "bash" terminal
* enter new username
* password twice
* display name
* `Enter` to accept language based on detected timezone
* pick `1` for "en_US.UTF-8"
* `apt update`
* `DEBIAN_FRONTEND=noninteractive apt upgrade -y`
* `armbian-config`
    * Personal > Timezone > set that
    * Personal > Hostname > type a new hostname
    * System > Install > Install/Update the bootloader on SD/eMMC > Yes
    * System > Install > Boot from eMMC - system on eMMC > Yes > ext4 > Power Off

Unplug power, Remove SD card, and reconnect power.

<!--
I think you could then reuse the SD card on additional boards
and only need to do the hostname, bootloader, eMMC steps
-->

## Installation

Connect all your door hardware.

Reconnect with Putty and use new username.

`git clone https://github.com/chrispalmeri/access-control.git`

`cd access-control`

`sudo ./install.sh`

`sudo shutdown -r now` to reboot

## Usage

Navigate to IP address in browser.

<!--
If weblog shows wrong contact status and wiegand readding errors

remote in `nano access-control/code/config.py`
change pin numbers to correct ones for your board
Ctrl+S, Ctrl+X
`sudo systemctl restart doorctl`

I think it has the 60 sec websocket hang when stopping again
just wait a minute and then it is good
-->

Swipe a card and check the logs for the number. Then use Postman to add a user with `POST` to `/api/users`.

Should be good to go. Check that the hardware is all working correctly.

## Troubleshooting

Restart process with `sudo systemctl restart doorctl`

Check for errors with `sudo journalctl -u doorctl --since "5 minutes ago"`

## Locally

`vagrant up` then go to http://localhost:8080/

Maybe `vagrant reload` but I don't think it is required

If there are issues `vagrant ssh` then use troubleshooting commands above.

There will be no GPIO locally, so none of that stuff will do anything.

## Update

`cd access-control`, `git fetch` then `git status`

If there are updates `git pull`. Maybe should `sudo ./install.sh` again?

`sudo systemctl restart doorctl`
