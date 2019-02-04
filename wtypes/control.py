from wtypes.object import WObject


class WControl(WObject):
    """Object that tells w_eval what to do in special cases."""
    pass


class WRaisedException(WControl):
    def __init__(self, exception, stack=None):
        super().__init__()
        self.exception = exception
        self.stack = stack


class WEvalRequired(WControl):
    def __init__(self, expr, callback, scope=None,
                 hide_callee_stack_frame=False):
        super().__init__()
        self.expr = expr
        self.callback = callback
        self.scope = scope
        self.hide_callee_stack_frame = hide_callee_stack_frame


class WSetHandlers(WControl):
    def __init__(self, exception_handler, finally_handler, callback):
        super().__init__()
        self.exception_handler = exception_handler
        self.finally_handler = finally_handler
        self.callback = callback


class WExecSrcRequired(WControl):
    def __init__(self, src, builtins_module, filename, callback):
        super().__init__()
        self.src = src
        self.builtins_module = builtins_module
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
