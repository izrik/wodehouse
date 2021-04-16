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
        # and
        self.assertEqual(s.char, 5)

    def test_triple_regular_string(self):
        # given
        s = WStream('"""abc"""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, 'abc')

    def test_triple_empty_string(self):
        # given
        s = WStream('""""""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '')
        # and
        self.assertEqual(s.char, 7)

    def test_triple_escaped_dquote(self):
        # given
        _p_s = """\""""
        self.assertEqual('"', _p_s)
        _s = '"""\\""""'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '"')
        self.assertEqual(_s[2], '"')
        self.assertEqual(_s[3], '\\')
        self.assertEqual(_s[4], '"')
        self.assertEqual(_s[5], '"')
        self.assertEqual(_s[6], '"')
        self.assertEqual(_s[7], '"')
        self.assertEqual(len(_s), 8)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '"')

    def test_triple_newline_also_included(self):
        # given
        _p_s = """
"""
        self.assertEqual('\n', _p_s)
        _s = '"""\n"""'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '"')
        self.assertEqual(_s[2], '"')
        self.assertEqual(_s[3], '\n')
        self.assertEqual(_s[4], '"')
        self.assertEqual(_s[5], '"')
        self.assertEqual(_s[6], '"')
        self.assertEqual(len(_s), 7)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\n')

    def test_triple_escaped_newline(self):
        # given
        _p_s = """\n"""
        self.assertEqual('\n', _p_s)
        _s = '"""\\n"""'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '"')
        self.assertEqual(_s[2], '"')
        self.assertEqual(_s[3], '\\')
        self.assertEqual(_s[4], 'n')
        self.assertEqual(_s[5], '"')
        self.assertEqual(_s[6], '"')
        self.assertEqual(_s[7], '"')
        self.assertEqual(len(_s), 8)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\n')

    def test_triple_escaped_tab(self):
        # given
        _s = '"""\\t"""'
        self.assertEqual(_s[0], '"')
        self.assertEqual(_s[1], '"')
        self.assertEqual(_s[2], '"')
        self.assertEqual(_s[3], '\\')
        self.assertEqual(_s[4], 't')
        self.assertEqual(_s[5], '"')
        self.assertEqual(_s[6], '"')
        self.assertEqual(_s[7], '"')
        self.assertEqual(len(_s), 8)
        s = WStream(_s)
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, '\t')

    def test_triple_no_closing_delim_raises(self):
        # given
        s = WStream('"""abc')
        result = None
        # expect
        with self.assertRaises(RanOutOfCharactersException) as exc:
            result = read_string(s)
        # and
        self.assertIsNone(result)
        # and
        self.assertEqual(str(exc.exception),
                         'Ran out of characters before string was finished.')
        # and
        self.assertEqual(s.char, 7)

    def test_triple_not_enough_closing_delim_raises_1(self):
        # given
        s = WStream('"""abc"')
        result = None
        # expect
        with self.assertRaises(RanOutOfCharactersException) as exc:
            result = read_string(s)
        # and
        self.assertIsNone(result)
        # and
        self.assertEqual(str(exc.exception),
                         'Ran out of characters before string was finished.')
        # and
        self.assertEqual(s.char, 8)

    def test_triple_not_enough_closing_delim_raises_2(self):
        # given
        s = WStream('"""abc""')
        result = None
        # expect
        with self.assertRaises(RanOutOfCharactersException) as exc:
            result = read_string(s)
        # and
        self.assertIsNone(result)
        # and
        self.assertEqual(str(exc.exception),
                         'Ran out of characters before string was finished.')
        # and
        self.assertEqual(s.char, 9)

    def test_triple_embedded_dquote(self):
        # given
        s = WStream('"""a"b"""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, 'a"b')
        # and
        self.assertEqual(s.char, 10)

    def test_triple_two_embedded_dquotes(self):
        # given
        s = WStream('"""a""b"""')
        # when
        result = read_string(s)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual(result, 'a""b')
        # and
        self.assertEqual(s.char, 11)
