from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope
from wtypes.boolean import WBoolean
from wtypes.stream import WStream
from wtypes.string import WString


class GetNextCharTest(TestCase):

    def test_get_next_char_gets_next_char(self):
        # when
        result = eval_str("(get_next_char (stream \"abc\"))",
                          create_global_scope())
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual("a", result)

    def test_get_next_char_advances_position(self):
        # given
        s = WStream("abc")
        scope = create_global_scope()
        scope['s'] = s
        # precondition
        self.assertEqual(eval_str("(get_next_char s)", scope), "a")
        # expect
        self.assertEqual(eval_str("(get_next_char s)", scope), "b")
        self.assertEqual(eval_str("(get_next_char s)", scope), "c")
        # then
        self.assertIs(WBoolean.false, eval_str("(has_chars s)", scope))

    def test_get_next_char_after_end_of_stream_raises(self):
        # expect
        self.assertRaisesRegex(
            Exception,
            "No more characters in the stream.",
            eval_str,
            "(get_next_char (stream \"\"))", create_global_scope())
