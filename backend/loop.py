import asyncio
from device import auth, sensors, entry, reader, wiegand
import broadcast
import session

class Loop():
    def __init__(self, app):
        self.loop_running = False
        self.task = None
        app.on_startup.append(self.startup)
        app.on_shutdown.append(self.shutdown)

    async def run(self, _app):
        while self.loop_running:
            rawdata = reader.read()
            data = await wiegand.parse(rawdata)

            if data is not None:
                valid = await auth.verify(data)

                if valid:
                    entry.allow()

            await sensors.check()
            await entry.secure()

            session.garbage_collect()

            await asyncio.sleep(0)

        # else:
        await broadcast.event('DEBUG', 'Hardware loop gracefully stopped')

    async def startup(self, app):
        await broadcast.event('DEBUG', 'Hardware loop startup')
        self.loop_running = True
        self.task = asyncio.create_task(self.run(app))

    async def shutdown(self, _app):
        await broadcast.event('DEBUG', 'Hardware loop shutdown')
        self.loop_running = False
        await self.task
