from wtypes.object import WObject


class WString(WObject):
    def __init__(self, value, position=None):
        super().__init__(position=position)
        if not isinstance(value, str):
            raise TypeError('Argument to WString.__init__ must be a '
                            'py-string.')
        self.value = value

    def __repr__(self):
        return 'WString("{}")'.format(self.escaped())

    def __str__(self):
        return '"{}"'.format(self.escaped())

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, WString):
            return self.value == other.value
        return False

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

    def __add__(self, other):
        if not isinstance(other, WObject):
            raise TypeError(f'Operand must be a WObject. '
                            f'Got {other} ({type(other)}) instead.')
        if not isinstance(other, WString):
            from wtypes.control import WRaisedException
            from wtypes.exception import WException
            from functions.types import get_type
            return WRaisedException(
                WException(f'Unsupported operand type(s) for +: '
                           f'"{get_type(self)}" and "{get_type(other)}"'))
        return WString(self.value + other.value)

    def escaped(self):
        def escape_char(_ch):
            if _ch == '\n':
                return '\\n'
            if _ch == '\r':
                return '\\r'
            if _ch == '\t':
                return '\\t'
            if _ch in '"\\':
                return '\\' + _ch
            return _ch

        return ''.join(escape_char(ch) for ch in self.value)
