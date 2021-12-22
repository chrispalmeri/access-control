from datetime import datetime
from config import conn

app = None

def setup(parent):
    global app
    app = parent

async def event(channel, message):
    conn.execute("""INSERT INTO logs (time, level, message)
        VALUES (?,?,?)""", (
            datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            channel,
            message
        ))
    conn.commit()

    # Ping websockets about update
    if app:
        for ws in app['websockets']:
            # not currently happening, but you should check if it is not in process of closing
            # just in case of 'ConnectionResetError: Cannot write to closing transport'
            # see aiohttp docs for WebSocketResponse
            await ws.send_str('Logs updated')
