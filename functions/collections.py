from wtypes.control import WEvalRequired, WRaisedException
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.scope import WScope
from wtypes.set import WSet
from wtypes.string import WString
from wtypes.symbol import WSymbol


def w_map(func, *exprlists):
    if not isinstance(func, WFunction):
        return WRaisedException(
            WException(
                f'Expected a function but '
                f'got "{func}" ({type(func)}) instead.'))

    if exprlists:
        for exprlist in exprlists:
            if not isinstance(exprlist, WList):
                return WRaisedException(
                    WException(
                        f'Argument passed to map must be lists. '
                        f'Got "{exprlist}" ({type(exprlist)}) instead.'))
    length = min(len(e) for e in exprlists)
    results = WList()
    if length < 1:
        return results

    e = WList(*exprlists)
    cars = WList(*list(exprlist.head for exprlist in e))
    cdrs = WList(*list(exprlist.remaining for exprlist in e))

    quote = WSymbol.get('quote')
    func_with_args = WList(func, *list(WList(quote, _) for _ in cars))

    def callback(result):
        nonlocal results
        nonlocal cdrs
        results = results.append(result)
        if len(results) >= length:
            return results
        e = cdrs
        cars = WList(*list(exprlist.head for exprlist in e))
        cdrs = WList(*list(exprlist.remaining for exprlist in e))
        return WEvalRequired(
            expr=WList(func, *list(WList(quote, _) for _ in cars)),
            callback=callback)

    return WEvalRequired(expr=func_with_args, callback=callback)


def w_in(expr, container):
    if not isinstance(container, (WString, WList, WScope)):
        return WRaisedException(
            WException(
                f'Container must be a string, list, or scope. '
                f'Got "{container}" ({type(container)}) instead.'))
    if isinstance(expr, WString) and isinstance(container, WString):
        if expr.value in container.value:
            return WBoolean.true
        return WBoolean.false
    if isinstance(container, WScope):
        return WBoolean.from_value(expr in container)
    # WList
    for item in container:
        if item is expr or item == expr:
            return WBoolean.true
    return WBoolean.false


def w_unique(arg):
    from wtypes.object import WObject
    from functions.types import get_type
    if not isinstance(arg, WObject):
        raise TypeError(f'Argument to unique must be a WObject. '
                        f'Got "{arg}" ({type(arg)}) instead.')
    if not isinstance(arg, WList):
        return WRaisedException(
            WException(f'Argument to unique must be a list. '
                       f'Got "{arg}" ({get_type(arg)}) instead.'))

    return WList(*set(arg))


def w_add(s, value):
    from wtypes.object import WObject
    from functions.types import get_type
    if not isinstance(s, WObject):
        raise TypeError(f'Arguments to add must be WObject. '
                        f'Got "{s}" ({type(s)}) instead.')
    if not isinstance(s, WSet):
        return WRaisedException(
            WException(f'Argument "s" must be a set. '
                       f'Got "{s}" ({get_type(s)}) instead.'))
    if not isinstance(value, WObject):
        raise TypeError(f'Arguments to add must be WObject. '
                        f'Got "{value}" ({type(value)}) instead.')
    try:
        rv = s.add(value)
    except TypeError as e:
        if 'unhashable type' in str(e):
            return WRaisedException(
                WException(f'Unhashable type: "{get_type(value)}"'))
        raise
    return rv


def w_to_list(s):
    from wtypes.object import WObject
    from functions.types import get_type
    if not isinstance(s, WObject):
        raise TypeError(f'Argument "s" to w_to_list must be a WObject. '
                        f'Got "{s}" ({type(s)}) instead.')
    if not isinstance(s, (WList, WSet)):
        return WRaisedException(
            WException(f'Argument "s" to to_list must be a list or set. '
                       f'Got "{s}" ({get_type(s)}) instead.'))
    return WList(*s.values)


def w_append(lst, value):
    from wtypes.object import WObject
    from functions.types import get_type
    if not isinstance(lst, WObject):
        raise TypeError(f'Arguments to w_append must be WObject. '
                        f'Got "{lst}" ({type(lst)}) instead.')
    if not isinstance(lst, WList):
        return WRaisedException(
            WException(f'Argument "lst" must be a List. '
                       f'Got "{lst}" ({get_type(lst)}) instead.'))
    if not isinstance(value, WObject):
        raise TypeError(f'Arguments to w_append must be WObject. '
                        f'Got "{value}" ({type(value)}) instead.')
    rv = lst.append(value)
    return rv
