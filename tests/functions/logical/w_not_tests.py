from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.boolean import WBoolean


class NotTest(TestCase):

    def test_not_inverts_true_to_false(self):
        # when
        result = eval_str("(not true)", create_builtins_module())
        # then
        self.assertIs(WBoolean.false, result)

    def test_not_inverts_false_to_true(self):
        # when
        result = eval_str("(not false)", create_builtins_module())
        # then
        self.assertIs(WBoolean.true, result)
