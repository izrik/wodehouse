from functions.collections import w_map, w_in
from functions.convert import int_from_str
import functions.exec_src
from functions.io import w_print, w_format, read_file
from functions.lisp import car, cdr, cons, atom
from functions.list import list_func
from functions.logical import w_not, w_or, w_and, less_than, \
    less_than_or_equal_to, greater_than, greater_than_or_equal_to, eq
# from functions.magic_function import WMagicFunction
from functions.math import add, sub, mult, div
from functions.raise_ import w_raise
from functions.str import w_str
from functions.stream import stream, stream_has_chars, stream_get_next_char, \
    stream_get_position, stream_peek
from functions.symbol import symbol_at
from functions.types import get_type, w_isinstance
# from macros.define import Define
# from macros.import_ import Import
from wtypes.list import WList
from wtypes.scope import WScope
import functions.magic_function

import macros.apply
import macros.assert_
import macros.cond
import macros.define
import macros.if_
import macros.import_
import macros.lambda_
import macros.let
import wtypes.boolean
# import wtypes.scope
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
# WScope = wtypes.scope.WScope
WStream = wtypes.stream.WStream



def new_scope(pairs=None):
    """(new_scope '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(pairs, WList):
            raise Exception(
                "Argument to new_scope must be a list of key-value pairs. "
                "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Argument to new_scope must be a list of key-value pairs. "
                    "Got \"{}\" ({}) instead.".format(pairs, type(pairs)))
    scope = WScope()
    if pairs is not None:
        for key, value in pairs:
            scope[key] = value
    return scope


def new_scope_proto(prototype, pairs=None):
    """(new_scope_proto proto '((key1 value1) (key2 value2)))"""
    if pairs is not None:
        if not isinstance(prototype, WScope):
            raise TypeError(
                "Prototype must be a scope object. "
                "Got \"{}\" ({}) instead.".format(prototype, type(prototype)))
        if not isinstance(pairs, WList):
            raise Exception(
                "Second argument to new_scope_proto must be a list of "
                "key-value pairs. Got \"{}\" ({}) instead.".format(
                    pairs, type(pairs)))
        for pair in pairs:
            if not isinstance(pair, WList) or len(pair) != 2:
                raise Exception(
                    "Second argument to new_scope_proto must be a list of "
                    "key-value pairs. Got \"{}\" ({}) instead.".format(
                        pairs, type(pairs)))
    scope = WScope(prototype=prototype)
    if pairs is not None:
        for key, value in pairs:
            scope[key] = value
    return scope


def get_scope_value(scope, name_or_symbol):
    key = WScope.normalize_key(name_or_symbol)
    return scope[key]


def list_scope(scope):
    return WList(*(key for key in scope.keys()))


def create_module_scope():
    fls = WScope()
    fls['fls'] = fls
    fls['define'] = Define(fls)
    fls['import'] = Import(fls)
    return fls


def create_global_scope(prototype=None):
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
        'exec': WMagicFunction(functions.exec_src.w_exec, scope, name='exec'),
        'int_from_str': WMagicFunction(int_from_str, scope),
        'symbol_at': WMagicFunction(symbol_at, scope),
    })
    return scope
