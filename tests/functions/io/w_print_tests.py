from unittest import TestCase
from unittest.mock import Mock

from functions.eval import eval_str
from functions.io import w_print
from modules.builtins import create_builtins_module
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction


class PrintTest(TestCase):

    def test_print_function(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        self.assertEqual("Hello, world!", result)

    def test_prints_integer(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print 123)', scope)
        # then
        printer.assert_called_once_with(123, end=None)
        self.assertEqual(123, result)

    def test_prints_string(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(
            lambda x: w_print(x, printer=printer),
            enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        printer.assert_called_once_with('Hello, world!', end=None)
        self.assertEqual('Hello, world!', result)

    def test_prints_escaped_chars_correctly(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "newline\\ncreturn\\rtab\\t")', scope)
        # then
        printer.assert_called_once_with('newline\ncreturn\rtab\t', end=None)
        self.assertEqual('newline\ncreturn\rtab\t', result)

    def test_prints_empty_list(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote ()))', scope)
        # then
        printer.assert_called_once_with([], end=None)
        printer.assert_called_once_with(WList(), end=None)
        self.assertEqual(result, [])
        self.assertEqual(result, WList())

    def test_prints_list(self):
        # given
        printer = Mock()
        scope = create_builtins_module()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote (1 2 "three")))', scope)
        # then
        printer.assert_called_once_with([1, 2, "three"], end=None)
        self.assertEqual(result, [1, 2, "three"])

    def test_prints_end_param(self):
        # given
        printer = Mock()
        scope = create_builtins_module()

        def print2(x, _end=None):
            return w_print(x, end=_end, printer=printer)

        scope['print'] = WMagicFunction(print2, enclosing_scope=scope,
                                        check_args=False)
        # when
        result = eval_str('(print 123 ",")', scope)
        # then
        printer.assert_called_once_with(123, end=',')
        self.assertEqual(123, result)
