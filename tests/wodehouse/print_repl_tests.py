import unittest
from unittest.mock import patch

from wodehouse import repl_print
from wtypes.number import WNumber


class PrintReplTest(unittest.TestCase):
    @patch('wodehouse.print')
    def test_print_number(self, _print):
        # when
        result = repl_print(WNumber(123))
        # then
        self.assertEqual(result, WNumber(123))
        # and
        _print.assert_called_once_with(123)

    @patch('wodehouse.print')
    def test_print_string(self, _print):
        # when
        from wtypes.string import WString
        result = repl_print(WString("abc\"'"))
        # then
        self.assertEqual(result, WString("abc\"'"))
        # and
        # TODO: fix double-escaping
        _print.assert_called_once_with("\"abc\\\"'\"")

    @patch('wodehouse.print')
    def test_print_list(self, _print):
        # when
        from wtypes.string import WString
        from wtypes.list import WList
        result = repl_print(WList(WString("a"), WNumber(2)))
        # then
        self.assertEqual(result, WList(WString("a"), WNumber(2)))
        # and
        _print.assert_called_once_with('("a" 2)')

    @patch('wodehouse.print')
    def test_print_other_wobject(self, _print):
        # given
        from wtypes.scope import WScope
        scope = WScope()
        # when
        result = repl_print(scope)
        # then
        self.assertIs(result, scope)
        # and
        _print.assert_called_once_with(scope)
