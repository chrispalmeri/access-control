# Specs

## FAQ

Q. Why not a microcontroller? It would make interrupts simpler and lower your power
requirements dramatically. And you don't really need a web server on device.

A. Networking, while possible, is more complicated and has minimal feature set.
TLS is the same story, but even more compromises, and super hard to find good
guides, especially for stuff like MQTT or websockets.

## Pins

Inputs are normally high, outputs are normally low.

Name  | Type | Phys | Nano | #     | Orange | #
---   | ---  | ---  | ---  | ---   | ---    | ---
LOCK  | OUT  | 22   | PA1  | 1     | PA2    | 2
RELAY | OUT  | 16   | PG8  | 200   | PC4    | 68
LED   | OUT  | 18   | PG9  | 201   | PC7    | 71
BZR   | OUT  | 12   | PA6  | 6     | PD14   | 110
D0    | IN   | 15   | PA3  | 3     | PA3    | 3
D1    | IN   | 7    | PG11 | 203   | PA6    | 6
DOOR  | IN   | 8    | PG6  | 198   | PA13   | 13
AUX   | IN   | 10   | PG7  | 199   | PA14   | 14

For the pin designators like `PG7` the `P` just means "pin", then each following
letter represents a group of 32 pins. So multiply the zero-indexed letter of the
alphabet position by 32 and add the number to get the final number. And they
were all on `gpiochip0` in my limited experience. For example:

`PA3` would be `0 * 32 + 3` so `gpiochip0 3`

`PG7` would be `6 * 32 + 7` so `gpiochip0 199` 

## Nano Pi

  * Power in is 5V 2A (4.7V-5.6V)
  * All 5V pins are connected
  * pins are 3.3V, output current is 5mA - this is just for calculating NPN/mosfet saturation
    although I think you applied it to input current also

## Reader

  * Power is 12V 80mA
  * Data pins are 5V normally high
  * BZR needs to sink ~ 4.8V 3.6mA
  * LED needs to sink ~ 3.5V 0.4mA
  * Three data resistors achieve pullup plus voltage divide (and current limiting?)
  * I think you have one reader that is 26 bit and the other is 34 bit

## Lock

  * Power is 12V 240mA
  * what is the mosfet saturation?

## Relay

  * Power is 5V 80mA
  * coil has no polarity
  * Can switch at least 3A at 250VAC or 30VDC
    (otherwise check sheet, can do more on NO, especially with AC)

## Contacts

  * Board is not powering, resistor divider is,
    and contact closure just sinks to ground
  * Normal alarm contacts are electrically NO, plus magnet, for a NC alarm loop
