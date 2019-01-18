from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.number import WNumber


class LetTest(TestCase):

    def test_let_assigns_values_sequentially(self):
        # given
        gs = create_global_scope()
        gs['x'] = WNumber(1)
        gs['y'] = WNumber(2)
        # when
        result = eval_str("(let (x 3) (y x) y)", gs)
        # then y is bound to the value of x after x is bound to 3
        self.assertEqual(3, result)
