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
            # do things
            rawdata = reader.read()
            data = wiegand.parse(rawdata)
            if data is not None:
                config.logger.debug(str(data))

                # verify code
                valid = auth.verify(data)
                config.logger.debug('Access granted' if valid else 'Access denied')

                if valid:
                    entry.allow()

            inputchange = sensors.check()

            # cleanup
            outputchange = entry.secure()

            if data is not None or inputchange or outputchange:
                # Ping websockets about log update
                for ws in app['websockets']:
                    await ws.send_str('Logs updated')

            await asyncio.sleep(0)
        else:
            print('gracefully stopped')

    async def startup(self, app):
        print('start hardware loop')
        app['hardware_loop'] = asyncio.create_task(self.run(app))

    async def shutdown(self, app):
        print('stop hardware loop')
        state.loopRunning = False
        await app['hardware_loop']
