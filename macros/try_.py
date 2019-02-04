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
        # code exc
        # code fin
        # code exc fin
        #

        s_exc = WSymbol.get('except')
        s_fin = WSymbol.get('finally')

        # check args
        if len(exprs) < 2:
            raise Exception(f"try requires at least two clauses. "
                            f"Got {len(exprs)} instead.")
        n = len(exprs)
        for expr in exprs[1:]:
            if not isinstance(expr, WList) or len(expr) != 2 or \
                    not isinstance(expr[0], WSymbol) or \
                    expr[0] not in [s_exc, s_fin]:
                raise Exception(
                    f'Clause should be an (except <expr>) '
                    f'or (finally <expr>). Got "{exprs[2]}" '
                    f'({type(exprs[2])}) instead.')

        code_clause = exprs[0]
        except_clause = None
        finally_clause = None
        for expr in exprs[1:]:
            head = expr.head
            if head == s_exc:
                if except_clause is not None:
                    raise Exception(f'Only one except clause is allowed.')
                if finally_clause is not None:
                    raise Exception('An except clause must appear before the '
                                    'finally clause')
                except_clause = expr[1]
            elif head == s_fin:
                if finally_clause is not None:
                    raise Exception('Only one finally clause is allowed.')
                finally_clause = expr[1]
            else:
                raise Exception(f'Invalid clause: {head}')

        def run_code_clause():
            return WEvalRequired(code_clause, callback=return_code_retval)

        def return_code_retval(rv):
            return rv

        return WSetHandlers(exception_handler=except_clause,
                            finally_handler=finally_clause,
                            callback=run_code_clause)
