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
            output = 0
            data.sort(key=lambda x: x.sec * 1000000000 + x.nsec)
            # should check data length
            # if 8, 12, 16 then split into 4's
            # Wiegand 4 bit, 8 bit, 24 bit, 26 bit, 32 bit and 34 bit
            # well you are not even parsing it here, so do that in the parser
            # either validate parity and get card/facility, or split and get digit(s)
            for obj in data:
                # you don't need to bit shift if you don't want
                # speed doesn't matter at this point vs clarity
                if obj.source.offset() == d0.offset():
                    output = output << 1
                elif obj.source.offset() == d1.offset():
                    output = output << 1 | 1
            #config.logger.debug(output)

    return output
