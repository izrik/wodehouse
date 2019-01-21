from wtypes.callstack import WStackFrame
from wtypes.control import WControl, WRaisedException, WMacroExpansion, \
    WReturnValue, WEvalRequired
from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from functions.read import parse
from wtypes.macro import WMacro
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.scope import WScope
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
    stack = WStackFrame(expr=expr, prev=stack)

    def expand_macros(_expr, _scope):
        if isinstance(_expr, WControl):
            raise Exception(f'A control object was passed to expand_macros: '
                            f'{_expr} ({type(_expr)})')
        if _scope is not None and not isinstance(_scope, WScope):
            raise Exception('A non-scope object was passed to expand_macros '
                            f'as the scope: {_scope} ({type(_scope)})')

        if not isinstance(_expr, WList):
            if _scope is not None:
                return WMacroExpansion(_expr, _scope)
            return _expr

        _head = _expr.head

        if _head == WSymbol.get('quote'):
            return _expr

        _evaled_head = w_eval(_head, _scope, stack=stack)
        if is_exception(_evaled_head, stack):
            return _evaled_head

        _args = _expr.remaining
        if not isinstance(_evaled_head, WMacro):
            _new_expr = WList(_evaled_head, *_args)
            if _scope is not None:
                return WMacroExpansion(_expr, _scope)
            return _new_expr

        _rv = _evaled_head.call_macro(_args, scope=_scope)
        if is_exception(_rv, _stack=stack):
            return _rv
        _rv2 = eval_for_magic(_rv, _scope, stack=stack)
        if is_exception(_rv2, _stack=stack):
            return _rv2

        _expr2 = _rv2
        if isinstance(_rv2, (WReturnValue, WMacroExpansion)):
            _expr2 = _rv2.expr
        _scope2 = _scope
        if isinstance(_rv2, WMacroExpansion) and _rv2.scope is not None:
            _scope2 = _rv2.scope
        return expand_macros(_expr2, _scope2)

    rv = expand_macros(expr, scope)
    if is_exception(rv, _stack=stack):
        return rv

    if isinstance(rv, WMacroExpansion):
        expr = rv.expr
        if rv.scope is not None:
            scope = rv.scope
    elif isinstance(rv, WReturnValue):
        expr = rv.expr
    elif not isinstance(rv, WControl):
        expr = rv
    else:
        raise Exception(f'Something strange returned from expand_macros: '
                        f'{rv} ({type(rv)})')

    if isinstance(expr, WList):
        head = expr.head
        if head == WSymbol.get('quote'):
            # TODO: more checks (e.g. make sure second is there)
            return expr.second
        callee = w_eval(head, scope, stack=stack)
        stack.callee = callee
        if is_exception(callee, stack):
            return callee
        args = expr.remaining
        if not isinstance(callee, WFunction):
            raise Exception(
                'Callee is not a function. Got "{}" ({}) instead.'.format(
                    callee, type(callee)))

        evaled_args = []
        for arg in args:
            evaled_arg = w_eval(arg, scope, stack=stack)
            if is_exception(evaled_arg, stack):
                return evaled_arg
            evaled_args.append(evaled_arg)

        if (callee.check_args and
                callee.num_parameters is not None and
                len(evaled_args) != callee.num_parameters):
            raise Exception(
                'Function expected {} args, got {} instead.'.format(
                    len(callee.parameters), len(evaled_args)))
        fscope = WScope(enclosing_scope=callee.enclosing_scope)
        for i, argname in enumerate(callee.parameters):
            fscope[argname] = evaled_args[i]

        if isinstance(callee, WMagicFunction):
            rv1 = callee.call_magic_function(*evaled_args)
            return eval_for_magic(rv1, scope, stack=stack)

        frv = w_eval(callee.expr, fscope, stack=stack)
        is_exception(frv, stack)  # set the stack attribute
        return frv
    if isinstance(expr, WSymbol):
        _scope = scope
        if expr not in _scope:
            _scope = _scope.get_global_scope()
        if _scope is None or expr not in _scope:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = _scope[expr]
        return value
    if isinstance(expr, (WNumber, WString, WBoolean, WFunction, WMacro,
                         WScope)):
        return expr
    raise Exception('Unknown object type: "{}" ({})'.format(expr, type(expr)))


_eval_source = w_eval.__doc__


def eval_for_magic(control, scope, stack):
    if is_exception(control, stack):
        return control
    if not isinstance(control, WObject):
        raise Exception(f'Invalid return from magic function: '
                        f'{control} ({type(control)}')
    if not isinstance(control, WControl):
        return control
    if isinstance(control, WReturnValue):
        return control
    if isinstance(control, WMacroExpansion):
        return control
    if not isinstance(control, WEvalRequired):
        raise Exception(f'Invalid return from magic function: '
                        f'{control} ({type(control)}')

    if control.callback:
        if control.expr is None:
            raise Exception(f'No value given for the '
                            f'callback: {control.callback}')
        scope2 = scope
        if control.scope is not None:
            scope2 = control.scope
        control2 = w_eval(control.expr, scope2, stack=stack)
        if is_exception(control2, stack):
            return control2
        return eval_for_magic(control.callback(control2), scope, stack=stack)
    if control.expr is None:
        raise Exception(f'Not sure what to do with the control: '
                        f'{control}')
    return control


def eval_str(input_s, scope=None):
    """
    (define eval_str
    (lambda (input scope)
        (w_eval (parse input) scope)))
    """
    expr = parse(input_s)
    value = w_eval(expr, scope)
    return value


def is_exception(rv, _stack=None):
    if isinstance(rv, WRaisedException) and rv.exception is not None:
        if rv.stack is None:
            rv.stack = _stack
        return True
    return False
