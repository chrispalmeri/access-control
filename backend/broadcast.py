from db import conn
import utils

app = None

def setup(parent):
    global app
    app = parent

async def event(channel, message):
    conn.execute("""INSERT INTO events (time, channel, message)
        VALUES (?, ?, ?)""", (utils.iso_timestamp(), channel, message))

    # Ping websockets about update
    if app:
        for ws in app['websockets']:
            # not currently happening, but you should check if it is not in process of closing
            # just in case of 'ConnectionResetError: Cannot write to closing transport'
            # see aiohttp docs for WebSocketResponse
            await ws.send_str('New events available')
