from functions.types import get_type
from wtypes.control import WSetHandlers, WEvalRequired, WRaisedException, \
    WExpandedAndEvaled
from wtypes.exception import WException, WSyntaxError
from wtypes.list import WList
from wtypes.magic_macro import WMagicMacro
from wtypes.symbol import WSymbol


class Try(WMagicMacro):
    def call_magic_macro(self, exprs, scope):
        # In python, the try statement has two forms:
        #   try/clause/except+/else?/finally?
        #   try/clause/finally
        # In the first form one or more "except"s are required but the others
        # are optional. In the second form, there are no "except"s or "else",
        # but "finally" is required.
        #
        # We will keep the two forms, with the differences that only one
        # except will be allowed for now (as we can't yet distinguish between
        # different exception classes), and that there will be no else clause.
        #
        # An except part is of the form:
        #   (except <expr>)
        #
        # A finally part is of the form:
        #   (finally <expr>)
        #
        # Fuller example:
        #   (try
        #       (call_some_function arg1 arg2 arg3)
        #   (except
        #       (print "Something bad happened!"))
        #   (finally
        #       (print "All done!")))
        #
        # And another:
        #
        #   (try
        #       (call_some_function arg1 arg2 arg3)
        #   (finally
        #       (print "Clean up!")))
        #
        # And another:
        #
        #   (try
        #       (call_some_function arg1 arg2 arg3)
        #   (except
        #       (print "Something bad happened!")))
        #
        # In an 'except' clause, you can also specify that the exception that
        # is currently being handled be stored into a temp variable for the
        # duration of the handler, like so:
        #
        #   (try
        #       (call_some_function arg1 arg2 arg3)
        #   (except as e
        #       (print (format "Something bad happened: {}" e))))
        #
        # This acts like an implicit 'let', so the variable will obscure any
        # other values with the same name in the current scope, and the
        # exception will not be available after the handler has completed.
        #
        # Additionally, the clause can filter what exception type it catches:
        #
        #   (try
        #       (call_some_function arg1 arg2 arg3)
        #   (except SystemExit as e
        #       (print (format "Tried to exit: {}" e))))
        #
        # The above will only catch a SystemExit exception (usually a result
        # of a call to the `exit` function of the `sys` module).
        #

        s_exc = WSymbol.get('except')
        s_fin = WSymbol.get('finally')
        s_as = WSymbol.get('as')

        # check args
        if len(exprs) < 2:
            return WRaisedException(
                # TODO: get the position of the enclosing macro call
                WSyntaxError(f"try requires at least two clauses. "
                             f"Got {len(exprs)} instead.",
                             exprs[0].position))
        for expr in exprs[1:]:
            if not isinstance(expr, WList):
                return WRaisedException(
                    WSyntaxError(f'Clause must be a list. '
                                 f'Got "{expr}" ({get_type(expr)}) instead.',
                                 expr.position))
            if not isinstance(expr[0], WSymbol):
                return WRaisedException(
                    WSyntaxError(f'Clause must start with a symbol. '
                                 f'Got "{expr[0]}" ({get_type(expr[0])}) '
                                 f'instead.',
                                 expr[0].position))
            if expr[0] == s_exc:
                if len(expr) < 2:
                    return WRaisedException(
                        WSyntaxError('No expression in except clause.',
                                     expr.position))
                elif len(expr) == 2:  # except expr
                    pass
                elif len(expr) == 3:  # except T expr
                    if expr[1] == s_as:
                        return WRaisedException(
                            WSyntaxError('No expression in except clause.',
                                         expr.position))
                    else:
                        exc_type_expr = expr[1]
                        if not isinstance(exc_type_expr, WSymbol) or \
                                (exc_type_expr != WSymbol.get('Exception') and
                                 exc_type_expr != WSymbol.get('SystemExit')):
                            return WRaisedException(
                                # TODO: TypeError
                                WException(
                                    'Except clause filter must be a '
                                    'subclass of Exception.'))
                elif len(expr) == 4:  # except as e expr
                    if expr[1] == s_as:
                        pass
                    else:
                        return WRaisedException(
                            WSyntaxError(
                                'Too many expressions in except clause.',
                                expr.position))
                elif len(expr) == 5:  # except T as e expr
                    exc_type_expr = expr[1]
                    if not isinstance(exc_type_expr, WSymbol) or \
                            (exc_type_expr != WSymbol.get('Exception') and
                             exc_type_expr != WSymbol.get('SystemExit')):
                        return WRaisedException(
                            # TODO: TypeError
                            WException(
                                'Except clause filter must be a '
                                'subclass of Exception.'))
                    if expr[2] != s_as:
                        return WRaisedException(
                            WSyntaxError(
                                'Too many expressions in except clause.',
                                expr.position))
                else:  # len(expr) > 5
                    return WRaisedException(
                        WSyntaxError('Too many expressions in except clause.',
                                     expr.position))
            elif expr[0] == s_fin:
                if len(expr) < 2:
                    return WRaisedException(
                        WSyntaxError('No expression in finally clause.',
                                     expr.position))
                elif len(expr) == 2:
                    pass
                else:  # len(expr) > 2
                    return WRaisedException(
                        WSyntaxError(
                            'Too many expressions in finally clause.',
                            expr.position))
            else:  # invalid clause
                return WRaisedException(
                    WSyntaxError(f'Invalid clause: {expr[0]}.',
                                 expr[0].position))

        code_clause = exprs[0]
        except_clauses = []
        finally_clause = None
        for expr in exprs[1:]:
            head = expr.head
            if head == s_exc:
                if finally_clause is not None:
                    return WRaisedException(
                        WSyntaxError(
                            'An except clause must appear before the '
                            'finally clause.',
                            expr.position))
                except_var_name = None
                filter_type = WSymbol.get('Exception')
                if len(expr) == 2:
                    pass
                elif len(expr) == 3:
                    filter_type = expr[1]
                elif len(expr) == 4:
                    except_var_name = expr[2]
                else:  # len(expr) == 5
                    filter_type = expr[1]
                    except_var_name = expr[3]
                except_clauses.append(ExceptClause(expr=expr[-1],
                                                   var_name=except_var_name,
                                                   filter_type=filter_type))
            else:  # head == s_fin:
                if finally_clause is not None:
                    return WRaisedException(
                        WSyntaxError('Too many finally clauses.',
                                     expr.position))
                finally_clause = expr[1]

        def run_code_clause():
            return WEvalRequired(code_clause, callback=return_code_retval)

        def return_code_retval(rv):
            return WExpandedAndEvaled(rv)

        return WSetHandlers(exception_handlers=except_clauses,
                            finally_handler=finally_clause,
                            callback=run_code_clause)


class ExceptClause:
    def __init__(self, expr, var_name, filter_type):
        self.expr = expr
        self.var_name = var_name
        self.filter_type = filter_type
