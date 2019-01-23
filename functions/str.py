from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from wtypes.boolean import WBoolean
import wtypes.list
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.string import WString
import wtypes.symbol


def w_str(arg):
    """
    Convert a WObject to a WString

    :param arg: an object to convert
    :return: the WString representation of `arg`.
    """
    if not isinstance(arg, WObject):
        raise Exception(f'Unknown object type: "{arg}" ({type(arg)})')
    if isinstance(arg, WString):
        return arg
    if isinstance(arg, WNumber):
        return WString(str(arg.value))
    if isinstance(arg, wtypes.symbol.WSymbol):
        return WString(arg.name)
    if isinstance(arg, wtypes.list.WList):
        return WString(str(arg))
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            return WString(str(arg.name))
        return w_str(
            wtypes.list.WList(
                wtypes.symbol.WSymbol.get('lambda'),
                wtypes.list.WList(*arg.parameters),
                wtypes.list.WList(*arg.expr)))
    if isinstance(arg, WBoolean):
        return WString(str(arg))
    from wtypes.scope import WScope
    if isinstance(arg, WScope):
        return WString(str(arg))
    raise Exception(f'Unknown object type: "{arg}" ({type(arg)})')
