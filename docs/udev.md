
`man udev`
`man udevadm`

get device info for making rules

`udevadm info -a /dev/gpiochip0`

"looking at device" will have the path
which you can use with `udevadmin test xxxx`
although this is not super useful

```
# /etc/udev/rules.d/99-custom.rules

SUBSYSTEM=="gpio", GROUP="gpio", MODE="0660"

```

`udevadm control --reload` won't change existing devices,
you have to reboot

check permissions

`ls -al /dev/gpiochip*`
