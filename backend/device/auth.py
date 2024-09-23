from db import conn
import broadcast

async def verify(code):
    if code.number is not None:
        row = conn.execute("""SELECT * FROM users
            WHERE card = ? AND facility = ?""", (code.number, code.facility)).fetchone()
    elif code.pin is not None:
        row = conn.execute('SELECT * FROM users WHERE pin = ?', (code.pin,)).fetchone()
    else:
        # don't even need the log otherwise, also prevents use of unassigned variable
        return False

    if row:
        await broadcast.event('INFO', 'Access granted for ' + row['name'])
        return True
    else:
        await broadcast.event('INFO', 'Access denied for ' + str(code))
        return False
