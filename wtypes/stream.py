from wtypes.object import WObject
from wtypes.position import Position


class WStream(WObject):
    def __init__(self, s, filename=None):
        super().__init__()
        self.s = s
        self.i = 0
        self.len = len(s)
        self.line = 1
        self.char = 1
        self.filename = filename
        self.lines = []
        self._current_line = []

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
            self.lines.append(''.join(self._current_line))
            self._current_line = []
        else:
            self.char += 1
            self._current_line.append(ch)
        return ch

    def peek(self):
        if not self.has_chars():
            return None
        return self.s[self.i]

    def get_position(self):
        return Position(self.filename, self.line, self.char, self)

    def get_line(self, line_num):
        from wtypes.number import WNumber
        if isinstance(line_num, WNumber):
            line_num = line_num.value
        if line_num == self.line:
            return ''.join(self._current_line)
        return self.lines[line_num - 1]
