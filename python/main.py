import sys
import config
import event
import wiegand
import entry
import sensors

try:
	while True:
		# 3ms delay affects everything following
		code = wiegand.read()
		
		if code != None:
			event.log('Code:', code)
		
			# unlock
			if code == 5: # fixme
				entry.allow()
		
		# check sensors
		sensors.check()
		
		# cleanup
		entry.secure()

except KeyboardInterrupt:
	# Ctrl+Z breaks this
	config.chip.close()
	sys.exit(130)
