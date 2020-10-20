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
