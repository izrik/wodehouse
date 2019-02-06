from wtypes.object import WObject


class Position(WObject):
    def __init__(self, filename, line, char, stream):
        self.filename = filename
        self.line = line
        self.char = char
        self.stream = stream

    def __str__(self):
        filename = self.filename or '<unknown>'
        return f'{filename}:{self.line},{self.char}'

    def get_source_line(self):
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
