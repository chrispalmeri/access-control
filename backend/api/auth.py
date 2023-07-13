from aiohttp import web

class View(web.View):
    """For /auth routes"""

    async def post(self):
        json = {}

        if self.request.body_exists:
            json = await self.request.json()

        session = self.request['session']
        # you really should regen the session before adding user to it
        session['username'] = json['username']

        resp = web.json_response({
            'success': True
        })

        return resp

    async def delete(self):
        self.request['session'].revoke()
        # would be better to replace session? if middleware can pass along

        raise web.HTTPNoContent()
