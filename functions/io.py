from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.string import WString
from pathlib import Path
from functions.str import w_str
import os.path


def w_print(x, end=None, *, printer=None):
    if printer is None:
        printer = print

    from wtypes.object import WObject
    if end is not None and isinstance(end, WObject):
        end = w_str(end)
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


def write_file(path, content):
    if isinstance(path, WObject):
        path = w_str(path).value
    if isinstance(content, WObject):
        content = w_str(content).value
    with open(path, 'w') as f:
        count = f.write(content)
        return WNumber(count)


def append_file(path, content):
    if isinstance(path, WObject):
        path = w_str(path).value
    if isinstance(content, WObject):
        content = w_str(content).value
    with open(path, 'a') as f:
        return WNumber(f.write(content))


def w_is_file(path):
    _path = Path(w_str(path).value)
    return WBoolean.from_value(_path.is_file())


def w_is_dir(path):
    _path = Path(w_str(path).value)
    return WBoolean.from_value(_path.is_dir())


def w_list_dir(path):
    _path = Path(w_str(path).value)
    return WList(*(WString(_) for _ in os.listdir(_path)))
