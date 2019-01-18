from wtypes.control import WRaisedException
from wtypes.exception import WException


def w_raise(description):
    return WRaisedException(exception=WException(description))
