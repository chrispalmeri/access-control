import sys
import ssl
from os import path
from socket import socket
from aiohttp import web

import api.users
import api.events
import api.database
import api.auth
import api.card

from loop import Loop
from websocket import WebSocket
from session import Session
from middleware import api_auth_ware, http_error_ware

# custom 404 page
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares
# https://stackoverflow.com/questions/60588736/how-to-redirect-404-into-another-template-with-aiohttp

async def root_handler(request):
    cookie = request.cookies.get('__Host-Session')
    session = Session(cookie)

    if session.get('username') is None:
        # actually this can take relative path
        raise web.HTTPFound(request.url.with_path('/login'))
        # .update_query({'redir': request.url.path})

    resp = web.FileResponse(path.dirname(__file__) + '/static/index.html')
    resp.headers['Cache-Control'] = 'no-store, must-revalidate'
    # should you set the cookie again here?
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
    web.view('/card', api.card.View),
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

CERT_PATH = path.normpath(path.dirname(__file__) + '/../ssl/cert.pem')
KEY_PATH = path.normpath(path.dirname(__file__) + '/../ssl/key.pem')

ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(CERT_PATH, KEY_PATH)

if sys.stdout.isatty():
    web.run_app(app, host='0.0.0.0', port=8080, ssl_context=ssl_context) # command line
else:
    web.run_app(app, sock=socket(fileno=3), ssl_context=ssl_context) # systemd
    # 3 is just the first file descriptor systemd will use
    # (0, 1, 2 are stdin, stdout and stderr, normal linux stuff)
    # your whole socket thing may be roundabout, dunno
    # https://docs.python.org/3/library/ssl.html#ssl-contexts

# code here won't run til server stops
