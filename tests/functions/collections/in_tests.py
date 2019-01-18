from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.boolean import WBoolean


class InTest(TestCase):

    def test_in_returns_false_if_item_present(self):
        # when
        result = eval_str("(in 'a '(a))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'a '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'b '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'c '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.true, result)

    def test_in_returns_false_if_item_not_present(self):
        # when
        result = eval_str("(in 'f '(a b c))", create_global_scope())
        # then
        self.assertIs(WBoolean.false, result)
