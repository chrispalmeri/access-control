import numpad
import config

class Card:
    def __init__(self, number, facility):
        self.number = number
        self.facility = facility
    def __str__(self):
        return f'{self.facility}:{self.number}'

def parity(datain, p):
    while datain:
        p ^= datain & 1
        datain >>= 1
    return p

def parse(data):
    if data is None:
        return None

    # get length also as parameter from reader?

    if data < 16:
        return numpad.press(data)

    '''
    update to handle both lengths

    26 bit:         1.01100011.1000.010101111001.0
    34 bit: 0.0000100101100011.1000010101111001.1

    26 bit:         1.11001100.1101001011111001.0
    34 bit: 0.0000011011001100.1101001011111001.1

    parity checks out
    the facility codes are different though, longer?!
    I mean, you could truncate it I guess
    seems better than just ignoring facility in auth.py
    '''

    config.logger.debug(format(data, 'b'))

    # 26 bit
    #evenParity = data >> 25 & 1
    #evenHalf = data >> 13 & 4095
    #oddHalf = data >> 1 & 4095
    #oddParity = data & 1

    # 34 bit
    evenParity = data >> 33 & 1
    evenHalf = data >> 17 & 65535
    oddHalf = data >> 1 & 65535
    oddParity = data & 1

    # if parity is valid, get the numbers
    if parity(evenHalf, 0) == evenParity and parity(oddHalf, 1) == oddParity:
        # 26 bit
        facility = data >> 17 & 255
        #34 bit, just keeping 26 code to truncate it to match
        #facility = data >> 17 & 65535
        number = data >> 1 & 65535

        return Card(number, facility)

    else:
        config.logger.warning('Wiegand reading error')
        return None
