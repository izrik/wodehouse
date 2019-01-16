
from wtypes.object import WObject


class WControl(WObject):
    """
    Object that tells w_eval what to do in special cases.

    If exception is not None, then just return the whole control object.
    If callback is not None, then evaluate expr and pass it to callback.
        If scope is not None, use that when evaluating expr
    Otherwise, simply return expr without evaluating it.

    The stack attribute is used for informational purposes in other parts of
    the program.
    """
    def __init__(self, expr=None, scope=None, callback=None, exception=None,
                 stack=None):
        """Initialize self."""
        super().__init__()
        self.expr = expr
        self.scope = scope
        self.callback = callback
        self.exception = exception
        self.stack = stack
