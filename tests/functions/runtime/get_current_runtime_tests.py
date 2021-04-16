import unittest

from functions.runtime import GetCurrentRuntime
from runtime import Runtime
from wtypes.list import WList


class GetCurrentRuntimeTest(unittest.TestCase):
    def test_gets_current_runtime(self):
        # given
        rt = Runtime(WList())
        gcr = GetCurrentRuntime(rt, None)
        # when
        result = gcr.call_magic_function()
        # then
        self.assertIs(result, rt)

    def test_is_created_by_the_runtime(self):
        # given
        rt = Runtime(WList())
        gcr = rt.builtins_module['get_current_runtime']
        # when
        result = gcr.call_magic_function()
        # then
        self.assertIs(result, rt)

    def test_if_no_runtime_not_created_by_builtins_module(self):
        from modules.builtins import create_builtins_module
        # when
        bm = create_builtins_module()
        # then
        self.assertNotIn('get_current_runtime', bm)
