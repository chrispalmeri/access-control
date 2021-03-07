import sys
from os import path
from socket import socket
from aiohttp import web

import config
import reader
import users
import events
import websocket

# custom 404 page
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares

async def root_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/static/index.html')

app = web.Application()
app['websockets'] = set()

# add trailing slash seperatley if you want it
app.add_routes([
    web.view('/api/users', users.view),
    web.view('/api/users/{id}', users.view),
    web.view('/api/events', events.view),
    web.get('/ws', websocket.get),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/static') # needs to be last
])

# avoid all the weigand stuff if no gpio, eg vagrant
if config.chip:
    app.on_startup.append(reader.startup)
    app.on_cleanup.append(reader.cleanup)

# logger (MyLoggerName) does not emit to console initially
# but once you have used logging (root) then it starts
#import logging
#logging.warning('test')
#config.logger.debug('startup')

if len(sys.argv) > 1:
    web.run_app(app, host='localhost', port=8080) # command line
else:
    web.run_app(app, sock=socket(fileno=3)) # systemd

# code here won't run til server stops
