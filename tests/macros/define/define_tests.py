from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_module_scope, create_global_scope
from wtypes.number import WNumber
from wtypes.string import WString
from wtypes.symbol import WSymbol


class DefineTest(TestCase):

    def test_define_in_module_adds_to_module_scope(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(global_scope=gs)
        # when
        result = eval_str("(define x 3)", scope)
        # then
        self.assertEqual(3, result)
        self.assertIn(WSymbol.get('x'), scope)
        self.assertEqual(WNumber(3), scope['x'])

    def test_define_with_undefined_symbol_raises(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(global_scope=gs)
        # expect
        self.assertRaisesRegex(
            Exception,
            "No object found by the name of \"\"y\"\"",
            eval_str,
            "(define x y)", scope)

    def test_define_with_defined_symbol_returned_value(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(global_scope=gs)
        scope['y'] = WString("abc")
        # when
        result = eval_str("(define x y)", scope)
        # then
        self.assertEqual('abc', result)
        self.assertIn(WSymbol.get('x'), scope)
        self.assertEqual('abc', scope['x'])

    def test_define_with_quoted_symbol(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(global_scope=gs)
        # when
        result = eval_str("(define x 'y)", scope)
        # then
        self.assertEqual(WSymbol.get('y'), result)
        self.assertIn(WSymbol.get('x'), scope)
        self.assertEqual(WSymbol.get('y'), scope['x'])

    def test_define_with_doubly_quoted_symbol(self):
        # given
        gs = create_global_scope()
        scope = create_module_scope(global_scope=gs)
        # when
        result = eval_str("(define x ''y)", scope)
        # then
        expected = [WSymbol.get('quote'), WSymbol.get('y')]
        self.assertEqual(expected, result)
        self.assertIn(WSymbol.get('x'), scope)
        self.assertEqual(expected, scope['x'])
