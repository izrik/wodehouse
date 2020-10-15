from wtypes.object import WObject


class WSet(WObject):
    def __init__(self, *values):
        super().__init__()
        self.values = set(values)

    def __repr__(self):
        return 'WSet({})'.format(
            ' '.join(repr(value) for value in self.values))

    def __str__(self):
        return '(set {})'.format(' '.join(str(value) for value
                                          in self.values))

    def __eq__(self, other):
        if isinstance(other, WSet):
            return self.values == other.values
        if isinstance(other, set):
            return self.values == other
        return False

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __contains__(self, item):
        return item in self.values

    def add(self, value):
        self.values.add(value)
