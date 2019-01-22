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
