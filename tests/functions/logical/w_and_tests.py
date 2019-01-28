from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.boolean import WBoolean


class AndTest(TestCase):

    def test_and_returns_false_if_any_false(self):
        # when
        result = eval_str("(and false true)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(and true false)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
        # when
        result = eval_str("(and false false)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)

    def test_and_returns_true_if_all_true(self):
        # when
        result = eval_str("(and true true)", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
