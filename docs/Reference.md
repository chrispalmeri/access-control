# Reference

## Dimensions

caps - 5mm dia 2mm leads

diode - DO-15 

----------

you are using a 10 mil grid

.004 - .008 inch larger than the actual dimensions (same for holes)

> you were doing 0.01 each side

----------

* min trace 3.5mil
* clearance 3.5mil

* min via 8mil inner 18mil outer
* clearance 5mil

* drill hole 8mil to 0.248
* Tolerance ± 3mil
* ring thickness > 3mil

> you are  gonna add 8mil then round to drill size

.08 pads seem good

trace to outline 8mil

--------------

.0465 - mosfet and connectors

.028 - everything else

--------------

https://www.pcbwizards.com/Drillchart.htm

https://www.4pcb.com/trace-width-calculator.html

## Classes

net classes have more info in PCB. Can back annotate schematic, change,
then update from related scematic in pcb

## Moving markings

select "View \ Component Markings \ Move Tool"

## Exporting

### BOM

In Schematic go to Objects > Bill Of material > Export to file (group by name/value)

### Gerber

Just click Export > Gerber and hit the "Export All" button

Select "Zip Archive: Gerber + NC Drill"

### PDF

temporarily set all Trace Color > By Layers when printing to pdf

### SVG

left out Top Paste when dropping into tracespace.io for svg's
(should prob remove paste from the power IC footprint)

> removed two transforms in bottom.svg to get it right side up

drag the svg's into GIMP and set at 100 pixels per inch
