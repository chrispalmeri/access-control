# libgpiod

## Installation

`armbian-config`

Software > Headers

install that

Back > Exit

> puts it in `/usr/src`
>
> it is not available in package manager

where ever I just did it in root home

`git clone https://git.kernel.org/pub/scm/libs/libgpiod/libgpiod.git`

`cd libgpiod`

`apt-get install -y autoconf-archive pkg-config libtool`

`mkdir m4`

> install doxygen and help2man

`./autogen.sh --enable-tools=yes --prefix=/usr/local`

`make`

`make install`

`ldconfig`

> can maybe delete it all now it is in `/usr/local/lib`

## Testing

> Pins are all on `gpiochip0` using the "BCM" nuumbers that WiringNP would show you with `gpio readall`

`gpioinfo`

`gpioset gpiochip0 0=1` lock

`gpioset gpiochip0 200=1` led

`gpioset gpiochip0 201=1` buzzer

`gpioset gpiochip0 203=1` relay

`gpioget gpiochip0 6` door contact (or mon falling)

`gpioget gpiochip0 1` doorbell (or mon falling)

`gpiomon --falling-edge gpiochip0 2 3` weigand d0 d1

...the reader I have is using 34bit instead of 26, otherwise working perfectly
