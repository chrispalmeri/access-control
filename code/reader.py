import logging
import asyncio
import gpiod

import config

if config.chip:
    d0 = config.chip.get_line(config.d0)
    d1 = config.chip.get_line(config.d1)

    lines = gpiod.LineBulk([d0, d1])
    lines.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN) # prevent initial interrupt
    lines.release()
    lines.request(consumer=config.name, type=gpiod.LINE_REQ_EV_FALLING_EDGE)

async def read(app):
    """
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
    events = lines.event_wait(nsec=3000000) # could catch InterruptedError here
    data = []
    output = 0

    while events:
        for line in events:
            event = line.event_read()
            data.append(event)

        """
        check for next event immediately, no yield to event loop
        this wait time is very specific
        if it times out after 3ms that means the transmission is done
        it is also a max, will return sooner if there is an event
        """
        events = lines.event_wait(nsec=3000000)
    else:
        # if data, sort it and return it
        # has nice benefit of returning output 0 properly
        if data:
            data.sort(key=lambda x: x.sec * 1000000000 + x.nsec)
            for obj in data:
                # you don't need to bit shift if you don't want
                # speed doesn't matter at this point vs clarity
                if obj.source.offset() == d0.offset():
                    output = output << 1
                elif obj.source.offset() == d1.offset():
                    output = output << 1 | 1
            #print(output)
            config.logger.debug(output)
            # Ping websockets about log update
            for ws in app['websockets']:
                await ws.send_str('Logs updated')

async def background_task(app):
    try:
        while True:
            try:
                await read(app)
            except InterruptedError:
                logging.warning('gpio task interrupted')

            # just to mess with the reading
            # as a reliability test
            #logging.warning('sleeping')
            #await asyncio.sleep(3)
            await asyncio.sleep(0)

            #logging.warning('background stuff')
            # Forward message to all connected websockets:
            #for ws in app['websockets']:
                #await ws.send_str('Hello Client')
    except asyncio.CancelledError:
        logging.warning('reader task cancelled')
    finally:
        logging.warning('Goodbye')

async def startup(app):
    app['my_task'] = asyncio.create_task(background_task(app))

async def cleanup(app):
    app['my_task'].cancel()
    await app['my_task']
