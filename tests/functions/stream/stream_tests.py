from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.stream import WStream


class StreamTest(TestCase):

    def test_stream_creates_stream_object(self):
        # when
        result = eval_str("(stream \"abc\")", create_builtins_module())
        # then
        self.assertIsInstance(result, WStream)
        self.assertEqual("abc", result.s)
