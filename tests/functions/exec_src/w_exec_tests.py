from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.magic_function import WMagicFunction
from wtypes.number import WNumber


class ExecTest(TestCase):

    def test_exec_execs_things(self):
        i = [0]

        def side_effect():
            i[0] += 1
            return WNumber(-1)

        scope = create_builtins_module()
        scope['side_effect'] = WMagicFunction(side_effect,
                                              enclosing_scope=scope)
        # when
        eval_str("(exec (side_effect) (side_effect))", scope)
        # then
        self.assertEqual(2, i[0])

    def test_exec_returns_the_last_expr(self):
        # when
        result = eval_str("(exec 2 3 5 7 11)", create_builtins_module())
        # then
        self.assertEqual(11, result)
