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
    scope = WScope(prototype=prototype)
    scope.update({
        '+': WMagicFunction(add, scope, name='+'),
        '-': WMagicFunction(sub, scope, name='-'),
        '*': WMagicFunction(mult, scope, name='*'),
        '/': WMagicFunction(div, scope, name='/'),
        'let': Let(),
        'apply': Apply(),
        'list': WMagicFunction(list_func, scope, name='list'),
        'car': WMagicFunction(car, scope),
        'cdr': WMagicFunction(cdr, scope),
        'cons': WMagicFunction(cons, scope),
        'atom': WMagicFunction(atom, scope),
        'eq': WMagicFunction(eq, scope),
        'print': WMagicFunction(w_print, scope, name='print'),
        'type': WMagicFunction(get_type, scope, name='type'),
        'isinstance': WMagicFunction(w_isinstance, scope, name='isinstance'),
        'lambda': WLambda(),
        'str': WMagicFunction(w_str, scope, name='str'),
        'format': WMagicFunction(w_format, scope, name='format'),
        'true': WBoolean.true,
        'false': WBoolean.false,
        'not': WMagicFunction(w_not, scope, name='not'),
        'or': WMagicFunction(w_or, scope, name='or'),
        'and': WMagicFunction(w_and, scope, name='and'),
        'cond': Cond(),
        'if': If(),
        '<': WMagicFunction(less_than, scope, name='<'),
        '<=': WMagicFunction(less_than_or_equal_to, scope, name='<='),
        '>': WMagicFunction(greater_than, scope, name='>'),
        '>=': WMagicFunction(greater_than_or_equal_to, scope, name='>='),
        'new_scope': WMagicFunction(new_scope, scope, check_args=False),
        'new_scope_proto': WMagicFunction(new_scope_proto, scope,
                                          check_args=False),
        'get': WMagicFunction(get_scope_value, scope, name='get'),
        'list_scope': WMagicFunction(list_scope, scope),
        'in': WMagicFunction(w_in, scope, name='in'),
        'map': WMagicFunction(w_map, scope, name='map', check_args=False),
        'read_file': WMagicFunction(read_file, scope),
        'assert': WAssert(),
        'raise': WMagicFunction(w_raise, scope, name='raise'),
        'stream': WMagicFunction(stream, scope),
        'has_chars': WMagicFunction(stream_has_chars, scope,
                                    name='has_chars'),
        'get_next_char': WMagicFunction(stream_get_next_char, scope,
                                        name='get_next_char'),
        'get_position': WMagicFunction(stream_get_position, scope,
                                       name='get_position'),
        'peek': WMagicFunction(stream_peek, scope, name='peek'),
        'exec': WMagicFunction(w_exec, scope, name='exec'),
        'int_from_str': WMagicFunction(int_from_str, scope),
        'symbol_at': WMagicFunction(symbol_at, scope),
    })
    return scope
