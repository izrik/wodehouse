import os

from functions.eval import w_eval
from functions.hash import w_hash
from macros.magic_macro import WMagicMacro
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol

_global_import_cache = WScope()


class Import(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        if len(exprs) < 1:
            raise Exception(
                "Macro 'import' expected at least 1 arguments. "
                "Got {} instead.".format(len(exprs)))
        filename, *import_names = exprs
        filename = w_eval(filename, scope)
        if not isinstance(filename, WString):
            raise Exception(
                "Arg 'filename' to 'import' must be a string. "
                "Got \"{}\" ({}) instead.".format(filename, type(filename)))
        for impname in import_names:
            if not isinstance(impname, WSymbol):
                raise Exception(
                    "Names to import must all be symbols. "
                    "Got \"{}\" ({}) instead.".format(impname, type(impname)))
        with open(filename.value) as f:
            src = WString(f.read())

        h = w_hash(src)
        if h in _global_import_cache:
            imported_ms = _global_import_cache[h]
        else:
            from functions.exec_src import w_exec_src
            gs = scope.get_outermost()
            imported_ms = w_exec_src(src, enclosing_scope=gs,
                                     filename=filename)
            _global_import_cache[h] = imported_ms

        basename = os.path.splitext(filename.value)[0]
        scope[basename] = imported_ms
        for impname in import_names:
            scope[impname] = imported_ms[impname]
        return imported_ms, scope
