from aiohttp import web
import config

class View(web.View):
    """For /database routes"""

    async def get(self):
        resp = web.FileResponse(path=config.DBPATH)
        resp.content_type = 'application/vnd.sqlite3'
        return resp

    async def post(self):
        # not ideal https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads
        data = await self.request.post()

        # not doing any error checking
        newfile = data['file'].file
        filename = data['file'].filename

        # check data starts with 'SQLite format 3'
        start = newfile.read(15).decode('utf-8')
        newfile.seek(0) # reset to beginning of file

        if start != 'SQLite format 3':
            raise web.HTTPUnprocessableEntity() #422

        # save it to filesystem
        with open(config.DBPATH, 'wb') as oldfile:
            oldfile.write(newfile.read())

        return web.json_response({'success': f'Restored from {filename}'})
