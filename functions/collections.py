from wtypes.control import WEvalRequired, WRaisedException
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.scope import WScope
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
