import wiegand
from config import conn, logger

def verify(code):
    if isinstance(code, wiegand.Card):
        row = conn.execute('SELECT * FROM users WHERE card = ? AND facility = ?', (code.number, code.facility)).fetchone()
    elif isinstance(code, str):
        row = conn.execute('SELECT * FROM users WHERE pin = ?', (code,)).fetchone()
        # either Pin should also be an object with a str method like Card
        # or you should just construct both strings here, so it will say 'Pin: 1234'

    if row:
        logger.info('Access granted for ' + row['name'])
        return True
    else:
        logger.info('Access denied for ' + str(code))
        return False
