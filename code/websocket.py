from aiohttp import web, WSMsgType
import config

async def get(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:

            #config.logger.warning(msg.data)
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
