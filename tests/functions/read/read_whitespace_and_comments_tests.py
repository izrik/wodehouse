from unittest import TestCase

from functions.read import read_whitespace_and_comments
from wtypes.position import Position
from wtypes.stream import WStream


class ReadWhitespaceAndCommentsTest(TestCase):
    def test_nothing(self):
        self.assertTrue(True)

    def test_reads_whitespace(self):
        # given
        s = WStream('   123')
        # when
        read_whitespace_and_comments(s)
        # then
        self.assertEqual('1', s.peek())
        self.assertEqual(Position(None, 1, 4, s), s.get_position())

    def test_reads_whitespace_through_end_of_stream(self):
        # given
        s = WStream('   ')
        # when
        read_whitespace_and_comments(s)
        # then
        self.assertIsNone(s.peek())
        self.assertFalse(s.has_chars())
        self.assertEqual(Position(None, 1, 4, s), s.get_position())

    def test_reads_interleaved_comment(self):
        # given
        s = WStream('   # abc \n 123')
        # when
        read_whitespace_and_comments(s)
        # then
        self.assertEqual('1', s.peek())
        self.assertEqual(Position(None, 2, 2, s), s.get_position())

    def test_reads_comment_through_end_of_stream(self):
        # given
        s = WStream('   # abc')
        # when
        read_whitespace_and_comments(s)
        # then
        self.assertIsNone(s.peek())
        self.assertFalse(s.has_chars())
        self.assertEqual(Position(None, 1, 9, s), s.get_position())
