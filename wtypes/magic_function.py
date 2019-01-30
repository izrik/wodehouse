from inspect import signature

from wtypes.function import WFunction
from wtypes.string import WString


class WMagicFunction(WFunction):
    special_names = {'__current_scope__'}

    def __init__(self, f, enclosing_scope, *, name=None, check_args=True):
        super().__init__([], None, enclosing_scope)
        self.f = f
        sig = signature(f)
        num_parameters = len(list(p for p in sig.parameters.values() if
                                  p.kind in [p.POSITIONAL_ONLY,
                                             p.POSITIONAL_OR_KEYWORD]))
        if any(p for p in sig.parameters.values()
               if p.kind == p.VAR_POSITIONAL):
            num_parameters = None
        self.num_parameters = num_parameters
        if name is None:
            name = f.__name__
        if isinstance(name, str):
            name = WString(name)
        self.name = name
        self.check_args = check_args
        self.sig = sig
        self.pnames = set(p.name for p in self.sig.parameters.values())
        self.names_to_remove = self.special_names.difference(self.pnames)

    def call_magic_function(self, *args, **kwargs):
        kwargs2 = dict(kwargs)
        for name in self.names_to_remove:
            del kwargs2[name]
        return self.f(*args, **kwargs2)
