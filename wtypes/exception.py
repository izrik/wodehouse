from wtypes.object import WObject
from wtypes.string import WString


class WException(WObject):
    def __init__(self, message):
        super().__init__()
        if isinstance(message, str):
            message = WString(message)
        self.message = message
        self.stack = None
