from datetime import datetime

def log(message, data=None):
	now = datetime.utcnow().isoformat(timespec='milliseconds')
	
	if data == None:
		print(f'{now}Z', message)
	else:
		print(f'{now}Z', message, data)
