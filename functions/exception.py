from wtypes.control import WRaisedException
from wtypes.exception import WException


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
