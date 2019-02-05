from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.string import WString
from pathlib import Path
from functions.str import w_str
import os.path


def w_print(x, end=None, *, printer=None):
    if printer is None:
        printer = print

    if isinstance(end, WString):
        end = end.value

    if isinstance(x, WNumber):
        printer(x.value, end=end)
    elif isinstance(x, WString):
        printer(x.value, end=end)
    else:
        printer(x, end=end)
    return x


def read_file(path):
    if isinstance(path, WString):
        path = path.value
    with open(path) as f:
        return WString(f.read())


def w_is_file(path):
    _path = Path(w_str(path).value)
    return WBoolean.from_value(_path.is_file())


def w_is_dir(path):
    _path = Path(w_str(path).value)
    return WBoolean.from_value(_path.is_dir())


def w_list_dir(path):
    _path = Path(w_str(path).value)
    return WList(*(WString(_) for _ in os.listdir(_path)))
