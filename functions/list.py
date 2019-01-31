from functions.types import get_type
from wtypes.boolean import WBoolean
from wtypes.control import WRaisedException, WEvalRequired
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.symbol import WSymbol


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


def w_filter(f, items):
    if not isinstance(f, WFunction):
        return WRaisedException(WException(
            "TypeError: first argument to filter should be a function"))
    if not isinstance(items, WList):
        return WRaisedException(WException(
            "TypeError: second argument to filter should be a list"))

    results = []

    def process_next_item(_items):
        if len(_items) < 1:
            return WList(*results)
        _item = _items.head
        return WEvalRequired(
            expr=WList(f, WList(WSymbol.get('quote'), _items.head)),
            callback=item_processed(_item, _items.remaining))

    def item_processed(_item, _items):
        def _item_processed(_eval_result):
            if _eval_result is WBoolean.true:
                results.append(_item)
            elif _eval_result is not WBoolean.false:
                return WRaisedException(
                    WException(
                        f'Condition evaluated to a non-boolean value: '
                        f'Got "{_eval_result}" ({type(_eval_result)}) '
                        f'instead.'))
            return process_next_item(_items)

        return _item_processed

    return process_next_item(items)
