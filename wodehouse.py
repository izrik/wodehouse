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
import hashlib
import os
import string

import sys
import traceback
from inspect import signature


class WStream(object):
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.len = len(s)
        self.line = 1
        self.char = 1

    def has_chars(self):
        return self.i < self.len

    def get_next_char(self):
        if not self.has_chars():
            raise Exception("No more characters in the stream.")
        ch = self.peek()
        self.i += 1
        if ch == '\n':
            self.char = 1
            self.line += 1
        else:
            self.char += 1
        return ch

    def peek(self):
        if not self.has_chars():
            return None
        return self.s[self.i]

    def get_position(self):
        return Position(self.line, self.char)


def stream(s):
    return WStream(w_str(s).value)


def stream_has_chars(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    if s.has_chars():
        return WBoolean.true
    return WBoolean.false


def stream_get_next_char(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return WString(s.get_next_char())


def stream_peek(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return WString(s.peek())


def stream_get_position(s):
    if not isinstance(s, WStream):
        raise TypeError(
            "Argument s should be a stream. "
            "Got \"{}\" ({}) instead.".format(s, type(s)))
    return s.get_position()


def parse(s):
    """
    (define parse
    (lambda (s)
        (read_expr
            (if
                (isinstance s 'Stream)
                s
                (stream s)))) )
    :param s:
    :return:
    """
    if not isinstance(s, WStream):
        s = WStream(str(s))
    return read_expr(s)


def read_whitespace_and_comments(s):
    ch = s.peek()
    while s.has_chars() and (ch.isspace() or ch == '#'):
        if ch == '#':
            # read a comment
            while s.has_chars() and ch != '\n':
                s.get_next_char()
                ch = s.peek()
            if not s.has_chars():
                raise Exception(
                    "Ran out of characters before reading expression.")
        s.get_next_char()
        ch = s.peek()


def read_expr(s):
    """
    (define read_expr
    (lambda (s)
    # convert this to an exec?
    (let (whitespace (read_whitespace_and_comments s))
    (let (ch (peek s))
    (cond
    ((not (has_chars s))
        (raise "Ran out of characters before reading expression."))
    ((eq ch "(") (read_list s))
    ((in ch digits) (read_integer_literal s))
    ((or (in ch "+-*/<>_") (in ch ascii_letters)) (read_symbol s))
    ((eq ch "\"") (read_string s))
    ((eq ch "'")
        (exec
            (get_next_char s)
            (list 'quote (read_expr s))))
    (true
        (raise
            (format
                "Unknown starting character \"{}\" in read_expr"
                ch))))))))
    """
    # _i = s.i
    ch = s.peek()
    if s.has_chars() and (ch.isspace() or ch == '#'):
        read_whitespace_and_comments(s)
    ch = s.peek()
    if not s.has_chars():
        raise Exception(
            "Ran out of characters before reading expression.")
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


class Position(object):
    def __init__(self, line, char):
        self.line = line
        self.char = char


class WObject(object):
    position = None

    def __init__(self, position=None):
        self.position = position


class WString(WObject):
    def __init__(self, value, position=None):
        super().__init__(position=position)
        self.value = value

    def __repr__(self):
        return 'WString("{}")'.format(self.escaped())

    def __str__(self):
        return '"{}"'.format(self.escaped())

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        if isinstance(other, WString):
            return self.value == other.value
        return False

    def __len__(self):
        return len(self.value)

    def __getitem__(self, item):
        return self.value[item]

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
        return WString(arg.name)
    if isinstance(arg, WList):
        return WString(str(arg))
    if isinstance(arg, WFunction):
        if isinstance(arg, WMagicFunction):
            return WString(str(arg.name))
        return w_str(
            WList(
                WSymbol.get('lambda'),
                WList(*arg.args),
                WList(*arg.expr)))
    if isinstance(arg, WBoolean):
        return WString(str(arg))
    raise Exception('Unknown object type: "{}" ({})'.format(arg, type(arg)))


def w_format(fmt, *args):
    if args is None:
        args = WList()
    elif not isinstance(args, WList):
        args = WList(*args)
    _args = args
    s = WStream(fmt.value)
    parts = WList()
    current = WList()
    # TODO: extract a formatter object and/or function
    while s.has_chars():
        ch = WString(s.peek())
        if ch == '{':
            s.get_next_char()
            ch = WString(s.peek())
            if ch == '}':
                if len(args) < 1:
                    raise Exception(
                        "Not enough arguments for format string \"{}\". "
                        "Only got {} arguments.".format(fmt, len(_args)))
                parts = parts.append(add(*current))
                parts = parts.append(w_str(args.head))
                args = args.remaining
                current = WList()
                s.get_next_char()
                continue
            elif ch == '{':
                pass
            else:
                raise Exception(
                    "Invalid format character "
                    "\"{}\" in \"{}\"".format(ch, fmt))
        current = current.append(ch)
        s.get_next_char()
    if len(current) > 0:
        parts = parts.append(add(*current))
    return add(*parts)


def read_string(s):
    """
    (define read_string_char
    (lambda (s)
    (if (not (has_chars s))
        (raise "Ran out of characters before string was finished.")
        (let (ch (get_next_char s))
        (if (eq ch "\"")
            (cons ch '())
            (cons
                (if (eq ch "\\")
                    (if (not (has_chars s))
                        (raise (+ "Ran out of characters before escape "
                                  "sequence was finished."))
                        (let (ch2 (get_next_char s))
                        (cond
                            ((eq ch2 "n") "\n")
                            ((eq ch2 "r") "\r")
                            ((eq ch2 "t") "\t")
                            (true ch2))))
                    ch)
                (read_string_char s)))))))

    (define read_string
    (lambda (s)
    (let (delim (get_next_char s))
    (exec
        (assert (eq "\"" delim))
        (+ (read_string_char s))))))

    :param s:
    :return:
    """
    delim = s.get_next_char()
    assert delim == '"'
    chs = []
    while s.has_chars():
        ch = s.get_next_char()
        if ch == delim:
            value = ''.join(chs)
            return WString(value, position=s.get_position())
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
    def __init__(self, name, position=None):
        super().__init__(position=position)
        if isinstance(name, str):
            name = WString(name)
        if not isinstance(name, WString):
            name = w_str(name)
        self.name = name

    def __repr__(self):
        return 'Symbol({})'.format(self.name.value)

    def __str__(self):
        return self.name.value

    def __eq__(self, other):
        if not isinstance(other, WSymbol):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((WSymbol, self.name))

    __symbol_cache__ = {}

    @staticmethod
    def get(name):
        if isinstance(name, str):
            name = WString(name)
        if name not in WSymbol.__symbol_cache__:
            WSymbol.__symbol_cache__[name] = WSymbol(name)
        return WSymbol.__symbol_cache__[name]


class WSymbolAt(WSymbol):
    def __init__(self, name, position=None):
        if isinstance(name, WSymbol):
            name = name.name
        super().__init__(name, position=position)
        self.src = WSymbol.get(name)

    def __repr__(self):
        return repr(self.src)

    def __str__(self):
        return str(self.src)

    def __eq__(self, other):
        return self.src == other

    def __hash__(self):
        return hash(self.src)


def read_symbol(s):
    ch = s.peek()
    if ch in string.ascii_letters or ch in '_':
        return read_name(s)
    if ch in '+-*/':
        s.get_next_char()
        return WSymbolAt(ch, s.get_position())
    if ch in '<>':
        s.get_next_char()
        ch2 = s.peek()
        if ch2 == '=':
            s.get_next_char()
            return WSymbolAt(ch + ch2, position=s.get_position())
        return WSymbolAt(ch, position=s.get_position())
    raise Exception(
        "Unexpected character while reading symbol: \"{}\"".format(ch))


def read_name(s):
    chs = []
    while s.has_chars() and \
            (s.peek() in string.ascii_letters or s.peek() in '_'):
        chs.append(s.get_next_char())
    name = ''.join(chs)
    return WSymbolAt(name, position=s.get_position())


class WNumber(WObject):
    def __init__(self, value, position=None):
        super().__init__(position=position)
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
        super().__init__()
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
    return WNumber(int(_s), position=s.get_position())


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
        super().__init__()
        self.args = args
        self.expr = expr
        self.num_args = len(args)
        self.check_args = True


class WMagicFunction(WFunction):
    def __init__(self, f, name=None, check_args=True):
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
        if name is None:
            name = f.__name__
        self.name = name
        self.check_args = check_args

    def __str__(self):
        return str(self.name)

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
        if isinstance(arg, WMagicFunction):
            return WSymbol.get('MagicFunction')
        return WSymbol.get('Function')
    if isinstance(arg, WBoolean):
        return WSymbol.get('Boolean')
    if isinstance(arg, WMacro):
        if isinstance(arg, WMagicMacro):
            return WSymbol.get('MagicMacro')
        return WSymbol.get('Macro')
    if isinstance(arg, WState):
        return WSymbol.get('State')
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


def w_eval(expr, state):
    """
(lambda (expr state)
    (cond
    ((isinstance expr 'Symbol)
        (get state expr))
    ((isinstance expr '(Number String Boolean))
        expr)
    ((isinstance expr 'List)
        (let (head (car expr))
        (if
            (eq head 'quote)
            (car (cdr expr))
            (let (callee w_eval(head state))
            (let (args (cdr expr))
            (cond
            ((isinstance callee 'Macro)
                (let (exprs_state (call_macro callee args state))
                (let (exprs (car exprs_state))
                (let (state (car (cdr exprs_state)))
                (w_eval exprs state)))))
            ((not (isinstance callee 'Function))
                (raise
                    (format
                        "Callee is not a function. Got \\"{}\\" ({}) instead."
                        callee
                        (type callee))))
            (true
                (let (args
                    (map
                        (lambda (name value)
                            (list name (w_eval value state)))
                        args (get_func_args callee)))
                (let (state (new_state_proto state args))
                (if
                    (isinstance callee 'MagicFunction)
                    implementation_specific
                    (w_eval (second callee) state)))))))))))
    (true
        (raise
            (format
                "Unknown object type: \\"{}\\" ({})" expr (type expr))))))


    """
    # TODO: proper subtypes and inheritance, instead of just symbols
    # TODO: w_eval
    # TODO: call_macro
    # TODO: varargs
    # TODO: get_func_args
    if state is None:
        state = WState()
    elif not isinstance(state, WState):
        state = WState(state)
    if not isinstance(expr, WObject):
        raise Exception(
            'Non-domain value escaped from containment! '
            'Got "{}" ({}).'.format(expr, type(expr)))
    if isinstance(expr, WList):
        head = expr.head
        if head == WSymbol.get('quote'):
            return expr.second
        callee = w_eval(head, state)
        args = expr.remaining
        if isinstance(callee, WMacro):
            expr2, state2 = callee.call_macro(args, state=state)
            return expr2
        if not isinstance(callee, WFunction):
            raise Exception(
                'Callee is not a function. Got "{}" ({}) instead.'.format(
                    callee, type(callee)))
        evaled_args = [w_eval(arg, state) for arg in args]
        if (callee.check_args and
                callee.num_args is not None and
                len(evaled_args) != callee.num_args):
            raise Exception(
                'Function expected {} args, got {} instead.'.format(
                    len(callee.args), len(evaled_args)))
        fstate = WState(prototype=state)
        for i, argname in enumerate(callee.args):
            fstate[argname] = evaled_args[i]
        if isinstance(callee, WMagicFunction):
            return callee(*evaled_args)
        return w_eval(callee.expr, fstate)
    if isinstance(expr, WSymbol):
        if expr not in state:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = state[expr]
        return value
    if isinstance(expr, (WNumber, WString, WBoolean, WFunction, WMacro,
                         WState)):
        return expr
    raise Exception('Unknown object type: "{}" ({})'.format(expr, type(expr)))


_eval_source = w_eval.__doc__


def add(*operands):
    # TODO: thorough consideration of all operand type combinations
    # TODO: types to consider: number, string, list
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
    def __init__(self, macro_name=None):
        if macro_name is None:
            macro_name = type(self).__name__.lower()
        self.macro_name = macro_name

    def __str__(self):
        return self.macro_name

    def call_macro(self, exprs, state):
        exprs, state = self.call_magic_macro(exprs, state)
        return exprs, state


class Let(WMagicMacro):
    """
    (let
        (name1 value1)
        (name2 value2)
        ...
        expr)

    Creates a new state with `name1` equal to the result of `value1`, etc. Then
    evaluates `expr`. Values are evaluated with the new state object as it is
    populated.
    """
    def call_magic_macro(self, exprs, state):
        if len(exprs) < 2:
            raise Exception(
                "Macro `let` expects at least one variable definition and "
                "exactly one expression. Get {} total args instead".format(
                    len(exprs)))
        *vardefs, retval = exprs
        for vardef in vardefs:
            if not isinstance(vardef, WList) or len(vardef) != 2 or \
                    not isinstance(vardef[0], WSymbol):
                raise Exception(
                    "Variable definition in macro `let` should be a list of "
                    "the form \"(<symbol> <expr>)\". Got \"{}\" ({}) "
                    "instead.".format(vardef, type(vardef)))

        state2 = WState(prototype=state)
        for vardef in vardefs:
            name, expr = vardef
            value = w_eval(expr, state2)
            state2[name] = value
        return w_eval(retval, state2), state


class Apply(WMagicMacro):
    def __init__(self):
        super(Apply, self).__init__()

    def __call__(self, *args, state=None, **kwargs):
        return args, state


class If(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        if state is None:
            state = WState()
        if len(exprs) != 3:
            raise Exception(
                "Expected 3 arguments to if, got {} instead.".format(
                    len(exprs)))
        condition = exprs[0]
        true_retval = exprs[1]
        false_retval = exprs[2]
        cond_result = w_eval(condition, state)
        if cond_result is WBoolean.true:
            return w_eval(true_retval, state), state
        return w_eval(false_retval, state), state


class Cond(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        if state is None:
            state = WState()
        for expr in exprs:
            if not isinstance(expr, WList) or len(expr) != 2:
                raise Exception(
                    "Argument to `cond` is not a condition-value pair: "
                    "\"{}\" ({})".format(expr, type(expr)))
        for expr in exprs:
            condition, retval = expr.values
            cond_result = w_eval(condition, state)
            if cond_result is WBoolean.true:
                return w_eval(retval, state), state
            if cond_result is not WBoolean.false:
                raise Exception(
                    "Condition evaluated to a non-boolean value: "
                    "\"{}\" ({})".format(cond_result, type(cond_result)))
        raise Exception("No condition evaluated to true.")


class Lambda(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        if state is None:
            state = WState()
        if len(exprs) != 2:
            raise Exception(
                "Wrong number of arguments to lambda. "
                "Expected 2, got {}.".format(len(exprs)))
        args = exprs[0]
        if isinstance(args, WSymbol):
            args = WList(args)
        if not isinstance(args, WList) or \
                not all(isinstance(arg, WSymbol) for arg in args):
            raise Exception(
                "First argument to lambda must be a symbol or a list of "
                "symbols.")
        expr = exprs[1]

        def subst_args(a, e):
            if isinstance(e, (WNumber, WFunction, WBoolean, WString)):
                return e
            if isinstance(e, WSymbol):
                if e == WSymbol.get('quote'):
                    return e
                if e in a:
                    return e
                if e in state:
                    return state[e]
                return e
            if isinstance(e, WList):
                return WList(*(subst_args(a, e2) for e2 in e))
            raise Exception(
                "Can't subst expression \"{}\" ({}).".format(e, type(e)))

        return WFunction(args, subst_args(args, expr)), state


class WList(WObject):
    def __init__(self, *values, position=None):
        super().__init__(position=position)
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

    def append(self, value):
        new_list = list(self.values)
        new_list.append(value)
        return WList(*new_list)

    def extend(self, *values):
        new_list = list(self.values)
        new_list.extend(values)
        return WList(*new_list)


def w_map(func, *exprlists):
    if not isinstance(func, WFunction):
        raise Exception(
            "Expected a function but got \"{}\" ({}) instead.".format(
                func, type(func)))
    if exprlists:
        for exprlist in exprlists:
            if not isinstance(exprlist, WList):
                raise Exception(
                    "Argument passed to map must be lists. "
                    "Got \"{}\" ({}) instead.".format(
                        exprlist, type(exprlist)))
        length = len(exprlists[0])
        for exprlist in exprlists:
            if len(exprlist) != length:
                raise Exception(
                    "All argument lists should have the same length. "
                    "Expected {}, but got {} instead.".format(
                        length, len(exprlist)))
    results = WList()
    e = WList(*exprlists)
    while len(e[0]) > 0:
        cars = WList(*list(exprlist.head for exprlist in e))
        cdrs = WList(*list(exprlist.remaining for exprlist in e))
        func_with_args = WList(func, *cars)
        result = w_eval(func_with_args, state=None)
        results = results.append(result)
        e = cdrs

    return results


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


def cons(a, b):
    if not isinstance(b, WList):
        raise Exception(
            "Expected b to be a list. "
            "Got \"{}\" ({}) instead.".format(b, type(b)))
    return WList(a, *b)


def atom(arg):
    return not isinstance(arg, WList)


def eq(a, b):
    if a == b:
        return WBoolean.true
    return WBoolean.false


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
    """
    (define eval_str
    (lambda (input state)
        w_eval(parse(input) state))
    """
    expr = parse(input_s)
    value = w_eval(expr, state)
    return value


class WState(WObject):
    def __init__(self, values=None, prototype=None):
        if values is None:
            values = {}
        self.prototype = prototype
        self.dict = {self.normalize_key(key): value
                     for key, value in values.items()}
        self.deleted = set()

    @staticmethod
    def normalize_key(key):
        if isinstance(key, WSymbolAt):
            return key.src
        if isinstance(key, WSymbol):
            return key
        if isinstance(key, str):
            return WSymbol.get(WString(key))
        return WSymbol.get(w_str(key))

    def __getitem__(self, item):
        key = self.normalize_key(item)
        if key in self.deleted:
            raise KeyError
        if key in self.dict:
            return self.dict.get(key)
        if self.prototype is not None:
            return self.prototype[key]
        raise KeyError(key.name)

    def __setitem__(self, key, value):
        key2 = self.normalize_key(key)
        self.dict[key2] = value
        self.deleted.discard(key2)

    def __contains__(self, item):
        key = self.normalize_key(item)
        if key in self.deleted:
            return False
        if key in self.dict:
            return True
        if self.prototype is not None:
            return key in self.prototype
        return False

    def __delitem__(self, key):
        key2 = self.normalize_key(key)
        self.deleted.add(key2)

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


def new_state(pairs=None):
    """(new_state '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(pairs, WList):
            raise Exception(
                "Argument to new_state must be a list of key-value pairs. "
                "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Argument to new_state must be a list of key-value pairs. "
                    "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
    state = WState()
    if pairs is not None:
        for key, value in pairs:
            state[key] = value
    return state


def new_state_proto(prototype, pairs=None):
    """(new_state_proto proto '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(prototype, WState):
            raise TypeError(
                "Prototype must be a state object. "
                "Got \"{}\" ({}) instead.".format(prototype, type(prototype)))
        if not isinstance(pairs, WList):
            raise Exception(
                "Second argument to new_state_proto must be a list of "
                "key-value pairs. Got \"{}\" ({}) instead.".format(
                    pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Second argument to new_state_proto must be a list of "
                    "key-value pairs. Got \"{}\" ({}) instead.".format(
                        pairs, type(pairs)))
    state = WState(prototype=prototype)
    if pairs is not None:
        for key, value in pairs:
            state[key] = value
    return state


def get_state_value(state, name_or_symbol):
    key = WState.normalize_key(name_or_symbol)
    return state[key]


def list_state(state):
    return WList(*(key for key in state.keys()))


def define(name, value):
    """
    We want to import definitions from one file into another. Specifically, we
    want to be able to import w_eval from wodehuouse.w into tests.w. We need
    some way to accomplish that. At present, we don't have any way of mutating
    a state object from within wodehouse-language code. All we have are macros
    (esp let) which are able to create a new state with the previous state as a
    prototype. Also, every function call implicitly creates a new prototyped
    state object, to handle the args. None of these is sufficient to enable
    importing, because their effects are all limited to within a particular
    scope.

    We could define something new, like `define`, that modifies some global
    state, but that would require creating the global state machinery. A
    file-level state (instead of truly global) would probably be better.

    For example: Every file will have a WState object accessible only to that
    file. This object will at first be empty. Every expression in the file that
    gets eval'd will have a new state passed to it having the file-level state
    object as its immediate prototype. So far, this is 100% compatible with
    what the system already does. If, however, any `define` expressions are
    eval'd, that will add an entry to the file-level state. So, when we call
    `(import "filename.w" name1 name2)`, that call will eval the entire
    `filename.w` file as stated before, and the resulting file-level state
    object will be returned. Then, the `name1` and `name2` from `filename.w`'s
    state will be added to the current file's file-level state.
    """
    pass


class Define(WMagicMacro):
    def __init__(self, file_level_state):
        self.file_level_state = file_level_state

    def call_magic_macro(self, exprs, state):
        if len(exprs) != 2:
            raise Exception(
                "Macro 'define' expected 2 arguments. "
                "Got {} instead.".format(len(exprs)))
        name, expr = exprs
        if not isinstance(name, WSymbol):
            raise Exception(
                "Arg 'name' to 'define' must be a symbol. "
                "Got \"{}\" ({}) instead.".format(name, type(name)))
        value = w_eval(expr, state)
        self.file_level_state[name] = value
        return value, state


_global_import_cache = WState()


class Import(WMagicMacro):
    def __init__(self, file_level_state):
        self.file_level_state = file_level_state

    def call_magic_macro(self, exprs, state):
        if len(exprs) < 1:
            raise Exception(
                "Macro 'import' expected at least 1 arguments. "
                "Got {} instead.".format(len(exprs)))
        filename, *import_names = exprs
        filename = w_eval(filename, state)
        if not isinstance(filename, WString):
            raise Exception(
                "Arg 'filename' to 'import' must be a string. "
                "Got \"{}\" ({}) instead.".format(filename, type(filename)))
        for impname in import_names:
            if not isinstance(impname, WSymbol):
                raise Exception(
                    "Names to import must all be symbols. "
                    "Got \"{}\" ({}) instead.".format(impname, type(impname)))
        with open(filename.value) as f:
            src = WString(f.read())

        h = w_hash(src)
        if h in _global_import_cache:
            other_fls = _global_import_cache[h]
        else:
            other_fls = w_exec_src(src)
            _global_import_cache[h] = other_fls

        basename = os.path.splitext(filename.value)[0]
        self.file_level_state[basename] = other_fls
        for impname in import_names:
            self.file_level_state[impname] = other_fls[impname]
        return other_fls, state


def read_file(path):
    with open(path.value) as f:
        return WString(f.read())


def w_hash(arg):
    bytes_arg = w_str(arg).value.encode('utf-8')
    h = hashlib.sha256(bytes_arg).hexdigest()
    return WString(h)


class Assert(WMagicMacro):
    def call_magic_macro(self, exprs, state):
        if len(exprs) != 1:
            raise Exception(
                "Macro assert expected 1 argument. "
                "Got {} instead.".format(len(exprs)))
        expr = exprs[0]
        src = w_str(expr)
        value = w_eval(expr, state)
        if value is WBoolean.false:
            raise Exception("Assertion failed: {}".format(src))
        return value, state


def w_raise(description):
    raise Exception(w_str(description).value)


def w_exec(*args):
    if len(args) < 1:
        raise Exception("Function exec requires at least one argument.")
    return args[-1]


def create_default_state(prototype=None):
    return WState({
        '+': WMagicFunction(add, '+'),
        '-': WMagicFunction(sub, '-'),
        '*': WMagicFunction(mult, '*'),
        '/': WMagicFunction(div, '/'),
        'let': Let(),
        'apply': Apply(),
        'list': WMagicFunction(list_func, 'list'),
        'car': WMagicFunction(car),
        'cdr': WMagicFunction(cdr),
        'cons': WMagicFunction(cons),
        'atom': WMagicFunction(atom),
        'eq': WMagicFunction(eq),
        'print': WMagicFunction(w_print, 'print'),
        'type': WMagicFunction(get_type, 'type'),
        'isinstance': WMagicFunction(w_isinstance, 'isinstance'),
        'lambda': Lambda(),
        'str': WMagicFunction(w_str, 'str'),
        'format': WMagicFunction(w_format, 'format'),
        'true': WBoolean.true,
        'false': WBoolean.false,
        'not': WMagicFunction(w_not, 'not'),
        'cond': Cond(),
        'if': If(),
        '<': WMagicFunction(less_than, '<'),
        '<=': WMagicFunction(less_than_or_equal_to, '<='),
        '>': WMagicFunction(greater_than, '>'),
        '>=': WMagicFunction(greater_than_or_equal_to, '>='),
        'new_state': WMagicFunction(new_state, check_args=False),
        'new_state_proto': WMagicFunction(new_state_proto, check_args=False),
        'get': WMagicFunction(get_state_value, 'get'),
        'list_state': WMagicFunction(list_state),
        'in': WMagicFunction(w_in, 'in'),
        'map': WMagicFunction(w_map, 'map', check_args=False),
        'read_file': WMagicFunction(read_file),
        'assert': Assert(),
        'raise': WMagicFunction(w_raise, 'raise'),
        'stream': WMagicFunction(stream),
        'has_chars': WMagicFunction(stream_has_chars, 'has_chars'),
        'get_next_char': WMagicFunction(stream_get_next_char, 'get_next_char'),
        'get_position': WMagicFunction(stream_get_position, 'get_position'),
        'peek': WMagicFunction(stream_peek, 'peek'),
        'exec': WMagicFunction(w_exec, 'exec'),
    }, prototype=prototype)


def create_file_level_state():
    fls = WState()
    fls['fls'] = fls
    fls['define'] = Define(fls)
    fls['import'] = Import(fls)
    return fls


def repl(prompt=None):
    if prompt is None:
        prompt = '>>> '
    fls = create_file_level_state()
    state = create_default_state(prototype=fls)
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


def w_exec_src(src):
    fls = create_file_level_state()
    state = create_default_state(prototype=fls)
    stream = WStream(src)
    read_whitespace_and_comments(stream)
    while stream.has_chars():
        expr = read_expr(stream)
        w_eval(expr, state)
        read_whitespace_and_comments(stream)
    return fls


def main():
    for arg in sys.argv[1:]:
        with open(arg) as f:
            src = f.read()
        w_exec_src(src)
    if len(sys.argv) < 2:
        repl()


if __name__ == '__main__':
    main()
