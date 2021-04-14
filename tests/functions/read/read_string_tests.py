from unittest import TestCase

from functions.read import read_string, RanOutOfCharactersException
from wtypes.stream import WStream
from wtypes.string import WString


class ReadStringTest(TestCase):
    def test_regular_string(self):
        # given
        s = WStream('"abc"')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, 'abc')

    def test_empty_string(self):
        # given
        s = WStream('""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '')
        # and
        self.assertEqual(s.char, 3)

    def test_escaped_dquote(self):
        # given
        _s = '"\\""'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '\\')
        self.assertEqual(_s[2], '"')
        self.assertEqual(_s[3], '"')
        self.assertEqual(len(_s), 4)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '"')

    def test_newline_also_included(self):
        # given
        _s = '"\n"'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '\n')
        self.assertEqual(_s[2], '"')
        self.assertEqual(len(_s), 3)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\n')

    def test_escaped_newline(self):
        # given
        _s = '"\\n"'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '\\')
        self.assertEqual(_s[2], 'n')
        self.assertEqual(_s[3], '"')
        self.assertEqual(len(_s), 4)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\n')

    def test_escaped_tab(self):
        # given
        _s = '"\\t"'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '\\')
        self.assertEqual(_s[2], 't')
        self.assertEqual(_s[3], '"')
        self.assertEqual(len(_s), 4)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\t')

    def test_no_closing_dquote_raises(self):
        # given
        s = WStream('"abc')
        result = None
        # expect
        with self.assertRaises(RanOutOfCharactersException) as exc:
            result = read_string(s)
        # and
        self.assertIsNone(result)
        # and
        self.assertEqual(str(exc.exception),
                         'Ran out of characters before string was finished.')

    def test_parsing_stops_before_triple_dquote(self):
        # given
        s = WStream('"""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '')
        # and
        self.assertEqual(s.char, 3)  # same as test_empty_string
