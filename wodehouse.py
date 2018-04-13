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
from inspect import signature


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
    if ch in '+-*/<>_' or ch in string.ascii_letters:
        return read_symbol(s)
    if ch == '"':
        return read_string(s)
    if ch == '\'':
        s.get_next_char()
        expr = read_expr(s)
        return WList(WSymbol.get('quote'), expr)
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
            if _ch in '"\\':
                return '\\' + _ch
            return _ch

        return ''.join(escape_char(ch) for ch in self.value)


def w_str(arg):
    if isinstance(arg, WString):
        return arg
    if isinstance(arg, WNumber):
        return WString(str(arg.value))
    if isinstance(arg, WSymbol):
        return WString(str(arg.name))
    if isinstance(arg, WList):
        return WString(str(arg))
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            return WString(str(arg))
        q = WSymbol.get('quote')
        return w_str(
            WList(
                WSymbol.get('lambda'),
                WList(q, arg.args),
                WList(q, arg.expr)))
    if isinstance(arg, WBoolean):
        return WString(str(arg))
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))


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


class WSymbol(WObject):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Symbol({})'.format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash((WSymbol, self.name))

    __symbol_cache__ = {}

    @staticmethod
    def get(name):
        if name not in WSymbol.__symbol_cache__:
            WSymbol.__symbol_cache__[name] = WSymbol(name)
        return WSymbol.__symbol_cache__[name]


def read_symbol(s):
    ch = s.peek()
    if ch in string.ascii_letters or ch in '_':
        return read_name(s)
    if ch in '+-*/':
        s.get_next_char()
        return WSymbol.get(ch)
    if ch in '<>':
        s.get_next_char()
        ch2 = s.peek()
        if ch2 == '=':
            s.get_next_char()
            return WSymbol.get(ch + ch2)
        return WSymbol.get(ch)
    raise Exception(
        "Unexpected character while reading symbol: \"{}\"".format(ch))


def read_name(s):
    chs = []
    while s.has_chars() and \
            (s.peek() in string.ascii_letters or s.peek() in '_'):
        chs.append(s.get_next_char())
    name = ''.join(chs)
    return WSymbol.get(name)


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


class WBoolean(WObject):
    true = None
    false = None

    def __init__(self, value):
        self.value = not not value

    def __repr__(self):
        return 'WBoolean({})'.format(str(self))

    def __str__(self):
        return 'true' if self.value else 'false'

    def __eq__(self, other):
        if isinstance(other, bool):
            return self.value == other
        if isinstance(other, WBoolean):
            return self.value == other.value
        return False


WBoolean.true = WBoolean(True)
WBoolean.false = WBoolean(False)


def w_not(arg):
    if arg is WBoolean.true:
        return WBoolean.false
    if arg is WBoolean.false:
        return WBoolean.true
    raise Exception('Unexpected object type: "{}" ({})'.format(arg, type(arg)))


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


class WFunction(WObject):
    def __init__(self, args, expr):
        self.args = args
        self.expr = expr
        self.num_args = len(args)


class WMagicFunction(WFunction):
    def __init__(self, f):
        super().__init__([], None)
        self.f = f
        sig = signature(f)
        num_args = len(list(p for p in sig.parameters.values() if
                            p.kind in [p.POSITIONAL_ONLY,
                                       p.POSITIONAL_OR_KEYWORD]))
        if any(p for p in sig.parameters.values()
               if p.kind == p.VAR_POSITIONAL):
            num_args = None
        self.num_args = num_args

    def __call__(self, *args, **kwargs):
        return self.f(*args)


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
        return WSymbol.get('Function')
    if isinstance(arg, WBoolean):
        return WSymbol.get('Boolean')
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))


def w_lambda(args, expr):
    if not isinstance(args, (WSymbol, WList)):
        raise TypeError(
            'First argument must be either a symbol or a list of symbols. '
            'Got "{}" ({}) instead'.format(args, type(args)))
    if isinstance(args, WList):
        if not all(isinstance(a, WSymbol) for a in args):
            raise TypeError(
                'First argument must be either a symbol or a list of symbols. '
                'Got "{}" ({}) instead'.format(args, type(args)))
    return WFunction(args, expr)


def w_eval(expr, state):
    """
    (lambda '(expr state)
        (if
        ((eq (type expr) 'Symbol)
            (get state expr))
        ((in (type expr) '(Number, String, Boolean))
            expr)
        ((eq (type expr) 'List)
            (let head (car expr)
            (if
            ((eq head 'quote)
                (cdr expr)) # not quite cdr. car of cdr i think.
            (true
                (let callee w_eval(head, state)
                (let args (cdr expr)
                (if
                ((eq (type callee) 'Macro)
                    (let exprs_state (call_macro callee args state)
                    (let exprs (car exprs_state)
                    (let state (car (cdr exprs_state))
                    w_eval exprs state))))
                ((neq (type callee) 'Function)
                    (raise Exception
                        (format
                           "Callee is not a function. Got \"{}\" ({}) instead."
                            callee
                            (type callee))))
                (true
                    (let args (map ....
                    (let state (new_state prototype=state args
                    (if
                    ((eq magicfunction ...
                    (true
                        w_eval


    """
    # TODO: isinstance, including subtypes
    # TODO: map
    # TODO: raise
    # TODO: w_eval
    # TODO: call_macro
    # TODO: neq
    # TODO: new_state prototype, optional/named arguments, or new_state_from
    if state is None:
        state = WState()
    elif not isinstance(state, WState):
        state = WState(state)
    if isinstance(expr, (int, str)):
        raise Exception('Non-domain value escaped from containment!')
    if isinstance(expr, WList):
        head = expr.head
        if head is WSymbol.get('quote'):
            return expr.second
        callee = w_eval(expr.head, state)
        args = expr.remaining
        if isinstance(callee, WMacro):
            exprs, state = callee.call_macro(args, state=state)
            if len(exprs) < 1:
                raise Exception('Ran out of arguments')
            return w_eval(exprs, state)
        if not isinstance(callee, WFunction):
            raise Exception(
                'Callee is not a function. Got "{}" ({}) instead.'.format(
                    callee, type(callee)))
        args = [w_eval(arg, state) for arg in args]
        if callee.num_args is not None and len(args) != callee.num_args:
            raise Exception(
                'Function expected {} args, got {} instead.'.format(
                    len(callee.args), len(args)))
        _state = state
        state = WState(prototype=_state)
        for i, argname in enumerate(callee.args):
            state[argname] = args[i]
        if isinstance(callee, WMagicFunction):
            return callee(*args)
        return w_eval(callee.expr, state)
    if isinstance(expr, WSymbol):
        if expr not in state:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = state[expr]
        return value
    if isinstance(expr, (WNumber, WString, WBoolean)):
        return expr
    raise Exception('Unknown object type: "{}" ({})'.format(expr, type(expr)))


def add(*operands):
    if not operands:
        return WNumber(0)
    x = 0
    for operand in operands:
        x += operand.value
    return WNumber(x)


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
        x /= operand.value
    return WNumber(x)


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


class WMacro(WObject):
    def call_macro(self, exprs, state):
        return exprs, state


class WMagicMacro(WMacro):
    def call_macro(self, exprs, state):
        exprs, state = self.call_magic_macro(exprs, state)
        if not isinstance(exprs, WList):
            raise TypeError(
                'Magic macro "{}" returned wrong kind of exprs'.format(self))
        return exprs, state


class Let(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        symbol, value, *exprs2 = exprs
        exprs = WList(*exprs2)
        _state = state
        state = WState(prototype=_state)
        state[symbol.name] = w_eval(value, _state)
        return exprs, state


class Apply(WMagicMacro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, state=None, **kwargs):
        return args, state


class If(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        if state is None:
            state = WState()
        for expr in exprs:
            if not isinstance(expr, WList) or len(expr) != 2:
                raise Exception(
                    "Argument to `if` is not a condition-value pair: "
                    "\"{}\" ({})".format(expr, type(expr)))
        for expr in exprs:
            condition, retval = expr.values
            cond_result = w_eval(condition, state)
            if cond_result is WBoolean.true:
                return retval, state
            if cond_result is not WBoolean.false:
                raise Exception(
                    "Condition evaluated to a non-boolean value: "
                    "\"{}\" ({})".format(cond_result, type(cond_result)))
        raise Exception("No condition evaluated to true.")


class WList(WObject):
    def __init__(self, *values):
        self.values = list(values)

    def __repr__(self):
        return 'WList({})'.format(
            ' '.join(repr(value) for value in self.values))

    def __str__(self):
        if len(self) == 2 and self.head == WSymbol.get('quote'):
            return "'{}".format(str(self.values[1]))
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

    def __len__(self):
        return len(self.values)

    def __getitem__(self, item):
        return self.values[item]

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


def w_in(expr, container):
    if not isinstance(container, WList):
        raise Exception(
            "Not a list: \"{}\" ({})".format(container, type(container)))
    for item in container:
        if item is expr or item == expr:
            return WBoolean.true
    return WBoolean.false


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
    return a == b


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


class WState:
    def __init__(self, values=None, prototype=None):
        if values is None:
            values = {}
        self.prototype = prototype
        self.dict = {self.normalize_key(key): value
                     for key, value in values.items()}
        self.deleted = set()

    @staticmethod
    def normalize_key(key):
        if isinstance(key, WSymbol):
            return key
        return WSymbol.get(str(key))

    def __getitem__(self, item):
        item = self.normalize_key(str(item))
        if item in self.deleted:
            raise KeyError
        if item in self.dict:
            return self.dict.get(item)
        if self.prototype is not None:
            return self.prototype[item]
        raise KeyError

    def __setitem__(self, key, value):
        key = self.normalize_key(str(key))
        self.dict[key] = value
        self.deleted.discard(key)

    def __contains__(self, item):
        item = self.normalize_key(str(item))
        if item in self.deleted:
            return False
        if item in self.dict:
            return True
        if self.prototype is not None:
            return item in self.prototype
        return False

    def __delitem__(self, key):
        key = self.normalize_key(key)
        self.deleted.add(key)

    def __len__(self):
        return len(list(self.keys()))

    def keys(self):
        keys = set(self.dict.keys())
        if self.prototype is not None:
            keys.update(self.prototype.keys())
        keys.difference_update(self.deleted)
        for key in keys:
            yield key


def iter_by_two(i):
    x = i.__iter__()
    while True:
        try:
            item1 = x.__next__()
        except StopIteration:
            break
        try:
            item2 = x.__next__()
        except StopIteration:
            raise Exception('Items are not in pairs')
        yield item1, item2


def new_state(*exprs):
    state = WState()
    for key, value in iter_by_two(exprs):
        state[key] = value
    return state


def get_state_value(state, name_or_symbol):
    key = WState.normalize_key(name_or_symbol)
    return state[key]


def create_default_state():
    return WState({
        '+': WMagicFunction(add),
        '-': WMagicFunction(sub),
        '*': WMagicFunction(mult),
        '/': WMagicFunction(div),
        'let': Let(),
        'apply': Apply(),
        'list': WMagicFunction(list_func),
        'car': WMagicFunction(car),
        'cdr': WMagicFunction(cdr),
        'atom': WMagicFunction(atom),
        'eq': WMagicFunction(eq),
        'print': WMagicFunction(w_print),
        'type': WMagicFunction(get_type),
        'lambda': WMagicFunction(w_lambda),
        'str': WMagicFunction(w_str),
        'true': WBoolean.true,
        'false': WBoolean.false,
        'not': WMagicFunction(w_not),
        'if': If(),
        '<': WMagicFunction(less_than),
        '<=': WMagicFunction(less_than_or_equal_to),
        '>': WMagicFunction(greater_than),
        '>=': WMagicFunction(greater_than_or_equal_to),
        'new_state': WMagicFunction(new_state),
        'get': WMagicFunction(get_state_value),
        'in': WMagicFunction(w_in),
    })


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
        except EOFError:
            print('')
            break
        except KeyboardInterrupt:
            print('')
            continue
        except Exception as ex:
            print('Caught the following exception:')
            tb = traceback.format_exception(type(ex), ex, ex.__traceback__)
            for line in tb:
                print('  ' + line, end='')


def main():
    for arg in sys.argv[1:]:
        print('{} -->'.format(arg))
        s = WStream(arg)
        print('  {}'.format(parse(s)))
    if len(sys.argv) < 2:
        repl()


if __name__ == '__main__':
    main()
