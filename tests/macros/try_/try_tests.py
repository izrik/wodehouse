from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.magic_function import WMagicFunction
from wtypes.magic_macro import WMagicMacro
from wtypes.number import WNumber
from wtypes.string import WString


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

    # TODO: clause syntactic order (check arguments)
