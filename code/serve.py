from os import path
import logging
import asyncio
from aiohttp import web
import gpiod
import socket
import websocket
import users
import events

try:
    chip = gpiod.Chip('gpiochip0')

    d0 = chip.get_line(3)
    d1 = chip.get_line(6)

    lines = gpiod.LineBulk([d0, d1])
    lines.request(consumer='doorctl', type=gpiod.LINE_REQ_DIR_IN) # prevent initial interrupt
    lines.release()
    lines.request(consumer='doorctl', type=gpiod.LINE_REQ_EV_FALLING_EDGE)
except FileNotFoundError:
    chip = None
    print('No GPIO detected')

def read():
    # tested with artificial delays in rest of app
    # event_read will return queued events so you don't miss them
    # but they might be out of order
    # so need to save and sort, can't just bit shift them into a value

    # (artificial 3s) delays in rest of app can cause keypresses to be combined
    # example there could be 8 inturrupts queued up
    # and the 3ms timeout would not split them
    # maybe an argument against bit shifting if you need to count/split them later

    # inital wait time is arbitrary
    # long would affect responsiveness of reading
    # long is probably blocking the rest of app
    # short will use the event loop more frequently
    events = lines.event_wait(nsec=3000000) # need to catch InterruptedError here
    data = []
    output = 0

    while events:
        for line in events:
            event = line.event_read()
            data.append(event)

        # check for next event immediately, no yield to event loop
        # this wait time is very specific
        # if it times out after 3ms that means the transmission is done
        # it is also a max, will return sooner if there is an event
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
            print(output)


# https://docs.aiohttp.org/en/stable/web.html
# https://github.com/aio-libs/aiohttp/issues/1220

# custom 404 page
# https://aiohttp-demos.readthedocs.io/en/latest/tutorial.html#aiohttp-demos-polls-middlewares

async def root_handler(request):
    return web.FileResponse(path.dirname(__file__) + '/static/index.html')

app = web.Application()

# add trailing slash seperatley if you want it
app.add_routes([
    web.view('/api/users', users.view),
    web.view('/api/users/{id}', users.view),
    web.view('/api/events', events.view),
    web.get('/ws', websocket.get),
    web.get('/', root_handler),
    web.static('/', path.dirname(__file__) + '/static') # needs to be last
])

async def background_task(app):
    try:
        while True:
            read()

            # just to mess with the reading
            # as a reliability test
            logging.warning('sleeping')
            await asyncio.sleep(3)

            #logging.warning('background stuff')
            # Forward message to all connected websockets:
            #for ws in app['websockets']:
                #await ws.send_str('Hello Client')
    except asyncio.CancelledError:
        pass
    finally:
        logging.warning('Goodbye')

async def start_background_tasks(app):
    app['my_task'] = asyncio.create_task(background_task(app))

async def cleanup_background_tasks(app):
    app['my_task'].cancel()
    await app['my_task']

# avoid all the weigand stuff if no gpio, eg vagrant
if chip:
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

app['websockets'] = set()

if __name__ == '__main__':
    sock = socket.socket(fileno=3)
    web.run_app(app, sock=sock)
