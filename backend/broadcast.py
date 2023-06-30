from db import conn
import utils

# I don't remember why this isn't a custom logger

clients = set()

async def event(channel, message):
    conn.execute("""INSERT INTO events (time, channel, message)
        VALUES (?, ?, ?)""", (utils.iso_timestamp(), channel, message))

    # if sys.stdout.isatty():
        # print(message)

    # mqtt

    # Ping websockets about update
    for ws in clients:
        # not currently happening, but you should check if it is not in process of closing
        # just in case of 'ConnectionResetError: Cannot write to closing transport'
        # see aiohttp docs for WebSocketResponse
        await ws.send_str('New events available')
