from wtypes.control import WRaisedException
from wtypes.exception import WException


def w_raise(description):
    exc = description
    if not isinstance(exc, WException):
        exc = WException(description)
    return WRaisedException(exception=exc)
