import wiegand
from db import conn
import broadcast

async def verify(code):
    if isinstance(code, wiegand.Card):
        row = conn.execute('SELECT * FROM users WHERE card = ? AND facility = ?', (code.number, code.facility)).fetchone()
    elif isinstance(code, str):
        row = conn.execute('SELECT * FROM users WHERE pin = ?', (code,)).fetchone()
        # either Pin should also be an object with a str method like Card
        # or you should just construct both strings here, so it will say 'Pin: 1234'

    if row:
        await broadcast.event('INFO', 'Access granted for ' + row['name'])
        return True
    else:
        await broadcast.event('INFO', 'Access denied for ' + str(code))
        return False
