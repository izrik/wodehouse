from wtypes.control import WEvalRequired, WReturnValue
from wtypes.function import WFunction
from wtypes.list import WList
from wtypes.macro import WMacro
from wtypes.magic_macro import WMagicMacro
from wtypes.symbol import WSymbol


class Define(WMagicMacro):
    """
    Given a name and an expression, evaluate the expression and store it in
    the enclosing scope under that name.
    """

    def call_magic_macro(self, exprs, scope):
        if len(exprs) != 2:
            raise Exception(
                "Macro 'define' expected 2 arguments. "
                "Got {} instead.".format(len(exprs)))
        name, expr = exprs
        if not isinstance(name, WSymbol):
            raise Exception(
                "Arg 'name' to 'define' must be a symbol. "
                "Got \"{}\" ({}) instead.".format(name, type(name)))

        def callback(_value):
            if isinstance(_value, (WFunction, WMacro)):
                _value.name = name
            scope[name] = _value
            return WReturnValue(expr=WList(WSymbol.get('quote'), _value))

        return WEvalRequired(expr=expr, callback=callback)
