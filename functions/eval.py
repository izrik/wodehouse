from wtypes.control import WControl
from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from functions.read import parse
from wtypes.macro import WMacro
from wtypes.boolean import WBoolean
from wtypes.list import WList
from wtypes.magic_macro import WMagicMacro
from wtypes.number import WNumber
from wtypes.object import WObject
from wtypes.scope import WScope
from wtypes.string import WString
from wtypes.symbol import WSymbol


def w_eval(expr, scope):
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

    def eval_for_magic(rv, s):
        if isinstance(rv, WControl):
            # if rv.exception:
            #     return rv
            if rv.callback:
                if rv.expr is None:
                    raise Exception(f'No value given for the '
                                    f'callback: {rv.callback}')
                s2 = s
                if rv.scope is not None:
                    s2 = rv.scope
                e2 = w_eval(rv.expr, s2)
                return eval_for_magic(rv.callback(e2), s)
            if rv.expr is None:
                raise Exception(f'Not sure what to do with the control: '
                                f'{rv}')
            return rv.expr
        if isinstance(rv, WObject):
            return rv
        if isinstance(rv, tuple):
            # magic macro returning (expr, scope)
            return rv[0]
        raise Exception(f'Invalid return from magic function: {rv}')

    if isinstance(expr, WList):
        head = expr.head
        if head == WSymbol.get('quote'):
            # TODO: more checks (e.g. make sure second is there)
            return expr.second
        callee = w_eval(head, scope)
        args = expr.remaining
        if isinstance(callee, WMacro):
            if isinstance(callee, WMagicMacro):
                rv1 = callee.call_macro(args, scope=scope)
                return eval_for_magic(rv1, scope)
            raise Exception(f'WMacro not implemented: {callee}')
        if not isinstance(callee, WFunction):
            raise Exception(
                'Callee is not a function. Got "{}" ({}) instead.'.format(
                    callee, type(callee)))
        evaled_args = [w_eval(arg, scope) for arg in args]
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
            return eval_for_magic(rv1, scope)

        return w_eval(callee.expr, fscope)
    if isinstance(expr, WSymbol):
        if expr not in scope:
            raise NameError(
                'No object found by the name of "{}"'.format(expr.name))
        value = scope[expr]
        return value
    if isinstance(expr, (WNumber, WString, WBoolean, WFunction, WMacro,
                         WScope)):
        return expr
    raise Exception('Unknown object type: "{}" ({})'.format(expr, type(expr)))


_eval_source = w_eval.__doc__


def eval_str(input_s, scope=None):
    """
    (define eval_str
    (lambda (input scope)
        (w_eval (parse input) scope)))
    """
    expr = parse(input_s)
    value = w_eval(expr, scope)
    return value
