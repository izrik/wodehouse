from wtypes.control import WSetHandlers, WEvalRequired
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

        s_exc = WSymbol.get('except')
        s_fin = WSymbol.get('finally')
        s_as = WSymbol.get('as')

        # check args
        if len(exprs) < 2:
            raise Exception(f"try requires at least two clauses. "
                            f"Got {len(exprs)} instead.")
        for expr in exprs[1:]:
            if not isinstance(expr, WList):
                raise Exception(f'Clause must be a list. '
                                f'Got "{expr}" ({type(expr)}) instead.')
            if not isinstance(expr[0], WSymbol):
                raise Exception(f'Clause must start with a symbol. '
                                f'Got "{expr[0]}" ({type(expr[0])}) instead.')
            if expr[0] == s_exc:
                if len(expr) < 2:
                    raise Exception('No expression in except clause.')
                elif len(expr) == 2:
                    pass
                elif len(expr) == 3:
                    if expr[1] == s_as:
                        raise Exception('No expression in except clause.')
                    else:
                        raise Exception(
                            'Too many expressions in except clause.')
                elif len(expr) == 4:
                    if expr[1] == s_as:
                        pass
                    else:
                        raise Exception(
                            'Too many expressions in except clause.')
                else:  # len(expr) > 4
                    raise Exception('Too many expressions in except clause.')
            elif expr[0] == s_fin:
                if len(expr) < 2:
                    raise Exception('No expression in finally clause.')
                elif len(expr) == 2:
                    pass
                else:  # len(expr) > 2
                    raise Exception('Too many expressions in finally clause.')
            else:  # invalid clause
                raise Exception(f'Invalid clause: {expr[0]}.')

        code_clause = exprs[0]
        except_clause = None
        except_var_name = None
        finally_clause = None
        for expr in exprs[1:]:
            head = expr.head
            if head == s_exc:
                if except_clause is not None:
                    raise Exception(f'Too many except clauses.')
                if finally_clause is not None:
                    raise Exception('An except clause must appear before the '
                                    'finally clause.')
                if len(expr) > 2:
                    except_var_name = expr[2]
                except_clause = expr[-1]
            else:  # head == s_fin:
                if finally_clause is not None:
                    raise Exception('Too many finally clauses.')
                finally_clause = expr[1]

        def run_code_clause():
            return WEvalRequired(code_clause, callback=return_code_retval)

        def return_code_retval(rv):
            return rv

        return WSetHandlers(exception_handler=except_clause,
                            exception_var_name=except_var_name,
                            finally_handler=finally_clause,
                            callback=run_code_clause)
