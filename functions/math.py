from functions.str import w_str
from wtypes.control import WControl
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.string import WString


def add(*operands):
    # TODO: thorough consideration of all operand type combinations
    # TODO: types to consider: number, string, list, boolean
    if not operands:
        return WNumber(0)
    if len(operands) == 1 and isinstance(operands[0], WList):
        operands = operands[0]
    if isinstance(operands[0], WNumber):
        x = 0
        for operand in operands:
            x += operand.value
        return WNumber(x)
    if isinstance(operands[0], WString):
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
    for operand in operands:
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
    if not operands:
        return WNumber(1)
    x = 1
    for operand in operands:
        try:
            x /= operand.value
        except ZeroDivisionError:
            return WControl(exception=WException('Division by zero'))
    return WNumber(x)
