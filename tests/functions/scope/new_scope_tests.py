from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.scope import WScope


class NewScopeTest(TestCase):

    def test_new_scope_creates_scope_object(self):
        # when
        result = eval_str("(new_scope)", create_builtins_module())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(0, len(result))

    def test_new_scope_with_empty_list_for_args_creates_scope_object(self):
        # when
        result = eval_str("(new_scope '())", create_builtins_module())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(0, len(result))

    def test_new_scope_args_become_keys_and_values(self):
        # when
        result = eval_str("(new_scope '((a 1) (b 2)))", create_builtins_module())
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(2, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])
