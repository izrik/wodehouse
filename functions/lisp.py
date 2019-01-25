from wtypes.list import WList


def car(first, *args):
    if args:
        raise Exception('Too many arguments given to car')
    if not isinstance(first, WList):
        raise TypeError('{} is not a list'.format(str(first)))
    if len(first) < 1:
        return WList()
    return first.head


def cdr(first, *args):
    if args:
        raise Exception('Too many arguments given to cdr')
    if not isinstance(first, WList):
        raise TypeError('{} is not a list'.format(str(first)))
    return first.remaining


def cons(a, b):
    if not isinstance(b, WList):
        raise Exception(
            "Expected b to be a list. "
            "Got \"{}\" ({}) instead.".format(b, type(b)))
    return WList(a, *b)


def atom(arg):
    return not isinstance(arg, WList)
