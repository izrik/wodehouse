from wtypes.object import WObject


class WControl(WObject):
    """Object that tells w_eval what to do in special cases."""
    pass


class WRaisedException(WControl):
    def __init__(self, exception, stack=None):
        super().__init__()
        self.exception = exception
        self._stack = stack

    @property
    def stack(self):
        return self._stack

    @stack.setter
    def stack(self, value):
        self._stack = value
        if self.exception:
            if not self.exception.stack:
                self.exception.stack = value


class WEvalRequired(WControl):
    def __init__(self, expr, callback, scope=None,
                 hide_callee_stack_frame=False):
        super().__init__()
        self.expr = expr
        self.callback = callback
        self.scope = scope
        self.hide_callee_stack_frame = hide_callee_stack_frame


class WSetHandlers(WControl):
    def __init__(self, exception_handlers, finally_handler, callback):
        super().__init__()
        self.exception_handlers = exception_handlers
        self.finally_handler = finally_handler
        self.callback = callback


class WExecSrcRequired(WControl):
    def __init__(self, src, name, builtins_module, filename, callback):
        super().__init__()
        self.src = src
        self.builtins_module = builtins_module
        self.name = name
        self.filename = filename
        self.callback = callback


class WMacroExpansion(WControl):
    def __init__(self, expr, scope=None):
        super().__init__()
        self.expr = expr
        self.scope = scope


class WReturnValue(WControl):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
