# Embedded file name: scripts/common/Lib/test/test_largefile.py
"""Test largefile support on system where this makes sense.
"""
from __future__ import print_function
import os
import stat
import sys
import unittest
from test.test_support import run_unittest, TESTFN, verbose, requires, unlink
import io
import _pyio as pyio
try:
    import signal
    oldhandler = signal.signal(signal.SIGXFSZ, signal.SIG_IGN)
except (ImportError, AttributeError):
    pass

size = 2500000000L

class LargeFileTest(unittest.TestCase):
    """Test that each file function works as expected for a large
    (i.e. > 2GB, do  we have to check > 4GB) files.
    
    NOTE: the order of execution of the test methods is important! test_seek
    must run first to create the test file. File cleanup must also be handled
    outside the test instances because of this.
    
    """

    def test_seek(self):
        if verbose:
            print('create large file via seek (may be sparse file) ...')
        with self.open(TESTFN, 'wb') as f:
            f.write('z')
            f.seek(0)
            f.seek(size)
            f.write('a')
            f.flush()
            if verbose:
                print('check file size with os.fstat')
            self.assertEqual(os.fstat(f.fileno())[stat.ST_SIZE], size + 1)

    def test_osstat(self):
        if verbose:
            print('check file size with os.stat')
        self.assertEqual(os.stat(TESTFN)[stat.ST_SIZE], size + 1)

    def test_seek_read(self):
        if verbose:
            print('play around with seek() and read() with the built largefile')
        with self.open(TESTFN, 'rb') as f:
            self.assertEqual(f.tell(), 0)
            self.assertEqual(f.read(1), 'z')
            self.assertEqual(f.tell(), 1)
            f.seek(0)
            self.assertEqual(f.tell(), 0)
            f.seek(0, 0)
            self.assertEqual(f.tell(), 0)
            f.seek(42)
            self.assertEqual(f.tell(), 42)
            f.seek(42, 0)
            self.assertEqual(f.tell(), 42)
            f.seek(42, 1)
            self.assertEqual(f.tell(), 84)
            f.seek(0, 1)
            self.assertEqual(f.tell(), 84)
            f.seek(0, 2)
            self.assertEqual(f.tell(), size + 1 + 0)
            f.seek(-10, 2)
            self.assertEqual(f.tell(), size + 1 - 10)
            f.seek(-size - 1, 2)
            self.assertEqual(f.tell(), 0)
            f.seek(size)
            self.assertEqual(f.tell(), size)
            self.assertEqual(f.read(1), 'a')
            f.seek(-size - 1, 1)
            self.assertEqual(f.read(1), 'z')
            self.assertEqual(f.tell(), 1)

    def test_lseek(self):
        if verbose:
            print('play around with os.lseek() with the built largefile')
        with self.open(TESTFN, 'rb') as f:
            self.assertEqual(os.lseek(f.fileno(), 0, 0), 0)
            self.assertEqual(os.lseek(f.fileno(), 42, 0), 42)
            self.assertEqual(os.lseek(f.fileno(), 42, 1), 84)
            self.assertEqual(os.lseek(f.fileno(), 0, 1), 84)
            self.assertEqual(os.lseek(f.fileno(), 0, 2), size + 1 + 0)
            self.assertEqual(os.lseek(f.fileno(), -10, 2), size + 1 - 10)
            self.assertEqual(os.lseek(f.fileno(), -size - 1, 2), 0)
            self.assertEqual(os.lseek(f.fileno(), size, 0), size)
            self.assertEqual(f.read(1), 'a')

    def test_truncate(self):
        if verbose:
            print('try truncate')
        with self.open(TESTFN, 'r+b') as f:
            if not hasattr(f, 'truncate'):
                raise unittest.SkipTest('open().truncate() not available on this system')
            f.seek(0, 2)
            self.assertEqual(f.tell(), size + 1)
            newsize = size - 10
            f.seek(newsize)
            f.truncate()
            self.assertEqual(f.tell(), newsize)
            f.seek(0, 2)
            self.assertEqual(f.tell(), newsize)
            newsize -= 1
            f.seek(42)
            f.truncate(newsize)
            if self.new_io:
                self.assertEqual(f.tell(), 42)
            f.seek(0, 2)
            self.assertEqual(f.tell(), newsize)
            f.seek(0)
            f.truncate(1)
            if self.new_io:
                self.assertEqual(f.tell(), 0)
            f.seek(0)
            self.assertEqual(len(f.read()), 1)

    def test_seekable(self):
        if not self.new_io:
            self.skipTest("builtin file doesn't have seekable()")
        for pos in (2147483647L, 2147483648L, 2147483649L):
            with self.open(TESTFN, 'rb') as f:
                f.seek(pos)
                self.assertTrue(f.seekable())


def test_main():
    if sys.platform[:3] == 'win' or sys.platform == 'darwin':
        requires('largefile', 'test requires %s bytes and a long time to run' % str(size))
    else:
        f = open(TESTFN, 'wb', buffering=0)
        try:
            f.seek(2147483649L)
            f.write('x')
            f.flush()
        except (IOError, OverflowError):
            f.close()
            unlink(TESTFN)
            raise unittest.SkipTest('filesystem does not have largefile support')
        else:
            f.close()

    suite = unittest.TestSuite()
    for _open, prefix in [(io.open, 'C'), (pyio.open, 'Py'), (open, 'Builtin')]:

        class TestCase(LargeFileTest):
            pass

        TestCase.open = staticmethod(_open)
        TestCase.new_io = _open is not open
        TestCase.__name__ = prefix + LargeFileTest.__name__
        suite.addTest(TestCase('test_seek'))
        suite.addTest(TestCase('test_osstat'))
        suite.addTest(TestCase('test_seek_read'))
        suite.addTest(TestCase('test_lseek'))
        with _open(TESTFN, 'wb') as f:
            if hasattr(f, 'truncate'):
                suite.addTest(TestCase('test_truncate'))
        suite.addTest(TestCase('test_seekable'))
        unlink(TESTFN)

    try:
        run_unittest(suite)
    finally:
        unlink(TESTFN)


if __name__ == '__main__':
    test_main()