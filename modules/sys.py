import sys
from itertools import takewhile

from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule


def create_sys_module(builtins_module, argv=None):
    """
    This module provides access to some objects used or maintained by the
    runtime.
    """
    if argv is None:
        argv = list(takewhile(lambda x: x != '--', sys.argv[1:]))
    argv = w_from_py(argv)
    mod = WModule(builtins_module=builtins_module, name='sys')
    mod['argv'] = argv
    mod['exit'] = WMagicFunction(w_exit, mod, name='exit', check_args=False)
    return mod


def w_from_py(p):
    from wtypes.object import WObject
    from wtypes.string import WString
    if isinstance(p, WObject):
        return p
    if isinstance(p, list):
        return WList(*list(w_from_py(_) for _ in p))
    if isinstance(p, str):
        return WString(p)
    raise Exception(f'Unknown object type: {p} ({type(p)})')


def py_from_w(w):
    from wtypes.object import WObject
    from wtypes.number import WNumber
    from wtypes.scope import WScope
    from functions.str import w_str
    if not isinstance(w, WObject):
        return w
    if isinstance(w, WNumber):
        return w.value
    if isinstance(w, WList):
        return [py_from_w(_) for _ in w]
    if isinstance(w, WScope):
        return w.dict
    return w_str(w).value


def w_exit(status=None):
    # TODO: raise a SystemExit exception so finally hnadlers get triggered
    #   TODO: filter exception handlers by type, so run-of-the-mill handlers
    #         don't accidentally catch SystemExit
    #   TODO: type system with sub-types and built-in exception classes
    sys.exit(py_from_w(status))
