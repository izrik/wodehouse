from unittest import TestCase

from functions.eval import eval_str
from functions.math import div
from modules.builtins import create_builtins_module
from wtypes.control import WRaisedException
from wtypes.exception import WException
from wtypes.number import WNumber


class DivTest(TestCase):

    def test_div_by_zero_raises_proper_wexception(self):
        # when
        result = eval_str('(/ 1 0)', create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)

    def test_div_with_no_args_returns_one(self):
        # when
        result = div()
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = eval_str("(/)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_div_single_number_returns_that_number(self):
        # when
        result = div(WNumber(5))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(5, result)
        # when
        result = eval_str("(/ 5)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(5, result)

    def test_div_divs_numbers(self):
        # when
        result = div(WNumber(24), WNumber(2), WNumber(3))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(4, result)
        # when
        result = eval_str("(/ 24 2 3)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(4, result)
        # when
        result = div(WNumber(9), WNumber(3))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)
        # when
        result = eval_str("(/ 9 3)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(3, result)

    # TODO: negative numbers
    # TODO: fractional/floating-point numbers
