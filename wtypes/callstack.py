from wtypes.object import WObject


class WStackFrame(WObject):

    location = None
    expr = None
    scope = None
    expanded_expr = None
    expanded_scope = None
    callee = None
    args = None
    evaled_args = None
    fscope = None
    exception_handlers = None
    finally_handler = None

    def __str__(self):
        return f'location={self.location}, expr={self.expr}, ' \
               f'scope={self.scope}, expanded_expr={self.expanded_expr}, ' \
               f'expanded_scope={self.expanded_scope}, ' \
               f'callee={self.callee}, args={self.args}, ' \
               f'evaled_args={self.evaled_args}, fscope={self.fscope}'

    def __init__(self, location, prev):
        super().__init__()
        self.location = location
        self.prev = prev

    def get_location(self):
        if self.location is not None:
            return self.location
        return '<module>'
