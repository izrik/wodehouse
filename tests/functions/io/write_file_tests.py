import unittest
from unittest.mock import patch, MagicMock

from functions.io import write_file
from wtypes.number import WNumber
from wtypes.string import WString


class WriteFileTest(unittest.TestCase):
    @patch('functions.io.open')
    def test_write_file_opens_file_and_writes(self, _open):
        # given
        _f = MagicMock()
        _f.write.return_value = 10
        _f.__enter__.return_value = _f
        _open.return_value = _f
        # when
        result = write_file(WString('abc'), WString('1234567890'))
        # then
        self.assertIsInstance(result, WNumber)
        self.assertEqual(result, 10)
        # and
        _open.assert_called_once_with('abc', 'w')
        _f.write.assert_called_once_with('1234567890')
        # and
        _f.__enter__.assert_called_once()
        _f.__exit__.assert_called_once()
