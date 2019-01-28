from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.scope import WScope


class NewScopeWithinTest(TestCase):

    def test_new_scope_within_create_scope_object_with_enclosing_scope(self):
        # given
        p = WScope({'a': 3, 'b': 4, 'c': 5})
        bm = create_builtins_module()
        bm['p'] = p
        # when
        result = eval_str("(new_scope_within p '((a 1) (b 2)))", bm)
        # then
        self.assertIsInstance(result, WScope)
        self.assertEqual(3, len(result))
        self.assertIn('a', result)
        self.assertEqual(1, result['a'])
        self.assertIn('b', result)
        self.assertEqual(2, result['b'])
        self.assertIn('c', result)
        self.assertNotIn('c', result.dict.keys())
        self.assertIn('c', result.enclosing_scope)
        self.assertEqual(5, result.enclosing_scope['c'])
        # expect
        p2 = result
        self.assertEqual(1, eval_str("a", p2))
        self.assertEqual(2, eval_str("b", p2))
        self.assertEqual(5, eval_str("c", p2))
