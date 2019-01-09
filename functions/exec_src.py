from functions.eval import w_eval
import functions.magic_function
from functions.read import read_whitespace_and_comments, read_expr
import functions.scope

# import macros.apply
# import macros.assert_
# import macros.cond
# import macros.define
# import macros.if_
# import macros.import_
# import macros.lambda_
# import macros.let
# import wtypes.boolean
# import wtypes.scope
import wtypes.stream

#
# WMagicFunction = functions.magic_function.WMagicFunction
# Apply = macros.apply.Apply
# WAssert = macros.assert_.WAssert
# Cond = macros.cond.Cond
# Define = macros.define.Define
# If = macros.if_.If
# Import = macros.import_.Import
# WLambda = macros.lambda_.WLambda
# Let = macros.let.Let
# WBoolean = wtypes.boolean.WBoolean
# WScope = wtypes.scope.WScope
WStream = wtypes.stream.WStream


def w_exec_src(src, enclosing_scope, filename=None):
    ms = functions.scope.create_module_scope(
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
