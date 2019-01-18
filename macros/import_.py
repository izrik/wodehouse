
from functions.eval import is_exception
from functions.hash import w_hash
from wtypes.control import WReturnValue
from wtypes.magic_macro import WMagicMacro
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol

_global_import_cache = WScope()


class Import(WMagicMacro):
    def __init__(self, loader=None):
        super().__init__()
        if loader is None:
            loader = Import.DefaultLoader()
        self.loader = loader

    class DefaultLoader:
        def get_filename_from_module_name(self, module_name):
            filename = f'{str(module_name)}.w'
            return filename

        def load(self, module_name):
            filename = self.get_filename_from_module_name(module_name)
            with open(filename) as f:
                return f.read()

    def call_magic_macro(self, exprs, scope):
        if len(exprs) < 1:
            raise Exception(
                "Macro 'import' expected at least 1 arguments. "
                "Got {} instead.".format(len(exprs)))
        module_name, *import_names = exprs

        if not isinstance(module_name, WSymbol):
            raise Exception(
                "Arg 'filename' to 'import' must be a symbol. "
                "Got \"{}\" ({}) instead.".format(module_name,
                                                  type(module_name)))
        for impname in import_names:
            if not isinstance(impname, WSymbol):
                raise Exception(
                    "Names to import must all be symbols. "
                    "Got \"{}\" ({}) instead.".format(impname,
                                                      type(impname)))

        src = WString(self.loader.load(module_name))

        h = w_hash(src)
        if h in _global_import_cache:
            imported_ms = _global_import_cache[h]
        else:
            from functions.exec_src import w_exec_src
            gs = scope.get_global_scope()
            filename = self.loader.get_filename_from_module_name(module_name)
            rv = w_exec_src(src, global_scope=gs, filename=filename)
            if is_exception(rv):
                return rv
            imported_ms = rv
            _global_import_cache[h] = imported_ms

        scope[module_name] = imported_ms
        for impname in import_names:
            scope[impname] = imported_ms[impname]
        return WReturnValue(imported_ms)
