# other option apt install python3-aiohttp-session
# https://github.com/aio-libs/aiohttp-session
# but would have to write your own sqlite handler, so skipping it

# this should be a middleware probably
# you should make more of your things async across the board btw

import uuid
import json
from datetime import datetime
from db import conn
from collections import UserDict
import time

# other columns to consider:
# created_date
# auth_date
# last_ip

class Session(UserDict):
    def __init__(self, cookie):
        super().__init__()
        self.access = datetime.utcnow().isoformat(timespec='milliseconds') + 'Z'

        if cookie:
            self.uuid = cookie
            row = conn.execute('SELECT * FROM sessions WHERE uuid = :uuid', vars(self)).fetchone()

        if row:
            # don't even read access
            self.json = row['data']
            self.data = json.loads(self.json)

            conn.execute("""UPDATE sessions SET
                access = :access
                WHERE uuid = :uuid""", vars(self))

            return

        self.uuid = str(uuid.uuid4())
        self.json = json.dumps(self.data)

        ins = conn.execute("""INSERT INTO sessions ( uuid, access, data )
            VALUES ( :uuid, :access, :json )""", vars(self)).lastrowid

    def __setitem__(self, key, value):
        self.data[key] = value
        self.json = json.dumps(self.data)

        # don't even write access
        count = conn.execute("""UPDATE sessions SET
            data = :json
            WHERE uuid = :uuid""", vars(self)).rowcount

    # not doing anything special so no need to overwrite
    #def __getitem__(self, key):
        #return self.data[key]

# probably move to config
maxlifetime = 300 # 5 minutes
gc_interval = 60 # 1 minute
last_gc = 0

def gc():
    global last_gc
    now = time.time()

    # this won't expire a frequently used session btw
    # not til it is unused for 5 minutes
    if now - last_gc > gc_interval:
        last_gc = now

        count = conn.execute("""DELETE FROM sessions
            WHERE strftime('%s', 'now') - strftime('%s', access) > ?""", (maxlifetime,)).rowcount
