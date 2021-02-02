# libgpiod setup

https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git/about/

`sudo apt install gpiod`

`sudo gpiodetect`

Need to do something about requiring sudo probably

https://forum.armbian.com/topic/8714-gpio-not-working-for-non-root/?do=findComment&comment=86295

## Input Example

`sudo gpiomon --num-events=1 --falling-edge gpiochip0 6`

## Output Example

On `sudo gpioset gpiochip0 2=1`

Off `sudo gpioset gpiochip0 2=0`