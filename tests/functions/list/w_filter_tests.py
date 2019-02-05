from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.list import WList


class FilterTest(TestCase):
    def test_empty_list_condition_always_false_yields_empty_list(self):
        # when
        result = eval_str("(filter (lambda (x) false) '())",
                          create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_empty_list_condition_always_true_yields_empty_list(self):
        # when
        result = eval_str("(filter (lambda (x) true) '())",
                          create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_non_empty_list_condition_always_false_yields_empty_list(self):
        # when
        result = eval_str("(filter (lambda (x) false) '(1 2 3))",
                          create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([], result)

    def test_non_empty_list_condition_always_true_yields_all_items(self):
        # when
        result = eval_str("(filter (lambda (x) true) '(1 2 3))",
                          create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 2, 3], result)

    def test_non_empty_list_varying_condition_yields_only_matching(self):
        # when
        result = eval_str(
            "(filter (lambda (x) (in x '(2 4 6 8))) '(1 2 3 4 5))",
            create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([2, 4], result)
        # when
        result = eval_str(
            "(filter (lambda (x) (not (in x '(2 4 6 8)))) '(1 2 3 4 5))",
            create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WList)
        self.assertEqual([1, 3, 5], result)
