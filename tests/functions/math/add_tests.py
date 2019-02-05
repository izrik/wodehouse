from unittest import TestCase

from functions.eval import eval_str
from functions.math import add
from modules.builtins import create_builtins_module
from wtypes.list import WList
from wtypes.number import WNumber
from wtypes.string import WString


class AddTest(TestCase):

    def test_plus_with_no_args_returns_zero(self):
        # when
        result = add()
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(0, result)
        # when
        result = eval_str("(+)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(0, result)

    def test_plus_adds_numbers(self):
        # when
        result = add(WNumber(1), WNumber(2), WNumber(3), WNumber(4))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)
        # when
        result = eval_str("(+ 1 2 3 4)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(10, result)

    def test_plus_single_number_returns_that_number(self):
        # when
        result = add(WNumber(1))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)
        # when
        result = eval_str("(+ 1)", create_builtins_module())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_plus_concatenates_strings(self):
        # when
        result = add(WString("one"), WString("two"), WString("three"))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("onetwothree", result)
        # when
        result = eval_str("(+ \"one\" \"two\" \"three\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("onetwothree", result)

    def test_plus_single_string_returns_that_string(self):
        # when
        result = add(WString("one"))
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("one", result)
        # when
        result = eval_str("(+ \"one\")",
                          create_builtins_module())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("one", result)

    def test_plus_concatenates_lists(self):
        # when
        result = add(WList(WNumber(1), WNumber(2)),
                     WList(WNumber(3), WNumber(4)))
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 2, 3, 4], result)
        # when
        result = eval_str("(+ '(1 2) '(3 4))", create_builtins_module())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 2, 3, 4], result)

    def test_plus_single_list_returns_that_list(self):
        # when
        result = add(WList(WNumber(1), WNumber(2)))
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 2], result)
        # when
        result = eval_str("(+ '(1 2))", create_builtins_module())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 2], result)
