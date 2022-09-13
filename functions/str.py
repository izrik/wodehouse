from wtypes.function import WFunction
from wtypes.macro import WMacro
from wtypes.magic_function import WMagicFunction
from wtypes.boolean import WBoolean
from wtypes.magic_macro import WMagicMacro
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.position import Position
from wtypes.stream import WStream
from wtypes.string import WString


def w_str(arg):
    """
    Convert a WObject to a WString

    :param arg: an object to convert
    :return: the WString representation of `arg`.
    """
    from wtypes.list import WList
    from wtypes.symbol import WSymbol
    from functions.function import w_name_of
    from wtypes.scope import WScope
    from wtypes.set import WSet
    if not isinstance(arg, WObject):
        raise Exception(f'Unknown object type: "{arg}" ({type(arg)})')
    if isinstance(arg, WString):
        return arg
    if isinstance(arg, WNumber):
        return WString(str(arg.value))
    if isinstance(arg, WSymbol):
        return w_str(arg.name)
    if isinstance(arg, (WList, WBoolean, WScope, Position, WSet)):
        return WString(str(arg))
    from wtypes.exception import WException
    if isinstance(arg, WException):
        message = ''
        if arg.message:
            message = w_str(arg.message)
        pos = '<unknown>'
        if arg.stack and arg.stack.expr and arg.stack.expr.position:
            pos = w_str(arg.stack.expr.position)
        return WString(f'Exception "{message}" at {pos}')
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            return w_name_of(arg)
        return w_str(
            WList(
                WSymbol.get('lambda'),
                WList(*arg.parameters),
                WList(*arg.expr)))
    if isinstance(arg, WMacro):
        if isinstance(arg, WMagicMacro):
            return w_name_of(arg)
        return WString("Unknown user-defined macro")
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


def w_replace(s, old, new):
    from wtypes.control import WRaisedException
    from wtypes.exception import WException
    from functions.types import get_type
    if not isinstance(s, WObject):
        raise TypeError(f'Argument "s" to replace should be a WString. '
                        f'Got "{s}" ({type(s)}) instead.')
    if not isinstance(old, WObject):
        raise TypeError(f'Argument "old" to replace should be a WString. '
                        f'Got "{old}" ({type(old)}) instead.')
    if not isinstance(new, WObject):
        raise TypeError(f'Argument "new" to replace should be a WString. '
                        f'Got "{new}" ({type(new)}) instead.')
    if not isinstance(s, WString):
        return WRaisedException(
            WException(f'Argument "s" to replace should be a String. '
                       f'Got "{s}" ({get_type(s)}) instead.'))
    if not isinstance(old, WString):
        return WRaisedException(
            WException(f'Argument "old" to replace should be a String. '
                       f'Got "{old}" ({get_type(old)}) instead.'))
    if not isinstance(new, WString):
        return WRaisedException(
            WException(f'Argument "new" to replace should be a String. '
                       f'Got "{new}" ({get_type(new)}) instead.'))
    return WString(s.value.replace(old.value, new.value))
