import logging
import asyncio
import gpiod

import config

class Reader():
    def __init__(self):
        self.alive = True

        self.d0 = config.chip.get_line(config.d0)
        self.d1 = config.chip.get_line(config.d1)

        self.lines = gpiod.LineBulk([self.d0, self.d1])
        self.lines.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN) # prevent initial interrupt
        self.lines.release()
        self.lines.request(consumer=config.name, type=gpiod.LINE_REQ_EV_FALLING_EDGE)

    def get_events(self):
        """
        specifically broken out to catch InterruptedError, cause even if
        you allow the task to keep running, somehow event_wait still gets
        interrupted by the Ctrl+C or term signal

        want to make sure you don't stop in the middle of a read

        wait time is very specific
        if it times out after 3ms that means the transmission is done
        it is also a max, will return sooner if there is an event
        """
        try:
            events = self.lines.event_wait(nsec=3000000)
        except InterruptedError:
            self.alive = False # ok fine you want to stop
            events = self.lines.event_wait(nsec=3000000) # but don't interrupt me
        return events

    async def read(self, app):
        """
        inifinite loop for weigand data

        tested with artificial delays in rest of app
        event_read will return queued events so you don't miss them
        but they might be out of order
        so need to save and sort, can't just bit shift them into a value

        (artificial 3s) delays in rest of app can cause keypresses to be combined
        example there could be 8 inturrupts queued up
        and the 3ms timeout would not split them
        maybe an argument against bit shifting if you need to count/split them later

        inital wait time is arbitrary
        long would affect responsiveness of reading
        long is probably blocking the rest of app
        short will use the event loop more frequently
        """
        while self.alive:
            events = self.get_events()
            data = []
            output = 0

            while events:
                for line in events:
                    event = line.event_read()
                    data.append(event)
                """
                check for next event immediately, no yield to event loop
                """
                events = self.get_events()
            else:
                # if data, sort it and return it
                # has nice benefit of returning output 0 properly
                if data:
                    data.sort(key=lambda x: x.sec * 1000000000 + x.nsec)
                    for obj in data:
                        # you don't need to bit shift if you don't want
                        # speed doesn't matter at this point vs clarity
                        if obj.source.offset() == self.d0.offset():
                            output = output << 1
                        elif obj.source.offset() == self.d1.offset():
                            output = output << 1 | 1
                    #print(output)
                    config.logger.debug(output)
                    # Ping websockets about log update
                    for ws in app['websockets']:
                        await ws.send_str('Logs updated')

            # just to mess with the reading
            # as a reliability test
            #logging.warning('sleeping')
            #await asyncio.sleep(3)
            await asyncio.sleep(0)
        else:
            print('reader stopped')

    async def startup(self, app):
        """ add it as a background task """
        print('reader startup signal')
        app['reader_task'] = asyncio.create_task(self.read(app))

    async def shutdown(self, app):
        """ remember this doesn't run til too late in package version """
        print('reader shutdown signal')
        self.alive = False
        await app['reader_task']
