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
            data = wiegand.parse(rawdata)

            if data is not None:
                valid = auth.verify(data)

                if valid:
                    entry.allow()

            inputchange = sensors.check()
            outputchange = entry.secure()

            # a little agressive to use 'rawdata' instead of 'data' but not bad
            # gets wiegand errors to pop up, but also refreshes each keypress when entering pin
            if rawdata is not None or inputchange or outputchange:
                # Ping websockets about log update
                for ws in app['websockets']:
                    await ws.send_str('Logs updated')

            await asyncio.sleep(0)
        else:
            print('gracefully stopped')

    async def startup(self, app):
        config.logger.debug('Hardware loop startup')
        app['hardware_loop'] = asyncio.create_task(self.run(app))

    async def shutdown(self, app):
        config.logger.debug('Hardware loop shutdown')
        state.loopRunning = False
        await app['hardware_loop']
