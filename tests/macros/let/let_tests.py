from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.number import WNumber


class LetTest(TestCase):

    def test_let_assigns_values_sequentially(self):
        # given
        bm = create_builtins_module()
        bm['x'] = WNumber(1)
        bm['y'] = WNumber(2)
        # when
        result = eval_str("(let (x 3) (y x) y)", bm)
        # then y is bound to the value of x after x is bound to 3
        self.assertEqual(3, result)
