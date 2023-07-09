from os import path
from aiohttp import web
from session import Session

async def handle_404(_request):
    return web.FileResponse(path.dirname(__file__) + '/static/404.html', status=404)

async def handle_500(_request):
    return web.FileResponse(path.dirname(__file__) + '/static/500.html', status=500)

# https://us-pycon-2019-tutorial.readthedocs.io/aiohttp_middlewares.html
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares

async def api_auth(request, handler):
    # now I'm not sure about having that be an html page
    if request.path == '/api':
        return await handler(request)

    cookie = request.cookies.get('__Host-Session')
    session = Session(cookie)

    try:
        if session.get('username') or request.path == '/api/auth':
            request['session'] = session
            response = await handler(request)
        else:
            raise web.HTTPForbidden()
    except web.HTTPException as exc: # all http errors
        response = web.json_response({
            'code': exc.status,
            'message': exc.reason
        }, status = exc.status)

        # you were losing the Allow header here
        # feels bad hardcoding it
        if 'Allow' in exc.headers:
            response.headers['Allow'] = exc.headers['Allow']

    # name '__Host-Session' and option 'secure = True' only work with https
    response.set_cookie('__Host-Session', session.uuid,
        secure = True,
        httponly = True,
        samesite = 'Strict'
    )
    return response

# equivalent to using decorator
api_auth_ware = web.middleware(api_auth)

# https://docs.aiohttp.org/en/stable/web_quickstart.html?highlight=httpnotfound#exceptions

async def http_error(request, handler):
    try:
        return await handler(request)
    except web.HTTPNotFound: # specifically 404
        return await handle_404(request)
    except web.HTTPServerError: # all 50x errors
        return await handle_500(request)

    # would like to fallback to original response if possible

http_error_ware = web.middleware(http_error)
