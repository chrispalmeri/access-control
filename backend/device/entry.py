import time
import gpiod
import config
import state
import broadcast

lock = config.CHIP.get_line(config.LOCK)
relay = config.CHIP.get_line(config.RELAY)
led = config.CHIP.get_line(config.LED)
buzzer = config.CHIP.get_line(config.BUZZER)

lock.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
relay.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
led.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
buzzer.request(consumer=config.NAME, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
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
