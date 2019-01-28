from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module
from wtypes.control import WRaisedException
from wtypes.exception import WException


class DivTest(TestCase):

    def test_div_by_zero_raises_proper_wexception(self):
        # when
        result = eval_str('(/ 1 0)', create_builtins_module())
        # then
        self.assertIsNotNone(result)
        self.assertIsInstance(result, WRaisedException)
        self.assertIsNotNone(result.exception)
        self.assertIsInstance(result.exception, WException)
