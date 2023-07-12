from aiohttp import web
from db import conn

class View(web.View):
    async def get(self):
        # 'Access denied for Card: xxxxx Facility: xxx'
        # is parsing it from the logs really the best way?
        # what if it was a long time ago? or was since assigned to a user?
        row = conn.execute("""SELECT * FROM events
            WHERE message LIKE 'Access denied for Card%'
            ORDER BY time DESC
            LIMIT 1""").fetchone()
        if row:
            return web.json_response(dict(row))
        else:
            raise web.HTTPNotFound()
