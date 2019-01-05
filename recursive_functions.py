#!/usr/bin/env python

"""
An attempted implementation of the original LISP.

See "Recursive Functions of Symbolic Expressions and Their Computation by
Machine, Part I", by John McCarthy 1960
"""

import string

import traceback
from collections import ChainMap


class Stream(object):
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.len = len(s)

    def has_chars(self):
        return self.i < self.len

    def get_next_char(self):
        if not self.has_chars():
            return None
        ch = self.peek()
        self.i += 1
        return ch

    def peek(self):
        if not self.has_chars():
            return None
        return self.s[self.i]


def parse(s):
    return read_expr(s)


def read_expr(s):
    ch = s.peek()
    if ch == '(':
        return read_call(s)
    if ch in string.digits:
        return read_integer_literal(s)
    if ch in '+-*/' or ch in string.ascii_letters:
        return read_symbol(s)
    raise Exception('Unknown starting character "{}" in read_expr'.format(ch))


class WObject(object):
    pass


__symbols__ = {}


def get_symbol(name):
    if name not in __symbols__:
        __symbols__[name] = Symbol(name)
    return __symbols__[name]


class Symbol(WObject):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Symbol({})'.format(self.name)


class Symbols:
    nil = get_symbol('nil')
    quote = get_symbol('quote')
    atom = get_symbol('atom')
    eq = get_symbol('eq')
    cond = get_symbol('cond')
    car = get_symbol('car')
    cdr = get_symbol('cdr')
    cons = get_symbol('cons')
    label = get_symbol('label')
    lambda_ = get_symbol('lambda')


def read_symbol(s):
    ch = s.peek()
    if ch in string.ascii_letters:
        return read_name(s)
    if ch in '+-*/':
        s.get_next_char()
        return Symbol(ch)


def read_name(s):
    chs = []
    while s.has_chars() and s.peek() in string.ascii_letters:
        chs.append(s.get_next_char())
    name = ''.join(chs)
    return Symbol(name)


class Number(WObject):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Number("{}")'.format(self.value)


def read_integer_literal(s):
    chs = []
    while s.has_chars() and s.peek() in string.digits:
        chs.append(s.get_next_char())
    _s = ''.join(chs)
    return Number(int(_s))


class Call(WObject):
    def __init__(self, exprs):
        self.exprs = exprs

    def __str__(self):
        return 'Call({})'.format(', '.join(str(x) for x in self.exprs))

    @property
    def callee(self):
        if self.exprs:
            return self.exprs[0]

    @property
    def arguments(self):
        if self.exprs:
            return self.exprs[1:]


def read_call(s):
    assert s.peek() == '('
    exprs = []
    s.get_next_char()
    while True:
        while True:
            if not s.has_chars():
                raise Exception(
                    'Ran out of characters before call was finished.')
            ch = s.peek()
            if ch not in string.whitespace:
                break
            s.get_next_char()
        if s.peek() == ')':
            s.get_next_char()
            break
        expr = read_expr(s)
        exprs.append(expr)
    return Call(exprs)


def apply_expr(expr, scope):
    if isinstance(expr, int):
        return expr
    if isinstance(expr, Call):
        callee = apply_expr(expr.callee, scope)
        args = expr.arguments
        while isinstance(callee, Macro):
            exprs, scope = callee(*args, scope=scope)
            if len(exprs) < 1:
                raise Exception('Ran out of arguments')
            callee = apply_expr(exprs[0], scope=scope)
            args = exprs[1:]
        args = [apply_expr(arg, scope) for arg in args]
        return callee(*args)
    if isinstance(expr, Symbol):
        if expr.name not in scope:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = scope[expr.name]
        # while isinstance(value, WodehouseObject):
        #     value = apply_expr(value, scope)
        return value
    if isinstance(expr, Number):
        return expr.value
    # if isinstance(expr, Macro):
    #     return expr
    raise Exception('Unknown object type: "{}" ({})'.format(expr, type(expr)))


def add(*operands):
    if not operands:
        return 0
    x = 0
    for operand in operands:
        x += operand
    return x


def sub(*operands):
    if not operands:
        return 0
    x = 0
    for operand in operands:
        x -= operand
    return x


def mult(*operands):
    if not operands:
        return 1
    x = 1
    for operand in operands:
        x *= operand
    return x


def div(*operands):
    if not operands:
        return 1
    x = 1
    for operand in operands:
        x /= operand
    return x


class Macro(WObject):
    def __init__(self, func=None):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.func:
            return self.func(*args, **kwargs)
        raise NotImplemented


class Let(Macro):
    def __init__(self):
        super(Let, self).__init__()

    def __call__(self, symbol, value, *exprs, scope=None, **kwargs):
        if scope is None:
            scope = {}
        _scope = scope
        scope = ChainMap({}, _scope)
        scope[symbol.name] = apply_expr(value, _scope)
        return exprs, scope


class Apply(Macro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, scope=None, **kwargs):
        return args, scope


# class MacroMacro(Macro):
#     def __call__(self, name, arglist, *body, scope=None, **kwargs):
#         pass

class Quote(Macro):
    def __call__(self, *args, scope=None, **kwargs):
        return args, scope


class WList(WObject):
    def __init__(self, *values):
        self.values = list(values)

    def __str__(self):
        return '({})'.format(' '.join(str(value) for value in self.values))

    @property
    def head(self):
        if not self.values:
            return None
        return self.values[0]

    @property
    def remaining(self):
        if not self.values:
            return WList()
        return WList(*self.values[1:])


def list_func(*args):
    return WList(*args)


def car(x):
    if atom(x):
        raise Exception('{} is atomic'.format(str(x)))
    # if args:
    #     raise Exception('Too many arguments given to car')
    # if not isinstance(first, WList):
    #     raise TypeError('{} is not a list'.format(str(first)))
    return x.head


def cdr(x):
    if atom(x):
        raise Exception('{} is atomic'.format(str(x)))
    # if args:
    #     raise Exception('Too many arguments given to cdr')
    # if not isinstance(first, WList):
    #     raise TypeError('{} is not a list'.format(str(first)))
    return x.tail


def caar(x):
    return car(car(x))


def cadr(x):
    return car(cdr(x))


def cadar(x):
    return car(cdr(car(x)))


def caddr(x):
    return car(cdr(cdr(x)))


def caddar(x):
    return car(cdr(cdr(car(x))))


def atom(x):
    # return not isinstance(x, WList)
    if isinstance(x, Symbol):
        return True
    return False


def eq(a, b):
    if not atom(a):
        return False
    if not atom(b):
        return False
    return a == b


def appq(m):
    if null(m):
        return Symbols.nil
    return cons(w_list(Symbols.quote, car(m)), appq(cdr(m)))


def apply(f, args):
    return w_eval(cons(f, appq(args)), Symbols.nil)


def equal(x, y):
    return (atom(x) and atom(y) and eq(x, y)) or \
           ((not atom(x)) and
            (not atom(y)) and
            equal(car(x), car(y)) and
            equal(cdr(x), cdr(y)))


def append(x, y):
    if null(x):
        return y
    return cons(car(x), append(cdr(x), y))


def among(x, y):
    return not null(y) and (equal(x, car(y)) or among(x, cdr(y)))


def pair(x, y):
    if null(x) and null(y):
        return Symbols.nil
    if (not atom(x)) and (not atom(y)):
        return cons(w_list(car(x), car(y)), pair(cdr(x), cdr(y)))
    raise Exception('Not defined')


def assoc(x, y):
    if eq(caar(y), x):
        return cadar(y)
    return assoc(x, cdr(y))


def null(x):
    return atom(x) and eq(x, Symbols.nil)


def sublis(x, y):
    def sub2(w, z):
        if null(x):
            return z
        if eq(caar(x), z):
            return cadar(x)
        return sub2(cdr(x), z)

    if atom(y):
        return sub2(x, y)
    return cons(sublis(x, car(y)), sublis(x, cdr(y)))


class SExpr(object):
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        return '({} . {})'.format(str(self.head), str(self.tail))


def cons(x, y):
    return SExpr(x, y)


def w_list(x, *args):
    if not args:
        return cons(x, Symbols.nil)
    return cons(x, w_list(*args))


def w_eval(e, a):
    if atom(e):
        return assoc(e, a)
    if atom(car(e)):
        if eq(car(e), Symbols.quote):
            return cadr(e)
        if eq(car(e), Symbols.atom):
            return atom(w_eval(cadr(e), a))
        if eq(car(e), Symbols.eq):
            return w_eval(cadr(e), a) == w_eval(caddr(e), a)
        if eq(car(e), Symbols.cond):
            return evcon(cdr(e), a)
        if eq(car(e), Symbols.car):
            return car(w_eval(cadr(e), a))
        if eq(car(e), Symbols.cdr):
            return cdr(w_eval(cadr(e), a))
        if eq(car(e), Symbols.cons):
            return cons(w_eval(cadr(e), a), w_eval(caddr(e), a))
        return w_eval(cons(assoc(car(e), a), evlis(cdr(e), a)), a)
    if eq(caar(e), Symbols.label):
        return w_eval(cons(caddar(e), cdr(e)),
                      w_list(cadar(e), car(e), a))
    if eq(caar(e), Symbols.lambda_):
        return w_eval(caddar(e), append(pair(cadar(e), evlis(cdr(e), a)), a))
    raise Exception('????')


def evcon(e, a):
    if w_eval(caar(e), a):
        return w_eval(cadar(e), a)
    return evcon(cdr(e), a)


def evlis(m, a):
    if null(m):
        return Symbols.nil
    return cons(w_eval(car(m), a), evlis(cdr(m), a))


def repl(prompt=None):
    if prompt is None:
        prompt = '>>> '
    scope = {
        '+': add,
        '-': sub,
        '*': mult,
        '/': div,
        'let': Let(),
        'apply': Apply(),
        'list': list_func,
        'car': car,
        'cdr': cdr,
        'atom': atom,
        'eq': eq,
    }
    while True:
        try:
            input_s = input(prompt)
            if input_s is None:
                continue
            if input_s.strip() in ['quit', 'exit']:
                break
            if input_s.strip() == '':
                continue
            stream = Stream(input_s)
            expr = parse(stream)
            value = apply_expr(expr, scope)
            print(value)
        except Exception as ex:
            print('Caught the following exception: {}'.format(ex))
            print(line for line in
                  traceback.format_exception(type(ex), ex, ex.__traceback__))


if __name__ == '__main__':
    # for arg in sys.argv[1:]:
    #     print('{} -->'.format(arg))
    #     s = Stream(arg)
    #     print('  {}'.format(parse(s)))
    # if len(sys.argv) < 2:
    #     repl()
    ff = get_symbol('ff')
    x = get_symbol('x')
    t = get_symbol('t')
    a = get_symbol('a')
    b = get_symbol('b')
    s = apply(
        w_list(
            Symbols.label,
            ff,
            w_list(
                Symbols.lambda_,
                w_list(x),
                w_list(
                    Symbols.cond,
                    w_list(Symbols.atom, x),
                    x),
                w_list(
                    w_list(
                        Symbols.quote,
                        t),
                    w_list(
                        ff,
                        w_list(Symbols.car, x))))),
        w_list(cons(a, b)))
    print(s)
