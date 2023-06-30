from types import SimpleNamespace
import time

self = SimpleNamespace()
self.pin = ''
self.last_press = 0

def press(key):
    now = time.time()

    # check if past the timeout
    # should you add a function and call in main loop
    # doesn't matter if it hangs around if not broadcast
    if now - self.last_press > 5:
        self.pin = ''
        # chirp buzzer?

    self.last_press = now

    if key == 10: # ESC
        self.pin = ''
    elif key == 11: # ENT
        temp = self.pin
        self.pin = ''
        if temp != '':
            return temp
    else:
        self.pin = self.pin + str(key)

        # auto submit if length is 6
        if len(self.pin) == 6:
            temp = self.pin
            self.pin = ''
            return temp

    return None
