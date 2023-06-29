from aiohttp import web
from db import conn

class View(web.View):
    async def get(self):
        # add pages or record count to response?

        # you need to make a UI switch for this
        # can you make some kind of 'all' option?
        channels = self.request.query.getall('channel', ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
        limit = self.request.query.get('limit', '10')
        offset = self.request.query.get('offset', '0')

        # becomes '?, ?, ?'
        placeholders = ', '.join('?' for unused in channels)
        query = 'SELECT * FROM events WHERE channel IN (' + placeholders + ') ORDER BY time DESC LIMIT ? OFFSET ?'

        params = []
        params.extend(channels)
        params.append(limit)
        params.append(offset)

        rows = conn.execute(query, tuple(params)).fetchall()
        return web.json_response([dict(x) for x in rows])
