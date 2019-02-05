from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.scope import WScope


def new_scope(pairs=None):
    """(new_scope '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(pairs, WList):
            raise Exception(
                "Argument to new_scope must be a list of key-value pairs. "
                "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Argument to new_scope must be a list of key-value pairs. "
                    "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
    scope = WScope()
    if pairs is not None:
        for key, value in pairs:
            scope[key] = value
    return scope


def new_scope_within(enclosing_scope, pairs=None):
    """(new_scope_within encl '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(enclosing_scope, WScope):
            raise TypeError(
                "Enclosing scope must be a scope object. "
                "Got \"{}\" ({}) instead.".format(enclosing_scope,
                                                  type(enclosing_scope)))
        if not isinstance(pairs, WList):
            raise Exception(
                "Second argument to new_scope_within must be a list of "
                "key-value pairs. Got \"{}\" ({}) instead.".format(
                    pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Second argument to new_scope_within must be a list of "
                    "key-value pairs. Got \"{}\" ({}) instead.".format(
                        pairs, type(pairs)))
    scope = WScope(enclosing_scope=enclosing_scope)
    if pairs is not None:
        for key, value in pairs:
            scope[key] = value
    return scope


def get_scope_value(scope, name_or_symbol):
    key = WScope.normalize_key(name_or_symbol)
    try:
        value = scope[key]
    except KeyError as e:
        return WRaisedException(
            WException(f"KeyError: {str(key)}"))
    return value


def w_dir(scope=None, *, __current_scope__):
    if scope is None:
        scope = __current_scope__
    return WList(*(key for key in scope.keys()))


def get_current_scope(*, __current_scope__):
    return __current_scope__
