from aiohttp import web, WSMsgType, WSCloseCode
import config

async def get(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:

            #config.logger.warning(msg.data)
            # should include ip and broadcast to all clients
            config.logger.debug('Websocket client connected')

            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str('Received: ' + msg.data)
        elif msg.type == WSMsgType.ERROR:
            config.logger.warning('Websocket connection closed with exception %s' % ws.exception())

    # actually not sure how it only comes to this block after close
    config.logger.debug('Websocket client disconnected')
    request.app['websockets'].remove(ws)

    return ws

async def shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')
