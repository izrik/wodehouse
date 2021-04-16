import unittest
from unittest.mock import Mock, ANY

from runtime import Runtime
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction
from wtypes.module import WModule


class EmitTest(unittest.TestCase):
    def test_exprs_are_emitted(self):
        from wtypes.number import WNumber
        # given
        rt = Runtime(WList())
        scope = WModule(builtins_module=rt.builtins_module, name='__main__')
        f = Mock()
        ff = WMagicFunction(f, None, name='f')
        rt.add_emit_listener(ff)
        expr = WNumber(123)
        # when
        result = rt.eval(expr, scope)
        # then
        self.assertIs(result, expr)
        # and
        f.assert_called_once_with(expr, ANY, ANY)
