
from functions.eval import w_eval
from functions.read import read_whitespace_and_comments, read_expr
from functions.scope import create_module_scope
from wtypes.stream import WStream


def w_exec_src(src, enclosing_scope, filename=None):
    ms = create_module_scope(
        enclosing_scope=enclosing_scope, name=filename, filename=filename)
    stream = WStream(src, filename=filename)
    read_whitespace_and_comments(stream)
    while stream.has_chars():
        expr = read_expr(stream)
        w_eval(expr, ms)
        read_whitespace_and_comments(stream)
    return ms


def w_exec(*args):
    if len(args) < 1:
        raise Exception("Function exec requires at least one argument.")
    return args[-1]
