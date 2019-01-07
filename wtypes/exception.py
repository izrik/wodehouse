from wtypes.object import WObject


class WException(WObject):
    def __init__(self, message):
        self.message = message
