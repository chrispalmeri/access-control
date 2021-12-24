from aiohttp import web

from config import conn

class view(web.View):
    async def get(self):
        # you need to make a UI switch for this
        #rows = conn.execute('SELECT * FROM events WHERE channel != ? ORDER BY time DESC LIMIT 20', ('DEBUG',)).fetchall()
        rows = conn.execute('SELECT * FROM events ORDER BY time DESC LIMIT 20').fetchall()
        return web.json_response([dict(x) for x in rows])
