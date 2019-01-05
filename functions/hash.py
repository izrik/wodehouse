import hashlib

from functions.str import w_str
from wtypes.string import WString


def w_hash(arg):
    bytes_arg = w_str(arg).value.encode('utf-8')
    h = hashlib.sha256(bytes_arg).hexdigest()
    return WString(h)
