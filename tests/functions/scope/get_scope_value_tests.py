from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module


class GetScopeValueTest(TestCase):

    def test_get_gets_value_by_key(self):
        # when
        result = eval_str("(get (new_scope '((a 1) (b 2))) 'a)",
                          create_builtins_module())
        # then
        self.assertEqual(1, result)
        # when
        result = eval_str("(get (new_scope '((a 1) (b 2))) 'b)",
                          create_builtins_module())
        # then
        self.assertEqual(2, result)
