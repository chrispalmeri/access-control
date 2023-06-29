from aiohttp import web
from db import conn

class View(web.View):
    async def get(self):
        # add pages or record count to response?

        # you need to make a UI switch for this
        # can you make some kind of 'all' option?
        default_all = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        channels = self.request.query.getall('channel', default_all)
        limit = self.request.query.get('limit', '10')
        offset = self.request.query.get('offset', '0')

        placeholders = ','.join('?' for _ in channels) # becomes '?,?,?'

        query = f"""SELECT * FROM events
            WHERE channel IN ( {placeholders} )
            ORDER BY time DESC
            LIMIT ?
            OFFSET ?"""

        params = []
        params.extend(channels)
        params.append(limit)
        params.append(offset)

        rows = conn.execute(query, tuple(params)).fetchall()

        return web.json_response([dict(x) for x in rows])
