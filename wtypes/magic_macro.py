from wtypes.macro import WMacro


class WMagicMacro(WMacro):
    def __init__(self, name=None):
        super().__init__()
        if name is None:
            name = type(self).__name__.lower()
        self.name = name

    def __str__(self):
        return self.name

    def call_macro(self, exprs, scope):
        exprs, scope = self.call_magic_macro(exprs, scope)
        return exprs, scope

    def call_magic_macro(self, exprs, scope):
        return exprs, scope
