from wtypes.function import WFunction
from wtypes.magic_macro import WMagicMacro
from wtypes.list import WList
from wtypes.scope import WScope
from wtypes.symbol import WSymbol


class WLambda(WMagicMacro):
    def __init__(self):
        super().__init__(name='lambda')

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

        return WFunction(args, expr, enclosing_scope=scope), scope
