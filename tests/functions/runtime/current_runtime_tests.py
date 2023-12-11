import unittest

from functions.runtime import GetCurrentRuntime
from runtime import Runtime
from wtypes.list import WList


class CurrentRuntimeTest(unittest.TestCase):

    def test_is_created_by_the_runtime(self):
        # given
        rt = Runtime(WList())
        # when
        result = rt.builtins_module['__current_runtime__']
        # then
        self.assertIs(result, rt)

    def test_if_no_runtime_not_created_by_builtins_module(self):
        from modules.builtins import create_builtins_module
        # when
        bm = create_builtins_module()
        # then
        self.assertNotIn('__current_runtime__', bm)
