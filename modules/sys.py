import sys
from itertools import takewhile

from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule
from version import __version__, __version_info__


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
    mod['version'] = w_from_py(__version__)
    mod['version_info'] = WList(*(w_from_py(_) for _ in __version_info__))
    return mod


def w_from_py(p):
    from wtypes.object import WObject
    from wtypes.string import WString
    from wtypes.number import WNumber
    if isinstance(p, WObject):
        return p
    if isinstance(p, list):
        return WList(*list(w_from_py(_) for _ in p))
    if isinstance(p, str):
        return WString(p)
    if isinstance(p, int):
        return WNumber(p)
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
    from wtypes.control import WRaisedException
    from wtypes.exception import WSystemExit
    from wtypes.exception import WException
    from wtypes.object import WObject
    from wtypes.number import WNumber
    from functions.types import get_type

    if not isinstance(status, WObject):
        raise TypeError(f'Code must be a WNumber. '
                        f'Got "{status}" ({type(status)}) instead.')
    # TODO: on non-number, print it and use 1 as the status code
    if not isinstance(status, WNumber):
        return WRaisedException(
            WException(f'Code must be a number. '
                       f'Got "{status}" '
                       f'({get_type(status)}) instead.'))

    return WRaisedException(WSystemExit(status))
