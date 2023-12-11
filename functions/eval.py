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

    from wtypes.callstack import WStackFrame
    from wtypes.scope import WScope
    from wtypes.object import WObject
    from wtypes.evaluator import WEvaluator

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

    _eval = None
    if scope.get_builtins_module() is not None and \
            '__current_runtime__' in scope.get_builtins_module() and \
            scope.get_builtins_module()['__current_runtime__'] is not None:
        rt = scope.get_builtins_module()['__current_runtime__']
        _eval = rt.evaluator
    if not _eval:
        _eval = WEvaluator.value()
    return _eval(expr, scope, stack)


_eval_source = w_eval.__doc__


def eval_str(input_s, scope=None):
    """
    (define eval_str
    (lambda (input scope)
        (w_eval (parse input) scope)))
    """
    from functions.read import parse
    expr = parse(input_s)
    value = w_eval(expr, scope)
    return value


def is_exception(rv, stack=None):
    from wtypes.control import WRaisedException
    if isinstance(rv, WRaisedException) and rv.exception is not None:
        if rv.stack is None:
            rv.stack = stack
        return True
    return False
