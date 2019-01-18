from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.list import WList
from wtypes.number import WNumber


class MiscMacroTest(TestCase):

    def test_call_macro_returns_number(self):
        # when
        result = eval_str("(if true 1 2)", create_global_scope())
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(1, result)

    def test_call_macro_returns_empty_list(self):
        # when
        result = eval_str("(if true '() 2)", create_global_scope())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_call_nested_macro_returns_empty_list(self):
        # when
        result = eval_str("(if true (if true '() 2) 3)",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)
