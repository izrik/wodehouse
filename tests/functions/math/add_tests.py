from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.number import WNumber
from wtypes.string import WString


class AddTest(TestCase):

    def test_plus_adds_numbers(self):
        # when
        result = eval_str("(+ 1 2 3 4)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)

    def test_plus_concatenates_strings(self):
        # when
        result = eval_str("(+ \"one\" \"two\" \"three\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("onetwothree", result)

    def test_plus_interprets_single_list_arg_as_varargs(self):
        # when
        result = eval_str("(+ (list 1 2 3 4))", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)
