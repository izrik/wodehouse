from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.boolean import WBoolean
from wtypes.control import WRaisedException
from wtypes.exception import WException


class WAssertTest(TestCase):

    def test_assert_raises_exception_on_false(self):
        # when
        result = eval_str("(assert false)", create_global_scope())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual('Assertion failed: "false"',
                         result.exception.message)

    def test_assert_raises_exception_on_false_expr(self):
        # when
        result = eval_str("(assert (< 3 1))", create_global_scope())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual('Assertion failed: "(< 3 1)"',
                         result.exception.message)

    def test_assert_returns_true_on_true(self):
        # when
        result = eval_str("(assert (< 1 2))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_assert_returns_arg_on_non_boolean(self):
        # when
        result = eval_str("(assert \"abc\")", create_global_scope())
        # then
        self.assertEqual("abc", result)
