from inspect import signature

from functions.function import WFunction


class WMagicFunction(WFunction):
    def __init__(self, f, name=None, check_args=True):
        super().__init__([], None)
        self.f = f
        sig = signature(f)
        num_args = len(list(p for p in sig.parameters.values() if
                            p.kind in [p.POSITIONAL_ONLY,
                                       p.POSITIONAL_OR_KEYWORD]))
        if any(p for p in sig.parameters.values()
               if p.kind == p.VAR_POSITIONAL):
            num_args = None
        self.num_args = num_args
        if name is None:
            name = f.__name__
        self.name = name
        self.check_args = check_args

    def __str__(self):
        return str(self.name)

    def __call__(self, *args, **kwargs):
        return self.f(*args)
