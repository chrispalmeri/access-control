import time

pin = ''
buttonTime = 0

def press(key):
    global pin
    global buttonTime
    
    now = time.time()
    
    # check if past the timeout
    # should you add a function and call in main loop
    # doesn't matter if it hangs around if not broadcast
    if now - buttonTime > 5:
        pin = ''
        # chirp buzzer?
    
    buttonTime = now
    
    if key == 10: # ESC
        pin = ''
    elif key == 11: # ENT
        temp = pin
        pin = ''
        return temp if temp != '' else None
    else:
        pin = pin + str(key)
        
        # auto submit if length is 6
        if len(pin) == 6:
            temp = pin
            pin = ''
            return temp
