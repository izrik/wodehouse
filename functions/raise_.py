from wtypes.control import WControl
from wtypes.exception import WException


def w_raise(description):
    return WControl(exception=WException(description))
