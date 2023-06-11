from os import path
import sqlite3
import gpiod

try:
    chip = gpiod.Chip('gpiochip0')
except FileNotFoundError:
    chip = None

name = 'doorctl'

# These are NanoPi NEO Core pins
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
#lock   = 2
#relay  = 68
#led    = 71
#buzzer = 110
#door   = 13
#aux    = 14
#d0     = 3
#d1     = 6

dbpath = path.normpath(path.dirname(__file__) + '/../db/database.db')

conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row
# don't forget to close this, same for chip
