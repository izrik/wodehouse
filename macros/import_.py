import os

from functions.eval import is_exception
from functions.hash import w_hash
from wtypes.control import WEvalRequired, WReturnValue
from wtypes.magic_macro import WMagicMacro
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol

_global_import_cache = WScope()


class Import(WMagicMacro):
    def __init__(self, loader=None):
        super().__init__()
        if loader is None:
            loader = Import.default_loader
        self.loader = loader

    @classmethod
    def default_loader(cls, filename):
        with open(filename) as f:
            return f.read()

    def call_magic_macro(self, exprs, scope):
        if len(exprs) < 1:
            raise Exception(
                "Macro 'import' expected at least 1 arguments. "
                "Got {} instead.".format(len(exprs)))
        filename, *import_names = exprs

        def callback(_filename):
            if not isinstance(filename, WString):
                raise Exception(
                    "Arg 'filename' to 'import' must be a string. "
                    "Got \"{}\" ({}) instead.".format(filename,
                                                      type(filename)))
            for impname in import_names:
                if not isinstance(impname, WSymbol):
                    raise Exception(
                        "Names to import must all be symbols. "
                        "Got \"{}\" ({}) instead.".format(impname,
                                                          type(impname)))

            src = WString(self.loader(filename.value))

            h = w_hash(src)
            if h in _global_import_cache:
                imported_ms = _global_import_cache[h]
            else:
                from functions.exec_src import w_exec_src
                gs = scope.get_global_scope()
                rv = w_exec_src(src, global_scope=gs, filename=filename)
                if is_exception(rv):
                    return rv
                imported_ms = rv
                _global_import_cache[h] = imported_ms

            basename = os.path.splitext(filename.value)[0]
            scope[basename] = imported_ms
            for impname in import_names:
                scope[impname] = imported_ms[impname]
            return WReturnValue(imported_ms)

        return WEvalRequired(expr=filename, callback=callback)
