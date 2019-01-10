from wtypes.object import WObject


class Position(WObject):
    def __init__(self, filename, line, char):
        self.filename = filename
        self.line = line
        self.char = char

    def __str__(self):
        filename = self.filename or '<unknown>'
        return f'{filename}:{self.line},{self.char}'
