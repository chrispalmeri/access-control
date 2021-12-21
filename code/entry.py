import time
import gpiod
import config
import state

# check first cause vagrant (this is in three files)
# even though in that case the loop would never run
# maybe this should be an init function or something cleaner
if config.chip:
    lock = config.chip.get_line(config.lock)
    relay = config.chip.get_line(config.relay)
    led = config.chip.get_line(config.led)
    buzzer = config.chip.get_line(config.buzzer)

    lock.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    relay.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    led.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    buzzer.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

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
            await config.myLog.log('INFO', 'Door secured')

