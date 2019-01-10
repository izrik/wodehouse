from wtypes.object import WObject
from wtypes.position import Position


class WStream(WObject):
    def __init__(self, s, filename=None):
        self.s = s
        self.i = 0
        self.len = len(s)
        self.line = 1
        self.char = 1
        self.filename = filename

    def has_chars(self):
        return self.i < self.len

    def get_next_char(self):
        if not self.has_chars():
            raise Exception("No more characters in the stream.")
        ch = self.peek()
        self.i += 1
        if ch == '\n':
            self.char = 1
            self.line += 1
        else:
            self.char += 1
        return ch

    def peek(self):
        if not self.has_chars():
            return None
        return self.s[self.i]

    def get_position(self):
        return Position(self.filename, self.line, self.char)
