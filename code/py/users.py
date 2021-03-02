from aiohttp import web

class view(web.View):
    async def get(self):
        userid = self.request.match_info.get('id', None)
        if userid:
            data = {'message': 'GET request with id ' + userid}
        else:
            data = {'message': 'GET request'}
        return web.json_response(data)

    async def post(self):
        userid = self.request.match_info.get('id', None)
        #raise web.HTTPBadRequest()
        #raise web.HTTPMethodNotAllowed()
        data = {'message': 'POST request', "user": userid}
        return web.json_response(data)

    async def put(self):
        userid = self.request.match_info.get('id', None)
        data = {'message': 'PUT request', "user": userid}
        return web.json_response(data)

    async def delete(self):
        userid = self.request.match_info.get('id', None)
        data = {'message': 'DELETE request', "user": userid}
        return web.json_response(data, status=204)
