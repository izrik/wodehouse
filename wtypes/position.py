
class Position(object):
    def __init__(self, line, char):
        self.line = line
        self.char = char

    def __str__(self):
        return f'{self.line}:{self.char}'
