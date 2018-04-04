#!/usr/bin/env python

"""Wodehouse: An Object-oriented Functional Programming Language"""

import string

import sys
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


class Symbol(WObject):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Symbol({})'.format(self.name)


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


def apply_expr(expr, state):
    if isinstance(expr, int):
        return expr
    if isinstance(expr, Call):
        callee = apply_expr(expr.callee, state)
        args = expr.arguments
        while isinstance(callee, Macro):
            exprs, state = callee(*args, state=state)
            if len(exprs) < 1:
                raise Exception('Ran out of arguments')
            callee = apply_expr(exprs[0], state=state)
            args = exprs[1:]
        args = [apply_expr(arg, state) for arg in args]
        return callee(*args)
    if isinstance(expr, Symbol):
        if expr.name not in state:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = state[expr.name]
        # while isinstance(value, WodehouseObject):
        #     value = apply_expr(value, state)
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

    def __call__(self, symbol, value, *exprs, state=None, **kwargs):
        if state is None:
            state = {}
        _state = state
        state = ChainMap({}, _state)
        state[symbol.name] = apply_expr(value, _state)
        return exprs, state


class Apply(Macro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, state=None, **kwargs):
        return args, state


# class MacroMacro(Macro):
#     def __call__(self, name, arglist, *body, state=None, **kwargs):
#         pass

class Quote(Macro):
    def __call__(self, *args, state=None, **kwargs):
        return args, state


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


def car(first, *args):
    if args:
        raise Exception('Too many arguments given to car')
    if not isinstance(first, WList):
        raise TypeError('{} is not a list'.format(str(first)))
    return first.head


def cdr(first, *args):
    if args:
        raise Exception('Too many arguments given to cdr')
    if not isinstance(first, WList):
        raise TypeError('{} is not a list'.format(str(first)))
    return first.remaining


def atom(arg):
    return not isinstance(arg, WList)


def eq(a, b):
    if not atom(a):
        return False
    if not atom(b):
        return False
    return a == b()


def repl(prompt=None):
    if prompt is None:
        prompt = '>>> '
    state = {
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
            value = apply_expr(expr, state)
            print(value)
        except Exception as ex:
            print('Caught the following exception: {}'.format(ex))
            print(line for line in
                  traceback.format_exception(type(ex), ex, ex.__traceback__))


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print('{} -->'.format(arg))
        s = Stream(arg)
        print('  {}'.format(parse(s)))
    if len(sys.argv) < 2:
        repl()
