from functions.eval import w_eval
from wtypes.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.scope import WScope


class Cond(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if scope is None:
            scope = WScope()
        for expr in exprs:
            if not isinstance(expr, WList) or len(expr) != 2:
                raise Exception(
                    "Argument to `cond` is not a condition-value pair: "
                    "\"{}\" ({})".format(expr, type(expr)))
        for expr in exprs:
            condition, retval = expr.values
            cond_result = w_eval(condition, scope)
            if cond_result is WBoolean.true:
                return w_eval(retval, scope), scope
            if cond_result is not WBoolean.false:
                raise Exception(
                    "Condition evaluated to a non-boolean value: "
                    "\"{}\" ({})".format(cond_result, type(cond_result)))
        raise Exception("No condition evaluated to true.")
