from functions.types import get_type
from wtypes.exception import WrappedWException, WException
from wtypes.object import WObject
from wtypes.position import Position


def w_filename_from_position(p):
    if not isinstance(p, WObject):
        raise TypeError(f'Argument "p" must be WString. '
                        f'Got "{p}" ({type(p)}) instead.')
    if not isinstance(p, Position):
        raise WrappedWException(
            WException(f'Argument "p" must be String. '
                       f'Got "{p}" ({get_type(p)}) '
                       f'instead.'))
    return p.filename
