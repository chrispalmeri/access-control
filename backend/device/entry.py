from types import SimpleNamespace
import time
import gpiod
import config
from device import sensors
import broadcast

# unclear about uppercasing instances of things, but won't be directly reassigned
LOCK = config.CHIP.get_line(config.LOCK)
RELAY = config.CHIP.get_line(config.RELAY)
LED = config.CHIP.get_line(config.LED)
BUZZER = config.CHIP.get_line(config.BUZZER)

LOCK.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
RELAY.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
LED.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
BUZZER.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
# there is no PWM in libgpiod, so no fancy buzzer sounds
# use this then: https://python-periphery.readthedocs.io/en/latest/pwm.html
# you were thinking about converting to that anyway

# not sure if good or bad, to avoid using global keyword
# self is just a convention for classes not actually reserved
# SimpleNamespace allows accessing with dot notation, unlike dict
self = SimpleNamespace()
self.unlocked = False
self.unlock_time = 0

def allow():
    LOCK.set_value(1)
    LED.set_value(1)
    self.unlocked = True
    self.unlock_time = time.time()

def deny():
    # buzzer
    # and then buzzerTime state so you can turn it off
    pass

async def secure():
    if self.unlocked:
        now = time.time()

        # if time is up and door is closed re-lock
        if now - self.unlock_time > 5 and sensors.status.door_closed: # add config for time
            LOCK.set_value(0)
            LED.set_value(0)
            self.unlocked = False
            await broadcast.event('INFO', 'Door secured')
