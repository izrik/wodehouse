import time

from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule
from wtypes.number import WNumber


def create_time_module(builtins_module):
    """
    This module provides various functions to manipulate time values.
    """
    mod = WModule(builtins_module=builtins_module, name='time')
    mod['time'] = WMagicFunction(w_time, mod, name='time', check_args=False)
    return mod


def w_time():
    return WNumber(time.time())
