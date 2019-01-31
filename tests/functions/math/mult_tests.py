from unittest import TestCase

from functions.eval import eval_str
from functions.math import mult
from modules.builtins import create_builtins_module
from wtypes.number import WNumber


class MultTest(TestCase):

    def test_mult_with_no_args_returns_one(self):
        # when
        result = mult()
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = eval_str("(*)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_mult_single_number_returns_that_number(self):
        # when
        result = mult(WNumber(5))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(5, result)
        # when
        result = eval_str("(* 5)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(5, result)

    def test_mult_mults_numbers(self):
        # when
        result = mult(WNumber(1), WNumber(2), WNumber(3), WNumber(4))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(24, result)
        # when
        result = eval_str("(* 1 2 3 4)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(24, result)
        # when
        result = mult(WNumber(3), WNumber(2))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(6, result)
        # when
        result = eval_str("(* 3 2)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(6, result)
        # when
        result = mult(WNumber(5), WNumber(2))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)
        # when
        result = eval_str("(* 5 2)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)

    # TODO: negative numbers
