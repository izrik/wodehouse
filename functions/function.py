from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.macro import WMacro
from wtypes.string import WString


def w_name_of(f):
    if f is None:
        raise Exception("No argument given to name_of.")
    if not isinstance(f, (WFunction, WMacro)):
        return WRaisedException(
            WException(
                f'Argument to name_of must be a function or macro. '
                f'Got "{f}" ({type(f)}) instead.'))
    if f.name is None:
        if isinstance(f, WFunction):
            return WString("<unnamed_function>")
        # isinstance(f, WMacro)
        return WString("<unnamed_macro>")
    return f.name
