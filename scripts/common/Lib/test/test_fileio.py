# Embedded file name: scripts/common/Lib/test/test_fileio.py
from __future__ import unicode_literals
import sys
import os
import errno
import unittest
from array import array
from weakref import proxy
from functools import wraps
from test.test_support import TESTFN, check_warnings, run_unittest, make_bad_fd
from test.test_support import py3k_bytes as bytes
from test.script_helper import run_python
from _io import FileIO as _FileIO

class AutoFileTests(unittest.TestCase):

    def setUp(self):
        self.f = _FileIO(TESTFN, u'w')

    def tearDown(self):
        if self.f:
            self.f.close()
        os.remove(TESTFN)

    def testWeakRefs(self):
        p = proxy(self.f)
        p.write(bytes(range(10)))
        self.assertEqual(self.f.tell(), p.tell())
        self.f.close()
        self.f = None
        self.assertRaises(ReferenceError, getattr, p, u'tell')
        return

    def testSeekTell(self):
        self.f.write(bytes(range(20)))
        self.assertEqual(self.f.tell(), 20)
        self.f.seek(0)
        self.assertEqual(self.f.tell(), 0)
        self.f.seek(10)
        self.assertEqual(self.f.tell(), 10)
        self.f.seek(5, 1)
        self.assertEqual(self.f.tell(), 15)
        self.f.seek(-5, 1)
        self.assertEqual(self.f.tell(), 10)
        self.f.seek(-5, 2)
        self.assertEqual(self.f.tell(), 15)

    def testAttributes(self):
        f = self.f
        self.assertEqual(f.mode, u'wb')
        self.assertEqual(f.closed, False)
        for attr in (u'mode', u'closed'):
            self.assertRaises((AttributeError, TypeError), setattr, f, attr, u'oops')

    def testReadinto(self):
        self.f.write('\x01\x02')
        self.f.close()
        a = array('b', 'xxxxxxxxxx')
        self.f = _FileIO(TESTFN, u'r')
        n = self.f.readinto(a)
        self.assertEqual(array('b', [1, 2]), a[:n])

    def test_none_args(self):
        self.f.write('hi\nbye\nabc')
        self.f.close()
        self.f = _FileIO(TESTFN, u'r')
        self.assertEqual(self.f.read(None), 'hi\nbye\nabc')
        self.f.seek(0)
        self.assertEqual(self.f.readline(None), 'hi\n')
        self.assertEqual(self.f.readlines(None), ['bye\n', 'abc'])
        return

    def testRepr(self):
        self.assertEqual(repr(self.f), u"<_io.FileIO name=%r mode='%s'>" % (self.f.name, self.f.mode))
        del self.f.name
        self.assertEqual(repr(self.f), u"<_io.FileIO fd=%r mode='%s'>" % (self.f.fileno(), self.f.mode))
        self.f.close()
        self.assertEqual(repr(self.f), u'<_io.FileIO [closed]>')

    def testErrors(self):
        f = self.f
        self.assertTrue(not f.isatty())
        self.assertTrue(not f.closed)
        self.assertRaises(ValueError, f.read, 10)
        f.close()
        self.assertTrue(f.closed)
        f = _FileIO(TESTFN, u'r')
        self.assertRaises(TypeError, f.readinto, u'')
        self.assertTrue(not f.closed)
        f.close()
        self.assertTrue(f.closed)

    def testMethods(self):
        methods = [u'fileno',
         u'isatty',
         u'read',
         u'readinto',
         u'seek',
         u'tell',
         u'truncate',
         u'write',
         u'seekable',
         u'readable',
         u'writable']
        if sys.platform.startswith(u'atheos'):
            methods.remove(u'truncate')
        self.f.close()
        self.assertTrue(self.f.closed)
        for methodname in methods:
            method = getattr(self.f, methodname)
            self.assertRaises(ValueError, method)

    def testOpendir(self):
        try:
            _FileIO(u'.', u'r')
        except IOError as e:
            self.assertNotEqual(e.errno, 0)
            self.assertEqual(e.filename, u'.')
        else:
            self.fail(u'Should have raised IOError')

    def ClosedFD(func):

        @wraps(func)
        def wrapper(self):
            f = self.f
            os.close(f.fileno())
            try:
                func(self, f)
            finally:
                try:
                    self.f.close()
                except IOError:
                    pass

        return wrapper

    def ClosedFDRaises(func):

        @wraps(func)
        def wrapper(self):
            f = self.f
            os.close(f.fileno())
            try:
                func(self, f)
            except IOError as e:
                self.assertEqual(e.errno, errno.EBADF)
            else:
                self.fail(u'Should have raised IOError')
            finally:
                try:
                    self.f.close()
                except IOError:
                    pass

        return wrapper

    @ClosedFDRaises
    def testErrnoOnClose(self, f):
        f.close()

    @ClosedFDRaises
    def testErrnoOnClosedWrite(self, f):
        f.write(u'a')

    @ClosedFDRaises
    def testErrnoOnClosedSeek(self, f):
        f.seek(0)

    @ClosedFDRaises
    def testErrnoOnClosedTell(self, f):
        f.tell()

    @ClosedFDRaises
    def testErrnoOnClosedTruncate(self, f):
        f.truncate(0)

    @ClosedFD
    def testErrnoOnClosedSeekable(self, f):
        f.seekable()

    @ClosedFD
    def testErrnoOnClosedReadable(self, f):
        f.readable()

    @ClosedFD
    def testErrnoOnClosedWritable(self, f):
        f.writable()

    @ClosedFD
    def testErrnoOnClosedFileno(self, f):
        f.fileno()

    @ClosedFD
    def testErrnoOnClosedIsatty(self, f):
        self.assertEqual(f.isatty(), False)

    def ReopenForRead(self):
        try:
            self.f.close()
        except IOError:
            pass

        self.f = _FileIO(TESTFN, u'r')
        os.close(self.f.fileno())
        return self.f

    @ClosedFDRaises
    def testErrnoOnClosedRead(self, f):
        f = self.ReopenForRead()
        f.read(1)

    @ClosedFDRaises
    def testErrnoOnClosedReadall(self, f):
        f = self.ReopenForRead()
        f.readall()

    @ClosedFDRaises
    def testErrnoOnClosedReadinto(self, f):
        f = self.ReopenForRead()
        a = array('b', 'xxxxxxxxxx')
        f.readinto(a)


class OtherFileTests(unittest.TestCase):

    def testAbles(self):
        try:
            f = _FileIO(TESTFN, u'w')
            self.assertEqual(f.readable(), False)
            self.assertEqual(f.writable(), True)
            self.assertEqual(f.seekable(), True)
            f.close()
            f = _FileIO(TESTFN, u'r')
            self.assertEqual(f.readable(), True)
            self.assertEqual(f.writable(), False)
            self.assertEqual(f.seekable(), True)
            f.close()
            f = _FileIO(TESTFN, u'a+')
            self.assertEqual(f.readable(), True)
            self.assertEqual(f.writable(), True)
            self.assertEqual(f.seekable(), True)
            self.assertEqual(f.isatty(), False)
            f.close()
            if sys.platform != u'win32':
                try:
                    f = _FileIO(u'/dev/tty', u'a')
                except EnvironmentError:
                    pass
                else:
                    self.assertEqual(f.readable(), False)
                    self.assertEqual(f.writable(), True)
                    if sys.platform != u'darwin' and u'bsd' not in sys.platform and not sys.platform.startswith(u'sunos'):
                        self.assertEqual(f.seekable(), False)
                    self.assertEqual(f.isatty(), True)
                    f.close()

        finally:
            os.unlink(TESTFN)

    def testModeStrings(self):
        for mode in (u'', u'aU', u'wU+', u'rw', u'rt'):
            try:
                f = _FileIO(TESTFN, mode)
            except ValueError:
                pass
            else:
                f.close()
                self.fail(u'%r is an invalid file mode' % mode)

    def testUnicodeOpen(self):
        f = _FileIO(str(TESTFN), u'w')
        f.close()
        os.unlink(TESTFN)

    def testBytesOpen(self):
        try:
            fn = TESTFN.encode(u'ascii')
        except UnicodeEncodeError:
            return

        f = _FileIO(fn, u'w')
        try:
            f.write('abc')
            f.close()
            with open(TESTFN, u'rb') as f:
                self.assertEqual(f.read(), 'abc')
        finally:
            os.unlink(TESTFN)

    def testInvalidFd(self):
        self.assertRaises(ValueError, _FileIO, -10)
        self.assertRaises(OSError, _FileIO, make_bad_fd())
        if sys.platform == u'win32':
            import msvcrt
            self.assertRaises(IOError, msvcrt.get_osfhandle, make_bad_fd())

    def testBadModeArgument(self):
        bad_mode = u'qwerty'
        try:
            f = _FileIO(TESTFN, bad_mode)
        except ValueError as msg:
            if msg.args[0] != 0:
                s = str(msg)
                if TESTFN in s or bad_mode not in s:
                    self.fail(u'bad error message for invalid mode: %s' % s)
        else:
            f.close()
            self.fail(u'no error for invalid mode: %s' % bad_mode)

    def testTruncate(self):
        f = _FileIO(TESTFN, u'w')
        f.write(bytes(bytearray(range(10))))
        self.assertEqual(f.tell(), 10)
        f.truncate(5)
        self.assertEqual(f.tell(), 10)
        self.assertEqual(f.seek(0, os.SEEK_END), 5)
        f.truncate(15)
        self.assertEqual(f.tell(), 5)
        self.assertEqual(f.seek(0, os.SEEK_END), 15)
        f.close()

    def testTruncateOnWindows(self):

        def bug801631():
            f = _FileIO(TESTFN, u'w')
            f.write(bytes(range(11)))
            f.close()
            f = _FileIO(TESTFN, u'r+')
            data = f.read(5)
            if data != bytes(range(5)):
                self.fail(u'Read on file opened for update failed %r' % data)
            if f.tell() != 5:
                self.fail(u'File pos after read wrong %d' % f.tell())
            f.truncate()
            if f.tell() != 5:
                self.fail(u'File pos after ftruncate wrong %d' % f.tell())
            f.close()
            size = os.path.getsize(TESTFN)
            if size != 5:
                self.fail(u'File size after ftruncate wrong %d' % size)

        try:
            bug801631()
        finally:
            os.unlink(TESTFN)

    def testAppend(self):
        try:
            f = open(TESTFN, u'wb')
            f.write('spam')
            f.close()
            f = open(TESTFN, u'ab')
            f.write('eggs')
            f.close()
            f = open(TESTFN, u'rb')
            d = f.read()
            f.close()
            self.assertEqual(d, 'spameggs')
        finally:
            try:
                os.unlink(TESTFN)
            except:
                pass

    def testInvalidInit(self):
        self.assertRaises(TypeError, _FileIO, u'1', 0, 0)

    def testWarnings(self):
        with check_warnings(quiet=True) as w:
            self.assertEqual(w.warnings, [])
            self.assertRaises(TypeError, _FileIO, [])
            self.assertEqual(w.warnings, [])
            self.assertRaises(ValueError, _FileIO, u'/some/invalid/name', u'rt')
            self.assertEqual(w.warnings, [])

    def test_surrogates(self):
        filename = u'\udc80.txt'
        try:
            with _FileIO(filename):
                pass
        except (UnicodeEncodeError, IOError):
            pass

        env = dict(os.environ)
        env['LC_CTYPE'] = 'C'
        _, out = run_python(u'-c', u'import _io; _io.FileIO(%r)' % filename, env=env)
        if u'UnicodeEncodeError' not in out and u'IOError: [Errno 2] No such file or directory' not in out:
            self.fail(u'Bad output: %r' % out)


def test_main():
    try:
        run_unittest(AutoFileTests, OtherFileTests)
    finally:
        if os.path.exists(TESTFN):
            os.unlink(TESTFN)


if __name__ == u'__main__':
    test_main()