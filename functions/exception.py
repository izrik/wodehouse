from wtypes.exception import WException


def exception(message=None):
    if message is None:
        message = 'Exception'
    return WException(message)
