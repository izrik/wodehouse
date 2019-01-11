from wtypes.object import WObject


class WMacro(WObject):
    def __init__(self):
        super().__init__()
        self.name = None

    def call_macro(self, exprs, scope):
        return exprs, scope
