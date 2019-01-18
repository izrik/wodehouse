from wtypes.control import WControl
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

        def run_next_expr(_exprs):
            if len(_exprs) < 1:
                raise Exception("No condition evaluated to true.")
            _expr = _exprs.head
            condition, retval = _expr.values
            return WControl(expr=condition,
                            callback=condition_evaluated(retval,
                                                         _exprs.remaining))

        def condition_evaluated(_retval, _exprs):
            def _condition_evaluated(_cond_result):
                if _cond_result is WBoolean.true:
                    return _retval
                if _cond_result is WBoolean.false:
                    return run_next_expr(_exprs)
                raise Exception(
                    "Condition evaluated to a non-boolean value: "
                    "\"{}\" ({})".format(_cond_result, type(_cond_result)))
            return _condition_evaluated

        return run_next_expr(exprs)
