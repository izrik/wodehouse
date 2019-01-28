import os.path

from wtypes.module import WModule

__src_file__ = None
__src__ = None


def create_argparse_module(builtins_module):
    global __src_file__
    global __src__

    __src_file__ = os.path.join(os.path.dirname(__file__), 'argparse.w')
    with open(__src_file__, 'r') as __f:
        __src__ = __f.read()
    from functions.exec_src import w_exec_src
    mod = WModule(builtins_module=builtins_module)
    w_exec_src(__src__, builtins_module=builtins_module,
               filename=__src_file__, scope=mod)
    return mod
