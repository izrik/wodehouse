from functions.eval import w_eval
from functions.str import w_str
from macros.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean


class WAssert(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if len(exprs) != 1:
            raise Exception(
                "Macro assert expected 1 argument. "
                "Got {} instead.".format(len(exprs)))
        expr = exprs[0]
        src = w_str(expr)
        value = w_eval(expr, scope)
        if value is WBoolean.false:
            raise Exception("Assertion failed: {}".format(src))
        return value, scope
