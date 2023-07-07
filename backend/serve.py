import sys
from os import path
from socket import socket
from aiohttp import web

import api.users
import api.events
import api.database
import api.auth

from loop import Loop
from websocket import WebSocket
from session import Session
from middleware import api_auth_ware, http_error_ware

# custom 404 page
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares
# https://stackoverflow.com/questions/60588736/how-to-redirect-404-into-another-template-with-aiohttp


async def root_handler(request):
    cookie = request.cookies.get('My-Session')
    session = Session(cookie)

    if session.get('username') is None:
        raise web.HTTPFound(request.url.with_path('/login'))
        # .update_query({'redir': request.url.path})

    resp = web.FileResponse(path.dirname(__file__) + '/static/index.html')
    resp.headers['Cache-Control'] = 'no-store, must-revalidate'
    return resp

async def api_handler(_request):
    return web.FileResponse(path.dirname(__file__) + '/static/api/index.html')

async def login_handler(_request):
    return web.FileResponse(path.dirname(__file__) + '/static/login.html')

app = web.Application(middlewares=[http_error_ware])
loop = Loop(app)
websocket = WebSocket(app)

api_app = web.Application(middlewares=[api_auth_ware])

api_app.add_routes([
    web.view('/users', api.users.View),
    web.view('/users/{id}', api.users.View),
    web.view('/events', api.events.View),
    web.view('/database', api.database.View),
    web.view('/auth', api.auth.View),
    web.get('', api_handler)
    # parent static doesn't work
])

app.add_subapp('/api/', api_app)

# HAS to come after subapp for some reason, else subapp not working
# add trailing slash seperatley if you want it
app.add_routes([
    web.get('/ws', websocket.get),
    web.get('/login', login_handler),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/static') # needs to be last
])

if sys.stdout.isatty():
    web.run_app(app, host='0.0.0.0', port=8080) # command line
else:
    web.run_app(app, sock=socket(fileno=3)) # systemd

# code here won't run til server stops
