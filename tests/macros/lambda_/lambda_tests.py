from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.function import WFunction
from wtypes.magic_function import WMagicFunction
from wtypes.symbol import WSymbol


class LambdaTest(TestCase):
    def test_lambda_creates_wfunction(self):
        # when
        result = eval_str("(lambda (x) 123)", create_global_scope())
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_parameters)
        self.assertEqual([WSymbol.get('x')], result.parameters)
        self.assertEqual(123, result.expr)

    def test_lambda_encloses_values(self):
        # given
        scope = create_global_scope()
        # when
        result = eval_str("(lambda (x) (* x x))", scope)
        # then
        self.assertIsInstance(result, WFunction)
        self.assertNotIsInstance(result, WMagicFunction)
        self.assertEqual(1, result.num_parameters)
        self.assertEqual([WSymbol.get('x')], result.parameters)
        times = WSymbol.get('*')
        x = WSymbol.get('x')
        self.assertEqual([times, x, x], result.expr)

    def test_wfunction_can_be_called(self):
        # when
        result = eval_str("((lambda (x) (* x x)) 4)", create_global_scope())
        # then
        self.assertEqual(16, result)

    def test_wfunctions_can_be_used_in_the_scope(self):
        # given
        scope = create_global_scope()
        scope['sqr'] = eval_str("(lambda (x) (* x x))", scope)
        # expect
        self.assertEqual(25, eval_str("(sqr 5)", scope))
        self.assertEqual(81, eval_str("(sqr 9)", scope))
