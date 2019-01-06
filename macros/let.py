from functions.eval import w_eval
from macros.magic_macro import WMagicMacro
from wtypes.list import WList
from wtypes.scope import WScope
from wtypes.symbol import WSymbol


class Let(WMagicMacro):
    """
    (let
        (name1 value1)
        (name2 value2)
        ...
        expr)

    Creates a new scope with `name1` equal to the result of `value1`, etc. Then
    evaluates `expr`. Values are evaluated with the new scope object as it is
    populated.
    """

    def call_magic_macro(self, exprs, scope):
        if len(exprs) < 2:
            raise Exception(
                "Macro `let` expects at least one variable definition and "
                "exactly one expression. Get {} total args instead".format(
                    len(exprs)))
        *vardefs, retval = exprs
        for vardef in vardefs:
            if not isinstance(vardef, WList) or len(vardef) != 2 or \
                    not isinstance(vardef[0], WSymbol):
                raise Exception(
                    "Variable definition in macro `let` should be a list of "
                    "the form \"(<symbol> <expr>)\". Got \"{}\" ({}) "
                    "instead.".format(vardef, type(vardef)))

        scope2 = WScope(enclosing_scope=scope)
        for vardef in vardefs:
            name, expr = vardef
            value = w_eval(expr, scope2)
            scope2[name] = value
        return w_eval(retval, scope2), scope
