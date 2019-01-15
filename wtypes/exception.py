from wtypes.object import WObject


class WException(WObject):
    def __init__(self, message):
        super().__init__()
        self.message = message
