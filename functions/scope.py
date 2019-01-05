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


def new_scope_proto(prototype, pairs=None):
    """(new_scope_proto proto '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(prototype, WScope):
            raise TypeError(
                "Prototype must be a scope object. "
                "Got \"{}\" ({}) instead.".format(prototype, type(prototype)))
        if not isinstance(pairs, WList):
            raise Exception(
                "Second argument to new_scope_proto must be a list of "
                "key-value pairs. Got \"{}\" ({}) instead.".format(
                    pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Second argument to new_scope_proto must be a list of "
                    "key-value pairs. Got \"{}\" ({}) instead.".format(
                        pairs, type(pairs)))
    scope = WScope(prototype=prototype)
    if pairs is not None:
        for key, value in pairs:
            scope[key] = value
    return scope


def get_scope_value(scope, name_or_symbol):
    key = WScope.normalize_key(name_or_symbol)
    return scope[key]


def list_scope(scope):
    return WList(*(key for key in scope.keys()))
