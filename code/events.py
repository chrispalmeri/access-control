from aiohttp import web

from config import conn

class view(web.View):
    async def get(self):
            rows = conn.execute('SELECT * FROM logs').fetchall()
            return web.json_response([dict(x) for x in rows])
