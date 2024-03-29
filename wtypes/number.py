from wtypes.object import WObject


class WNumber(WObject):
    def __init__(self, value, position=None):
        super().__init__(position=position)
        if not isinstance(value, (bool, int, complex, float)):
            raise TypeError(f'Argument "value" should be a numerical type. '
                            f'Got "{value}" ({type(value)}) instead.')
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

    def __hash__(self):
        return self.value.__hash__()
