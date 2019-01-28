from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.boolean import WBoolean


class GreaterThanTest(TestCase):

    def test_greater_than_returns_false_for_lesser(self):
        # when
        result = eval_str("(> 1 2)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)

    def test_greater_than_returns_true_for_greater(self):
        # when
        result = eval_str("(> 2 1)", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_greater_than_returns_false_for_equal(self):
        # when
        result = eval_str("(> 1 1)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
