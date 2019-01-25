import os.path

__src_file__ = None
__src__ = None


def create_argparse_module(global_module):
    global __src_file__
    global __src__

    __src_file__ = os.path.join(os.path.dirname(__file__), 'argparse.w')
    with open(__src_file__, 'r') as __f:
        __src__ = __f.read()
    from functions.exec_src import w_exec_src
    mod = w_exec_src(__src__, global_scope=global_module,
                     filename=__src_file__)
    return mod
