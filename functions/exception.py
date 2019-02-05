from wtypes.callstack import WStackFrame
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.string import WString


def exception(message=None):
    if message is None:
        message = 'Exception'
    return WException(message)


def get_message(exc):
    if not isinstance(exc, WException):
        return WRaisedException(
            WException(
                f'Argument to get_message must be an exception. '
                f'Got "{exc}" ({type(exc)}) instead.'))
    return exc.message


def w_format_stacktrace(exc_or_stack, default_filename=None):
    if not isinstance(exc_or_stack, (WRaisedException, WException,
                                     WStackFrame)):
        return WRaisedException(
            WException(
                f'First argument to format_stacktrace must be a '
                f'WRaisedException or WException or WStackFrame. '
                f'Got "{exc_or_stack}" ({type(exc_or_stack)})" instead.'))

    if default_filename is None:
        default_filename = '<unknown>'
    elif not isinstance(default_filename, WString):
        return WRaisedException(
            WException(
                f'Second argument to format_stacktrace must be a string. '
                f'Got "{default_filename}" ({type(default_filename)}) '
                f'instead.'))
    else:
        default_filename = default_filename.value

    stack = exc_or_stack
    if isinstance(exc_or_stack, (WRaisedException, WException)):
        stack = exc_or_stack.stack

    s = format_stacktrace(stack, default_filename)

    return WString(s)


def format_stacktrace(stack, default_filename=None):
    if default_filename is None:
        default_filename = '<unknown>'
    frames = []
    while stack is not None:
        expr = stack.expanded_expr
        if not expr:
            expr = stack.expr
        if not expr:
            stack = stack.prev
            continue

        filename = default_filename
        line = '<unknown>'
        expansion = '<unknown>'
        pos = expr.position
        if pos:
            filename = pos.filename or default_filename
            line = pos.line or '<unknown>'
            expansion = pos.get_source_line().strip()
        if len(expansion) > 64:
            expansion = expansion[0:60] + ' ...'
        frames.append(
            f'  File "{filename}", line {line}, in '
            f'{stack.get_location()}\n'
            f'    {expansion}')
        stack = stack.prev
    frames.reverse()
    return '\n'.join(frames)
