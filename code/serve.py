import sys
from os import path
from socket import socket
from aiohttp import web

import config
import api.users
import api.events
import api.database
import websocket
import broadcast

from loop import Loop
loop = Loop()

# custom 404 page (also should be consistent with svelte-spa-router 404 page)
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares
# https://stackoverflow.com/questions/60588736/how-to-redirect-404-into-another-template-with-aiohttp

async def root_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/www/index.html')
async def api_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/www/api/index.html')

app = web.Application()
app['websockets'] = set()

broadcast.setup(app)

# add trailing slash seperatley if you want it
app.add_routes([
    web.view('/api/users', api.users.view),
    web.view('/api/users/{id}', api.users.view),
    web.view('/api/events', api.events.view),
    web.view('/api/database', api.database.view),
    web.get('/ws', websocket.get),
    web.get('/api', api_handler),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/www') # needs to be last
])

# cleanup websockets so it doesn't take 60 sec to restart
app.on_shutdown.append(websocket.shutdown)

app.on_startup.append(loop.startup)
app.on_shutdown.append(loop.shutdown)

if len(sys.argv) > 1:
    web.run_app(app, host='localhost', port=8080) # command line
else:
    web.run_app(app, sock=socket(fileno=3)) # systemd

# code here won't run til server stops
