import sys
from os import path
from socket import socket
from aiohttp import web

import config
import api.users
import api.events
import websocket

from logger import Logger

from loop import Loop
loop = Loop()

# custom 404 page
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares

async def root_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/static/index.html')

app = web.Application()
app['websockets'] = set()

config.myLog = Logger(app, config.conn)

# add trailing slash seperatley if you want it
app.add_routes([
    web.view('/api/users', api.users.view),
    web.view('/api/users/{id}', api.users.view),
    web.view('/api/events', api.events.view),
    web.get('/ws', websocket.get),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/static') # needs to be last
])

# cleanup websockets so it doesn't take 60 sec to restart
app.on_shutdown.append(websocket.shutdown)

# avoid all the weigand stuff if no gpio, eg vagrant
if config.chip:
    app.on_startup.append(loop.startup)
    app.on_shutdown.append(loop.shutdown)

# logger (MyLoggerName) does not emit to console initially
# but once you have used logging (root) then it starts
#import logging
#logging.warning('test')
#config.logger.debug('startup')
# INTERESTING that might be a transient thing? SQLite saves loop startup log that is missing in journalctl
# oh no, still an issue, nothing from customer logger goes to journalctl unless you use a defautl logger first
# switched websocket connection from defautl logger and see issue again
# although I don't really care if SQL has the logs?

# I think you didn't get a SQL startup log on a cold boot though
# test that

if len(sys.argv) > 1:
    web.run_app(app, host='localhost', port=8080) # command line
else:
    web.run_app(app, sock=socket(fileno=3)) # systemd

# code here won't run til server stops
