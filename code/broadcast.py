from datetime import datetime
from db import conn

app = None

def setup(parent):
    global app
    app = parent

def saveMessage(channel, message):
    conn.execute("""INSERT INTO events (time, channel, message)
        VALUES (?,?,?)""", (
            datetime.utcnow().isoformat(timespec='milliseconds') + 'Z',
            channel,
            message
        )
    )
    conn.commit()

def createTable():
    conn.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        time TEXT,
        channel TEXT,
        message TEXT
    )""")
    saveMessage('DEBUG', 'Created events table')

async def event(channel, message):
    try:
        saveMessage(channel, message)
    except Exception as e:
        # Exception > sqlite3.Error > sqlite3.DatabaseError > sqlite3.OperationalError
        if str(e) == 'no such table: events':
            createTable()
            saveMessage(channel, message)
        else:
            raise e

    # Ping websockets about update
    if app:
        for ws in app['websockets']:
            # not currently happening, but you should check if it is not in process of closing
            # just in case of 'ConnectionResetError: Cannot write to closing transport'
            # see aiohttp docs for WebSocketResponse
            await ws.send_str('New events available')
