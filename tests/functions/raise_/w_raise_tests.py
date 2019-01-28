from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_builtins_module
from wtypes.control import WRaisedException
from wtypes.exception import WException


class RaiseTest(TestCase):

    def test_raise_raises(self):
        # when
        result = eval_str("(raise \"this is the description\")",
                          create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual('this is the description',
                         result.exception.message)
