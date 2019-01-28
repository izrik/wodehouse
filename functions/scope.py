from wtypes.list import WList
from wtypes.scope import WScope
from wtypes.string import WString


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
    return scope[key]


def w_dir(scope=None, *, __current_scope__):
    if scope is None:
        scope = __current_scope__
    return WList(*(key for key in scope.keys()))


def create_module_scope(builtins_module=None, name=None, filename=None):
    ms = WScope(builtins_module=builtins_module)
    ms['__module__'] = ms
    if name:
        ms['__name__'] = WString(name)
    if filename:
        ms['__file__'] = WString(filename)
    if builtins_module is not None:
        ms['__global__'] = builtins_module
    return ms
