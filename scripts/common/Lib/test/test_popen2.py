# Embedded file name: scripts/common/Lib/test/test_popen2.py
"""Test script for popen2.py"""
import warnings
warnings.filterwarnings('ignore', '.*popen2 module is deprecated.*', DeprecationWarning)
warnings.filterwarnings('ignore', 'os\\.popen. is deprecated.*', DeprecationWarning)
import os
import sys
import unittest
import popen2
from test.test_support import run_unittest, reap_children
if sys.platform[:4] == 'beos' or sys.platform[:6] == 'atheos':
    raise unittest.SkipTest("popen2() doesn't work on " + sys.platform)
try:
    from os import popen
    del popen
except ImportError:
    from os import fork
    del fork

class Popen2Test(unittest.TestCase):
    cmd = 'cat'
    if os.name == 'nt':
        cmd = 'more'
    teststr = 'ab cd\n'
    expected = teststr.strip()

    def setUp(self):
        popen2._cleanup()
        self.assertFalse(popen2._active, 'Active pipes when test starts' + repr([ c.cmd for c in popen2._active ]))

    def tearDown(self):
        for inst in popen2._active:
            inst.wait()

        popen2._cleanup()
        self.assertFalse(popen2._active, 'popen2._active not empty')
        import subprocess
        for inst in subprocess._active:
            inst.wait()

        subprocess._cleanup()
        self.assertFalse(subprocess._active, 'subprocess._active not empty')
        reap_children()

    def validate_output(self, teststr, expected_out, r, w, e = None):
        w.write(teststr)
        w.close()
        got = r.read()
        self.assertEqual(expected_out, got.strip(), 'wrote %r read %r' % (teststr, got))
        if e is not None:
            got = e.read()
            self.assertFalse(got, 'unexpected %r on stderr' % got)
        return

    def test_popen2(self):
        r, w = popen2.popen2(self.cmd)
        self.validate_output(self.teststr, self.expected, r, w)

    def test_popen3(self):
        if os.name == 'posix':
            r, w, e = popen2.popen3([self.cmd])
            self.validate_output(self.teststr, self.expected, r, w, e)
        r, w, e = popen2.popen3(self.cmd)
        self.validate_output(self.teststr, self.expected, r, w, e)

    def test_os_popen2(self):
        if os.name == 'posix':
            w, r = os.popen2([self.cmd])
            self.validate_output(self.teststr, self.expected, r, w)
            w, r = os.popen2(['echo', self.teststr])
            got = r.read()
            self.assertEqual(got, self.teststr + '\n')
        w, r = os.popen2(self.cmd)
        self.validate_output(self.teststr, self.expected, r, w)

    def test_os_popen3(self):
        if os.name == 'posix':
            w, r, e = os.popen3([self.cmd])
            self.validate_output(self.teststr, self.expected, r, w, e)
            w, r, e = os.popen3(['echo', self.teststr])
            got = r.read()
            self.assertEqual(got, self.teststr + '\n')
            got = e.read()
            self.assertFalse(got, 'unexpected %r on stderr' % got)
        w, r, e = os.popen3(self.cmd)
        self.validate_output(self.teststr, self.expected, r, w, e)

    def test_os_popen4(self):
        if os.name == 'posix':
            w, r = os.popen4([self.cmd])
            self.validate_output(self.teststr, self.expected, r, w)
            w, r = os.popen4(['echo', self.teststr])
            got = r.read()
            self.assertEqual(got, self.teststr + '\n')
        w, r = os.popen4(self.cmd)
        self.validate_output(self.teststr, self.expected, r, w)


def test_main():
    run_unittest(Popen2Test)


if __name__ == '__main__':
    test_main()