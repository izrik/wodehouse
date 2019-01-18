from unittest import TestCase

from functions.eval import eval_str
from functions.scope import create_global_scope


class ReadFileTest(TestCase):

    def test_read_file_reads_files(self):
        # when
        result = eval_str("(read_file \"input2.txt\")", create_global_scope())
        # then
        self.assertEqual("( 123 )\n", result)
