import sqlite3
import config

class Db:
    def __init__(self, file):
        self.file = file
        self.open()

    def open(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row

        self.conn.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            time TEXT,
            channel TEXT,
            message TEXT
        )""")

        # broadcasting would be circular, but could directly insert event
        # that table was recreated, same for users and admin created
        # with same not exists clauses

        self.conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            pin TEXT,
            card INTEGER,
            facility INTEGER
        )""")

        self.conn.execute("""INSERT INTO users (name, pin)
        SELECT 'Admin', '1234'
        WHERE NOT EXISTS (SELECT * FROM users)""")

        self.conn.execute("""CREATE TABLE IF NOT EXISTS sessions (
            uuid TEXT NOT NULL PRIMARY KEY,
            access TEXT,
            data TEXT
        )""")

    def reopen(self):
        self.conn.close()
        self.open()

    def execute(self, query, params=()):
        try:
            res = self.conn.execute(query, params)
            self.conn.commit() # no-op if unneeded
        except sqlite3.Error as err:
            # Exception > sqlite3.Error > sqlite3.DatabaseError > sqlite3.OperationalError
            if str(err).startswith((
                    'no such table',
                    'attempt to write a readonly',
                    'Cannot operate on a closed'
                )):
                self.reopen()
                res = self.conn.execute(query, params)
                self.conn.commit()
            else:
                raise err

        return res

conn = Db(config.DBPATH)
