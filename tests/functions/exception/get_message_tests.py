from unittest import TestCase

from functions.exception import get_message
from wtypes.exception import WException
from wtypes.string import WString


class GetMessageTest(TestCase):
    def test_gets_message_from_exception(self):
        # given
        e = WException('I am going to my room!')
        # when
        result = get_message(e)
        # then
        self.assertIsInstance(result, WString)
        self.assertEqual('I am going to my room!', result)

    def test_non_exception_raises_w_exception(self):
        from wtypes.list import WList
        from wtypes.control import WRaisedException
        # when
        result = get_message(WList())
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertEqual('Argument to get_message must be an exception. '
                         'Got "()" (List) instead.',
                         result.exception.message)

    def test_non_wobject_raises_py_exception(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            get_message([])
        # then
        self.assertEqual('Argument to get_message must be a WObject. '
                         'Got "[]" (<class \'list\'>) instead.',
                         str(exc.exception))
