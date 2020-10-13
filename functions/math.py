from functions.types import get_type
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.string import WString


def add(*operands):
    # TODO: thorough consideration of all operand type combinations
    # TODO: types to consider: number, string, list, boolean
    if operands is None:
        return WNumber(0)
    if not isinstance(operands, (tuple, list, WList)):
        raise ValueError(f'Argument to + should be a list. '
                         f'Get "{operands}" ({get_type(operands)}) instead.')
    if len(operands) < 1:
        return WNumber(0)
    if isinstance(operands[0], WList):
        x = []
        for operand in operands:
            x += operand
        return WList(*x)
    if isinstance(operands[0], WNumber):
        x = 0
        for operand in operands:
            x += operand.value
        return WNumber(x)
    if isinstance(operands[0], WString):
        from functions.str import w_str
        parts = WList()
        for operand in operands:
            parts = parts.append(w_str(operand).value)
        return WString(''.join(parts))
    raise Exception(
        "Unknown operand type: "
        "\"{}\" ({})".format(operands[0], type(operands[0])))


def sub(*operands):
    if not operands:
        return WNumber(0)
    x = 0
    first = True
    for operand in operands:
        if first:
            x = operand.value
            first = False
            continue
        x -= operand.value
    return WNumber(x)


def mult(*operands):
    if not operands:
        return WNumber(1)
    x = 1
    for operand in operands:
        x *= operand.value
    return WNumber(x)


def div(*operands):
    if not operands or len(operands) < 1:
        return WNumber(1)
    x = 1
    first = True
    for operand in operands:
        if first:
            x = operand.value
            first = False
            continue
        try:
            x /= operand.value
        except ZeroDivisionError:
            return WRaisedException(exception=WException('Division by zero'))
    return WNumber(x)
