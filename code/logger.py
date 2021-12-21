from datetime import datetime

class Logger():
    def __init__(self, app, conn):
        self.conn = conn
        self.app = app

    async def log(self, level, msg):

        self.conn.execute("""INSERT INTO logs (time, level, message)
            VALUES (?,?,?)""", (
                datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
                level,
                msg
            ))
        self.conn.commit()

        # Ping websockets about log update
        for ws in self.app['websockets']:
            await ws.send_str('Logs updated')
