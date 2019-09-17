# WiringNP

## Installation

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

## Testing

`gpio readall`

`gpio mode 3 out` enable led pin

`gpio write 3 1` turn led on

`gpio write 3 0` turn led off

`gpio mode 4 in` enable d1 input pin

There is nothing to set these up currently you have to manually set modes each boot
