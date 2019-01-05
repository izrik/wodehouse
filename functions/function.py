from wtypes.object import WObject


class WFunction(WObject):
    def __init__(self, args, expr):
        super().__init__()
        self.args = args
        self.expr = expr
        self.num_args = len(args)
        self.check_args = True
