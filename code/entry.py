import time
import gpiod
import config
import state
import broadcast

lock = config.chip.get_line(config.lock)
relay = config.chip.get_line(config.relay)
led = config.chip.get_line(config.led)
buzzer = config.chip.get_line(config.buzzer)

lock.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
relay.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
led.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
buzzer.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
# there is no PWM in libgpiod, so no fancy buzzer sounds

unlocked = False # move to state
unlockTime = 0

def allow():
    global unlocked
    global unlockTime

    lock.set_value(1)
    led.set_value(1)
    unlocked = True
    unlockTime = time.time()

def deny():
    # buzzer
    # and then buzzerTime state so you can turn it off
    pass

async def secure():
    global unlocked
    global unlockTime

    if unlocked:
        now = time.time()

        # if time is up and door is closed re-lock
        if now - unlockTime > 5 and state.doorClosed: # add config for time
            lock.set_value(0)
            led.set_value(0)
            unlocked = False
            await broadcast.event('INFO', 'Door secured')

