
from wtypes.control import WEvalRequired, WMacroExpansion
from wtypes.magic_macro import WMagicMacro
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
    # TODO: clean up syntax. use "((n1 v1) (n2 v2))" for multiple vars

    def call_magic_macro(self, exprs, scope):
        if len(exprs) < 2:
            raise Exception(
                "Macro `let` expects at least one variable definition and "
                "exactly one expression. Get {} total args instead".format(
                    len(exprs)))
        *vardefs, retval = exprs
        vardefs = WList(*vardefs)
        for vardef in vardefs:
            if not isinstance(vardef, WList) or len(vardef) != 2 or \
                    not isinstance(vardef[0], WSymbol):
                raise Exception(
                    "Variable definition in macro `let` should be a list of "
                    "the form \"(<symbol> <expr>)\". Got \"{}\" ({}) "
                    "instead.".format(vardef, type(vardef)))

        scope2 = WScope(enclosing_scope=scope)

        def assign_next_var(_vardefs):
            if len(_vardefs) < 1:
                return WMacroExpansion(expr=retval, scope=scope2)
            _vardef = _vardefs.head
            _name, _expr = _vardef
            return WEvalRequired(
                expr=_expr,
                scope=scope2,
                callback=var_evaluated(_name, _vardefs.remaining))

        def var_evaluated(_name, _vardefs):
            def _var_evaluated(_value):
                scope2[_name] = _value
                return assign_next_var(_vardefs)
            return _var_evaluated

        return assign_next_var(vardefs)
