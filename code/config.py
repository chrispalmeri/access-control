import gpiod
from configparser import ConfigParser

try:
    chip = gpiod.Chip('gpiochip0')
except FileNotFoundError:
    chip = None

name = 'doorctl'

parser = ConfigParser()
with open('/etc/armbian-release') as raw_file:
    # cause configparser requires ini sections
    file_content = '[armbian-release]\n' + raw_file.read()
    parser.read_string(file_content)

# These are NanoPi NEO Core pins
if parser['armbian-release']['BOARD'] == 'nanopineo':
    lock   = 1
    relay  = 200
    led    = 201
    buzzer = 6
    door   = 198
    aux    = 199
    d0     = 3
    d1     = 203

# These are Orange PI PC+ pins
# Used for development
if parser['armbian-release']['BOARD'] == 'orangepipcplus':
    lock   = 2
    relay  = 68
    led    = 71
    buzzer = 110
    door   = 13
    aux    = 14
    d0     = 3
    d1     = 6
