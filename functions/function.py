from wtypes.object import WObject


class WFunction(WObject):
    def __init__(self, parameters, expr, enclosing_scope):
        super().__init__()
        self.parameters = parameters
        self.expr = expr
        self.num_parameters = len(parameters)
        self.check_args = True
