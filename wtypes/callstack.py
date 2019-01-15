from wtypes.function import WFunction
from wtypes.macro import WMacro
from wtypes.magic_function import WMagicFunction
from wtypes.magic_macro import WMagicMacro
from wtypes.object import WObject


class WStackFrame(WObject):
    def __init__(self, expr, prev):
        super().__init__()
        self.expr = expr
        self.prev = prev
        self.callee = None

    def get_callable(self):
        if self.callee is not None:
            return self.callee
        head = self.expr.head
        if not isinstance(head, (WMagicFunction, WMagicMacro)) and \
                isinstance(head, (WFunction, WMacro)):
            return head
        if self.prev is None:
            return '<module>'
        return self.prev.get_callable()
