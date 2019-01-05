from functions.collections import w_map, w_in
from functions.convert import int_from_str
from functions.eval import w_eval
from functions.io import w_print, w_format, read_file
from functions.lisp import car, cdr, cons, atom
from functions.list import list_func
from functions.logical import w_not, w_or, w_and, less_than, \
    less_than_or_equal_to, greater_than, greater_than_or_equal_to, eq
import functions.magic_function
from functions.math import add, sub, mult, div
from functions.raise_ import w_raise
from functions.read import read_whitespace_and_comments, read_expr
from functions.scope import get_scope_value, list_scope, new_scope, \
    new_scope_proto
from functions.str import w_str
from functions.stream import stream, stream_has_chars, stream_get_next_char, \
    stream_get_position, stream_peek
from functions.symbol import symbol_at
from functions.types import get_type, w_isinstance

import macros.apply
import macros.assert_
import macros.cond
import macros.define
import macros.if_
import macros.import_
import macros.lambda_
import macros.let
import wtypes.boolean
import wtypes.scope
import wtypes.stream

WMagicFunction = functions.magic_function.WMagicFunction
Apply = macros.apply.Apply
WAssert = macros.assert_.WAssert
Cond = macros.cond.Cond
Define = macros.define.Define
If = macros.if_.If
Import = macros.import_.Import
WLambda = macros.lambda_.WLambda
Let = macros.let.Let
WBoolean = wtypes.boolean.WBoolean
WScope = wtypes.scope.WScope
WStream = wtypes.stream.WStream


def w_exec_src(src, filename=None):
    fls = create_file_level_scope()
    scope = create_default_scope(prototype=fls)
    stream = WStream(src, filename=filename)
    read_whitespace_and_comments(stream)
    while stream.has_chars():
        expr = read_expr(stream)
        w_eval(expr, scope)
        read_whitespace_and_comments(stream)
    return fls


def w_exec(*args):
    if len(args) < 1:
        raise Exception("Function exec requires at least one argument.")
    return args[-1]


def create_file_level_scope():
    fls = WScope()
    fls['fls'] = fls
    fls['define'] = Define(fls)
    fls['import'] = Import(fls)
    return fls


def create_default_scope(prototype=None):
    return WScope({
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
        'lambda': WLambda(),
        'str': WMagicFunction(w_str, 'str'),
        'format': WMagicFunction(w_format, 'format'),
        'true': WBoolean.true,
        'false': WBoolean.false,
        'not': WMagicFunction(w_not, 'not'),
        'or': WMagicFunction(w_or, 'or'),
        'and': WMagicFunction(w_and, 'and'),
        'cond': Cond(),
        'if': If(),
        '<': WMagicFunction(less_than, '<'),
        '<=': WMagicFunction(less_than_or_equal_to, '<='),
        '>': WMagicFunction(greater_than, '>'),
        '>=': WMagicFunction(greater_than_or_equal_to, '>='),
        'new_scope': WMagicFunction(new_scope, check_args=False),
        'new_scope_proto': WMagicFunction(new_scope_proto, check_args=False),
        'get': WMagicFunction(get_scope_value, 'get'),
        'list_scope': WMagicFunction(list_scope),
        'in': WMagicFunction(w_in, 'in'),
        'map': WMagicFunction(w_map, 'map', check_args=False),
        'read_file': WMagicFunction(read_file),
        'assert': WAssert(),
        'raise': WMagicFunction(w_raise, 'raise'),
        'stream': WMagicFunction(stream),
        'has_chars': WMagicFunction(stream_has_chars, 'has_chars'),
        'get_next_char': WMagicFunction(stream_get_next_char, 'get_next_char'),
        'get_position': WMagicFunction(stream_get_position, 'get_position'),
        'peek': WMagicFunction(stream_peek, 'peek'),
        'exec': WMagicFunction(w_exec, 'exec'),
        'symbol_at': WMagicFunction(symbol_at),
        'int_from_str': WMagicFunction(int_from_str),
    }, prototype=prototype)
