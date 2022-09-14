from wtypes.control import WEvalRequired, WReturnValue, WRaisedException
from wtypes.exception import WException, WSyntaxError
from wtypes.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean
from wtypes.scope import WScope


class If(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if scope is None:
            scope = WScope()
        if len(exprs) not in [2, 3]:
            return WRaisedException(WSyntaxError(
                "Expected 2 or 3 arguments to if, got {} instead.".format(
                    len(exprs))))
        condition = exprs[0]
        true_retval = exprs[1]
        if len(exprs) > 2:
            false_retval = exprs[2]
        else:
            from wtypes.list import WList
            false_retval = WList()

        def callback(_cond_result):
            if _cond_result is WBoolean.true:
                return WReturnValue(true_retval)
            if _cond_result is WBoolean.false:
                return WReturnValue(false_retval)
            return WRaisedException(WException(
                "Condition evaluated to a non-boolean value: "
                "\"{}\" ({})".format(_cond_result, type(_cond_result))))

        return WEvalRequired(expr=condition, callback=callback)
