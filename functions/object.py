from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.object import WObject
from wtypes.position import Position


def w_position_of(expr):
    if not isinstance(expr, WObject):
        return WRaisedException(
            WException(f'Argument to position_of must be a WObject. '
                       f'Got "{expr}" ({type(expr)}) instead.'))
    if expr.position is not None:
        return expr.position
    return Position('<unknown>', '<unknown>', '<unknown>', None)
