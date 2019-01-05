from wtypes.object import WObject


class WNumber(WObject):
    def __init__(self, value, position=None):
        super().__init__(position=position)
        if isinstance(value, WObject):
            raise TypeError(
                "Value should not be a w-object: \"{}\"".format(
                    value, type(value)))
        self.value = value

    def __repr__(self):
        return 'WNumber({})'.format(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, WNumber):
            return self.value == other.value
        return False
