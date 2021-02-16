import gpiod
import config

d0 = config.chip.get_line(config.d0)
d1 = config.chip.get_line(config.d1)

lines = gpiod.LineBulk([d0, d1])
lines.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN) # prevent initial interrupt
lines.release()
lines.request(consumer=config.name, type=gpiod.LINE_REQ_EV_FALLING_EDGE)

reading = False
data = 0

def parity(datain, p):
	while datain:
		p ^= datain & 1
		datain >>= 1
	return p

def parse():
	evenParity = data >> 25 & 1
	evenHalf = data >> 13 & 4095
	oddHalf = data >> 1 & 4095
	oddParity = data & 1

	# if parity is valid, get the numbers
	if parity(evenHalf, 0) == evenParity and parity(oddHalf, 1) == oddParity:
		facility = data >> 17 & 255
		number = data >> 1 & 65535

		return (facility, number)
		
	else:
		return False # invalid card

def read():
	global reading
	global data
	
	events = lines.event_wait(nsec=3000000) # 3ms
	
	if events:
		reading = True
		for line in events:
			event = line.event_read()
			
			if event.source.offset() == d0.offset(): # or config.d0
				data = data << 1
			elif event.source.offset() == d1.offset(): # or config.d1
				data = data << 1 | 1
	
	# if it timed out after 3ms that means it's done
	elif reading:
		reading = False
		
		if data < 16:
			out = data # just a keypress
		else:
			out = parse() # 26-bit wiegand card
		
		data = 0
		
		return out
	
	# returns None by default
