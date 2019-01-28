from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.magic_function import WMagicFunction
from wtypes.symbol import WSymbol


class CondTest(TestCase):

    def test_cond_no_conditions_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "No condition evaluated to true.",
            eval_str,
            "(cond)", create_builtins_module())

    def test_cond_condition_is_true_returns_corresponding_retval(self):
        # when
        result = eval_str("(cond (true 'a))", create_builtins_module())
        # then
        self.assertEqual(WSymbol.get('a'), result)

    def test_cond_condition_is_false_moves_to_next_condition(self):
        # when
        result = eval_str("(cond (false 'a) (true 'b))",
                          create_builtins_module())
        # then
        self.assertEqual(WSymbol.get('b'), result)

    def test_cond_condition_is_true_evaluates_true_side(self):
        evaled = False

        def f():
            nonlocal evaled
            evaled = True
            return WSymbol.get('f')

        scope = create_builtins_module()
        scope['f'] = WMagicFunction(f, scope)

        # when
        result = eval_str("(cond (true (f)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f'), result)
        self.assertTrue(evaled)

    def test_cond_condition_is_false_does_not_evaluate_prior_retvals(self):
        evaled1 = False
        evaled2 = False

        def f1():
            nonlocal evaled1
            evaled1 = True
            return WSymbol.get('f1')

        def f2():
            nonlocal evaled2
            evaled2 = True
            return WSymbol.get('f2')

        scope = create_builtins_module()
        scope['f1'] = WMagicFunction(f1, scope)
        scope['f2'] = WMagicFunction(f2, scope)

        # when
        result = eval_str("(cond (false (f1)) (true (f2)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f2'), result)
        self.assertFalse(evaled1)
        self.assertTrue(evaled2)

    def test_cond_condition_is_true_does_not_evaluate_later_retvals(self):
        evaled1 = False
        evaled2 = False

        def f1():
            nonlocal evaled1
            evaled1 = True
            return WSymbol.get('f1')

        def f2():
            nonlocal evaled2
            evaled2 = True
            return WSymbol.get('f2')

        scope = create_builtins_module()
        scope['f1'] = WMagicFunction(f1, scope)
        scope['f2'] = WMagicFunction(f2, scope)

        # when
        result = eval_str("(cond (true (f1)) (false (f2)))",
                          scope)
        # then
        self.assertEqual(WSymbol.get('f1'), result)
        self.assertTrue(evaled1)
        self.assertFalse(evaled2)

    # TODO: test cond with various levels of quoting
