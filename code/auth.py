import wiegand
import config

async def verify(code):
    if isinstance(code, wiegand.Card):
        row = config.conn.execute('SELECT * FROM users WHERE card = ? AND facility = ?', (code.number, code.facility)).fetchone()
    elif isinstance(code, str):
        row = config.conn.execute('SELECT * FROM users WHERE pin = ?', (code,)).fetchone()
        # either Pin should also be an object with a str method like Card
        # or you should just construct both strings here, so it will say 'Pin: 1234'

    if row:
        await config.myLog.log('INFO', 'Access granted for ' + row['name'])
        return True
    else:
        await config.myLog.log('INFO', 'Access denied for ' + str(code))
        return False
