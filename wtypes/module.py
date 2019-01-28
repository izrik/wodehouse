from wtypes.scope import WScope


class WModule(WScope):
    def __init__(self, values=None, enclosing_scope=None,
                 builtins_module=None):
        super().__init__(values, enclosing_scope, builtins_module)
