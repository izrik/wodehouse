from functions.eval import w_eval
from wtypes.callstack import WStackFrame
from wtypes.object import WObject
from wtypes.scope import WScope


class WEvaluator:
    def eval(
            self,
            expr: WObject,
            scope: WScope,
            stack: WStackFrame = None
    ) -> WObject:
        return w_eval(expr, scope, stack)
