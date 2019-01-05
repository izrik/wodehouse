from functions.function import WFunction
from macros.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol


class WLambda(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if scope is None:
            scope = WScope()
        if len(exprs) != 2:
            raise Exception(
                "Wrong number of arguments to lambda. "
                "Expected 2, got {}.".format(len(exprs)))
        args = exprs[0]
        if isinstance(args, WSymbol):
            args = WList(args)
        if not isinstance(args, WList) or \
                not all(isinstance(arg, WSymbol) for arg in args):
            raise Exception(
                "First argument to lambda must be a symbol or a list of "
                "symbols.")
        expr = exprs[1]

        def subst_args(a, e):
            if isinstance(e, (WNumber, WFunction, WBoolean, WString)):
                return e
            if isinstance(e, WSymbol):
                if e == WSymbol.get('quote'):
                    return e
                if e in a:
                    return e
                if e in scope:
                    return scope[e]
                return e
            if isinstance(e, WList):
                return WList(*(subst_args(a, e2) for e2 in e))
            raise Exception(
                "Can't subst expression \"{}\" ({}).".format(e, type(e)))

        return WFunction(args, expr, enclosing_scope=scope), scope
