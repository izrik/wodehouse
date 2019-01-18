from unittest import TestCase

from functions.exec_src import w_exec_src
from wtypes.scope import WScope


class ExecSrcTest(TestCase):

    def test_w_exec_src_execs_src_and_returns_ms(self):
        # given
        gs = WScope()
        # when
        result = w_exec_src(src="", filename="<test>", global_scope=gs)
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WScope)
        self.assertEqual(4, len(result))
        self.assertIn('__module__', result)
        self.assertIs(result, result['__module__'])
        self.assertIn('__global__', result)
        self.assertIs(gs, result['__global__'])
        self.assertIn('__name__', result)
        self.assertEqual("<test>", result['__name__'])
        self.assertIn('__file__', result)
        self.assertEqual("<test>", result['__file__'])
