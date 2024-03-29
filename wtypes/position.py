from wtypes.object import WObject


class Position(WObject):
    def __init__(self, filename, line, char, stream):
        from functions.types import get_type
        from wtypes.string import WString
        from wtypes.number import WNumber
        from wtypes.exception import WException, WrappedWException
        from wtypes.stream import WStream

        super().__init__()

        if filename is None:
            filename = WString('')
        if isinstance(filename, str):
            filename = WString(filename)
        if not isinstance(filename, WObject):
            raise TypeError(f'Argument "filename" must be WString. '
                            f'Got "{filename}" ({type(filename)}) instead.')
        if not isinstance(filename, WString):
            raise WrappedWException(
                WException(f'Argument "filename" must be String. '
                           f'Got "{filename}" ({get_type(filename)}) '
                           f'instead.'))

        if isinstance(line, int):
            line = WNumber(line)
        if not isinstance(line, WObject):
            raise TypeError(f'Argument "line" must be WNumber. '
                            f'Got "{line}" ({type(line)}) instead.')
        if not isinstance(line, WNumber):
            raise WrappedWException(
                WException(f'Argument "line" must be Number. '
                           f'Got "{line}" ({get_type(line)}) instead.'))

        if isinstance(char, int):
            char = WNumber(char)
        if not isinstance(char, WObject):
            raise TypeError(f'Argument "char" must be WNumber. '
                            f'Got "{char}" ({type(char)}) instead.')
        if not isinstance(char, WNumber):
            raise WrappedWException(
                WException(f'Argument "char" must be Number. '
                           f'Got "{char}" ({get_type(char)}) instead.'))

        if stream is not None:
            if not isinstance(stream, WObject):
                raise TypeError(f'Argument "stream" must be WStream. '
                                f'Got "{stream}" ({type(stream)}) instead.')
            if not isinstance(stream, WStream):
                raise WrappedWException(
                    WException(f'Argument "stream" must be Stream. '
                               f'Got "{stream}" ({get_type(stream)}) '
                               f'instead.'))

        self.filename = filename
        self.line = line
        self.char = char
        self.stream = stream

    def __str__(self):
        filename = self.filename.value or '<unknown>'
        line = self.line
        if line is None:
            line = '<unknown>'
        char = self.char
        if char is None:
            char = '<unknown>'
        return f'{filename}:{line},{char}'

    def get_source_line(self):
        if self.stream is None:
            return '<unavailable>'
        return self.stream.get_line(self.line)

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False

        def is_or_equals(a, b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            return a == b

        return \
            is_or_equals(self.filename, other.filename) and \
            is_or_equals(self.line, other.line) and \
            is_or_equals(self.char, other.char)

    def __hash__(self):
        return hash((self.filename, self.line, self.char))

    @classmethod
    def from_wstr(cls, s):
        """Convert a WString (from Position.__str__) back into a Position."""
        from wtypes.exception import WException
        from wtypes.exception import WrappedWException
        from functions.types import get_type
        from wtypes.string import WString
        from functions.str import w_split

        if not isinstance(s, WObject):
            raise TypeError(f'Argument "s" must be WString. '
                            f'Got "{s}" ({type(s)}) instead.')
        if not isinstance(s, WString):
            raise WrappedWException(
                WException(f'Argument "s" must be String. '
                           f'Got "{s}" ({get_type(s)}) '
                           f'instead.'))

        filename, parts = w_split(s, WString(':'))
        line, ch = w_split(parts, WString(','))
        assert isinstance(line, WString)
        line = int(line.value)
        assert isinstance(ch, WString)
        ch = int(ch.value)
        return cls(filename, line, ch, None)
