from functions.eval import w_eval
from macros.magic_macro import WMagicMacro
from wtypes.symbol import WSymbol


class Define(WMagicMacro):
    # TODO: complete re-do this class
    """
    Every file will have a WScope object accessible only to that file. This
    object will at first be empty. Every top-level expression in the file that
    gets eval'd will have a new scope passed to it having the file-level scope
    object as its immediate prototype. If, however, any `define` expressions
    are eval'd, that will add an entry to the file-level scope. So, when we
    call `(import "filename.w" name1 name2)`, that call will eval the entire
    `filename.w` file as scoped before, and the resulting file-level scope
    object will be returned. Then, the `name1` and `name2` from `filename.w`'s
    scope will be added to the importing file's file-level scope.
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
        value = w_eval(expr, scope)
        scope[name] = value
        return value, scope
