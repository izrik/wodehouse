from functions.str import w_str
from functions.types import get_type
from wtypes.control import WReturnValue
from wtypes.function import WFunction
from wtypes.list import WList
from wtypes.magic_macro import WMagicMacro
from wtypes.symbol import WSymbol


class Def(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if len(exprs) != 3:
            raise Exception(
                "Wrong number of arguments to def. "
                "Expected 3, got {}.".format(len(exprs)))

        name, args, body = exprs

        if not isinstance(name, WSymbol):
            raise Exception(
                f"Arg 'name' to def must be a symbol. "
                f"Got \"{name}\" ({get_type(name)}) instead.")
        if isinstance(args, WSymbol):
            args = WList(args)
        if not isinstance(args, WList) or \
                not all(isinstance(arg, WSymbol) for arg in args):
            raise Exception(
                f'Second argument to def must be a symbol or a list of '
                f'symbols. Got "{args}" ({get_type(args)}) instead.')

        f = WFunction(args, body, enclosing_scope=scope)
        f.name = w_str(name)
        scope[name] = f
        return WReturnValue(expr=f)
