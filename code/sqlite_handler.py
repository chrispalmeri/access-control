import logging
import os
from datetime import datetime

class SQLiteHandler(logging.Handler):
    def __init__(self, conn):
        logging.Handler.__init__(self)
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
