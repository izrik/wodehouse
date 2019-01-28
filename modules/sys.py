import sys
from itertools import takewhile

from wtypes.list import WList
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
