from functions.types import get_type
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.object import WObject


def car(arg):
    if not isinstance(arg, WObject):
        raise TypeError(f'Argument to car must be a WObject. '
                        f'Got "{arg}" ({type(arg)}) instead.')
    if not isinstance(arg, WList):
        return WRaisedException(
            WException(f'Argument to car must be a list. '
                       f'Got "{arg}" ({get_type(arg)}) instead.'))
    if len(arg) < 1:
        return WList()
    return arg.head


def cdr(arg):
    if not isinstance(arg, WObject):
        raise TypeError(f'Argument to cdr must be a WObject. '
                        f'Got "{arg}" ({type(arg)}) instead.')
    if not isinstance(arg, WList):
        return WRaisedException(
            WException(f'Argument to cdr must be a list. '
                       f'Got "{arg}" ({get_type(arg)}) instead.'))
    return arg.remaining


def cons(a, b):
    if not isinstance(b, WList):
        raise Exception(
            "Expected b to be a list. "
            "Got \"{}\" ({}) instead.".format(b, type(b)))
    return WList(a, *b)


def atom(arg):
    return not isinstance(arg, WList)
