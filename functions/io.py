from functions.math import add
from functions.str import w_str
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.stream import WStream
from wtypes.string import WString


def w_print(x, *, printer=None):
    if printer is None:
        printer = print

    if isinstance(x, WNumber):
        printer(x.value)
    elif isinstance(x, WString):
        printer(x.value)
    else:
        printer(x)
    return x


def w_format(fmt, *args):
    if args is None:
        args = WList()
    elif not isinstance(args, WList):
        args = WList(*args)
    _args = args
    s = WStream(fmt.value)
    parts = WList()
    current = WList()
    # TODO: extract a formatter object and/or function
    while s.has_chars():
        ch = WString(s.peek())
        if ch == '{':
            s.get_next_char()
            ch = WString(s.peek())
            if ch == '}':
                if len(args) < 1:
                    raise Exception(
                        "Not enough arguments for format string \"{}\". "
                        "Only got {} arguments.".format(fmt, len(_args)))
                parts = parts.append(add(*current))
                parts = parts.append(w_str(args.head))
                args = args.remaining
                current = WList()
                s.get_next_char()
                continue
            elif ch == '{':
                pass
            else:
                raise Exception(
                    "Invalid format character "
                    "\"{}\" in \"{}\"".format(ch, fmt))
        current = current.append(ch)
        s.get_next_char()
    if len(current) > 0:
        parts = parts.append(add(*current))
    return add(*parts)


def read_file(path):
    if isinstance(path, WString):
        path = path.value
    with open(path) as f:
        return WString(f.read())
