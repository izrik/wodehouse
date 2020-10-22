import unittest

from modules.sys import w_exit
from wtypes.number import WNumber


class ExitTest(unittest.TestCase):
    def test_normal_exit_wraises_wsystemexit(self):
        from wtypes.control import WRaisedException
        from wtypes.exception import WSystemExit
        # when
        result = w_exit(WNumber(0))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WSystemExit)
        self.assertIsInstance(result.exception.code, WNumber)
        self.assertEqual(result.exception.code, 0)
        self.assertEqual(result.exception.message, 'WSystemExit(0)')

    def test_non_wobject_raises(self):
        # expect
        with self.assertRaises(TypeError) as exc:
            w_exit(0)
        # and
        self.assertEqual(str(exc.exception),
                         'Code must be a WNumber. '
                         'Got "0" (<class \'int\'>) instead.')

    def test_non_wnumber_wraises(self):
        # when
        from wtypes.string import WString
        from wtypes.control import WRaisedException
        from wtypes.exception import WException, WSystemExit
        result = w_exit(WString("zero"))
        # then
        self.assertIsInstance(result, WRaisedException)
        self.assertIsInstance(result.exception, WException)
        self.assertNotIsInstance(result.exception, WSystemExit)
        self.assertEqual(result.exception.message,
                         'Code must be a number. Got ""zero"" (String) '
                         'instead.')  # TODO: fix double-quoting
