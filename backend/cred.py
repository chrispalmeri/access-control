class Cred:
    def __init__(self, number, facility, pin=None, action=None):
        self.number = number # aka 'user code', 'unique id', 'card number'
        self.facility = facility
        self.pin = pin
        self.action = action

    def __str__(self):
        s = ''

        if self.number is not None:
            s += f'Card: {self.number} '
        if self.facility is not None:
            s += f'Facility: {self.facility} '
        if self.pin is not None:
            s += f'Pin: {self.pin} '
        if self.action is not None:
            s += f'Action: {self.action} '

        return s.rstrip()
