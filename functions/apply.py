from functions.types import get_type
from wtypes.control import WRaisedException, WEvalRequired
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.list import WList
from wtypes.object import WObject
from wtypes.symbol import WSymbol


def w_apply(func, args):
    if not isinstance(func, WObject):
        raise TypeError(f'First argument to apply must be a WObject. '
                        f'Got "{func}" ({type(func)}) instead.')

    if not isinstance(args, WObject):
        raise TypeError(f'Second argument to apply must be a WObject. '
                        f'Got "{args}" ({type(args)}) instead.')
    if not isinstance(func, WFunction):
        return WRaisedException(
            WException(f'First argument to apply must be a function. '
                       f'Got "{func}" ({get_type(func)}) instead.'))
    if not isinstance(args, WList):
        return WRaisedException(
            WException(f'Second argument to apply must be a list. '
                       f'Got "{args}" ({get_type(args)}) instead.'))

    new_expr = WList(func, *(WList(WSymbol.get('quote'), x) for x in args))
    return WEvalRequired(expr=new_expr, callback=lambda _: _)
