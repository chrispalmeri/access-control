from aiohttp import web

from config import conn, logger

# should try catch the json parsing
# has no type checking of json values
# would seperate views for /users and /users/{id} be better

class view(web.View):
    """For /users and /users/{id} routes"""

    async def get(self):
        userid = self.request.match_info.get('id', None)
        if userid:
            row = conn.execute('SELECT * FROM users WHERE id = ?', (userid,)).fetchone()
            if row:
                return web.json_response(dict(row))
            else:
                raise web.HTTPNotFound()
        else:
            rows = conn.execute('SELECT * FROM users').fetchall()
            return web.json_response([dict(x) for x in rows])

    async def post(self):
        userid = self.request.match_info.get('id', None)
        if userid:
            raise web.HTTPMethodNotAllowed('POST', ['GET', 'PUT', 'DELETE'])

        if self.request.body_exists:
            json = await self.request.json()
        else:
            json = {}

        # merge default values with received values
        # so there is nothing missing for the sql binding
        temp = {'name': None, 'pin': None, 'card': None, 'facility': None}
        temp.update((key, value) for key, value in json.items() if key in temp.keys())

        if temp.get('name') == None:
            raise web.HTTPUnprocessableEntity() #422

        try:
            userid = conn.execute("""INSERT INTO users ( name, pin, card, facility )
                VALUES ( :name, :pin, :card, :facility )""", temp).lastrowid
            conn.commit()

            # Log it
            logger.debug(f'User {userid} created')

            # Ping websockets about log update
            for ws in self.request.app['websockets']:
                await ws.send_str('Logs updated')

            return web.json_response({'id': userid, **temp})
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

    async def put(self):
        """btw you have no type checking, but it's fine
        SELECT seems like overkill, but it was hard to dynamically generate
        UPDATE statement with optional columns, same for POST
        """

        userid = self.request.match_info.get('id', None)
        if userid is None:
            raise web.HTTPMethodNotAllowed('PUT', ['GET', 'POST'])
        row = conn.execute('SELECT * FROM users WHERE id = ?', (userid,)).fetchone()

        if row is None:
            raise web.HTTPNotFound()
        temp = dict(row)

        if self.request.body_exists is False:
            raise web.HTTPUnprocessableEntity()
        json = await self.request.json()

        json.pop('id', None) # id is valid key, but don't want it changed from body
        temp.update((key, value) for key, value in json.items() if key in temp.keys())

        try:
            count = conn.execute("""UPDATE users SET
                name = :name,
                pin = :pin,
                card = :card,
                facility = :facility
                WHERE id = :id""", temp).rowcount
            # not checking count before returning, but you did already do a select
            return web.json_response(temp)
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

    async def delete(self):
        userid = self.request.match_info.get('id', None)
        if userid is None:
            raise web.HTTPMethodNotAllowed('DELETE', ['GET', 'POST'])

        try:
            count = conn.execute('DELETE FROM users WHERE id = ?', (userid,)).rowcount
            conn.commit()
            # you could return count if you wanted
        except Exception as e:
            return web.json_response({'error': str(e)}, status=500)

        raise web.HTTPNoContent()