from wtypes.number import WNumber
from wtypes.string import WString


def int_from_str(s, position=None):
    if isinstance(s, WString):
        s = s.value
    s = str(s)
    return WNumber(int(s), position=position)
