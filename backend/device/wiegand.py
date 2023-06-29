from device import numpad
import broadcast

class Card:
    def __init__(self, number, facility):
        self.number = number # aka 'user code', 'unique id', 'card number'
        self.facility = facility

    def __str__(self):
        return f'Card: {self.number} Facility: {self.facility}'

def parity(datain, p):
    while datain:
        p ^= datain & 1
        datain >>= 1
    return p

async def parse(data):
    if data is None:
        return None

    length = len(data)

    await broadcast.event('DEBUG', 'Data: ' + data + ' Length: ' + str(length))
    # convert to actual binary (integer instead of string)
    # since existing parser expects that
    data = int(data, 2)

    # this should maybe go at the end, and split up if divisible by 4
    if length == 4:
        return numpad.press(data)

    # facility code is not the same for same card, it is actually a bigger number
    # so I am gonna just truncate it

    # example
    # 26 bit:         1.01100011.1000.010101111001.0
    # 34 bit: 0.0000100101100011.1000010101111001.1

    # this could be specific to 13.56 MHz cards (may not really have facility, vs 125KHz)
    # sending as Wiegand, and 34 bit which is less standardized than 26 bit is

    # FYI Wiegand has 4 bit, 8 bit, 24 bit, 26 bit, 32 bit and 34 bit formats

    if length == 34:
        # 34 bit
        even_parity = data >> 33 & 1
        even_half = data >> 17 & 65535
        odd_half = data >> 1 & 65535
        odd_parity = data & 1
    else:
        # default 26 bit
        # just so they are  not undefined if something weird happens
        even_parity = data >> 25 & 1
        even_half = data >> 13 & 4095
        odd_half = data >> 1 & 4095
        odd_parity = data & 1

    # if parity is valid, get the numbers
    # you should skip this somehow if it's neither 26 or 34 bit
    if parity(even_half, 0) == even_parity and parity(odd_half, 1) == odd_parity:
        # 26 bit
        facility = data >> 17 & 255
        #34 bit, just keeping 26 code which will truncate it to match
        #facility = data >> 17 & 65535
        number = data >> 1 & 65535

        return Card(number, facility)

    else:
        await broadcast.event('WARNING', 'Wiegand reading error')
        return None
