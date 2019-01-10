from functions.eval import w_eval
from wtypes.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean
from wtypes.scope import WScope


class If(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if scope is None:
            scope = WScope()
        if len(exprs) != 3:
            raise Exception(
                "Expected 3 arguments to if, got {} instead.".format(
                    len(exprs)))
        condition = exprs[0]
        true_retval = exprs[1]
        false_retval = exprs[2]
        cond_result = w_eval(condition, scope)
        if cond_result is WBoolean.true:
            return w_eval(true_retval, scope), scope
        return w_eval(false_retval, scope), scope
