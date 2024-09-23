from types import SimpleNamespace
import time
from cred import Cred

self = SimpleNamespace()
self.pin = ''
self.last_press = 0

def check_expiry():
    now = time.time()

    # check if past the timeout
    # should you add a function and call in main loop
    # doesn't matter if it hangs around if not broadcast
    if now - self.last_press > 5:
        self.pin = ''

    return now

def press(key):
    self.last_press = check_expiry()

    self.pin = self.pin + str(key)

    # this part is no longer right after adding actions
    # auto submit if length is 6
    # if len(self.pin) == 6:
        # temp = self.pin
        # self.pin = ''
        # return temp

    # return None

def get_value():
    check_expiry()

    temp = self.pin
    self.pin = ''

    if temp != '':
        if len(temp) == 1: # one is action only
            return Cred(None, None, None, temp)
        if len(temp) % 2: # odd is pin and action
            return Cred(None, None, temp[1:], temp[0])
        # even is pin only
        return Cred(None, None, temp)

    return None

def clear_value():
    self.pin = ''
