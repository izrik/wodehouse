from unittest import TestCase
from unittest.mock import Mock

from functions.eval import eval_str
from functions.io import w_print
from functions.scope import create_global_scope
from wtypes.list import WList
from wtypes.magic_function import WMagicFunction


class PrintTest(TestCase):

    def test_print_function(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        self.assertEqual("Hello, world!", result)

    def test_prints_integer(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print 123)', scope)
        # then
        printer.assert_called_once_with(123)
        self.assertEqual(123, result)

    def test_prints_string(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(
            lambda x: w_print(x, printer=printer),
            enclosing_scope=scope)
        # when
        result = eval_str('(print "Hello, world!")', scope)
        # then
        printer.assert_called_once_with('Hello, world!')
        self.assertEqual('Hello, world!', result)

    def test_prints_escaped_chars_correctly(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print "newline\\ncreturn\\rtab\\t")', scope)
        # then
        printer.assert_called_once_with('newline\ncreturn\rtab\t')
        self.assertEqual('newline\ncreturn\rtab\t', result)

    def test_prints_empty_list(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote ()))', scope)
        # then
        printer.assert_called_once_with([])
        printer.assert_called_once_with(WList())
        self.assertEqual(result, [])
        self.assertEqual(result, WList())

    def test_prints_list(self):
        # given
        printer = Mock()
        scope = create_global_scope()
        scope['print'] = WMagicFunction(lambda x: w_print(x, printer=printer),
                                        enclosing_scope=scope)
        # when
        result = eval_str('(print (quote (1 2 "three")))', scope)
        # then
        printer.assert_called_once_with([1, 2, "three"])
        self.assertEqual(result, [1, 2, "three"])
