from os import path
import gpiod
import sqlite3
import logging
import sqlite_handler

try:
    chip = gpiod.Chip('gpiochip0')
except FileNotFoundError:
    chip = None

name = 'doorctl'

lock   = 2
relay  = 68
led    = 71
buzzer = 110
door   = 13
aux    = 14
d0     = 3
d1     = 6

dbpath = path.normpath(path.dirname(__file__) + '/../db/database.db')

conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row
# don't forget to close this, same for chip

logger = logging.getLogger('MyLoggerName')
logger.setLevel(logging.DEBUG)
logger.addHandler(sqlite_handler.SQLiteHandler(conn))
