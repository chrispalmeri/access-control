from logging import Handler
from datetime import datetime

class SQLiteHandler(Handler):
    def __init__(self, conn):
        Handler.__init__(self)
        self.conn = conn

    def emit(self, record):
        created = datetime.utcfromtimestamp(record.created).isoformat(timespec='milliseconds') + 'Z'

        self.conn.execute("""INSERT INTO logs (time, logger, level, message, file, line)
            VALUES (?,?,?,?,?,?)""", (
                created,
                record.name,
                record.levelname,
                record.msg,
                record.pathname,
                record.lineno
            ))
        self.conn.commit()
