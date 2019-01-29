from modules.argparse import create_argparse_module
from modules.builtins import create_builtins_module
from modules.sys import create_sys_module
from wtypes.symbol import WSymbol


class Runtime:
    def __init__(self, argv):
        from macros.import_ import Import
        self.import_ = Import()
        cache = self.import_.module_cache
        self.builtins_module = create_builtins_module(import_=self.import_)
        self.sys_module = create_sys_module(self.builtins_module, argv=argv)
        cache[WSymbol.get('sys')] = self.sys_module
        self.argparse_module = create_argparse_module(self.builtins_module)
        cache[WSymbol.get('argparse')] = self.argparse_module