from unittest import TestCase

from functions.apply import w_apply
from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.control import WEvalRequired
from wtypes.list import WList
from wtypes.symbol import WSymbol


class ApplyTest(TestCase):
    def test_applies_function_to_arguments(self):
        # given
        bm = create_builtins_module()
        func = bm['+']
        args = WList(WList(WSymbol.get('a')),
                     WList(WSymbol.get('b')),
                     WList(WSymbol.get('c')))
        # when
        result = w_apply(func, args)
        # then
        self.assertIsInstance(result, WEvalRequired)

    def test_eval_applies_function_to_arguments(self):
        # when
        result = eval_str("""(apply + (map list '("a" "b" "c")))""",
                          create_builtins_module())
        # then
        self.assertEqual(['a', 'b', 'c'], result)
