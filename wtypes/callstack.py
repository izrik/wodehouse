
from wtypes.object import WObject


class WStackFrame(WObject):
    def __init__(self, expr, prev):
        super().__init__()
        self.expr = expr
        self.prev = prev
