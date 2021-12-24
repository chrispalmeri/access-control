from aiohttp import web
import config

class view(web.View):
    """For /database routes"""

    async def get(self):
        return web.FileResponse(path=config.dbpath)

    async def post(self):
        # not ideal https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
        data = await self.request.post()

        # not doing any error checking
        newfile = data['file'].file
        filename = data['file'].filename

        # save it to filesystem
        with open(config.dbpath, 'wb') as oldfile:
            oldfile.write(newfile.read())

        return web.Response(text='Restored {}'.format(filename))
