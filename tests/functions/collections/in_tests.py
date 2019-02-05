from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.boolean import WBoolean


class InTest(TestCase):

    def test_in_returns_false_if_item_present(self):
        # when
        result = eval_str("(in 'a '(a))", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'a '(a b c))", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'b '(a b c))", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
        # when
        result = eval_str("(in 'c '(a b c))", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)

    def test_in_returns_false_if_item_not_present(self):
        # when
        result = eval_str("(in 'f '(a b c))", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)
