import sys
import config
import event
import wiegand
import sensors
import entry
import numpad
import auth

code = None

try:
    while True:
        # 3ms delay affects everything following
        response = wiegand.read()
        
        if isinstance(response, int):
            code = numpad.press(response) # button
        else:
            code = response # card (or None)
        
        # check the code
        if code != None:
            if auth.verify(code):
                # unlock
                entry.allow()
                event.log('Access granted', code)
            else:
                entry.deny()
                event.log('Access denied', code)
            
            code = None
        
        # check sensors
        sensors.check()
        
        # cleanup
        entry.secure()

except KeyboardInterrupt:
    # Ctrl+Z breaks this
    config.chip.close()
    sys.exit(130)
