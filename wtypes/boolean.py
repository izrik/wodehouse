from wtypes.object import WObject


class WBoolean(WObject):
    true = None
    false = None

    def __init__(self, value):
        super().__init__()
        self.value = not not value

    def __repr__(self):
        return 'WBoolean({})'.format(str(self))

    def __str__(self):
        return 'true' if self.value else 'false'

    def __eq__(self, other):
        if isinstance(other, bool):
            return self.value == other
        if isinstance(other, WBoolean):
            return self.value == other.value
        return False


WBoolean.true = WBoolean(True)
WBoolean.false = WBoolean(False)

