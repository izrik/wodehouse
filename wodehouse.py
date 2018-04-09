#!/usr/bin/env python

"""
Wodehouse: An Object-oriented Functional Programming Language

(+ 1 2 3)
requires:
    integer literals
    '+' as a reference to a function
    function call

(print "Hello, world!")
requires:
    a `print` function
    function call
    a string type

(quote 1) --> 1
requires:
    quote symbol
    quote machinery in w_eval --> either macro or special code in w_eval

(quote (1)) --> (1)
requires
    quote a list
    proper list type, esp. comparing `WList` to python built-in `list`

'(1) --> (1)
requires
    syntax change: squote not allowed when delimiting strings, only dquote
    syntax change: read_expr("'(1)") --> WList(1)

"""

import string

import sys
import traceback
from collections import ChainMap


class WStream(object):
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
        return read_list(s)
    if ch in string.digits:
        return read_integer_literal(s)
    if ch in '+-*/' or ch in string.ascii_letters:
        return read_symbol(s)
    if ch == '"':
        return read_string(s)
    if ch == '\'':
        s.get_next_char()
        expr = read_expr(s)
        return WList(WSymbols.quote, expr)
    raise Exception('Unknown starting character "{}" in read_expr'.format(ch))


class WObject(object):
    pass


class WString(WObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'WString("{}")'.format(self.escaped())

    def __str__(self):
        return '"{}"'.format(self.escaped())

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, WString):
            return self.value == other.value
        return False

    def escaped(self):
        def escape_char(_ch):
            if _ch == '\n':
                return '\\n'
            if _ch == '\r':
                return '\\r'
            if _ch == '\t':
                return '\\t'
            if _ch in '"\'\\':
                return '\\' + _ch
            return _ch

        return ''.join(escape_char(ch) for ch in self.value)


def read_string(s):
    delim = s.get_next_char()
    assert delim == '"'
    chs = []
    while s.has_chars():
        ch = s.get_next_char()
        if ch == delim:
            value = ''.join(chs)
            return WString(value)
        if ch == '\\':
            ch = s.get_next_char()
            if ch == 'n':
                ch = '\n'
            if ch == 'r':
                ch = '\r'
            if ch == 't':
                ch = '\t'
        chs.append(ch)
    raise Exception('Ran out of characters before string was finished.')


__symbols__ = {}


def get_symbol(name):
    if name not in __symbols__:
        __symbols__[name] = WSymbol(name)
    return __symbols__[name]


class WSymbol(WObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Symbol({})'.format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self is other


class WSymbols:
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
        return get_symbol(ch)


def read_name(s):
    chs = []
    while s.has_chars() and s.peek() in string.ascii_letters:
        chs.append(s.get_next_char())
    name = ''.join(chs)
    return get_symbol(name)


class WNumber(WObject):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'WNumber({})'.format(self.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, WNumber):
            return self.value == other.value
        return False


def read_integer_literal(s):
    chs = []
    while s.has_chars() and s.peek() in string.digits:
        chs.append(s.get_next_char())
    _s = ''.join(chs)
    return WNumber(int(_s))


def read_list(s):
    assert s.peek() == '('
    exprs = []
    s.get_next_char()
    while True:
        while True:
            if not s.has_chars():
                raise Exception(
                    'Ran out of characters before list was finished.')
            ch = s.peek()
            if ch not in string.whitespace:
                break
            s.get_next_char()
        if s.peek() == ')':
            s.get_next_char()
            break
        expr = read_expr(s)
        exprs.append(expr)
    return WList(*exprs)


def get_type(arg):
    if isinstance(arg, WNumber):
        return get_symbol('Number')
    if isinstance(arg, WString):
        return get_symbol('String')
    if isinstance(arg, WSymbol):
        return get_symbol('Symbol')
    if isinstance(arg, WList):
        return get_symbol('List')
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))


def w_eval(expr, state):
    if state is None:
        state = {}
    if isinstance(expr, (int, str)):
        raise Exception('Non-domain value escaped from containment!')
    if isinstance(expr, WList):
        head = expr.head
        if head is WSymbols.quote:
            return expr.second
        callee = w_eval(expr.head, state)
        args = expr.remaining
        while isinstance(callee, Macro):
            exprs, state = callee(*args, state=state)
            if len(exprs) < 1:
                raise Exception('Ran out of arguments')
            callee = w_eval(exprs[0], state=state)
            args = exprs[1:]
        args = [w_eval(arg, state) for arg in args]
        return callee(*args)
    if isinstance(expr, WSymbol):
        if expr.name not in state:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = state[expr.name]
        # while isinstance(value, WodehouseObject):
        #     value = apply_expr(value, state)
        return value
    if isinstance(expr, (WNumber, WString)):
        return expr
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
        state[symbol.name] = w_eval(value, _state)
        return exprs, state


class Apply(Macro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, state=None, **kwargs):
        return args, state


# class MacroMacro(Macro):
#     def __call__(self, name, arglist, *body, state=None, **kwargs):
#         pass


class WList(WObject):
    def __init__(self, *values):
        self.values = list(values)

    def __repr__(self):
        return 'WList({})'.format(
            ' '.join(repr(value) for value in self.values))

    def __str__(self):
        return '({})'.format(' '.join(str(value) for value in self.values))

    def __eq__(self, other):
        if isinstance(other, WList):
            return self.values == other.values
        if isinstance(other, list):
            return self.values == other
        if isinstance(other, tuple):
            return self.values == list(other)
        return False

    def __iter__(self):
        return self.values.__iter__()

    @property
    def head(self):
        if not self.values:
            return None
        return self.values[0]

    @property
    def second(self):
        if self.values and len(self.values) > 1:
            return self.values[1]

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


def w_print(x, *, printer=None):
    if printer is None:
        printer = print

    if isinstance(x, WNumber):
        printer(x.value)
    elif isinstance(x, WString):
        printer(x.value)
    else:
        printer(x)
    return x


def repl_print(x):
    if isinstance(x, WNumber):
        print(x.value)
    elif isinstance(x, WString):
        print(str(x))
    elif isinstance(x, WList):
        print(str(x))
    else:
        print(x)
    return x


def eval_str(input_s, state=None):
    stream = WStream(input_s)
    expr = parse(stream)
    value = w_eval(expr, state)
    return value


def create_default_state():
    return {
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
        'print': w_print,
        'type': get_type,
    }


def repl(prompt=None):
    if prompt is None:
        prompt = '>>> '
    state = create_default_state()
    while True:
        try:
            input_s = input(prompt)
            if input_s is None:
                continue
            if input_s.strip() in ['quit', 'exit']:
                break
            if input_s.strip() == '':
                continue
            value = eval_str(input_s, state)
            repl_print(value)
        except Exception as ex:
            print('Caught the following exception: {}'.format(ex))
            print(line for line in
                  traceback.format_exception(type(ex), ex, ex.__traceback__))


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print('{} -->'.format(arg))
        s = WStream(arg)
        print('  {}'.format(parse(s)))
    if len(sys.argv) < 2:
        repl()
