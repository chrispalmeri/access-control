import gpiod
import config
import state

d0 = config.chip.get_line(config.d0)
d1 = config.chip.get_line(config.d1)

lines = gpiod.LineBulk([d0, d1])
lines.request(consumer=config.name, type=gpiod.LINE_REQ_DIR_IN) # prevent initial interrupt
lines.release()
lines.request(consumer=config.name, type=gpiod.LINE_REQ_EV_FALLING_EDGE)

def get_events():
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
        events = lines.event_wait(nsec=3000000)
    except InterruptedError:
        state.LoopRunning = False
        events = lines.event_wait(nsec=3000000) # don't interrupt me
    return events

def read():
    """
    inifinite loop for weigand data

    tested with artificial delays in rest of app
    event_read will return queued events so you don't miss them
    but they might be out of order, so need to save and sort
    also keypresses might be combined
    example there could be 8 inturrupts queued up
    and the 3ms timeout would not split them

    inital wait time is arbitrary
    long would affect responsiveness of reading
    long is probably blocking the rest of app
    short will use the event loop more frequently
    """
    events = get_events()
    data = []
    output = None

    while events:
        for line in events:
            event = line.event_read()
            data.append(event)
        """
        check for next event immediately, no yield to event loop
        """
        events = get_events()
    else:
        # if data, sort it and return it
        # has nice benefit of returning output 0 properly
        if data:
            output = ''
            data.sort(key=lambda x: x.sec * 1000000000 + x.nsec)

            for obj in data:
                # speed doesn't matter at this point vs clarity
                # using a string cause it has length and easy enough to convert to binary later
                if obj.source.offset() == d0.offset():
                    output += '0'
                elif obj.source.offset() == d1.offset():
                    output += '1'

    return output
