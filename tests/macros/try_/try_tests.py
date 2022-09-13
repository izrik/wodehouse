from unittest import TestCase
from unittest.mock import Mock

from functions.eval import eval_str
from functions.str import w_str
from modules.builtins import create_builtins_module
from modules.sys import create_sys_module
from wtypes.control import WRaisedException
from wtypes.exception import WException, WSystemExit, WSyntaxError
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.magic_macro import WMagicMacro
from wtypes.number import WNumber
from wtypes.position import Position
from wtypes.string import WString
from wtypes.symbol import WSymbol


def mkfunc(name, calls, s, _f=None):
    def f():
        calls.append(name)
        return WString(name)

    mf = WMagicFunction(f, enclosing_scope=s, name=name)
    s[name] = mf
    return mf


class TryTest(TestCase):
    def test_w_when_no_exception_in_code_then_handler_not_triggered(self):
        # when
        result = eval_str('''(try
                                "code"
                             (except
                                "exc")
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("code", result)
        # when
        result = eval_str('''(try
                                "code"
                             (except
                                "exc"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("code", result)

        # when
        result = eval_str('''(try
                                "code"
                             (except
                                (raise "exc")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("code", result)

    def test_w_exception_in_finally_overrides_retval_in_code(self):
        # when
        result = eval_str('''(try
                                "code"
                             (except
                                "exc")
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)
        # when
        result = eval_str('''(try
                                "code"
                             (except
                                (raise "exc"))
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)
        # when
        result = eval_str('''(try
                                "code"
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)

    def test_w_except_is_ignored_if_no_exception_in_code(self):
        # when
        result = eval_str('''(try
                                "code"
                             (except
                                (raise "exc"))
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("code", result)

    def test_w_except_provides_retval_when_exception_in_code(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                "exc")
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)

    def test_w_exception_in_finally_overrides_retval_in_except(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                "exc")
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)

    def test_w_retval_in_finally_does_not_override_exception_in_except(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                (raise "exc"))
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("exc", result.exception.message)

    def test_w_exception_in_finally_overrides_exception_in_except(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                (raise "exc"))
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)

    def test_w_return_value_in_except_overrides_exception_from_code(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                "exc"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)

    def test_w_exception_in_except_overrides_exception_from_code_block(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (except
                                (raise "exc")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("exc", result.exception.message)

    def test_w_return_value_in_finally_does_not_override_normal_retval(self):
        # when
        result = eval_str('''(try
                                "code"
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("code", result)

    def test_w_retval_in_finally_does_not_override_exception_in_code(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (finally
                                "fin"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("code", result.exception.message)

    def test_w_exception_in_finally_overrides_exception_in_code(self):
        # when
        result = eval_str('''(try
                                (raise "code")
                             (finally
                                (raise "fin")))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("fin", result.exception.message)

    def test_exceptions_raised_in_callee_caught_in_caller(self):
        # given
        s = create_builtins_module()
        eval_str('(def x () (try (y) (except 3)))', s)
        eval_str('(def y () (raise "a"))', s)
        # when
        result = eval_str("(x)", s)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)

    def test_finally_executes_after_except(self):
        # given
        calls = []
        s = create_builtins_module()
        mkfunc('x', calls, s)
        mkfunc('y', calls, s)
        # when
        result = eval_str(
            '(try (raise "asdf") (except (x)) (finally (y)))', s)

        # then
        self.assertEqual(['x', 'y'], calls)
        self.assertIsInstance(result, WString)
        self.assertEqual('x', result)

    def test_finally_executes_after_code_clause_without_except(self):
        # given
        calls = []
        s = create_builtins_module()
        mkfunc('x', calls, s)
        mkfunc('y', calls, s)
        # when
        result = eval_str(
            '(try (x) (finally (y)))', s)

        # then
        self.assertEqual(['x', 'y'], calls)
        self.assertIsInstance(result, WString)
        self.assertEqual('x', result)

    def test_nested_finally_clauses_evaluated_inside_out(self):
        calls = []
        s = create_builtins_module()
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)
        mkfunc('c', calls, s)
        mkfunc('d', calls, s)
        mkfunc('e', calls, s)
        mkfunc('f', calls, s)
        mkfunc('g', calls, s)
        mkfunc('h', calls, s)
        mkfunc('i', calls, s)
        # when
        result = eval_str(
            """(try
                (exec
                    (a)
                    (try
                        (exec
                            (b)
                            (try
                                (exec
                                    (c)
                                    (raise "asdf")
                                    (d))
                            (finally
                                (e)))
                            (f))
                    (finally
                        (g)))
                    (h))
            (finally
                (i)))""", s)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("asdf", result.exception.message)
        # and
        self.assertEqual(['a', 'b', 'c', 'e', 'g', 'i'], calls)

    def test_exception_finally_clauses_in_other_functions_eval_in_order(self):
        calls = []
        s = create_builtins_module()
        x = eval_str(
            """(def x ()
                    (try
                        (exec
                            (c)
                            (raise "asdf")
                            (d))
                    (finally
                        (e))))""", s)
        y = eval_str(
            """(def y ()
                (try
                    (exec
                        (b)
                        (x)
                        (f))
                (finally
                    (g))))""", s)
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)
        mkfunc('c', calls, s)
        mkfunc('d', calls, s)
        mkfunc('e', calls, s)
        mkfunc('f', calls, s)
        mkfunc('g', calls, s)
        mkfunc('h', calls, s)
        mkfunc('i', calls, s)
        # precondition
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        # when
        result = eval_str(
            """(try
                (exec
                    (a)
                    (y)
                    (h))
            (finally
                (i)))""", s)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual("asdf", result.exception.message)
        # and
        self.assertEqual(['a', 'b', 'c', 'e', 'g', 'i'], calls)

    def test_exception_in_function_argument_gets_handled(self):
        # given
        s = create_builtins_module()
        calls = []
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)
        mkfunc('c', calls, s)
        mkfunc('d', calls, s)
        # when
        result = eval_str(
            """(try
                (exec
                    (a)
                    (print
                        (+ a b (/ 1 0)))
                    (b))
                (except
                    (exec
                        (c)
                        "exc"))
                (finally
                    (d)))""", s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)
        # and
        self.assertEqual(['a', 'c', 'd'], calls)

    def test_exception_in_macro_triggers_handler(self):
        # given
        s = create_builtins_module()
        calls = []
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)

        class CustomMacro(WMagicMacro):
            def call_magic_macro(self, exprs, scope):
                return WRaisedException(WException("exception in macro"))

        s['throw'] = CustomMacro()
        # when
        result = eval_str("""(try
                                (throw)
                             (except
                                (exec
                                    (a)
                                    "exc"))
                             (finally
                                (exec
                                    (b)
                                    "fin")))""", s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)
        # and
        self.assertEqual(['a', 'b'], calls)

    def test_exception_in_result_of_macro_expansion_triggers_handler(self):
        # given
        s = create_builtins_module()
        calls = []
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)
        mkfunc('c', calls, s)
        mkfunc('d', calls, s)
        mkfunc('e', calls, s)
        # when
        result = eval_str("""(try
                                (if (exec
                                        (a)
                                        (/ 1 0))
                                    (exec
                                        (b)
                                        "true")
                                     (exec
                                        (c)
                                        "false"))
                             (except
                                (exec
                                    (d)
                                    "exc"))
                             (finally
                                (exec
                                    (e)
                                    "fin")))""", s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)
        # and
        self.assertEqual(['a', 'd', 'e'], calls)

    def test_exception_in_callee_triggers_handler(self):
        # given
        s = create_builtins_module()
        calls = []
        mkfunc('a', calls, s)
        mkfunc('b', calls, s)
        mkfunc('c', calls, s)
        mkfunc('d', calls, s)
        mkfunc('e', calls, s)
        x = eval_str('(def x () (raise "asdf"))', s)
        y = eval_str('(def y () ((x) (b) 2 3 4))', s)
        # precondition
        self.assertIsNotNone(x)
        self.assertIsNotNone(y)
        # when
        result = eval_str("""(try
                                (exec
                                    (a)
                                    (y)
                                    (c))
                             (except
                                (exec
                                    (d)
                                    "exc"))
                             (finally
                                (exec
                                    (e)
                                    "fin")))""", s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("exc", result)
        # and
        self.assertEqual(['a', 'd', 'e'], calls)

    def test_var_name_in_except_adds_exception_to_scope(self):
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except as e
                                e))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WException)
        self.assertEqual("asdf", result.message)

    def test_filter_with_var_name_in_except_is_allowed(self):
        # TODO: rename once filtering is working
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Exception as e
                                e))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WException)
        # TODO: The following will not be true once filtering is working
        self.assertNotIsInstance(result, WSystemExit)
        self.assertEqual("asdf", result.message)

    # TODO: check stacktraces

    def test_too_few_args_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf"))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'try requires at least two clauses. Got 1 instead.')
        self.assertEqual(result.exception.position.line, 2)
        self.assertEqual(result.exception.position.char, 34)

    def test_no_finally_expr_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (finally))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'No expression in finally clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_too_many_finally_exprs_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (finally 1 2))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Too many expressions in finally clause.')

    def test_no_expr_in_except_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (except))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'No expression in except clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_no_expr_in_except_as_e_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (except as e))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'No expression in except clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_too_many_exprs_in_except_without_as_e_raises_2(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (except 1 2 3))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Too many expressions in except clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_too_many_exprs_in_except_with_as_e_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (except as e 1 2 3))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Too many expressions in except clause.')

    def test_too_many_finally_clauses_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (finally 1)
                             (finally 2))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Too many finally clauses.')

    def test_finally_except_clauses_wrong_order_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (finally 1)
                             (except 2))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        wexc = result.exception
        self.assertIsInstance(wexc, WSyntaxError)
        self.assertEqual(w_str(wexc.message),
                         'An except clause must appear before the finally '
                         'clause.')
        self.assertEqual(wexc.position.line, 4)
        self.assertEqual(wexc.position.char, 30)

    def test_invalid_clause_head_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (something 1))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Invalid clause: something.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 31)

    def test_invalid_clause_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             1)''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Clause must be a list. Got "1" '
                         '(Number) instead.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_non_symbol_clause_head_raises(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (1 2 3))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Clause must start with a symbol. Got "1" '
                         '(Number) instead.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 31)

    def test_filter_exception_catches_regular_exception(self):
        # when
        result = eval_str('''(try
                                 (raise "asdf")
                             (except Exception 2))''',
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 2)

    def test_filter_systemexit_does_not_catch_regular_exception(self):
        # given
        bm = create_builtins_module()
        calls = []
        mkfunc('a', calls, bm)
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except SystemExit
                                (a)))''',
                          bm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message), 'asdf')

    def test_filter_exception_does_not_catch_systemexit(self):
        # given
        bm = create_builtins_module()
        sm = create_sys_module(bm, argv=[])
        # when
        result = eval_str('''(try
                                 (exit 1)
                             (except Exception 2))''',
                          sm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSystemExit)
        self.assertEqual(result.exception.code, 1)

    def test_filter_systemexit_catches_systemexit(self):
        # given
        bm = create_builtins_module()
        sm = create_sys_module(bm, argv=[])
        # when
        result = eval_str('''(try
                                (exit 1)
                             (except SystemExit 2))''',
                          sm)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 2)

    def test_bad_filter_type_wraises_3(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Something 2))''',
                          bm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Except clause filter must be a subclass of '
                         'Exception.')

    def test_bad_filter_type_wraises_5(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Something as e 2))''',
                          bm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertEqual(w_str(result.exception.message),
                         'Except clause filter must be a subclass of '
                         'Exception.')

    def test_many_expressions_after_filter_as_e_wraises(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Exception as e 2 3))''',
                          bm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Too many expressions in except clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_many_expressions_after_filter_wraises(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Exception 2 3 4))''',
                          bm)
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSyntaxError)
        self.assertEqual(w_str(result.exception.message),
                         'Too many expressions in except clause.')
        self.assertEqual(result.exception.position.line, 3)
        self.assertEqual(result.exception.position.char, 30)

    def test_multiple_clauses_filter_systemexit_catches_systemexit(self):
        # given
        bm = create_builtins_module()
        sm = create_sys_module(bm, argv=[])
        # when
        result = eval_str('''(try
                                (exit 1)
                             (except SystemExit 2)
                             (except Exception 3))''',
                          sm)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 2)

    def test_multiple_clauses_filter_systemexit_catches_systemexit_2(self):
        # given
        bm = create_builtins_module()
        sm = create_sys_module(bm, argv=[])
        # when
        result = eval_str('''(try
                                (exit 1)
                             (except Exception 2)
                             (except SystemExit 3))''',
                          sm)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 3)

    def test_multiple_clauses_filter_exception_catches_exception(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except SystemExit 2)
                             (except Exception 3))''',
                          bm)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 3)

    def test_multiple_clauses_filter_exception_catches_exception_2(self):
        # given
        bm = create_builtins_module()
        # when
        result = eval_str('''(try
                                (raise "asdf")
                             (except Exception 2)
                             (except SystemExit 3))''',
                          bm)
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 2)

    def test_body_is_evaluated_only_once_1(self):
        # given
        bm = create_builtins_module()
        mm = Mock(return_value=WList(WSymbol("f")))
        fname = 'f'
        mf = WMagicFunction(mm, enclosing_scope=bm, name=fname)
        bm[fname] = mf

        # `f` returns a call (in the form of a list with a symbol) of itself
        # without arguments. It should only be called once; the return value
        # should NOT be evaluated.

        # when
        result = eval_str("""(try
                                (f)
                             (finally 0))""",
                          bm)
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual(result, [WSymbol("f")])
        mm.assert_called_once_with()

    def test_body_is_evaluated_only_once_2(self):
        # given
        bm = create_builtins_module()
        # mm = Mock(return_value=WList(WSymbol("f")))
        mm = Mock()
        fname = 'f'
        mf = WMagicFunction(mm, enclosing_scope=bm, name=fname)
        mm.return_value = WList(mf)
        bm[fname] = mf

        # `f` returns a call (in the form of a list with a reference to `f`)
        # of itself without arguments. It should only be called once; the
        # return value should NOT be evaluated.

        # when
        result = eval_str("""(try
                                (f)
                             (finally 0))""",
                          bm)
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual(result, [mf])
        mm.assert_called_once_with()
