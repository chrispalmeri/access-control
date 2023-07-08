from aiohttp import WSCloseCode
from db import conn
import utils

# I don't remember why this isn't a custom logger

clients = []

async def event(channel, message):
    conn.execute("""INSERT INTO events (time, channel, message)
        VALUES (?, ?, ?)""", (utils.iso_timestamp(), channel, message))

    # if sys.stdout.isatty():
        # print(message)

    # mqtt

    # Ping websockets about update
    # print(len(clients)) # temporary
    expired = []
    failed = []

    for ws in clients:
        if ws['session'].is_still_valid() is False:
            expired.append(ws)
        else:
            # in case of 'ConnectionResetError: Cannot write to closing transport'
            # not really sure how long 'in process of closing' lasts after cable
            # disconnect. somehow it was still possible to sometimes get the error
            # though even when using `if not ws.closed:`

            # but now I can't get the error to happen to test the new handling,
            # orphaned connections just keep getting sent messages
            # until close() when session expires
            try:
                await ws.send_str('New events available')
            except ConnectionResetError:
                failed.append(ws)

    # remove first so don't get same issue when broadcasting disconnect event
    for item in [*expired, *failed]:
        clients.remove(item)

    for exp in expired:
        await exp.close(code=WSCloseCode.POLICY_VIOLATION, message='login')

    for fail in failed:
        # so far has not needed try
        await fail.close()
