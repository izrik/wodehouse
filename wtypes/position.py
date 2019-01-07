
class Position(object):
    def __init__(self, filename, line, char):
        self.filename = filename
        self.line = line
        self.char = char

    def __str__(self):
        filename = self.filename or '<unknown>'
        return f'{filename}:{self.line},{self.char}'
