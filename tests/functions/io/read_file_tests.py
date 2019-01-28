from unittest import TestCase

from functions.eval import eval_str
from modules.builtins import create_builtins_module


class ReadFileTest(TestCase):

    def test_read_file_reads_files(self):
        # when
        result = eval_str("(read_file \"input2.txt\")", create_builtins_module())
        # then
        self.assertEqual("( 123 )\n", result)
