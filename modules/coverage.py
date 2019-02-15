import os.path

from functions.types import get_type
from wtypes.boolean import WBoolean
from wtypes.control import WSetHandlers, WEvalRequired, WRaisedException
from wtypes.exception import WException
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.magic_macro import WMagicMacro
from wtypes.module import WModule
from wtypes.object import WObject
from wtypes.symbol import WSymbol

__src_file__ = None
__src__ = None


def create__coverage_module(builtins_module):
    mod = WModule(builtins_module=builtins_module, name='_coverage')
    mod['with_capture_exprs'] = WithCaptureExprs()

def create_coverage_module(builtins_module):
    global __src_file__
    global __src__

    __src_file__ = os.path.join(os.path.dirname(__file__), 'coverage.w')
    with open(__src_file__, 'r') as __f:
        __src__ = __f.read()
    from functions.exec_src import w_exec_src
    mod = WModule(builtins_module=builtins_module, name='coverage',
                  filename=__src_file__)
    from wtypes.magic_function import WMagicFunction
    mod['run_file'] = WMagicFunction(run_file, mod)
    mod['run_module'] = WMagicFunction(run_module, mod)
    w_exec_src(__src__, builtins_module=builtins_module, name='coverage',
               filename=__src_file__, scope=mod)
    return mod


class WithCaptureExprs(WMagicMacro):
    def __init__(self):
        super().__init__()

    def call_magic_macro(self, exprs, scope):
        from functions.eval import add_emit_listener, remove_emit_listener
        from wtypes.scope import WScope

        expr = exprs[0]

        if not isinstance(expr, WObject):
            raise TypeError(f'Argument to with_capture_exprs must be a '
                            f'WObject. Got "{expr}" ({type(expr)}) instead.')
        if not isinstance(expr, WList):
            return WRaisedException(
                WException(f'Argument to with_capture_exprs must be a list. '
                           f'Got "{expr}" ({get_type(expr)}) instead.'))

        captured_positions = WScope()

        def process_expr(_expr):
            pos = _expr.position
            if pos is not None and pos in captured_positions:
                captured_positions[pos] = WBoolean.true

        f = process_expr
        add_emit_listener(f)

        def on_finally():
            remove_emit_listener(f)

        def return_results(_expr):
            return WList(_expr, captured_positions)

        def eval_expr():
            return WEvalRequired(expr, callback=return_results, scope=scope)

        return WSetHandlers(exception_handler=None, exception_var_name=None,
                            finally_handler=WList(WMagicFunction(on_finally,
                                                                 None)),
                            callback=eval_expr)


def run_file(filename, argv):
    def run_with_runtime(rt):
        from wodehouse import run_file as run_file_1
        return run_file_1(filename, argv=argv, runtime=rt)

    return WEvalRequired(WSymbol.get('__runtime__'),
                         callback=run_with_runtime)


def run_module(module_name, argv):
    def run_with_runtime(rt):
        from wodehouse import run_module as run_module_1
        return run_module_1(module_name, argv=argv, runtime=rt)

    return WEvalRequired(WSymbol.get('__runtime__'),
                         callback=run_with_runtime)
