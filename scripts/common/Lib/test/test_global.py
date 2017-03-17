# Embedded file name: scripts/common/Lib/test/test_global.py
"""Verify that warnings are issued for global statements following use."""
from test.test_support import run_unittest, check_syntax_error
import unittest
import warnings

class GlobalTests(unittest.TestCase):

    def test1(self):
        prog_text_1 = 'def wrong1():\n    a = 1\n    b = 2\n    global a\n    global b\n'
        check_syntax_error(self, prog_text_1)

    def test2(self):
        prog_text_2 = 'def wrong2():\n    print x\n    global x\n'
        check_syntax_error(self, prog_text_2)

    def test3(self):
        prog_text_3 = 'def wrong3():\n    print x\n    x = 2\n    global x\n'
        check_syntax_error(self, prog_text_3)

    def test4(self):
        prog_text_4 = 'global x\nx = 2\n'
        compile(prog_text_4, '<test string>', 'exec')


def test_main():
    with warnings.catch_warnings():
        warnings.filterwarnings('error', module='<test string>')
        run_unittest(GlobalTests)


if __name__ == '__main__':
    test_main()