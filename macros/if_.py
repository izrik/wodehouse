
from wtypes.control import WControl
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

        def callback(_cond_result):
            if _cond_result is WBoolean.true:
                return true_retval
            if _cond_result is WBoolean.false:
                return false_retval
            raise Exception(
                "Condition evaluated to a non-boolean value: "
                "\"{}\" ({})".format(_cond_result, type(_cond_result)))

        return WControl(expr=condition, callback=callback)
