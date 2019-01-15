from functions.str import w_str
from wtypes.control import WControl
from wtypes.exception import WException
from wtypes.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean


class WAssert(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if len(exprs) != 1:
            raise Exception(
                "Macro assert expected 1 argument. "
                "Got {} instead.".format(len(exprs)))
        expr = exprs[0]
        src = w_str(expr)

        def callback(_value):
            if _value is WBoolean.false:
                return WControl(
                    exception=WException(f'Assertion failed: {src}'))
            return WControl(expr=_value, callback=lambda _e: (_e, scope))

        return WControl(expr=expr, callback=callback)
