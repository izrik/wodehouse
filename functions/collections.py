from functions.eval import w_eval
from functions.function import WFunction
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.string import WString


def w_map(func, *exprlists):
    if not isinstance(func, WFunction):
        raise Exception(
            "Expected a function but got \"{}\" ({}) instead.".format(
                func, type(func)))
    if exprlists:
        for exprlist in exprlists:
            if not isinstance(exprlist, WList):
                raise Exception(
                    "Argument passed to map must be lists. "
                    "Got \"{}\" ({}) instead.".format(
                        exprlist, type(exprlist)))
        length = min(len(e) for e in exprlists)
    results = WList()
    e = WList(*exprlists)
    while len(results) < length:
        cars = WList(*list(exprlist.head for exprlist in e))
        cdrs = WList(*list(exprlist.remaining for exprlist in e))
        func_with_args = WList(func, *cars)
        result = w_eval(func_with_args, scope=None)
        results = results.append(result)
        e = cdrs

    return results


def w_in(expr, container):
    if isinstance(expr, WString) and isinstance(container, WString):
        if expr.value in container.value:
            return WBoolean.true
        return WBoolean.false
    if not isinstance(container, WList):
        raise Exception(
            "Not a list: \"{}\" ({})".format(container, type(container)))
    for item in container:
        if item is expr or item == expr:
            return WBoolean.true
    return WBoolean.false
