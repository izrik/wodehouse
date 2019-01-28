from wtypes.number import WNumber
from wtypes.string import WString


def w_print(x, *, printer=None):
    if printer is None:
        printer = print

    if isinstance(x, WNumber):
        printer(x.value)
    elif isinstance(x, WString):
        printer(x.value)
    else:
        printer(x)
    return x


def read_file(path):
    if isinstance(path, WString):
        path = path.value
    with open(path) as f:
        return WString(f.read())
