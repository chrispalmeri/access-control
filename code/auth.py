import wiegand

def verify(code):
    if isinstance(code, wiegand.Card):
        if code.number == 34169 and code.facility == 99:
            return True
        else:
            return False

    elif isinstance(code, str):
        if code in ['1234', '000000']:
            return True
        else:
            return False

    else:
        return False
