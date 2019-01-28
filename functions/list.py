from functions.types import get_type
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.number import WNumber


def list_func(*args):
    return WList(*args)


def w_len(arg):
    if not isinstance(arg, WList):
        return WRaisedException(
            WException(
                f'Expected a list. Got "{arg}" ({get_type(arg)}) instead.'))
    return WNumber(len(arg))


def nth(list_, n):
    if not isinstance(list_, WList):
        return WRaisedException(WException(
            "TypeError: first argument to nth should be a list"))
    if not isinstance(n, WNumber):
        return WRaisedException(WException(
            "TypeError: second argument to nth should be a number"))

    n = n.value
    if n >= 0 and n >= len(list_):
        return WRaisedException(WException("IndexError: index out of bounds"))
    if n < 0 and -n > len(list_):
        return WRaisedException(WException("IndexError: index out of bounds"))

    return list_[n]
