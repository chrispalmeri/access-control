from aiohttp import web

class MyView(web.View):
    async def get(self):
        name = self.request.match_info.get('name', None) # second arg is default value I guess
        data = {'some': 'data', "name": name}
        return web.json_response(data)

    async def post(self):
        #return await post_resp(self.request) # if you wanna call some other function
        return web.Response(text="Hello")
