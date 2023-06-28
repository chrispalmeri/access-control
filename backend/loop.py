import asyncio
from device import auth, sensors, entry, reader, wiegand
import broadcast
import state
import session

class Loop():
    def __init__(self, app):
        app.on_startup.append(self.startup)
        app.on_shutdown.append(self.shutdown)

    async def run(self, app):
        while state.loopRunning:
            rawdata = reader.read()
            data = await wiegand.parse(rawdata)

            if data is not None:
                valid = await auth.verify(data)

                if valid:
                    entry.allow()

            await sensors.check()
            await entry.secure()

            session.gc()

            await asyncio.sleep(0)
        else:
            await broadcast.event('DEBUG', 'Hardware loop gracefully stopped')

    async def startup(self, app):
        await broadcast.event('DEBUG', 'Hardware loop startup')
        app['hardware_loop'] = asyncio.create_task(self.run(app))

    async def shutdown(self, app):
        await broadcast.event('DEBUG', 'Hardware loop shutdown')
        state.loopRunning = False
        await app['hardware_loop']
