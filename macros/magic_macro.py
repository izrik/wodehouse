from macros.macro import WMacro


class WMagicMacro(WMacro):
    def __init__(self, macro_name=None):
        if macro_name is None:
            macro_name = type(self).__name__.lower()
        self.macro_name = macro_name

    def __str__(self):
        return self.macro_name

    def call_macro(self, exprs, scope):
        exprs, scope = self.call_magic_macro(exprs, scope)
        return exprs, scope
