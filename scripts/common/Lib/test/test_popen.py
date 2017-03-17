# Embedded file name: scripts/common/Lib/test/test_popen.py
"""Basic tests for os.popen()

  Particularly useful for platforms that fake popen.
"""
import unittest
from test import test_support
import os, sys
python = sys.executable

class PopenTest(unittest.TestCase):

    def _do_test_commandline(self, cmdline, expected):
        cmd = '%s -c "import sys;print sys.argv" %s' % (python, cmdline)
        data = os.popen(cmd).read() + '\n'
        got = eval(data)[1:]
        self.assertEqual(got, expected)

    def test_popen(self):
        self.assertRaises(TypeError, os.popen)
        self._do_test_commandline('foo bar', ['foo', 'bar'])
        self._do_test_commandline('foo "spam and eggs" "silly walk"', ['foo', 'spam and eggs', 'silly walk'])
        self._do_test_commandline('foo "a \\"quoted\\" arg" bar', ['foo', 'a "quoted" arg', 'bar'])
        test_support.reap_children()

    def test_return_code(self):
        self.assertEqual(os.popen('exit 0').close(), None)
        if os.name == 'nt':
            self.assertEqual(os.popen('exit 42').close(), 42)
        else:
            self.assertEqual(os.popen('exit 42').close(), 10752)
        return


def test_main():
    test_support.run_unittest(PopenTest)


if __name__ == '__main__':
    test_main()