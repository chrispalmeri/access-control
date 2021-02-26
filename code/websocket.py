
from aiohttp import web, WSMsgType
import logging

#app.add_routes([web.get('/ws', websocket_handler)])

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].add(ws)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:

            logging.warning(msg.data)

            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str('Received: ' + msg.data)
        elif msg.type == WSMsgType.ERROR:
            logging.error('ws connection closed with exception %s' %
                  ws.exception())

    # actually not sure how it only comes to this block after close
    logging.warning('websocket connection closed')
    request.app['websockets'].remove(ws)

    return ws
