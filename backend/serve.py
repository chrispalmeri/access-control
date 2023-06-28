import sys
from os import path
from socket import socket
from aiohttp import web

import api.users
import api.events
import api.database
import api.auth
import broadcast

from loop import Loop
from websocket import WebSocket

# custom 404 page (also should be consistent with svelte-spa-router 404 page)
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares
# https://stackoverflow.com/questions/60588736/how-to-redirect-404-into-another-template-with-aiohttp

async def root_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/static/index.html')
async def api_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/static/api/index.html')

app = web.Application()
loop = Loop(app)
websocket = WebSocket(app)

broadcast.setup(app)

# add trailing slash seperatley if you want it
app.add_routes([
    web.view('/api/users', api.users.view),
    web.view('/api/users/{id}', api.users.view),
    web.view('/api/events', api.events.view),
    web.view('/api/database', api.database.view),
    web.view('/api/auth', api.auth.view),
    web.get('/ws', websocket.get),
    web.get('/api', api_handler),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/static') # needs to be last
])

if len(sys.argv) > 1:
    web.run_app(app, host='localhost', port=8080) # command line
else:
    web.run_app(app, sock=socket(fileno=3)) # systemd

# code here won't run til server stops