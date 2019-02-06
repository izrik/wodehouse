from wtypes.list import WList


def car(arg):
    if not isinstance(arg, WList):
        raise TypeError('{} is not a list'.format(str(arg)))
    if len(arg) < 1:
        return WList()
    return arg.head


def cdr(arg):
    if not isinstance(arg, WList):
        raise TypeError('{} is not a list'.format(str(arg)))
    return arg.remaining


def cons(a, b):
    if not isinstance(b, WList):
        raise Exception(
            "Expected b to be a list. "
            "Got \"{}\" ({}) instead.".format(b, type(b)))
    return WList(a, *b)


def atom(arg):
    return not isinstance(arg, WList)
