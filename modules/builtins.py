from functions.str import w_starts_with, w_ends_with, w_join
from wtypes.module import WModule


def create_builtins_module(import_=None):
    from functions.collections import w_map, w_in
    from functions.convert import int_from_str
    from functions.exception import exception
    from functions.exec_src import w_exec
    from functions.io import w_print, read_file
    from functions.lisp import car, cdr, cons, atom
    from functions.list import list_func
    from functions.logical import w_not, w_or, w_and, less_than, \
        less_than_or_equal_to, greater_than, greater_than_or_equal_to, eq
    from wtypes.magic_function import WMagicFunction
    from functions.math import add, sub, mult, div
    from functions.raise_ import w_raise
    from functions.str import w_str, w_format
    from functions.stream import stream, stream_has_chars, \
        stream_get_next_char, stream_get_position, stream_peek
    from functions.symbol import symbol_at
    from functions.types import get_type, w_isinstance
    from macros.apply import Apply
    from macros.assert_ import WAssert
    from macros.cond import Cond
    from macros.define import Define
    from macros.if_ import If
    from macros.import_ import Import
    from macros.lambda_ import WLambda
    from macros.let import Let
    from wtypes.boolean import WBoolean
    from functions.help import w_help
    from functions.list import w_len
    from functions.scope import new_scope
    from functions.scope import new_scope_within
    from functions.scope import get_scope_value
    from functions.scope import w_dir
    from macros.def_ import Def
    from functions.io import w_is_file, w_is_dir
    from functions.io import w_list_dir
    from functions.list import nth
    from functions.exec_src import w_exec_src
    from functions.function import w_name_of
    from functions.list import w_filter
    from functions.module import w_module

    if import_ is None:
        import_ = Import()

    module = WModule(name='builtins')
    module.update({
        '+': WMagicFunction(add, module, name='+'),
        '-': WMagicFunction(sub, module, name='-'),
        '*': WMagicFunction(mult, module, name='*'),
        '/': WMagicFunction(div, module, name='/'),
        'let': Let(),
        'apply': Apply(),
        'list': WMagicFunction(list_func, module, name='list'),
        'len': WMagicFunction(w_len, module, name='len'),
        'car': WMagicFunction(car, module),
        'cdr': WMagicFunction(cdr, module),
        'cons': WMagicFunction(cons, module),
        'atom': WMagicFunction(atom, module),
        'eq': WMagicFunction(eq, module),
        'print': WMagicFunction(w_print, module, name='print',
                                check_args=False),
        'type': WMagicFunction(get_type, module, name='type'),
        'isinstance': WMagicFunction(w_isinstance, module, name='isinstance'),
        'lambda': WLambda(),
        'str': WMagicFunction(w_str, module, name='str'),
        'format': WMagicFunction(w_format, module, name='format'),
        'true': WBoolean.true,
        'false': WBoolean.false,
        'not': WMagicFunction(w_not, module, name='not'),
        'or': WMagicFunction(w_or, module, name='or'),
        'and': WMagicFunction(w_and, module, name='and'),
        'cond': Cond(),
        'if': If(),
        '<': WMagicFunction(less_than, module, name='<'),
        '<=': WMagicFunction(less_than_or_equal_to, module, name='<='),
        '>': WMagicFunction(greater_than, module, name='>'),
        '>=': WMagicFunction(greater_than_or_equal_to, module, name='>='),
        'new_scope': WMagicFunction(new_scope, module, check_args=False),
        'new_scope_within': WMagicFunction(new_scope_within, module,
                                           check_args=False),
        'get': WMagicFunction(get_scope_value, module, name='get'),
        'dir': WMagicFunction(w_dir, module, name='dir', check_args=False),
        'in': WMagicFunction(w_in, module, name='in'),
        'map': WMagicFunction(w_map, module, name='map', check_args=False),
        'read_file': WMagicFunction(read_file, module),
        'assert': WAssert(),
        'raise': WMagicFunction(w_raise, module, name='raise'),
        'stream': WMagicFunction(stream, module),
        'has_chars': WMagicFunction(stream_has_chars, module,
                                    name='has_chars'),
        'get_next_char': WMagicFunction(stream_get_next_char, module,
                                        name='get_next_char'),
        'get_position': WMagicFunction(stream_get_position, module,
                                       name='get_position'),
        'peek': WMagicFunction(stream_peek, module, name='peek'),
        'exec': WMagicFunction(w_exec, module, name='exec'),
        'int_from_str': WMagicFunction(int_from_str, module),
        'symbol_at': WMagicFunction(symbol_at, module),
        'define': Define(),
        'import': import_,
        'exception': WMagicFunction(exception, module, check_args=False),
        'help': WMagicFunction(w_help, module, name='help'),
        'def': Def(),
        'is_file': WMagicFunction(w_is_file, module, name='is_file'),
        'is_dir': WMagicFunction(w_is_dir, module, name='is_dir'),
        'list_dir': WMagicFunction(w_list_dir, module, name='list_dir'),
        'nth': WMagicFunction(nth, module),
        'starts_with': WMagicFunction(w_starts_with, module,
                                      name='starts_with'),
        'ends_with': WMagicFunction(w_ends_with, module, name='ends_with'),
        'join': WMagicFunction(w_join, module, name='join'),
        'exec_src': WMagicFunction(w_exec_src, module, name='exec_src',
                                   check_args=False),
        'name_of': WMagicFunction(w_name_of, module, name='name_of'),
        'filter': WMagicFunction(w_filter, module, name='filter'),
        'module': WMagicFunction(w_module, module, name='module',
                                 check_args=False),
    })
    return module
