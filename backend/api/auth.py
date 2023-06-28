from aiohttp import web
from session import Session

class view(web.View):
    """For /auth routes"""

    async def post(self):
        json = {}

        if self.request.body_exists:
            json = await self.request.json()

        cookie = self.request.cookies.get('__Host-Session')

        session = Session(cookie)
        session['username'] = json['username']

        resp = web.json_response({
            'success': 'probably',
            'session_id': session.uuid,
            'session_data': dict(session)
        })

        resp.set_cookie('__Host-Session', session.uuid,
            #secure = True, # can't use yet
            httponly = True,
            samesite = 'Strict'
        )

        return resp
