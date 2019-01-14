
from wtypes.object import WObject


class WControl(WObject):
    def __init__(self, expr=None, scope=None, callback=None, exception=None):
        super().__init__()
        self.expr = expr
        self.scope = scope
        self.callback = callback
        self.exception = exception
