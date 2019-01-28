from wtypes.scope import WScope
from wtypes.string import WString


class WModule(WScope):
    def __init__(self, builtins_module=None, name=None, filename=None):
        super().__init__(builtins_module=builtins_module)
        self['__module__'] = self
        if name:
            self['__name__'] = WString(name)
        if filename:
            self['__file__'] = WString(filename)
        if builtins_module is not None:
            self['__global__'] = builtins_module
