from functions.eval import is_exception
from functions.exception import format_stacktrace
from functions.exec_src import w_exec_src
from modules.argparse import create_argparse_module
from modules.builtins import create_builtins_module
from modules.coverage import create_coverage_module
from modules.runw import create_runw_module
from modules.sys import create_sys_module
from modules.time import create_time_module
from modules.unittest import create_unittest_module
from wtypes.object import WObject
from wtypes.string import WString
from wtypes.symbol import WSymbol


class Runtime(WObject):
    def __init__(self, argv):
        super().__init__()
        from macros.import_ import Import
        self.import_ = Import()
        cache = self.import_.module_cache
        self.builtins_module = create_builtins_module(import_=self.import_)

        # TODO: don't execute the modules' w-lang code until they're imported.
        # Otherwise "-m" won't work

        self.sys_module = create_sys_module(self.builtins_module, argv=argv)
        cache[WSymbol.get('sys')] = self.sys_module

        self.argparse_module = create_argparse_module(self.builtins_module)
        cache[WSymbol.get('argparse')] = self.argparse_module

        self.time_module = create_time_module(self.builtins_module)
        cache[WSymbol.get('time')] = self.time_module

        self.unittest_module = create_unittest_module(self.builtins_module)
        cache[WSymbol.get('unittest')] = self.unittest_module

        self.runw_module = create_runw_module(self.builtins_module, self)
        cache[WSymbol.get('runw')] = self.runw_module

        self.coverage_module = create_coverage_module(self.builtins_module)
        cache[WSymbol.get('coverage')] = self.coverage_module

    def run_file(self, filename, argv=None):
        # TODO: look into the runpy module
        """(def run_file (filename argv)
            (let (src (read_file filename))
                (run_source src filename argv)))"""
        with open(filename.value) as f:
            src = WString(f.read())
        return self.run_source(src, filename=filename, argv=argv)

    def run_source(self, src, filename=None, argv=None):
        # TODO: look into the runpy module
        """(def run_source (src filename argv)
            (let (r (runtime argv))
                (let (rv (exec_src src (get_builtins_module r) "__main__"
                                    filename))
                    (if (isinstance rv 'Exception)
                        (let (stacktrace "TODO: format_stacktrace")
                            (exec
                                (print "Stacktrace (most recent call last):")
                                (print stacktrace)
                                (print
                                    (format
                                        "Exception: {}"
                                        "TODO: get exception message from rv"))
                                "TODO: get exception from rv"))
                        rv))))"""
        rv = w_exec_src(src, builtins_module=self.builtins_module,
                        filename=filename, name='__main__')
        if is_exception(rv):
            stacktrace = format_stacktrace(rv.stack)
            print('Stacktrace (most recent call last):')
            print(stacktrace)
            print(f'Exception: {rv.exception.message.value}')
            return rv.exception
        return rv

    def run_module(self, module, argv):
        # TODO: look into the runpy module
        import os.path
        from wtypes.list import WList

        if isinstance(module, str):
            module = WString(module)
        module_file = module + WString('.w')
        module_file = WString(os.path.abspath(module_file.value))
        if os.path.exists(module_file.value):
            argv = WList([module_file] + argv.values)
            return self.run_file(module_file, argv)

        from wtypes.symbol import WSymbol
        from macros.import_ import Import
        from functions.str import w_str
        module_symbol = WSymbol.get(w_str(module))
        loader = Import.FileLoader()
        filename = loader.get_filename_from_module_name(module_symbol)
        print(f'filename: {filename}')
        if os.path.exists(filename):
            argv = WList([WString(filename)] + argv.values)
            return self.run_file(WString(filename), argv)

        print(f'import module cache: {self.import_.module_cache}')
        if module_symbol in self.import_.module_cache:
            mod = self.import_.module_cache[module_symbol]
            if "__file__" in mod:
                argv = WList([mod["__file__"]] + argv.values)
                return self.run_file(mod["__file__"], argv)

        from wtypes.control import WRaisedException
        from wtypes.exception import WException
        return WRaisedException(
            WException(WString(f'No module named {module}')))
