from functions.exec_src import w_exec_src
from wtypes.callstack import WStackFrame
from wtypes.control import WControl, WRaisedException, WMacroExpansion, \
    WReturnValue, WEvalRequired, WExecSrcRequired, WSetHandlers, \
    WExpandedAndEvaled
from wtypes.exception import WException
from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from functions.read import parse
from wtypes.macro import WMacro
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.scope import WScope
from wtypes.set import WSet
from wtypes.string import WString
from wtypes.symbol import WSymbol


def w_eval(expr, scope, stack=None):
    """
(define w_eval
(lambda (expr scope)
    (cond
    ((isinstance expr 'Symbol)
        (get scope expr))
    ((isinstance expr '(Number String Boolean))
        expr)
    ((isinstance expr 'List)
        (let (head (car expr))
        (if
            (eq head 'quote)
            (car (cdr expr))
            (let (callee w_eval(head scope))
            (let (args (cdr expr))
            (cond
            ((isinstance callee 'Macro)
                (let (exprs_scope (call_macro callee args scope))
                (let (exprs (car exprs_scope))
                (let (scope (car (cdr exprs_scope)))
                (w_eval exprs scope)))))
            ((not (isinstance callee 'Function))
                (raise
                    (format
                        "Callee is not a function. Got \\"{}\\" ({}) instead."
                        callee
                        (type callee))))
            (true
                (let (evaled_args
                    (map
                        (lambda (name value)
                            (list name (w_eval value scope)))
                        args (get_func_args callee)))
                (let (scope (new_scope_within
                                (get_func_enclosing_scope callee)
                                evaled_args))
                (if
                    (isinstance callee 'MagicFunction)
                    implementation_specific
                    (w_eval (get_func_expr callee) scope)))))))))))
    (true
        (raise
            (format
                "Unknown object type: \\"{}\\" ({})" expr (type expr)))))))


    """
    # TODO: proper subtypes and inheritance, instead of just symbols
    # TODO: w_eval
    # TODO: call_macro
    # TODO: varargs
    # TODO: get_func_args
    # TODO: get_func_expr
    # TODO: get_func_enclosing_scope
    if scope is None:
        scope = WScope()
    elif not isinstance(scope, WScope):
        scope = WScope(scope)
    if not isinstance(expr, WObject):
        raise Exception(
            'Non-domain value escaped from containment! '
            'Got "{}" ({}).'.format(expr, type(expr)))
    if stack is None:
        stack = WStackFrame(location=None, prev=None)

    # check callstack height
    if stack.depth >= 400:
        return handle_finally(
            WRaisedException(
                exception=WException(f'Stack overflow'),
                stack=stack),
            scope,
            stack)

    # Look up the current runtime and emit the expr
    get_rt = None
    if 'get_current_runtime' in scope and \
            scope['get_current_runtime'] is not None:
        get_rt = scope['get_current_runtime']
    elif scope.get_builtins_module() is not None and \
            'get_current_runtime' in scope.get_builtins_module() and \
            scope.get_builtins_module()['get_current_runtime'] is not None:
        get_rt = scope.get_builtins_module()['get_current_runtime']
    if get_rt:
        rt = get_rt.call_magic_function()
        rt.emit(expr, scope, stack)

    stack.expr = expr
    stack.scope = scope

    rv = expand_macros(expr, scope, stack=stack)
    if is_exception(rv, stack=stack):
        rv2 = handle_exception(rv, scope, stack)
        return handle_finally(rv2, scope, stack)

    expanded_scope = scope
    if isinstance(rv, WExpandedAndEvaled):
        return handle_finally(rv.expr, scope, stack)
    if isinstance(rv, WMacroExpansion):
        expanded_expr = rv.expr
        if rv.scope is not None:
            expanded_scope = rv.scope
    elif isinstance(rv, WReturnValue):
        expanded_expr = rv.expr
    elif not isinstance(rv, WControl):
        expanded_expr = rv
    else:
        raise Exception(f'Something strange returned from expand_macros: '
                        f'{rv} ({type(rv)})')

    stack.expanded_expr = expanded_expr
    stack.expanded_scope = expanded_scope

    if isinstance(expanded_expr, WList):
        if len(expanded_expr) == 0:
            return handle_finally(expanded_expr, scope, stack)
        head = expanded_expr.head
        if head == WSymbol.get('quote'):
            # TODO: more checks (e.g. make sure second is there)
            return handle_finally(expanded_expr.second, scope, stack)

        callee = head
        if not isinstance(callee, WFunction):
            from functions.types import get_type
            return handle_finally(
                WRaisedException(exception=WException(
                    f'Callee is not a function. '
                    f'Got "{callee}" ({get_type(callee)}) instead.'),
                    stack=stack),
                scope,
                stack)
        stack.callee = callee

        args = expanded_expr.remaining
        stack.args = args

        evaled_args = []
        for arg in args:
            astack = WStackFrame(location=stack.location, prev=stack.prev)
            evaled_arg = w_eval(arg, expanded_scope, stack=astack)
            if is_exception(evaled_arg, astack):
                rv2 = handle_exception(evaled_arg, scope, stack)
                return handle_finally(rv2, scope, stack)
            evaled_args.append(evaled_arg)
        stack.evaled_args = evaled_args

        if (callee.check_args and
                callee.num_parameters is not None and
                len(evaled_args) != callee.num_parameters):
            # TODO: w-exception
            raise Exception(
                f'Function "{callee.name}" expected {callee.num_parameters} '
                f'args, got {len(evaled_args)} instead.')

        fstack = WStackFrame(location=callee, prev=stack)

        if isinstance(callee, WMagicFunction):
            rv1 = callee.call_magic_function(*evaled_args,
                                             __current_scope__=expanded_scope)
            return handle_finally(
                process_controls(rv1, expanded_scope, stack=fstack),
                scope,
                stack)

        fscope = WScope(enclosing_scope=callee.enclosing_scope)
        for i, argname in enumerate(callee.parameters):
            fscope[argname] = evaled_args[i]
        stack.fscope = fscope
        frv = w_eval(callee.expr, fscope, stack=fstack)
        if is_exception(frv, fstack):
            frv2 = handle_exception(frv, scope, stack)
            return handle_finally(frv2, scope, stack)
        return handle_finally(frv, scope, stack)
    if isinstance(expanded_expr, WSymbol):
        scope2 = expanded_scope
        if expanded_expr not in scope2:
            scope2 = scope2.get_builtins_module()
        if scope2 is None or expanded_expr not in scope2:
            return handle_finally(
                WRaisedException(
                    exception=WException(
                        f'No object found by the name of '
                        f'"{expanded_expr.name}"'),
                    stack=stack),
                scope,
                stack)
        value = scope2[expanded_expr]
        return handle_finally(value, scope, stack)
    if isinstance(expanded_expr, (WNumber, WString, WBoolean, WFunction,
                                  WMacro, WScope, WSet)):
        return handle_finally(expanded_expr, scope, stack)
    if isinstance(expanded_expr, (WStackFrame,)):
        return handle_finally(expanded_expr, scope, stack)
    raise Exception(f'Unknown object type: '
                    f'"{expanded_expr}" ({type(expanded_expr)})')


def matches_exception_type(exc, exc_type):
    from wtypes.exception import WSystemExit
    if isinstance(exc, WSystemExit) and exc_type == WSymbol.get('SystemExit'):
        return True
    if type(exc) == WException and exc_type == WSymbol.get('Exception'):
        return True
    return False


def handle_exception(rv, scope, stack):
    if stack.exception_handlers:
        for eh in stack.exception_handlers:
            if not matches_exception_type(rv.exception, eh.filter_type):
                continue
            ehstack = WStackFrame(stack.location, stack)
            ehscope = scope
            ehscope = WScope(enclosing_scope=ehscope)
            if eh.var_name:
                ehscope[eh.var_name] = rv.exception
            rv2 = w_eval(eh.expr, ehscope, ehstack)
            is_exception(rv2, stack)
            return rv2
    return rv


def handle_finally(rv, scope, stack):
    if stack.finally_handler:
        fhstack = WStackFrame(stack.location, stack)
        fhscope = scope
        fhscope = WScope(enclosing_scope=fhscope)
        rv2 = w_eval(stack.finally_handler, fhscope, fhstack)
        if is_exception(rv2, stack):
            return rv2
    return rv


_eval_source = w_eval.__doc__


def process_controls(control, scope, stack):
    if is_exception(control, stack):
        return control
    if not isinstance(control, WObject):
        raise Exception(f'Invalid return from magic function: '
                        f'{control} ({type(control)})')
    if not isinstance(control, WControl):
        return control
    if isinstance(control, WExpandedAndEvaled):
        return control
    if isinstance(control, WReturnValue):
        return control
    if isinstance(control, WMacroExpansion):
        return control
    if isinstance(control, WSetHandlers):
        pstack = stack.prev
        pstack.exception_handlers = control.exception_handlers
        pstack.finally_handler = control.finally_handler
        return process_controls(control.callback(), scope, stack)
    if not isinstance(control, (WEvalRequired, WExecSrcRequired)):
        raise Exception(f'Invalid return from magic function: '
                        f'{control} ({type(control)}')
    if isinstance(control, WExecSrcRequired):
        ms = w_exec_src(src=control.src,
                        builtins_module=control.builtins_module,
                        name=control.name,
                        filename=control.filename, prevstack=stack)
        if is_exception(ms, stack):
            return ms
        return process_controls(control.callback(ms), scope, stack)
    if isinstance(control, WEvalRequired):
        if control.expr is None:
            raise Exception(f'No value given for the '
                            f'callback: {control.callback}')
        scope2 = scope
        if control.scope is not None:
            scope2 = control.scope
        stack2 = stack
        if control.hide_callee_stack_frame:
            stack2 = stack2.prev
        control2 = w_eval(control.expr, scope2, stack=stack2)
        if is_exception(control2, stack2):
            return control2
        return process_controls(control.callback(control2),
                                scope, stack=stack2)
    raise Exception(f'Unknown control type: "{control}" ({type(control)}).')


def expand_macros(expr, scope, stack):
    if isinstance(expr, WControl):
        raise Exception(f'A control object was passed to expand_macros: '
                        f'{expr} ({type(expr)})')
    if scope is not None and not isinstance(scope, WScope):
        raise Exception('A non-scope object was passed to expand_macros '
                        f'as the scope: {scope} ({type(scope)})')

    if not isinstance(expr, WList):
        if scope is not None:
            return WMacroExpansion(expr, scope)
        return expr

    if len(expr) == 0:
        return WMacroExpansion(expr, scope)

    head = expr.head

    if head == WSymbol.get('quote'):
        return expr

    hstack = WStackFrame(location=stack.location, prev=stack.prev)
    evaled_head = w_eval(head, scope, stack=hstack)
    if is_exception(evaled_head, hstack):
        return evaled_head

    args = expr.remaining
    if not isinstance(evaled_head, WMacro):
        new_expr = WList(evaled_head, *args, position=expr.position)
        if scope is not None:
            return WMacroExpansion(new_expr, scope)
        return new_expr

    mstack = WStackFrame(location=evaled_head, prev=stack)
    rv = evaled_head.call_macro(args, scope=scope)
    if is_exception(rv, stack=mstack):
        return rv
    rv2 = process_controls(rv, scope, stack=mstack)
    if is_exception(rv2, stack=mstack):
        return rv2

    if isinstance(rv2, (WExpandedAndEvaled)):
        return rv2
    expr2 = rv2
    if isinstance(rv2, (WReturnValue, WMacroExpansion)):
        expr2 = rv2.expr
    scope2 = scope
    if isinstance(rv2, WMacroExpansion) and rv2.scope is not None:
        scope2 = rv2.scope
    return expand_macros(expr2, scope2, stack=stack)


def eval_str(input_s, scope=None):
    """
    (define eval_str
    (lambda (input scope)
        (w_eval (parse input) scope)))
    """
    expr = parse(input_s)
    value = w_eval(expr, scope)
    return value


def is_exception(rv, stack=None):
    if isinstance(rv, WRaisedException) and rv.exception is not None:
        if rv.stack is None:
            rv.stack = stack
        return True
    return False
