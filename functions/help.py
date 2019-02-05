from functions.str import w_str
from functions.types import get_type
from wtypes.string import WString


def w_help(obj):
    t = get_type(obj)
    if hasattr(obj, 'name'):
        name = obj.name
    elif hasattr(obj, '__name__'):
        name = obj.__name__
    else:
        name = w_str(obj)

    return WString(f'{name} ({t})')
