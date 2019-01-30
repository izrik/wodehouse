
from functions.read import read_whitespace_and_comments, read_expr
from wtypes.callstack import WStackFrame
from wtypes.module import WModule
from wtypes.stream import WStream


def w_exec_src(src, builtins_module, filename=None, scope=None,
               prevstack=None):
    from functions.eval import w_eval, is_exception
    if scope is None:
        scope = WModule(builtins_module=builtins_module, name=filename,
                        filename=filename)
    stream = WStream(src, filename=filename)
    read_whitespace_and_comments(stream)
    while stream.has_chars():
        expr = read_expr(stream)
        estack = WStackFrame(location=None, prev=prevstack)
        rv = w_eval(expr, scope, stack=estack)
        if is_exception(rv, estack):
            return rv
        read_whitespace_and_comments(stream)
    return scope


def w_exec(*args):
    if len(args) < 1:
        raise Exception("Function exec requires at least one argument.")
    return args[-1]
