import sys
import time
import gpiod
import config
import wiegand

# Setup gpio

chip = gpiod.Chip('gpiochip0')

lock   = chip.get_line(config.lock)
relay  = chip.get_line(config.relay)
led    = chip.get_line(config.led)
buzzer = chip.get_line(config.buzzer)
door   = chip.get_line(config.door)
aux    = chip.get_line(config.aux)
d0     = chip.get_line(config.d0)
d1     = chip.get_line(config.d1)

lock.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
relay.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
led.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
buzzer.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

door.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)
aux.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)

wiegandBulk = gpiod.LineBulk([d0, d1])
wiegandBulk.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN)
wiegandBulk.release()
wiegandBulk.request(consumer=config.name, type=gpiod.LINE_REQ_EV_FALLING_EDGE)

# Function stuff

unlocked = False
unlockTime = 0

def lockLock():
	global unlocked
	global unlockTime
	
	# should also check if door is closed
	
	if unlocked:
		now = time.time()
		if now - unlockTime > 10:
			lock.set_value(0)
			led.set_value(0)
			unlocked = False

def unlockLock():
	global unlocked
	global unlockTime
	
	lock.set_value(1)
	led.set_value(1)
	unlocked = True
	unlockTime = time.time()

# Loop stuff

#print('Waiting for events')

reading = False
doorTrigger = False
auxTrigger = False

try:
	while True:
		# 3ms delay affects everything following
		events = wiegandBulk.event_wait(nsec=3000000)
		
		# wiegand events
		if events:
			reading = True
			for line in events:
				event = line.event_read()
				wiegand.store(event)
		elif reading:
			reading = False
			wiegand.handle()
		
		# door check
		if door.get_value() == 0:
			doorTemp = True
		else:
			doorTemp = False
		
		if doorTrigger != doorTemp:
			doorTrigger = doorTemp
			print('Door', 'Open' if doorTrigger else 'Close')
		
		# aux check
		if aux.get_value() == 0:
			auxTemp = True
		else:
			auxTemp = False
		
		if auxTrigger != auxTemp:
			auxTrigger = auxTemp
			print('Aux', 'Open' if auxTrigger else 'Close')
		
		# cleanup
		lockLock()

except KeyboardInterrupt:
	chip.close()
	sys.exit(130)

