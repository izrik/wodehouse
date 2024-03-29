from functions.str import w_str
from wtypes.boolean import WBoolean
from wtypes.stream import WStream
from wtypes.string import WString


def stream(s, filename=None):
    return WStream(w_str(s).value, filename=filename)


def stream_has_chars(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    if s.has_chars():
        return WBoolean.true
    return WBoolean.false


def stream_get_next_char(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return WString(s.get_next_char())


def stream_peek(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    if not s.has_chars():
        return WString('')
    return WString(s.peek())


def stream_get_position(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return s.get_position()


def get_stream_index(s):
    from wtypes.number import WNumber
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return WNumber(s.i)
