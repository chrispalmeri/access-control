from os import path
import gpiod
import utils

try:
    CHIP = gpiod.Chip('gpiochip0')
except FileNotFoundError:
    CHIP = None

NAME = 'doorctl'

armbian_release = utils.read_config_file('/etc/armbian-release')

# These are NanoPi NEO Core pins
if armbian_release['BOARD'] == 'nanopineo':
    LOCK   = 1
    RELAY  = 200
    LED    = 201
    BUZZER = 6
    DOOR   = 198
    AUX    = 199
    D0     = 3
    D1     = 203

# These are Orange PI PC+ pins
# Used for development
if armbian_release['BOARD'] == 'orangepipcplus':
    LOCK   = 2
    RELAY  = 68
    LED    = 71
    BUZZER = 110
    DOOR   = 13
    AUX    = 14
    D0     = 3
    D1     = 6

DBPATH = path.normpath(path.dirname(__file__) + '/../db/database.db')
