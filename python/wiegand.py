import time
import config

data = 0

def store(event):
	global data
	if event.source.offset() == config.d0:
		data = data << 1
	elif event.source.offset() == config.d1:
		data = data << 1 | 1

def parity(datain, p):
	while datain:
		p ^= datain & 1
		datain >>= 1
	return p

def handleCard():
	evenParity = data >> 25 & 1
	evenHalf = data >> 13 & 4095
	oddHalf = data >> 1 & 4095
	oddParity = data & 1

	# if parity is valid, get the numbers
	if parity(evenHalf, 0) == evenParity and parity(oddHalf, 1) == oddParity:
		facility = data >> 17 & 255
		number = data >> 1 & 65535

		print(time.time(), 'Card number:', number, 'Facility code:', facility)
		
		# unlock
		#if number == 34169:
		#	unlockLock()
	else:
		print('Invalid card')

def handleKey():
	# 10 = ESC
	# 11 = ENT
	print('Key press:', data)

def handle():
	global data
	#print('Event captured')
	if data < 16:
		# must be a keypress
		handleKey()
	else:
		# assume it is 26-bit wiegand
		handleCard()
	data = 0
