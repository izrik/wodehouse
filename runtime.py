from modules.argparse import create_argparse_module
from modules.builtins import create_builtins_module
from modules.coverage import create_coverage_module, create__coverage_module
from modules.runw import create_runw_module
from modules.sys import create_sys_module
from modules.time import create_time_module
from modules.unittest import create_unittest_module
from wtypes.object import WObject
from wtypes.symbol import WSymbol


class Runtime(WObject):
    def __init__(self, argv):
        super().__init__()
        from macros.import_ import Import
        self.import_ = Import()
        cache = self.import_.module_cache
        self.builtins_module = create_builtins_module(import_=self.import_)
        # self.builtins_module['__runtime__'] = self

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

        self.runw_module = create_runw_module(self.builtins_module)
        cache[WSymbol.get('runw')] = self.runw_module

        self.coverage_module = create_coverage_module(self.builtins_module)
        cache[WSymbol.get('coverage')] = self.coverage_module
