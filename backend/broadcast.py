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
        # check if it is not in process of closing
        # in case of 'ConnectionResetError: Cannot write to closing transport'
        # not really sure how long 'in process of closing' lasts after cable
        # disconnect, but maybe don't care if there is minimal overhead
        if not ws.closed:
            await ws.send_str('New events available')
