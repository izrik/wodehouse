from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module


class IfTest(TestCase):

    def test_if_condition_is_true_returns_first_retval(self):
        # when
        result = eval_str("(if (< 2 3) 4 5)",
                          create_builtins_module())
        # then
        self.assertEqual(4, result)

    def test_if_condition_is_false_returns_second_retval(self):
        # when
        result = eval_str("(if (> 2 3) 4 5)",
                          create_builtins_module())
        # then
        self.assertEqual(5, result)
