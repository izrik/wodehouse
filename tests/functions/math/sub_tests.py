from unittest import TestCase

from functions.eval import eval_str
from functions.math import sub
from modules.builtins import create_builtins_module
from wtypes.number import WNumber


class SubTest(TestCase):

    def test_sub_with_no_args_returns_zero(self):
        # when
        result = sub()
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(0, result)
        # when
        result = eval_str("(-)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(0, result)

    def test_sub_single_number_returns_that_number(self):
        # when
        result = sub(WNumber(1))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = eval_str("(- 1)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_sub_subs_numbers(self):
        # when
        result = sub(WNumber(1), WNumber(2), WNumber(3), WNumber(4))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(-8, result)
        # when
        result = eval_str("(- 1 2 3 4)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(-8, result)
        # when
        result = sub(WNumber(3), WNumber(2))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = eval_str("(- 3 2)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = sub(WNumber(5), WNumber(1), WNumber(1))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)
        # when
        result = eval_str("(- 5 1 1)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)
