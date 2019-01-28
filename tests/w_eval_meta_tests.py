from unittest import TestCase

import functions.eval
from functions.eval import w_eval, eval_str
from functions.read import parse
from functions.scope import create_builtins_module
from wtypes.function import WFunction


class EvalMetaTest(TestCase):

    def test_parses_w_eval(self):
        # given
        source = functions.eval._eval_source
        # when
        result = parse(source)
        # then
        self.assertNotEqual([], result)

    def test_compiles_w_eval(self):
        # given
        eval_source = functions.eval._eval_source
        parsed_eval = parse(eval_source)
        bm = create_builtins_module()
        bm['scope'] = bm
        # when
        compiled_eval = w_eval(parsed_eval, bm)
        # then
        self.assertIsInstance(compiled_eval, WFunction)

    def test_compiled_w_eval_evals_things(self):
        # given
        eval_source = functions.eval._eval_source
        parsed_eval = parse(eval_source)
        bm = create_builtins_module()
        bm['scope'] = bm
        compiled_eval = w_eval(parsed_eval, bm)
        bm['w_eval'] = compiled_eval
        # when
        result = eval_str('(w_eval 2 scope)', bm)
        # then
        self.assertEqual(2, result)
