from wtypes.object import WObject
from wtypes.symbol import WSymbol


class WList(WObject):
    def __init__(self, *values, position=None):
        super().__init__(position=position)
        self.values = list(values)

    def __repr__(self):
        return 'WList({})'.format(
            ' '.join(repr(value) for value in self.values))

    def __str__(self):
        if len(self) == 2 and self.head == WSymbol.get('quote'):
            return "'{}".format(str(self.values[1]))
        return '({})'.format(' '.join(str(value) for value in self.values))

    def __eq__(self, other):
        if isinstance(other, WList):
            return self.values == other.values
        if isinstance(other, list):
            return self.values == other
        if isinstance(other, tuple):
            return self.values == list(other)
        return False

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

    def __contains__(self, item):
        return item in self.values

    @property
    def head(self):
        if not self.values:
            return None
        return self.values[0]

    @property
    def second(self):
        if self.values and len(self.values) > 1:
            return self.values[1]

    @property
    def remaining(self):
        if not self.values:
            return WList()
        return WList(*self.values[1:])

    def append(self, value):
        new_list = list(self.values)
        new_list.append(value)
        return WList(*new_list)

    def extend(self, *values):
        new_list = list(self.values)
        new_list.extend(values)
        return WList(*new_list)
