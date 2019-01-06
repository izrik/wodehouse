from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber


def eq(a, b):
    if a == b:
        return WBoolean.true
    return WBoolean.false


def w_not(arg):
    if arg is WBoolean.true:
        return WBoolean.false
    if arg is WBoolean.false:
        return WBoolean.true
    raise Exception('Unexpected object type: "{}" ({})'.format(arg, type(arg)))


def w_or(*operands):
    # TODO: thorough consideration of all operand type combinations
    if not operands:
        raise Exception("No arguments given to 'or'.")
    if len(operands) == 1 and isinstance(operands[0], WList):
        operands = operands[0]
    if len(operands) < 1:
        raise Exception("No arguments given to 'or'.")
    if any(not isinstance(op, WBoolean) for op in operands):
        raise Exception("Only booleans are allowed in logical operations.")
    for operand in operands:
        if operand is WBoolean.true:
            return WBoolean.true
    return WBoolean.false


def w_and(*operands):
    # TODO: thorough consideration of all operand type combinations
    if not operands:
        raise Exception("No arguments given to 'and'.")
    if len(operands) == 1 and isinstance(operands[0], WList):
        operands = operands[0]
    if len(operands) < 1:
        raise Exception("No arguments given to 'and'.")
    if any(not isinstance(op, WBoolean) for op in operands):
        raise Exception("Only booleans are allowed in logical operations.")
    for operand in operands:
        if operand is WBoolean.false:
            return WBoolean.false
    return WBoolean.true


def less_than(a, b):
    if not isinstance(a, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(a, type(a)))
    if not isinstance(b, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(b, type(b)))
    if a.value < b.value:
        return WBoolean.true
    return WBoolean.false


def less_than_or_equal_to(a, b):
    if not isinstance(a, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(a, type(a)))
    if not isinstance(b, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(b, type(b)))
    if a.value <= b.value:
        return WBoolean.true
    return WBoolean.false


def greater_than(a, b):
    if not isinstance(a, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(a, type(a)))
    if not isinstance(b, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(b, type(b)))
    if a.value > b.value:
        return WBoolean.true
    return WBoolean.false


def greater_than_or_equal_to(a, b):
    if not isinstance(a, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(a, type(a)))
    if not isinstance(b, WNumber):
        raise Exception(
            "Value is not a number: \"{}\" ({})".format(b, type(b)))
    if a.value >= b.value:
        return WBoolean.true
    return WBoolean.false
