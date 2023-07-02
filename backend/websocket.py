from aiohttp import web, WSMsgType, WSCloseCode
import broadcast

class WebSocket():
    def __init__(self, app):
        # cleanup websockets so it doesn't take 60 sec to restart
        app.on_shutdown.append(self.shutdown)

    async def get(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        broadcast.clients.add(ws)

        # should include ip
        await broadcast.event('DEBUG', 'Websocket client connected')

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                # is this close fake?
                if msg.data == 'close':
                    await ws.close()
                # these were just for testing
                # elif msg.data == 'ping':
                    # pass
                # else:
                    # await ws.send_str('Received: ' + msg.data)
            elif msg.type == WSMsgType.ERROR:
                await broadcast.event('WARNING',
                    f'Websocket connection closed with exception {ws.exception()}')

        # actually not sure how it only comes to this block after close
        broadcast.clients.remove(ws)
        await broadcast.event('DEBUG', 'Websocket client disconnected')

        return ws

    async def shutdown(self, _app):
        # cause of 'RuntimeError: Set changed size during iteration'
        # I think cause when you close it it triggers above to remove from set
        copy = broadcast.clients.copy()
        for ws in copy:
            await ws.close()
