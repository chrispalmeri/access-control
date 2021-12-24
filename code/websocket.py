from aiohttp import web, WSMsgType, WSCloseCode
import broadcast

async def get(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:

            # can also include `msg.data` if you want
            # should include ip
            await broadcast.event('DEBUG', 'Websocket client connected')

            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str('Received: ' + msg.data)
        elif msg.type == WSMsgType.ERROR:
            await broadcast.event('WARNING', 'Websocket connection closed with exception %s' % ws.exception())

    # actually not sure how it only comes to this block after close
    request.app['websockets'].remove(ws)
    await broadcast.event('DEBUG', 'Websocket client disconnected')

    return ws

async def shutdown(app):
    # cause of 'RuntimeError: Set changed size during iteration'
    # I think cause when you close it it triggers above to remove from set
    copy = app['websockets'].copy()
    for ws in copy:
        await ws.close()
