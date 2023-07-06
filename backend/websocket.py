from aiohttp import web, WSMsgType, WSCloseCode
import broadcast
from session import Session

class WebSocket():
    def __init__(self, app):
        # cleanup websockets so it doesn't take 60 sec to restart
        app.on_shutdown.append(self.shutdown)

    async def get(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        # drop it if not logged in
        cookie = request.cookies.get('My-Session')
        session = Session(cookie)
        if session.get('username') is None:
            return await ws.close(code=WSCloseCode.POLICY_VIOLATION, message='login')

        broadcast.clients.add(ws)

        # should include ip
        await broadcast.event('DEBUG', 'Websocket client connected')

        async for msg in ws:

            # socket won't extend session, but api will...
            # also this kinda depends on the client
            if session.is_still_valid() is False:
                await ws.close(code=WSCloseCode.POLICY_VIOLATION, message='login')

            # if msg.type == WSMsgType.TEXT:
                # these were just for testing
                # if msg.data == 'ping':
                    # pass
                # else:
                    # await ws.send_str('Received: ' + msg.data)
            if msg.type == WSMsgType.ERROR:
                await broadcast.event('WARNING',
                    f'Websocket connection closed with exception {ws.exception()}')

        # actually not sure how it only comes to this block after close
        broadcast.clients.remove(ws)
        await broadcast.event('DEBUG', 'Websocket client disconnected')

    async def shutdown(self, _app):
        # cause of 'RuntimeError: Set changed size during iteration'
        # I think cause when you close it it triggers above to remove from set
        copy = broadcast.clients.copy()
        for ws in copy:
            await ws.close(code=WSCloseCode.SERVICE_RESTART)
