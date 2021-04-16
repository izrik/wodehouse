from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from wtypes.macro import WMacro
from wtypes.magic_macro import WMagicMacro
from wtypes.boolean import WBoolean
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.module import WModule
from wtypes.number import WNumber
from wtypes.scope import WScope
from wtypes.set import WSet
from wtypes.string import WString
from wtypes.symbol import WSymbol


def get_type(arg):
    if isinstance(arg, WNumber):
        return WSymbol.get('Number')
    if isinstance(arg, WString):
        return WSymbol.get('String')
    if isinstance(arg, WSymbol):
        return WSymbol.get('Symbol')
    if isinstance(arg, WList):
        return WSymbol.get('List')
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            return WSymbol.get('MagicFunction')
        return WSymbol.get('Function')
    if isinstance(arg, WBoolean):
        return WSymbol.get('Boolean')
    if isinstance(arg, WMacro):
        if isinstance(arg, WMagicMacro):
            return WSymbol.get('MagicMacro')
        return WSymbol.get('Macro')
    if isinstance(arg, WScope):
        if isinstance(arg, WModule):
            return WSymbol.get('Module')
        return WSymbol.get('Scope')
    if isinstance(arg, WException):
        return WSymbol.get('Exception')
    if isinstance(arg, WSet):
        return WSymbol.get('Set')
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))


def w_isinstance(arg, type_or_types):
    if isinstance(type_or_types, WSymbol):
        argtype = get_type(arg)
        if type_or_types == WSymbol.get('Function') and \
                argtype == WSymbol.get('MagicFunction'):
            return WBoolean.true
        if type_or_types == WSymbol.get('Macro') and \
                argtype == WSymbol.get('MagicMacro'):
            return WBoolean.true
        if type_or_types == WSymbol.get('Scope') and \
                argtype == WSymbol.get('Module'):
            return WBoolean.true
        if argtype == type_or_types:
            return WBoolean.true
        return WBoolean.false
    if not isinstance(type_or_types, WList):
        raise Exception(
            "Expected symbol or list, got \"{}\" ({}) instead.".format(
                type_or_types, type(type_or_types)))
    for t in type_or_types:
        if w_isinstance(arg, t):
            return WBoolean.true
    return WBoolean.false
