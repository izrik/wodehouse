from wtypes.module import WModule


def w_module(builtins_module, name=None, filename=None):
    return WModule(builtins_module=builtins_module, name=name,
                   filename=filename)
