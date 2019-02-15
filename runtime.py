from modules.argparse import create_argparse_module
from modules.builtins import create_builtins_module
from modules.coverage import create_coverage_module
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
        create_funcs_by_name = {
            'sys': lambda: create_sys_module(self.builtins_module,
                                             argv=argv),
            'argparse': lambda: create_argparse_module(
                self.builtins_module),
            'time': lambda: create_time_module(self.builtins_module),
            'unittest': lambda: create_unittest_module(
                self.builtins_module),
            'runw': lambda: create_runw_module(self.builtins_module),
            'coverage': lambda: create_coverage_module(
                self.builtins_module),
        }
        loader = Import.BuiltinLoader(create_funcs_by_name,
                                      Import.FileLoader())
        self.import_ = Import(loader=loader)
        cache = self.import_.module_cache
        self.builtins_module = create_builtins_module(import_=self.import_)
