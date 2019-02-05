from wtypes.scope import WScope
from wtypes.string import WString


class WModule(WScope):
    name = None

    def __init__(self, builtins_module=None, name=None, filename=None):
        super().__init__(builtins_module=builtins_module)
        self['__module__'] = self
        if name:
            if isinstance(name, str):
                name = WString(name)
            self['__name__'] = name
            self.name = name
        if filename:
            if isinstance(filename, str):
                filename = WString(filename)
            self['__file__'] = filename
        if builtins_module is not None:
            self['__builtins__'] = builtins_module

    def __str__(self):
        if self.name:
            return f'WModule("{self.name}", {len(self)} keys)'
        return f'WModule("{len(self)} keys)'
