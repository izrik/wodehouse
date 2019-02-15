import os

from functions.eval import is_exception
from wtypes.control import WReturnValue, WExecSrcRequired
from wtypes.magic_macro import WMagicMacro
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol


class Import(WMagicMacro):
    def __init__(self, loader=None):
        super().__init__()
        if loader is None:
            loader = Import.FileLoader()
        self.loader = loader
        self.module_cache = WScope()

    class Loader:
        def _normalize_module_name(self, module_name):
            if isinstance(module_name, WSymbol):
                module_name = module_name.name
            if isinstance(module_name, WString):
                module_name = module_name.value
            if not isinstance(module_name, str):
                raise ValueError(f'Argument module_name must be a str, '
                                 f'WString, or WSymbol. Got "{module_name}" '
                                 f'({type(module_name)}) instead.')
            return module_name

        def get_filename_from_module_name(self, module_name):
            raise NotImplementedError

        def can_load_module(self, module_name):
            raise NotImplementedError

        def load(self, module_name):
            raise NotImplementedError

    class FileLoader(Loader):
        def get_filename_from_module_name(self, module_name):
            filename = f'{str(module_name)}.w'
            import os.path
            fullpath = os.path.join(os.getcwd(), filename)
            return fullpath

        def can_load_module(self, module_name):
            return os.path.exists(self._normalize_module_name(module_name))

        def load(self, module_name):
            filename = self.get_filename_from_module_name(module_name)
            with open(filename) as f:
                return f.read()

    class BuiltinLoader(Loader):
        def __init__(self, create_funcs_by_name, next_=None):
            self.create_funcs_by_name = create_funcs_by_name
            self.next_ = next_

        def get_filename_from_module_name(self, module_name):
            module_name = self._normalize_module_name(module_name)
            if module_name not in self.create_funcs_by_name:
                if self.next_:
                    return self.next_.get_filename_from_module_name(
                        module_name)

            raise NotImplementedError

        def can_load_module(self, module_name):
            module_name = self._normalize_module_name(module_name)
            if module_name in self.create_funcs_by_name:
                return True
            if self.next_:
                return self.next_.can_load_module(module_name)
            return False

        def load(self, module_name):
            module_name = self._normalize_module_name(module_name)

            if module_name not in self.create_funcs_by_name:
                if self.next_:
                    return self.next_.load(module_name)
                raise KeyError(f'No builtin module found by the name '
                               f'of "{module_name}".')

            func = self.create_funcs_by_name[module_name]
            module = func()
            return module

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

        def complete_module(imported_ms):
            scope[module_name] = imported_ms
            for impname in import_names:
                scope[impname] = imported_ms[impname]
            return WReturnValue(imported_ms)

        if module_name in self.module_cache:
            imported_ms = self.module_cache[module_name]
            return complete_module(imported_ms)
        else:
            bm = scope.get_builtins_module()
            filename = self.loader.get_filename_from_module_name(module_name)
            src = WString(self.loader.load(module_name))

            def callback(rv):
                if is_exception(rv):
                    return rv
                imported_ms = rv
                self.module_cache[module_name] = imported_ms
                return complete_module(imported_ms)

            from functions.str import w_str
            return WExecSrcRequired(src, builtins_module=bm,
                                    name=w_str(module_name),
                                    filename=filename, callback=callback)

    # def