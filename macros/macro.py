from wtypes.magic_macro import WMagicMacro


class Macro(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        raise Exception('Not implemented')
