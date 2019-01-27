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
