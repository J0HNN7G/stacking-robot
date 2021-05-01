
def checkType(val, type, msg):
    if not isinstance(val, type):
        raise TypeError(msg)
