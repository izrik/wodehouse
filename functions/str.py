from functions.function import WFunction
from functions.magic_function import WMagicFunction
from wtypes.boolean import WBoolean
import wtypes.list
from wtypes.number import WNumber
from wtypes.string import WString
import wtypes.symbol


def w_str(arg):
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
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))
