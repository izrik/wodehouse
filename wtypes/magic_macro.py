from wtypes.macro import WMacro
from wtypes.string import WString


class WMagicMacro(WMacro):
    def __init__(self, name=None):
        super().__init__()
        if name is None:
            name = type(self).__name__.lower()
        if isinstance(name, str):
            name = WString(name)
        self.name = name

    def __str__(self):
        return self.name.value

    def call_macro(self, exprs, scope):
        return self.call_magic_macro(exprs, scope)

    def call_magic_macro(self, exprs, scope):
        return exprs, scope
