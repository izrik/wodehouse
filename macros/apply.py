from wtypes.magic_macro import WMagicMacro


class Apply(WMagicMacro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, scope=None, **kwargs):
        return args, scope
