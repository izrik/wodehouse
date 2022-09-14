from wtypes.object import WObject
from wtypes.string import WString


class WException(WObject):
    def __init__(self, message):
        super().__init__()
        if isinstance(message, str):
            message = WString(message)
        self.message = message
        self.stack = None


class WSystemExit(WException):
    """Request to exit."""

    def __init__(self, code=None):
        from wtypes.number import WNumber
        from functions.types import get_type
        from functions.str import w_str
        if not isinstance(code, WObject):
            raise TypeError(f'Code must be a WNumber. '
                            f'Got "{code}" ({type(code)}) instead.')
        if not isinstance(code, WNumber):
            # return WRaisedException(  # can't return from a constructor
            #     WException(
            raise TypeError(f'Code must be a number. '
                            f'Got "{code}" '
                            f'({get_type(code)}) instead.')
        super().__init__(WString(f'WSystemExit({w_str(code).value})'))
        self.code = code

    @staticmethod
    def get_code(exc):
        return exc.code


class WrappedWException(Exception):
    def __init__(self, exc):
        if not isinstance(exc, WException):
            raise TypeError(f'Argument "exc" must be of type WException. '
                            f'Got "{exc}" ({type(exc)}) instead.')
        self.exc = exc


class WSyntaxError(WException):
    """ Invalid syntax. """

    def __init__(self, message, position):
        super().__init__(message)
        self.position = position

# TODO: BaseException
# TODO:   eventually, GeneratorExit
# TODO:   KeyboardInterrupt

# TODO: ArithmeticError
# TODO:   FloatingPointError
# TODO:   OverflowError
# TODO:   ZeroDivisionError
# TODO: AssertionError
# TODO: eventually, AttributeError
# TODO: ImportError
# TODO:   ModuleNotFoundError
# TODO: LookupError
# TODO:   KeyError
# TODO:   IndexError
# TODO: NameError
# TODO:   UnboundLocalError
# TODO: OSError
# TODO: RuntimeError
# TODO:   NotImplementedError
# TODO:   RecursionError
# TODO: StopIteration
# TODO: TypeError
# TODO: ValueError
# TODO:   UnicodeError, et al
