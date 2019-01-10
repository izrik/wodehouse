from inspect import signature

from wtypes.function import WFunction


class WMagicFunction(WFunction):
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
        self.name = name
        self.check_args = check_args

    def __str__(self):
        return str(self.name)

    def call_magic_function(self, *args, **kwargs):
        return self.f(*args, **kwargs)
