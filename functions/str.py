from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from wtypes.boolean import WBoolean
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.position import Position
from wtypes.stream import WStream
from wtypes.string import WString
import wtypes.symbol


def w_str(arg):
    """
    Convert a WObject to a WString

    :param arg: an object to convert
    :return: the WString representation of `arg`.
    """
    from wtypes.list import WList
    if not isinstance(arg, WObject):
        raise Exception(f'Unknown object type: "{arg}" ({type(arg)})')
    if isinstance(arg, WString):
        return arg
    if isinstance(arg, WNumber):
        return WString(str(arg.value))
    if isinstance(arg, wtypes.symbol.WSymbol):
        return w_str(arg.name)
    if isinstance(arg, WList):
        return WString(str(arg))
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            from functions.function import w_name_of
            return w_name_of(arg)
        return w_str(
            WList(
                wtypes.symbol.WSymbol.get('lambda'),
                WList(*arg.parameters),
                WList(*arg.expr)))
    if isinstance(arg, WBoolean):
        return WString(str(arg))
    from wtypes.scope import WScope
    if isinstance(arg, WScope):
        return WString(str(arg))
    if isinstance(arg, Position):
        return WString(str(arg))
    raise Exception(f'Unknown object type: "{arg}" ({type(arg)})')


def w_format(fmt, *args):
    from functions.math import add
    from wtypes.list import WList
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
                if len(current) > 0:
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


def w_starts_with(s, prefix):
    if not isinstance(s, WString):
        raise Exception(f'Argument "s" to starts_with should be a '
                        f'string. Got "{s}" ({type(s)}) instead.')
    if not isinstance(prefix, WString):
        raise Exception(f'Argument "prefix" to starts_with should be a '
                        f'string. Got "{prefix}" ({type(prefix)}) instead.')
    if s.value.startswith(prefix.value):
        return WBoolean.true
    return WBoolean.false


def w_ends_with(s, prefix):
    if not isinstance(s, WString):
        raise Exception(f'Argument "s" to ends_with should be a '
                        f'string. Got "{s}" ({type(s)}) instead.')
    if not isinstance(prefix, WString):
        raise Exception(f'Argument "prefix" to ends_with should be a '
                        f'string. Got "{prefix}" ({type(prefix)}) instead.')
    if s.value.endswith(prefix.value):
        return WBoolean.true
    return WBoolean.false


def w_join(delim, parts):
    import wtypes.list
    if not isinstance(delim, WString):
        raise Exception(f'Argument "delim" to join should be a '
                        f'string. Got "{delim}" ({type(delim)}) instead.')
    if not isinstance(parts, wtypes.list.WList) or \
            any(not isinstance(p, WString) for p in parts):
        raise Exception(f'Argument "parts" to join should be a list of '
                        f'strings. Got "{parts}" ({type(parts)}) instead.')
    return WString(delim.value.join(p.value for p in parts))


def w_split(s, sep):
    if not isinstance(s, WObject):
        raise TypeError(f'First argument to split should be a WObject.'
                        f'Got "{s}" ({type(s)}) instead.')
    if not isinstance(sep, WObject):
        raise TypeError(f'First argument to split should be a WObject.'
                        f'Got "{sep}" ({type(sep)}) instead.')

    s = w_str(s)
    sep = w_str(sep)

    from wtypes.list import WList
    return WList(*(WString(_) for _ in s.value.split(sep.value)))
