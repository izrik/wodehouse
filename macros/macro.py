from wtypes.object import WObject


class WMacro(WObject):
    def call_macro(self, exprs, scope):
        return exprs, scope
