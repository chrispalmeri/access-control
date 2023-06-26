from os import path
import sqlite3

dbpath = path.normpath(path.dirname(__file__) + '/../db/database.db')

conn = sqlite3.connect(dbpath)
conn.row_factory = sqlite3.Row
