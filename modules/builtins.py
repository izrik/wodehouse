

def create_builtins_module(import_=None):
    from functions.collections import w_map, w_in
    from functions.convert import int_from_str
    from functions.exception import exception
    from functions.exec_src import w_exec
    from functions.io import w_print, w_format, read_file
    from functions.lisp import car, cdr, cons, atom
    from functions.list import list_func
    from functions.logical import w_not, w_or, w_and, less_than, \
        less_than_or_equal_to, greater_than, greater_than_or_equal_to, eq
    from wtypes.magic_function import WMagicFunction
    from functions.math import add, sub, mult, div
    from functions.raise_ import w_raise
    from functions.str import w_str
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
    from wtypes.scope import WScope

    if import_ is None:
        import_ = Import()

    scope = WScope()
    scope.update({
        '+': WMagicFunction(add, scope, name='+'),
        '-': WMagicFunction(sub, scope, name='-'),
        '*': WMagicFunction(mult, scope, name='*'),
        '/': WMagicFunction(div, scope, name='/'),
        'let': Let(),
        'apply': Apply(),
        'list': WMagicFunction(list_func, scope, name='list'),
        'len': WMagicFunction(w_len, scope, name='len'),
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
        'new_scope_within': WMagicFunction(new_scope_within, scope,
                                           check_args=False),
        'get': WMagicFunction(get_scope_value, scope, name='get'),
        'dir': WMagicFunction(w_dir, scope, name='dir', check_args=False),
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
        'define': Define(),
        'import': import_,
        'exception': WMagicFunction(exception, scope, check_args=False),
        'help': WMagicFunction(w_help, scope, name='help'),
        'def': Def(),
    })
    return scope
