from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.boolean import WBoolean


class OrTest(TestCase):

    def test_or_returns_true_if_any_true(self):
        # when
        result = eval_str("(or false true)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(or true false)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(or true true)", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_or_returns_false_if_all_false(self):
        # when
        result = eval_str("(or false false)", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)
