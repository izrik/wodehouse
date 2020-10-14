import unittest
from unittest.mock import patch

from runtime import Runtime
from wodehouse import repl


class ReplTest(unittest.TestCase):
    @patch('wodehouse.input')
    @patch('wodehouse.print')
    def test_ctrl_d_exits(self, _print, _input):
        # given
        rt = Runtime(['program'])
        _input.side_effect = EOFError
        # when
        repl(rt)
        # then
        _print.call_arg_list == [
            ('Wodehouse 0.1',),
            ('Copyright © 2014-2019 izrik',),
            ('Type "quit" or "exit" to quit.',),
            ('',),
        ]
        _input.assert_called_once_with('>>> ')

    @patch('wodehouse.input')
    @patch('wodehouse.print')
    def test_exit_exits(self, _print, _input):
        # given
        rt = Runtime(['program'])
        _input.return_value = 'exit'
        # when
        repl(rt)
        # then
        _print.call_arg_list == [
            ('Wodehouse 0.1',),
            ('Copyright © 2014-2019 izrik',),
            ('Type "quit" or "exit" to quit.',),
            ('',),
        ]
        _input.assert_called_once_with('>>> ')

    @patch('wodehouse.input')
    @patch('wodehouse.print')
    def test_quit_exits(self, _print, _input):
        # given
        rt = Runtime(['program'])
        _input.return_value = 'quit'
        # when
        repl(rt)
        # then
        _print.call_arg_list == [
            ('Wodehouse 0.1',),
            ('Copyright © 2014-2019 izrik',),
            ('Type "quit" or "exit" to quit.',),
            ('',),
        ]
        _input.assert_called_once_with('>>> ')
