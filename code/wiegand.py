import numpad

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

    if data < 16:
        return numpad.press(data)

    evenParity = data >> 25 & 1
    evenHalf = data >> 13 & 4095
    oddHalf = data >> 1 & 4095
    oddParity = data & 1

    # if parity is valid, get the numbers
    if parity(evenHalf, 0) == evenParity and parity(oddHalf, 1) == oddParity:
        facility = data >> 17 & 255
        number = data >> 1 & 65535

        return Card(number, facility)

    else:
        print('Wiegand reading error')
        return None
