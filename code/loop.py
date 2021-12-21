import asyncio
import sensors
import entry
import reader
import wiegand
import config
import state
import auth

class Loop():
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

            await asyncio.sleep(0)
        else:
            print('gracefully stopped')

    async def startup(self, app):
        await config.myLog.log('DEBUG', 'Hardware loop startup')
        app['hardware_loop'] = asyncio.create_task(self.run(app))

    async def shutdown(self, app):
        await config.myLog.log('DEBUG', 'Hardware loop shutdown')
        state.loopRunning = False
        await app['hardware_loop']
