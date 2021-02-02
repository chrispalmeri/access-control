This should all go in the schematic probably

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

## Notes

  * Resistor values were adjusted a little after real world measurements
