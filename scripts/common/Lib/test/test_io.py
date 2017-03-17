# Embedded file name: scripts/common/Lib/test/test_io.py
u"""Unit tests for the io module."""
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import time
import array
import random
import unittest
import weakref
import abc
import signal
import errno
from itertools import cycle, count
from collections import deque
from test import test_support as support
import codecs
import io
import _pyio as pyio
try:
    import threading
except ImportError:
    threading = None

try:
    import fcntl
except ImportError:
    fcntl = None

__metaclass__ = type
bytes = support.py3k_bytes

def _default_chunk_size():
    u"""Get the default TextIOWrapper chunk size"""
    with io.open(__file__, u'r', encoding=u'latin1') as f:
        return f._CHUNK_SIZE


class MockRawIOWithoutRead():
    u"""A RawIO implementation without read(), so as to exercise the default
    RawIO.read() which calls readinto()."""

    def __init__(self, read_stack = ()):
        self._read_stack = list(read_stack)
        self._write_stack = []
        self._reads = 0
        self._extraneous_reads = 0

    def write(self, b):
        self._write_stack.append(bytes(b))
        return len(b)

    def writable(self):
        return True

    def fileno(self):
        return 42

    def readable(self):
        return True

    def seekable(self):
        return True

    def seek(self, pos, whence):
        return 0

    def tell(self):
        return 0

    def readinto(self, buf):
        self._reads += 1
        max_len = len(buf)
        try:
            data = self._read_stack[0]
        except IndexError:
            self._extraneous_reads += 1
            return 0

        if data is None:
            del self._read_stack[0]
            return
        else:
            n = len(data)
            if len(data) <= max_len:
                del self._read_stack[0]
                buf[:n] = data
                return n
            buf[:] = data[:max_len]
            self._read_stack[0] = data[max_len:]
            return max_len
            return

    def truncate(self, pos = None):
        return pos


class CMockRawIOWithoutRead(MockRawIOWithoutRead, io.RawIOBase):
    pass


class PyMockRawIOWithoutRead(MockRawIOWithoutRead, pyio.RawIOBase):
    pass


class MockRawIO(MockRawIOWithoutRead):

    def read(self, n = None):
        self._reads += 1
        try:
            return self._read_stack.pop(0)
        except:
            self._extraneous_reads += 1
            return ''


class CMockRawIO(MockRawIO, io.RawIOBase):
    pass


class PyMockRawIO(MockRawIO, pyio.RawIOBase):
    pass


class MisbehavedRawIO(MockRawIO):

    def write(self, b):
        return MockRawIO.write(self, b) * 2

    def read(self, n = None):
        return MockRawIO.read(self, n) * 2

    def seek(self, pos, whence):
        return -123

    def tell(self):
        return -456

    def readinto(self, buf):
        MockRawIO.readinto(self, buf)
        return len(buf) * 5


class CMisbehavedRawIO(MisbehavedRawIO, io.RawIOBase):
    pass


class PyMisbehavedRawIO(MisbehavedRawIO, pyio.RawIOBase):
    pass


class CloseFailureIO(MockRawIO):
    closed = 0

    def close(self):
        if not self.closed:
            self.closed = 1
            raise IOError


class CCloseFailureIO(CloseFailureIO, io.RawIOBase):
    pass


class PyCloseFailureIO(CloseFailureIO, pyio.RawIOBase):
    pass


class MockFileIO():

    def __init__(self, data):
        self.read_history = []
        super(MockFileIO, self).__init__(data)

    def read(self, n = None):
        res = super(MockFileIO, self).read(n)
        self.read_history.append(None if res is None else len(res))
        return res

    def readinto(self, b):
        res = super(MockFileIO, self).readinto(b)
        self.read_history.append(res)
        return res


class CMockFileIO(MockFileIO, io.BytesIO):
    pass


class PyMockFileIO(MockFileIO, pyio.BytesIO):
    pass


class MockNonBlockWriterIO():

    def __init__(self):
        self._write_stack = []
        self._blocker_char = None
        return

    def pop_written(self):
        s = ''.join(self._write_stack)
        self._write_stack[:] = []
        return s

    def block_on(self, char):
        u"""Block when a given char is encountered."""
        self._blocker_char = char

    def readable(self):
        return True

    def seekable(self):
        return True

    def writable(self):
        return True

    def write(self, b):
        b = bytes(b)
        n = -1
        if self._blocker_char:
            try:
                n = b.index(self._blocker_char)
            except ValueError:
                pass
            else:
                if n > 0:
                    self._write_stack.append(b[:n])
                    return n
                self._blocker_char = None
                return

        self._write_stack.append(b)
        return len(b)


class CMockNonBlockWriterIO(MockNonBlockWriterIO, io.RawIOBase):
    BlockingIOError = io.BlockingIOError


class PyMockNonBlockWriterIO(MockNonBlockWriterIO, pyio.RawIOBase):
    BlockingIOError = pyio.BlockingIOError


class IOTest(unittest.TestCase):

    def setUp(self):
        support.unlink(support.TESTFN)

    def tearDown(self):
        support.unlink(support.TESTFN)

    def write_ops(self, f):
        self.assertEqual(f.write('blah.'), 5)
        f.truncate(0)
        self.assertEqual(f.tell(), 5)
        f.seek(0)
        self.assertEqual(f.write('blah.'), 5)
        self.assertEqual(f.seek(0), 0)
        self.assertEqual(f.write('Hello.'), 6)
        self.assertEqual(f.tell(), 6)
        self.assertEqual(f.seek(-1, 1), 5)
        self.assertEqual(f.tell(), 5)
        self.assertEqual(f.write(bytearray(' world\n\n\n')), 9)
        self.assertEqual(f.seek(0), 0)
        self.assertEqual(f.write('h'), 1)
        self.assertEqual(f.seek(-1, 2), 13)
        self.assertEqual(f.tell(), 13)
        self.assertEqual(f.truncate(12), 12)
        self.assertEqual(f.tell(), 13)
        self.assertRaises(TypeError, f.seek, 0.0)

    def read_ops(self, f, buffered = False):
        data = f.read(5)
        self.assertEqual(data, 'hello')
        data = bytearray(data)
        self.assertEqual(f.readinto(data), 5)
        self.assertEqual(data, ' worl')
        self.assertEqual(f.readinto(data), 2)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[:2], 'd\n')
        self.assertEqual(f.seek(0), 0)
        self.assertEqual(f.read(20), 'hello world\n')
        self.assertEqual(f.read(1), '')
        self.assertEqual(f.readinto(bytearray('x')), 0)
        self.assertEqual(f.seek(-6, 2), 6)
        self.assertEqual(f.read(5), 'world')
        self.assertEqual(f.read(0), '')
        self.assertEqual(f.readinto(bytearray()), 0)
        self.assertEqual(f.seek(-6, 1), 5)
        self.assertEqual(f.read(5), ' worl')
        self.assertEqual(f.tell(), 10)
        self.assertRaises(TypeError, f.seek, 0.0)
        if buffered:
            f.seek(0)
            self.assertEqual(f.read(), 'hello world\n')
            f.seek(6)
            self.assertEqual(f.read(), 'world\n')
            self.assertEqual(f.read(), '')

    LARGE = 2147483648L

    def large_file_ops(self, f):
        raise f.readable() or AssertionError
        raise f.writable() or AssertionError
        self.assertEqual(f.seek(self.LARGE), self.LARGE)
        self.assertEqual(f.tell(), self.LARGE)
        self.assertEqual(f.write('xxx'), 3)
        self.assertEqual(f.tell(), self.LARGE + 3)
        self.assertEqual(f.seek(-1, 1), self.LARGE + 2)
        self.assertEqual(f.truncate(), self.LARGE + 2)
        self.assertEqual(f.tell(), self.LARGE + 2)
        self.assertEqual(f.seek(0, 2), self.LARGE + 2)
        self.assertEqual(f.truncate(self.LARGE + 1), self.LARGE + 1)
        self.assertEqual(f.tell(), self.LARGE + 2)
        self.assertEqual(f.seek(0, 2), self.LARGE + 1)
        self.assertEqual(f.seek(-1, 2), self.LARGE)
        self.assertEqual(f.read(2), 'x')

    def test_invalid_operations(self):
        for mode in (u'w', u'wb'):
            with self.open(support.TESTFN, mode) as fp:
                self.assertRaises(IOError, fp.read)
                self.assertRaises(IOError, fp.readline)

        with self.open(support.TESTFN, u'rb') as fp:
            self.assertRaises(IOError, fp.write, 'blah')
            self.assertRaises(IOError, fp.writelines, ['blah\n'])
        with self.open(support.TESTFN, u'r') as fp:
            self.assertRaises(IOError, fp.write, u'blah')
            self.assertRaises(IOError, fp.writelines, [u'blah\n'])

    def test_raw_file_io(self):
        with self.open(support.TESTFN, u'wb', buffering=0) as f:
            self.assertEqual(f.readable(), False)
            self.assertEqual(f.writable(), True)
            self.assertEqual(f.seekable(), True)
            self.write_ops(f)
        with self.open(support.TESTFN, u'rb', buffering=0) as f:
            self.assertEqual(f.readable(), True)
            self.assertEqual(f.writable(), False)
            self.assertEqual(f.seekable(), True)
            self.read_ops(f)

    def test_buffered_file_io(self):
        with self.open(support.TESTFN, u'wb') as f:
            self.assertEqual(f.readable(), False)
            self.assertEqual(f.writable(), True)
            self.assertEqual(f.seekable(), True)
            self.write_ops(f)
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.readable(), True)
            self.assertEqual(f.writable(), False)
            self.assertEqual(f.seekable(), True)
            self.read_ops(f, True)

    def test_readline(self):
        with self.open(support.TESTFN, u'wb') as f:
            f.write('abc\ndef\nxyzzy\nfoo\x00bar\nanother line')
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.readline(), 'abc\n')
            self.assertEqual(f.readline(10), 'def\n')
            self.assertEqual(f.readline(2), 'xy')
            self.assertEqual(f.readline(4), 'zzy\n')
            self.assertEqual(f.readline(), 'foo\x00bar\n')
            self.assertEqual(f.readline(None), 'another line')
            self.assertRaises(TypeError, f.readline, 5.3)
        with self.open(support.TESTFN, u'r') as f:
            self.assertRaises(TypeError, f.readline, 5.3)
        return

    def test_raw_bytes_io(self):
        f = self.BytesIO()
        self.write_ops(f)
        data = f.getvalue()
        self.assertEqual(data, 'hello world\n')
        f = self.BytesIO(data)
        self.read_ops(f, True)

    def test_large_file_ops(self):
        if sys.platform[:3] == u'win' or sys.platform == u'darwin':
            if not support.is_resource_enabled(u'largefile'):
                print(u'\nTesting large file ops skipped on %s.' % sys.platform, file=sys.stderr)
                print(u'It requires %d bytes and a long time.' % self.LARGE, file=sys.stderr)
                print(u"Use 'regrtest.py -u largefile test_io' to run it.", file=sys.stderr)
                return
        with self.open(support.TESTFN, u'w+b', 0) as f:
            self.large_file_ops(f)
        with self.open(support.TESTFN, u'w+b') as f:
            self.large_file_ops(f)

    def test_with_open(self):
        for bufsize in (0, 1, 100):
            f = None
            with self.open(support.TESTFN, u'wb', bufsize) as f:
                f.write('xxx')
            self.assertEqual(f.closed, True)
            f = None
            try:
                with self.open(support.TESTFN, u'wb', bufsize) as f:
                    1 // 0
            except ZeroDivisionError:
                self.assertEqual(f.closed, True)
            else:
                self.fail(u"1 // 0 didn't raise an exception")

        return

    def test_append_mode_tell(self):
        with self.open(support.TESTFN, u'wb') as f:
            f.write('xxx')
        with self.open(support.TESTFN, u'ab', buffering=0) as f:
            self.assertEqual(f.tell(), 3)
        with self.open(support.TESTFN, u'ab') as f:
            self.assertEqual(f.tell(), 3)
        with self.open(support.TESTFN, u'a') as f:
            self.assertTrue(f.tell() > 0)

    def test_destructor(self):
        record = []

        class MyFileIO(self.FileIO):

            def __del__(self):
                record.append(1)
                try:
                    f = super(MyFileIO, self).__del__
                except AttributeError:
                    pass
                else:
                    f()

            def close(self):
                record.append(2)
                super(MyFileIO, self).close()

            def flush(self):
                record.append(3)
                super(MyFileIO, self).flush()

        f = MyFileIO(support.TESTFN, u'wb')
        f.write('xxx')
        del f
        support.gc_collect()
        self.assertEqual(record, [1, 2, 3])
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.read(), 'xxx')

    def _check_base_destructor(self, base):
        record = []

        class MyIO(base):

            def __init__(self):
                self.on_del = 1
                self.on_close = 2
                self.on_flush = 3

            def __del__(self):
                record.append(self.on_del)
                try:
                    f = super(MyIO, self).__del__
                except AttributeError:
                    pass
                else:
                    f()

            def close(self):
                record.append(self.on_close)
                super(MyIO, self).close()

            def flush(self):
                record.append(self.on_flush)
                super(MyIO, self).flush()

        f = MyIO()
        del f
        support.gc_collect()
        self.assertEqual(record, [1, 2, 3])

    def test_IOBase_destructor(self):
        self._check_base_destructor(self.IOBase)

    def test_RawIOBase_destructor(self):
        self._check_base_destructor(self.RawIOBase)

    def test_BufferedIOBase_destructor(self):
        self._check_base_destructor(self.BufferedIOBase)

    def test_TextIOBase_destructor(self):
        self._check_base_destructor(self.TextIOBase)

    def test_close_flushes(self):
        with self.open(support.TESTFN, u'wb') as f:
            f.write('xxx')
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.read(), 'xxx')

    def test_array_writes(self):
        a = array.array('i', range(10))
        n = len(a.tostring())
        with self.open(support.TESTFN, u'wb', 0) as f:
            self.assertEqual(f.write(a), n)
        with self.open(support.TESTFN, u'wb') as f:
            self.assertEqual(f.write(a), n)

    def test_closefd(self):
        self.assertRaises(ValueError, self.open, support.TESTFN, u'w', closefd=False)

    def test_read_closed(self):
        with self.open(support.TESTFN, u'w') as f:
            f.write(u'egg\n')
        with self.open(support.TESTFN, u'r') as f:
            file = self.open(f.fileno(), u'r', closefd=False)
            self.assertEqual(file.read(), u'egg\n')
            file.seek(0)
            file.close()
            self.assertRaises(ValueError, file.read)

    def test_no_closefd_with_filename(self):
        self.assertRaises(ValueError, self.open, support.TESTFN, u'r', closefd=False)

    def test_closefd_attr(self):
        with self.open(support.TESTFN, u'wb') as f:
            f.write('egg\n')
        with self.open(support.TESTFN, u'r') as f:
            self.assertEqual(f.buffer.raw.closefd, True)
            file = self.open(f.fileno(), u'r', closefd=False)
            self.assertEqual(file.buffer.raw.closefd, False)

    def test_garbage_collection(self):
        f = self.FileIO(support.TESTFN, u'wb')
        f.write('abcxxx')
        f.f = f
        wr = weakref.ref(f)
        del f
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.read(), 'abcxxx')
        return

    def test_unbounded_file(self):
        zero = u'/dev/zero'
        if not os.path.exists(zero):
            self.skipTest(u'{0} does not exist'.format(zero))
        if sys.maxsize > 2147483647:
            self.skipTest(u'test can only run in a 32-bit address space')
        if support.real_max_memuse < support._2G:
            self.skipTest(u'test requires at least 2GB of memory')
        with self.open(zero, u'rb', buffering=0) as f:
            self.assertRaises(OverflowError, f.read)
        with self.open(zero, u'rb') as f:
            self.assertRaises(OverflowError, f.read)
        with self.open(zero, u'r') as f:
            self.assertRaises(OverflowError, f.read)

    def test_flush_error_on_close(self):
        f = self.open(support.TESTFN, u'wb', buffering=0)

        def bad_flush():
            raise IOError()

        f.flush = bad_flush
        self.assertRaises(IOError, f.close)

    def test_multi_close(self):
        f = self.open(support.TESTFN, u'wb', buffering=0)
        f.close()
        f.close()
        f.close()
        self.assertRaises(ValueError, f.flush)

    def test_RawIOBase_read(self):
        rawio = self.MockRawIOWithoutRead(('abc', 'd', None, 'efg', None))
        self.assertEqual(rawio.read(2), 'ab')
        self.assertEqual(rawio.read(2), 'c')
        self.assertEqual(rawio.read(2), 'd')
        self.assertEqual(rawio.read(2), None)
        self.assertEqual(rawio.read(2), 'ef')
        self.assertEqual(rawio.read(2), 'g')
        self.assertEqual(rawio.read(2), None)
        self.assertEqual(rawio.read(2), '')
        return


class CIOTest(IOTest):

    def test_IOBase_finalize(self):

        class MyIO(self.IOBase):

            def close(self):
                pass

        MyIO()
        obj = MyIO()
        obj.obj = obj
        wr = weakref.ref(obj)
        del MyIO
        del obj
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        return


class PyIOTest(IOTest):
    test_array_writes = unittest.skip(u'len(array.array) returns number of elements rather than bytelength')(IOTest.test_array_writes)


class CommonBufferedTests():

    def test_detach(self):
        raw = self.MockRawIO()
        buf = self.tp(raw)
        self.assertIs(buf.detach(), raw)
        self.assertRaises(ValueError, buf.detach)

    def test_fileno(self):
        rawio = self.MockRawIO()
        bufio = self.tp(rawio)
        self.assertEqual(42, bufio.fileno())

    def test_no_fileno(self):
        pass

    def test_invalid_args(self):
        rawio = self.MockRawIO()
        bufio = self.tp(rawio)
        self.assertRaises(ValueError, bufio.seek, 0, -1)
        self.assertRaises(ValueError, bufio.seek, 0, 3)

    def test_override_destructor(self):
        tp = self.tp
        record = []

        class MyBufferedIO(tp):

            def __del__(self):
                record.append(1)
                try:
                    f = super(MyBufferedIO, self).__del__
                except AttributeError:
                    pass
                else:
                    f()

            def close(self):
                record.append(2)
                super(MyBufferedIO, self).close()

            def flush(self):
                record.append(3)
                super(MyBufferedIO, self).flush()

        rawio = self.MockRawIO()
        bufio = MyBufferedIO(rawio)
        writable = bufio.writable()
        del bufio
        support.gc_collect()
        if writable:
            self.assertEqual(record, [1, 2, 3])
        else:
            self.assertEqual(record, [1, 2])

    def test_context_manager(self):
        rawio = self.MockRawIO()
        bufio = self.tp(rawio)

        def _with():
            with bufio:
                pass

        _with()
        self.assertRaises(ValueError, _with)

    def test_error_through_destructor(self):
        rawio = self.CloseFailureIO()

        def f():
            self.tp(rawio).xyzzy

        with support.captured_output(u'stderr') as s:
            self.assertRaises(AttributeError, f)
        s = s.getvalue().strip()
        if s:
            self.assertEqual(len(s.splitlines()), 1)
            self.assertTrue(s.startswith(u'Exception IOError: '), s)
            self.assertTrue(s.endswith(u' ignored'), s)

    def test_repr(self):
        raw = self.MockRawIO()
        b = self.tp(raw)
        clsname = u'%s.%s' % (self.tp.__module__, self.tp.__name__)
        self.assertEqual(repr(b), u'<%s>' % clsname)
        raw.name = u'dummy'
        self.assertEqual(repr(b), u"<%s name=u'dummy'>" % clsname)
        raw.name = 'dummy'
        self.assertEqual(repr(b), u"<%s name='dummy'>" % clsname)

    def test_flush_error_on_close(self):
        raw = self.MockRawIO()

        def bad_flush():
            raise IOError()

        raw.flush = bad_flush
        b = self.tp(raw)
        self.assertRaises(IOError, b.close)

    def test_multi_close(self):
        raw = self.MockRawIO()
        b = self.tp(raw)
        b.close()
        b.close()
        b.close()
        self.assertRaises(ValueError, b.flush)

    def test_readonly_attributes(self):
        raw = self.MockRawIO()
        buf = self.tp(raw)
        x = self.MockRawIO()
        with self.assertRaises((AttributeError, TypeError)):
            buf.raw = x


class BufferedReaderTest(unittest.TestCase, CommonBufferedTests):
    read_mode = u'rb'

    def test_constructor(self):
        rawio = self.MockRawIO(['abc'])
        bufio = self.tp(rawio)
        bufio.__init__(rawio)
        bufio.__init__(rawio, buffer_size=1024)
        bufio.__init__(rawio, buffer_size=16)
        self.assertEqual('abc', bufio.read())
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=0)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-16)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-1)
        rawio = self.MockRawIO(['abc'])
        bufio.__init__(rawio)
        self.assertEqual('abc', bufio.read())

    def test_read(self):
        for arg in (None, 7):
            rawio = self.MockRawIO(('abc', 'd', 'efg'))
            bufio = self.tp(rawio)
            self.assertEqual('abcdefg', bufio.read(arg))

        self.assertRaises(ValueError, bufio.read, -2)
        return None

    def test_read1(self):
        rawio = self.MockRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        self.assertEqual('a', bufio.read(1))
        self.assertEqual('b', bufio.read1(1))
        self.assertEqual(rawio._reads, 1)
        self.assertEqual('c', bufio.read1(100))
        self.assertEqual(rawio._reads, 1)
        self.assertEqual('d', bufio.read1(100))
        self.assertEqual(rawio._reads, 2)
        self.assertEqual('efg', bufio.read1(100))
        self.assertEqual(rawio._reads, 3)
        self.assertEqual('', bufio.read1(100))
        self.assertEqual(rawio._reads, 4)
        self.assertRaises(ValueError, bufio.read1, -1)

    def test_readinto(self):
        rawio = self.MockRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        b = bytearray(2)
        self.assertEqual(bufio.readinto(b), 2)
        self.assertEqual(b, 'ab')
        self.assertEqual(bufio.readinto(b), 2)
        self.assertEqual(b, 'cd')
        self.assertEqual(bufio.readinto(b), 2)
        self.assertEqual(b, 'ef')
        self.assertEqual(bufio.readinto(b), 1)
        self.assertEqual(b, 'gf')
        self.assertEqual(bufio.readinto(b), 0)
        self.assertEqual(b, 'gf')

    def test_readlines(self):

        def bufio():
            rawio = self.MockRawIO(('abc\n', 'd\n', 'ef'))
            return self.tp(rawio)

        self.assertEqual(bufio().readlines(), ['abc\n', 'd\n', 'ef'])
        self.assertEqual(bufio().readlines(5), ['abc\n', 'd\n'])
        self.assertEqual(bufio().readlines(None), ['abc\n', 'd\n', 'ef'])
        return

    def test_buffering(self):
        data = 'abcdefghi'
        dlen = len(data)
        tests = [[100, [3,
           1,
           4,
           8], [dlen, 0]], [100, [3, 3, 3], [dlen]], [4, [1,
           2,
           4,
           2], [4, 4, 1]]]
        for bufsize, buf_read_sizes, raw_read_sizes in tests:
            rawio = self.MockFileIO(data)
            bufio = self.tp(rawio, buffer_size=bufsize)
            pos = 0
            for nbytes in buf_read_sizes:
                self.assertEqual(bufio.read(nbytes), data[pos:pos + nbytes])
                pos += nbytes

            self.assertEqual(rawio.read_history, raw_read_sizes)

    def test_read_non_blocking(self):
        rawio = self.MockRawIO(('abc', 'd', None, 'efg', None, None, None))
        bufio = self.tp(rawio)
        self.assertEqual('abcd', bufio.read(6))
        self.assertEqual('e', bufio.read(1))
        self.assertEqual('fg', bufio.read())
        self.assertEqual('', bufio.peek(1))
        self.assertIsNone(bufio.read())
        self.assertEqual('', bufio.read())
        rawio = self.MockRawIO(('a', None, None))
        self.assertEqual('a', rawio.readall())
        self.assertIsNone(rawio.readall())
        return None

    def test_read_past_eof(self):
        rawio = self.MockRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        self.assertEqual('abcdefg', bufio.read(9000))

    def test_read_all(self):
        rawio = self.MockRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        self.assertEqual('abcdefg', bufio.read())

    @unittest.skipUnless(threading, u'Threading required for this test.')
    @support.requires_resource(u'cpu')
    def test_threads(self):
        try:
            N = 1000
            l = list(range(256)) * N
            random.shuffle(l)
            s = bytes(bytearray(l))
            with self.open(support.TESTFN, u'wb') as f:
                f.write(s)
            with self.open(support.TESTFN, self.read_mode, buffering=0) as raw:
                bufio = self.tp(raw, 8)
                errors = []
                results = []

                def f():
                    try:
                        for n in cycle([1, 19]):
                            s = bufio.read(n)
                            if not s:
                                break
                            results.append(s)

                    except Exception as e:
                        errors.append(e)
                        raise

                threads = [ threading.Thread(target=f) for x in range(20) ]
                for t in threads:
                    t.start()

                time.sleep(0.02)
                for t in threads:
                    t.join()

                self.assertFalse(errors, u'the following exceptions were caught: %r' % errors)
                s = ''.join(results)
                for i in range(256):
                    c = bytes(bytearray([i]))
                    self.assertEqual(s.count(c), N)

        finally:
            support.unlink(support.TESTFN)

    def test_misbehaved_io(self):
        rawio = self.MisbehavedRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        self.assertRaises(IOError, bufio.seek, 0)
        self.assertRaises(IOError, bufio.tell)

    def test_no_extraneous_read(self):
        bufsize = 16
        for n in (2,
         bufsize - 1,
         bufsize,
         bufsize + 1,
         bufsize * 2):
            rawio = self.MockRawIO(['x' * n])
            bufio = self.tp(rawio, bufsize)
            self.assertEqual(bufio.read(n), 'x' * n)
            self.assertEqual(rawio._extraneous_reads, 0, u'failed for {}: {} != 0'.format(n, rawio._extraneous_reads))
            rawio = self.MockRawIO(['x' * (n - 1), 'x'])
            bufio = self.tp(rawio, bufsize)
            self.assertEqual(bufio.read(n), 'x' * n)
            self.assertEqual(rawio._extraneous_reads, 0, u'failed for {}: {} != 0'.format(n, rawio._extraneous_reads))


class CBufferedReaderTest(BufferedReaderTest):
    tp = io.BufferedReader

    def test_constructor(self):
        BufferedReaderTest.test_constructor(self)
        if sys.maxsize > 2147483647:
            rawio = self.MockRawIO()
            bufio = self.tp(rawio)
            self.assertRaises((OverflowError, MemoryError, ValueError), bufio.__init__, rawio, sys.maxsize)

    def test_initialization(self):
        rawio = self.MockRawIO(['abc'])
        bufio = self.tp(rawio)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=0)
        self.assertRaises(ValueError, bufio.read)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-16)
        self.assertRaises(ValueError, bufio.read)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-1)
        self.assertRaises(ValueError, bufio.read)

    def test_misbehaved_io_read(self):
        rawio = self.MisbehavedRawIO(('abc', 'd', 'efg'))
        bufio = self.tp(rawio)
        self.assertRaises(IOError, bufio.read, 10)

    def test_garbage_collection(self):
        rawio = self.FileIO(support.TESTFN, u'w+b')
        f = self.tp(rawio)
        f.f = f
        wr = weakref.ref(f)
        del f
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        return


class PyBufferedReaderTest(BufferedReaderTest):
    tp = pyio.BufferedReader


class BufferedWriterTest(unittest.TestCase, CommonBufferedTests):
    write_mode = u'wb'

    def test_constructor(self):
        rawio = self.MockRawIO()
        bufio = self.tp(rawio)
        bufio.__init__(rawio)
        bufio.__init__(rawio, buffer_size=1024)
        bufio.__init__(rawio, buffer_size=16)
        self.assertEqual(3, bufio.write('abc'))
        bufio.flush()
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=0)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-16)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-1)
        bufio.__init__(rawio)
        self.assertEqual(3, bufio.write('ghi'))
        bufio.flush()
        self.assertEqual(''.join(rawio._write_stack), 'abcghi')

    def test_detach_flush(self):
        raw = self.MockRawIO()
        buf = self.tp(raw)
        buf.write('howdy!')
        self.assertFalse(raw._write_stack)
        buf.detach()
        self.assertEqual(raw._write_stack, ['howdy!'])

    def test_write(self):
        writer = self.MockRawIO()
        bufio = self.tp(writer, 8)
        bufio.write('abc')
        self.assertFalse(writer._write_stack)

    def test_write_overflow(self):
        writer = self.MockRawIO()
        bufio = self.tp(writer, 8)
        contents = 'abcdefghijklmnop'
        for n in range(0, len(contents), 3):
            bufio.write(contents[n:n + 3])

        flushed = ''.join(writer._write_stack)
        self.assertTrue(flushed.startswith(contents[:-8]), flushed)

    def check_writes(self, intermediate_func):
        contents = bytes(range(256)) * 1000
        n = 0
        writer = self.MockRawIO()
        bufio = self.tp(writer, 13)

        def gen_sizes():
            for size in count(1):
                for i in range(15):
                    yield size

        sizes = gen_sizes()
        while n < len(contents):
            size = min(next(sizes), len(contents) - n)
            self.assertEqual(bufio.write(contents[n:n + size]), size)
            intermediate_func(bufio)
            n += size

        bufio.flush()
        self.assertEqual(contents, ''.join(writer._write_stack))

    def test_writes(self):
        self.check_writes(lambda bufio: None)

    def test_writes_and_flushes(self):
        self.check_writes(lambda bufio: bufio.flush())

    def test_writes_and_seeks(self):

        def _seekabs(bufio):
            pos = bufio.tell()
            bufio.seek(pos + 1, 0)
            bufio.seek(pos - 1, 0)
            bufio.seek(pos, 0)

        self.check_writes(_seekabs)

        def _seekrel(bufio):
            pos = bufio.seek(0, 1)
            bufio.seek(+1, 1)
            bufio.seek(-1, 1)
            bufio.seek(pos, 0)

        self.check_writes(_seekrel)

    def test_writes_and_truncates(self):
        self.check_writes(lambda bufio: bufio.truncate(bufio.tell()))

    def test_write_non_blocking(self):
        raw = self.MockNonBlockWriterIO()
        bufio = self.tp(raw, 8)
        self.assertEqual(bufio.write('abcd'), 4)
        self.assertEqual(bufio.write('efghi'), 5)
        raw.block_on('k')
        self.assertEqual(bufio.write('jklmn'), 5)
        raw.block_on('0')
        try:
            bufio.write('opqrwxyz0123456789')
        except self.BlockingIOError as e:
            written = e.characters_written
        else:
            self.fail(u'BlockingIOError should have been raised')

        self.assertEqual(written, 16)
        self.assertEqual(raw.pop_written(), 'abcdefghijklmnopqrwxyz')
        self.assertEqual(bufio.write('ABCDEFGHI'), 9)
        s = raw.pop_written()
        self.assertTrue(s.startswith('01234567A'), s)

    def test_write_and_rewind(self):
        raw = io.BytesIO()
        bufio = self.tp(raw, 4)
        self.assertEqual(bufio.write('abcdef'), 6)
        self.assertEqual(bufio.tell(), 6)
        bufio.seek(0, 0)
        self.assertEqual(bufio.write('XY'), 2)
        bufio.seek(6, 0)
        self.assertEqual(raw.getvalue(), 'XYcdef')
        self.assertEqual(bufio.write('123456'), 6)
        bufio.flush()
        self.assertEqual(raw.getvalue(), 'XYcdef123456')

    def test_flush(self):
        writer = self.MockRawIO()
        bufio = self.tp(writer, 8)
        bufio.write('abc')
        bufio.flush()
        self.assertEqual('abc', writer._write_stack[0])

    def test_destructor(self):
        writer = self.MockRawIO()
        bufio = self.tp(writer, 8)
        bufio.write('abc')
        del bufio
        support.gc_collect()
        self.assertEqual('abc', writer._write_stack[0])

    def test_truncate(self):
        with self.open(support.TESTFN, self.write_mode, buffering=0) as raw:
            bufio = self.tp(raw, 8)
            bufio.write('abcdef')
            self.assertEqual(bufio.truncate(3), 3)
            self.assertEqual(bufio.tell(), 6)
        with self.open(support.TESTFN, u'rb', buffering=0) as f:
            self.assertEqual(f.read(), 'abc')

    @unittest.skipUnless(threading, u'Threading required for this test.')
    @support.requires_resource(u'cpu')
    def test_threads(self):
        try:
            N = 1000
            contents = bytes(range(256)) * N
            sizes = cycle([1, 19])
            n = 0
            queue = deque()
            while n < len(contents):
                size = next(sizes)
                queue.append(contents[n:n + size])
                n += size

            del contents
            with self.open(support.TESTFN, self.write_mode, buffering=0) as raw:
                bufio = self.tp(raw, 8)
                errors = []

                def f():
                    try:
                        while True:
                            try:
                                s = queue.popleft()
                            except IndexError:
                                return

                            bufio.write(s)

                    except Exception as e:
                        errors.append(e)
                        raise

                threads = [ threading.Thread(target=f) for x in range(20) ]
                for t in threads:
                    t.start()

                time.sleep(0.02)
                for t in threads:
                    t.join()

                self.assertFalse(errors, u'the following exceptions were caught: %r' % errors)
                bufio.close()
            with self.open(support.TESTFN, u'rb') as f:
                s = f.read()
            for i in range(256):
                self.assertEqual(s.count(bytes([i])), N)

        finally:
            support.unlink(support.TESTFN)

    def test_misbehaved_io(self):
        rawio = self.MisbehavedRawIO()
        bufio = self.tp(rawio, 5)
        self.assertRaises(IOError, bufio.seek, 0)
        self.assertRaises(IOError, bufio.tell)
        self.assertRaises(IOError, bufio.write, 'abcdef')

    def test_max_buffer_size_deprecation(self):
        with support.check_warnings((u'max_buffer_size is deprecated', DeprecationWarning)):
            self.tp(self.MockRawIO(), 8, 12)


class CBufferedWriterTest(BufferedWriterTest):
    tp = io.BufferedWriter

    def test_constructor(self):
        BufferedWriterTest.test_constructor(self)
        if sys.maxsize > 2147483647:
            rawio = self.MockRawIO()
            bufio = self.tp(rawio)
            self.assertRaises((OverflowError, MemoryError, ValueError), bufio.__init__, rawio, sys.maxsize)

    def test_initialization(self):
        rawio = self.MockRawIO()
        bufio = self.tp(rawio)
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=0)
        self.assertRaises(ValueError, bufio.write, 'def')
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-16)
        self.assertRaises(ValueError, bufio.write, 'def')
        self.assertRaises(ValueError, bufio.__init__, rawio, buffer_size=-1)
        self.assertRaises(ValueError, bufio.write, 'def')

    def test_garbage_collection(self):
        rawio = self.FileIO(support.TESTFN, u'w+b')
        f = self.tp(rawio)
        f.write('123xxx')
        f.x = f
        wr = weakref.ref(f)
        del f
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.read(), '123xxx')
        return


class PyBufferedWriterTest(BufferedWriterTest):
    tp = pyio.BufferedWriter


class BufferedRWPairTest(unittest.TestCase):

    def test_constructor(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertFalse(pair.closed)

    def test_detach(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertRaises(self.UnsupportedOperation, pair.detach)

    def test_constructor_max_buffer_size_deprecation(self):
        with support.check_warnings((u'max_buffer_size is deprecated', DeprecationWarning)):
            self.tp(self.MockRawIO(), self.MockRawIO(), 8, 12)

    def test_constructor_with_not_readable(self):

        class NotReadable(MockRawIO):

            def readable(self):
                return False

        self.assertRaises(IOError, self.tp, NotReadable(), self.MockRawIO())

    def test_constructor_with_not_writeable(self):

        class NotWriteable(MockRawIO):

            def writable(self):
                return False

        self.assertRaises(IOError, self.tp, self.MockRawIO(), NotWriteable())

    def test_read(self):
        pair = self.tp(self.BytesIO('abcdef'), self.MockRawIO())
        self.assertEqual(pair.read(3), 'abc')
        self.assertEqual(pair.read(1), 'd')
        self.assertEqual(pair.read(), 'ef')
        pair = self.tp(self.BytesIO('abc'), self.MockRawIO())
        self.assertEqual(pair.read(None), 'abc')
        return

    def test_readlines(self):
        pair = lambda : self.tp(self.BytesIO('abc\ndef\nh'), self.MockRawIO())
        self.assertEqual(pair().readlines(), ['abc\n', 'def\n', 'h'])
        self.assertEqual(pair().readlines(), ['abc\n', 'def\n', 'h'])
        self.assertEqual(pair().readlines(5), ['abc\n', 'def\n'])

    def test_read1(self):
        pair = self.tp(self.BytesIO('abcdef'), self.MockRawIO())
        self.assertEqual(pair.read1(3), 'abc')

    def test_readinto(self):
        pair = self.tp(self.BytesIO('abcdef'), self.MockRawIO())
        data = bytearray(5)
        self.assertEqual(pair.readinto(data), 5)
        self.assertEqual(data, 'abcde')

    def test_write(self):
        w = self.MockRawIO()
        pair = self.tp(self.MockRawIO(), w)
        pair.write('abc')
        pair.flush()
        pair.write('def')
        pair.flush()
        self.assertEqual(w._write_stack, ['abc', 'def'])

    def test_peek(self):
        pair = self.tp(self.BytesIO('abcdef'), self.MockRawIO())
        self.assertTrue(pair.peek(3).startswith('abc'))
        self.assertEqual(pair.read(3), 'abc')

    def test_readable(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertTrue(pair.readable())

    def test_writeable(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertTrue(pair.writable())

    def test_seekable(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertFalse(pair.seekable())

    def test_close_and_closed(self):
        pair = self.tp(self.MockRawIO(), self.MockRawIO())
        self.assertFalse(pair.closed)
        pair.close()
        self.assertTrue(pair.closed)

    def test_isatty(self):

        class SelectableIsAtty(MockRawIO):

            def __init__(self, isatty):
                MockRawIO.__init__(self)
                self._isatty = isatty

            def isatty(self):
                return self._isatty

        pair = self.tp(SelectableIsAtty(False), SelectableIsAtty(False))
        self.assertFalse(pair.isatty())
        pair = self.tp(SelectableIsAtty(True), SelectableIsAtty(False))
        self.assertTrue(pair.isatty())
        pair = self.tp(SelectableIsAtty(False), SelectableIsAtty(True))
        self.assertTrue(pair.isatty())
        pair = self.tp(SelectableIsAtty(True), SelectableIsAtty(True))
        self.assertTrue(pair.isatty())


class CBufferedRWPairTest(BufferedRWPairTest):
    tp = io.BufferedRWPair


class PyBufferedRWPairTest(BufferedRWPairTest):
    tp = pyio.BufferedRWPair


class BufferedRandomTest(BufferedReaderTest, BufferedWriterTest):
    read_mode = u'rb+'
    write_mode = u'wb+'

    def test_constructor(self):
        BufferedReaderTest.test_constructor(self)
        BufferedWriterTest.test_constructor(self)

    def test_read_and_write(self):
        raw = self.MockRawIO(('asdf', 'ghjk'))
        rw = self.tp(raw, 8)
        self.assertEqual('as', rw.read(2))
        rw.write('ddd')
        rw.write('eee')
        self.assertFalse(raw._write_stack)
        self.assertEqual('ghjk', rw.read())
        self.assertEqual('dddeee', raw._write_stack[0])

    def test_seek_and_tell(self):
        raw = self.BytesIO('asdfghjkl')
        rw = self.tp(raw)
        self.assertEqual('as', rw.read(2))
        self.assertEqual(2, rw.tell())
        rw.seek(0, 0)
        self.assertEqual('asdf', rw.read(4))
        rw.write('123f')
        rw.seek(0, 0)
        self.assertEqual('asdf123fl', rw.read())
        self.assertEqual(9, rw.tell())
        rw.seek(-4, 2)
        self.assertEqual(5, rw.tell())
        rw.seek(2, 1)
        self.assertEqual(7, rw.tell())
        self.assertEqual('fl', rw.read(11))
        rw.flush()
        self.assertEqual('asdf123fl', raw.getvalue())
        self.assertRaises(TypeError, rw.seek, 0.0)

    def check_flush_and_read(self, read_func):
        raw = self.BytesIO('abcdefghi')
        bufio = self.tp(raw)
        self.assertEqual('ab', read_func(bufio, 2))
        bufio.write('12')
        self.assertEqual('ef', read_func(bufio, 2))
        self.assertEqual(6, bufio.tell())
        bufio.flush()
        self.assertEqual(6, bufio.tell())
        self.assertEqual('ghi', read_func(bufio))
        raw.seek(0, 0)
        raw.write('XYZ')
        bufio.flush()
        bufio.seek(0, 0)
        self.assertEqual('XYZ', read_func(bufio, 3))

    def test_flush_and_read(self):
        self.check_flush_and_read(lambda bufio, *args: bufio.read(*args))

    def test_flush_and_readinto(self):

        def _readinto(bufio, n = -1):
            b = bytearray(n if n >= 0 else 9999)
            n = bufio.readinto(b)
            return bytes(b[:n])

        self.check_flush_and_read(_readinto)

    def test_flush_and_peek(self):

        def _peek(bufio, n = -1):
            b = bufio.peek(n)
            if n != -1:
                b = b[:n]
            bufio.seek(len(b), 1)
            return b

        self.check_flush_and_read(_peek)

    def test_flush_and_write(self):
        raw = self.BytesIO('abcdefghi')
        bufio = self.tp(raw)
        bufio.write('123')
        bufio.flush()
        bufio.write('45')
        bufio.flush()
        bufio.seek(0, 0)
        self.assertEqual('12345fghi', raw.getvalue())
        self.assertEqual('12345fghi', bufio.read())

    def test_threads(self):
        BufferedReaderTest.test_threads(self)
        BufferedWriterTest.test_threads(self)

    def test_writes_and_peek(self):

        def _peek(bufio):
            bufio.peek(1)

        self.check_writes(_peek)

        def _peek(bufio):
            pos = bufio.tell()
            bufio.seek(-1, 1)
            bufio.peek(1)
            bufio.seek(pos, 0)

        self.check_writes(_peek)

    def test_writes_and_reads(self):

        def _read(bufio):
            bufio.seek(-1, 1)
            bufio.read(1)

        self.check_writes(_read)

    def test_writes_and_read1s(self):

        def _read1(bufio):
            bufio.seek(-1, 1)
            bufio.read1(1)

        self.check_writes(_read1)

    def test_writes_and_readintos(self):

        def _read(bufio):
            bufio.seek(-1, 1)
            bufio.readinto(bytearray(1))

        self.check_writes(_read)

    def test_write_after_readahead(self):
        for overwrite_size in [1, 5]:
            raw = self.BytesIO('AAAAAAAAAA')
            bufio = self.tp(raw, 4)
            self.assertEqual(bufio.read(1), 'A')
            self.assertEqual(bufio.tell(), 1)
            bufio.write('B' * overwrite_size)
            self.assertEqual(bufio.tell(), overwrite_size + 1)
            bufio.flush()
            self.assertEqual(bufio.tell(), overwrite_size + 1)
            s = raw.getvalue()
            self.assertEqual(s, 'A' + 'B' * overwrite_size + 'A' * (9 - overwrite_size))

    def test_write_rewind_write(self):

        def mutate(bufio, pos1, pos2):
            raise pos2 >= pos1 or AssertionError
            bufio.seek(pos1)
            bufio.read(pos2 - pos1)
            bufio.write('\x02')
            bufio.seek(pos1)
            bufio.write('\x01')

        b = '\x80\x81\x82\x83\x84'
        for i in range(0, len(b)):
            for j in range(i, len(b)):
                raw = self.BytesIO(b)
                bufio = self.tp(raw, 100)
                mutate(bufio, i, j)
                bufio.flush()
                expected = bytearray(b)
                expected[j] = 2
                expected[i] = 1
                self.assertEqual(raw.getvalue(), expected, u'failed result for i=%d, j=%d' % (i, j))

    def test_truncate_after_read_or_write(self):
        raw = self.BytesIO('AAAAAAAAAA')
        bufio = self.tp(raw, 100)
        self.assertEqual(bufio.read(2), 'AA')
        self.assertEqual(bufio.truncate(), 2)
        self.assertEqual(bufio.write('BB'), 2)
        self.assertEqual(bufio.truncate(), 4)

    def test_misbehaved_io(self):
        BufferedReaderTest.test_misbehaved_io(self)
        BufferedWriterTest.test_misbehaved_io(self)

    def test_interleaved_read_write(self):
        with self.BytesIO('abcdefgh') as raw:
            with self.tp(raw, 100) as f:
                f.write('1')
                self.assertEqual(f.read(1), 'b')
                f.write('2')
                self.assertEqual(f.read1(1), 'd')
                f.write('3')
                buf = bytearray(1)
                f.readinto(buf)
                self.assertEqual(buf, 'f')
                f.write('4')
                self.assertEqual(f.peek(1), 'h')
                f.flush()
                self.assertEqual(raw.getvalue(), '1b2d3f4h')
        with self.BytesIO('abc') as raw:
            with self.tp(raw, 100) as f:
                self.assertEqual(f.read(1), 'a')
                f.write('2')
                self.assertEqual(f.read(1), 'c')
                f.flush()
                self.assertEqual(raw.getvalue(), 'a2c')

    def test_interleaved_readline_write(self):
        with self.BytesIO('ab\ncdef\ng\n') as raw:
            with self.tp(raw) as f:
                f.write('1')
                self.assertEqual(f.readline(), 'b\n')
                f.write('2')
                self.assertEqual(f.readline(), 'def\n')
                f.write('3')
                self.assertEqual(f.readline(), '\n')
                f.flush()
                self.assertEqual(raw.getvalue(), '1b\n2def\n3\n')


class CBufferedRandomTest(CBufferedReaderTest, CBufferedWriterTest, BufferedRandomTest):
    tp = io.BufferedRandom

    def test_constructor(self):
        BufferedRandomTest.test_constructor(self)
        if sys.maxsize > 2147483647:
            rawio = self.MockRawIO()
            bufio = self.tp(rawio)
            self.assertRaises((OverflowError, MemoryError, ValueError), bufio.__init__, rawio, sys.maxsize)

    def test_garbage_collection(self):
        CBufferedReaderTest.test_garbage_collection(self)
        CBufferedWriterTest.test_garbage_collection(self)


class PyBufferedRandomTest(BufferedRandomTest):
    tp = pyio.BufferedRandom


class StatefulIncrementalDecoder(codecs.IncrementalDecoder):
    u"""
    For testing seek/tell behavior with a stateful, buffering decoder.
    
    Input is a sequence of words.  Words may be fixed-length (length set
    by input) or variable-length (period-terminated).  In variable-length
    mode, extra periods are ignored.  Possible words are:
      - 'i' followed by a number sets the input length, I (maximum 99).
        When I is set to 0, words are space-terminated.
      - 'o' followed by a number sets the output length, O (maximum 99).
      - Any other word is converted into a word followed by a period on
        the output.  The output word consists of the input word truncated
        or padded out with hyphens to make its length equal to O.  If O
        is 0, the word is output verbatim without truncating or padding.
    I and O are initially set to 1.  When I changes, any buffered input is
    re-scanned according to the new I.  EOF also terminates the last word.
    """

    def __init__(self, errors = u'strict'):
        codecs.IncrementalDecoder.__init__(self, errors)
        self.reset()

    def __repr__(self):
        return u'<SID %x>' % id(self)

    def reset(self):
        self.i = 1
        self.o = 1
        self.buffer = bytearray()

    def getstate(self):
        i, o = self.i ^ 1, self.o ^ 1
        return (bytes(self.buffer), i * 100 + o)

    def setstate(self, state):
        buffer, io = state
        self.buffer = bytearray(buffer)
        i, o = divmod(io, 100)
        self.i, self.o = i ^ 1, o ^ 1

    def decode(self, input, final = False):
        output = u''
        for b in input:
            if self.i == 0:
                if b == u'.':
                    if self.buffer:
                        output += self.process_word()
                else:
                    self.buffer.append(b)
            else:
                self.buffer.append(b)
                if len(self.buffer) == self.i:
                    output += self.process_word()

        if final and self.buffer:
            output += self.process_word()
        return output

    def process_word(self):
        output = u''
        if self.buffer[0] == ord(u'i'):
            self.i = min(99, int(self.buffer[1:] or 0))
        elif self.buffer[0] == ord(u'o'):
            self.o = min(99, int(self.buffer[1:] or 0))
        else:
            output = self.buffer.decode(u'ascii')
            if len(output) < self.o:
                output += u'-' * self.o
            if self.o:
                output = output[:self.o]
            output += u'.'
        self.buffer = bytearray()
        return output

    codecEnabled = False

    @classmethod
    def lookupTestDecoder(cls, name):
        if cls.codecEnabled and name == u'test_decoder':
            latin1 = codecs.lookup(u'latin-1')
            return codecs.CodecInfo(name=u'test_decoder', encode=latin1.encode, decode=None, incrementalencoder=None, streamreader=None, streamwriter=None, incrementaldecoder=cls)
        else:
            return None


codecs.register(StatefulIncrementalDecoder.lookupTestDecoder)

class StatefulIncrementalDecoderTest(unittest.TestCase):
    u"""
    Make sure the StatefulIncrementalDecoder actually works.
    """
    test_cases = [('abcd', False, u'a.b.c.d.'),
     ('oiabcd', True, u'abcd.'),
     ('oi...abcd...', True, u'abcd.'),
     ('i.o6.x.xyz.toolongtofit.', False, u'x-----.xyz---.toolon.'),
     ('i.i2.o6xyz', True, u'xy----.z-----.'),
     ('i.o3.i6.abcdefghijklmnop', True, u'abc.ghi.mno.'),
     ('i.o29.a.b.cde.o15.abcdefghijabcdefghij.i3.a.b.c.d.ei00k.l.m', True, u'a----------------------------.' + u'b----------------------------.' + u'cde--------------------------.' + u'abcdefghijabcde.' + u'a.b------------.' + u'.c.------------.' + u'd.e------------.' + u'k--------------.' + u'l--------------.' + u'm--------------.')]

    def test_decoder(self):
        for input, eof, output in self.test_cases:
            d = StatefulIncrementalDecoder()
            self.assertEqual(d.decode(input, eof), output)

        d = StatefulIncrementalDecoder()
        self.assertEqual(d.decode('oiabcd'), u'')
        self.assertEqual(d.decode('', 1), u'abcd.')


class TextIOWrapperTest(unittest.TestCase):

    def setUp(self):
        self.testdata = 'AAA\r\nBBB\rCCC\r\nDDD\nEEE\r\n'
        self.normalized = 'AAA\nBBB\nCCC\nDDD\nEEE\n'.decode(u'ascii')
        support.unlink(support.TESTFN)

    def tearDown(self):
        support.unlink(support.TESTFN)

    def test_constructor(self):
        r = self.BytesIO('\xc3\xa9\n\n')
        b = self.BufferedReader(r, 1000)
        t = self.TextIOWrapper(b)
        t.__init__(b, encoding=u'latin1', newline=u'\r\n')
        self.assertEqual(t.encoding, u'latin1')
        self.assertEqual(t.line_buffering, False)
        t.__init__(b, encoding=u'utf8', line_buffering=True)
        self.assertEqual(t.encoding, u'utf8')
        self.assertEqual(t.line_buffering, True)
        self.assertEqual(u'\xe9\n', t.readline())
        self.assertRaises(TypeError, t.__init__, b, newline=42)
        self.assertRaises(ValueError, t.__init__, b, newline=u'xyzzy')

    def test_detach(self):
        r = self.BytesIO()
        b = self.BufferedWriter(r)
        t = self.TextIOWrapper(b)
        self.assertIs(t.detach(), b)
        t = self.TextIOWrapper(b, encoding=u'ascii')
        t.write(u'howdy')
        self.assertFalse(r.getvalue())
        t.detach()
        self.assertEqual(r.getvalue(), 'howdy')
        self.assertRaises(ValueError, t.detach)

    def test_repr(self):
        raw = self.BytesIO(u'hello'.encode(u'utf-8'))
        b = self.BufferedReader(raw)
        t = self.TextIOWrapper(b, encoding=u'utf-8')
        modname = self.TextIOWrapper.__module__
        self.assertEqual(repr(t), u"<%s.TextIOWrapper encoding='utf-8'>" % modname)
        raw.name = u'dummy'
        self.assertEqual(repr(t), u"<%s.TextIOWrapper name=u'dummy' encoding='utf-8'>" % modname)
        raw.name = 'dummy'
        self.assertEqual(repr(t), u"<%s.TextIOWrapper name='dummy' encoding='utf-8'>" % modname)

    def test_line_buffering(self):
        r = self.BytesIO()
        b = self.BufferedWriter(r, 1000)
        t = self.TextIOWrapper(b, newline=u'\n', line_buffering=True)
        t.write(u'X')
        self.assertEqual(r.getvalue(), '')
        t.write(u'Y\nZ')
        self.assertEqual(r.getvalue(), 'XY\nZ')
        t.write(u'A\rB')
        self.assertEqual(r.getvalue(), 'XY\nZA\rB')

    def test_encoding(self):
        b = self.BytesIO()
        t = self.TextIOWrapper(b, encoding=u'utf8')
        self.assertEqual(t.encoding, u'utf8')
        t = self.TextIOWrapper(b)
        self.assertTrue(t.encoding is not None)
        codecs.lookup(t.encoding)
        return

    def test_encoding_errors_reading(self):
        b = self.BytesIO('abc\n\xff\n')
        t = self.TextIOWrapper(b, encoding=u'ascii')
        self.assertRaises(UnicodeError, t.read)
        b = self.BytesIO('abc\n\xff\n')
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'strict')
        self.assertRaises(UnicodeError, t.read)
        b = self.BytesIO('abc\n\xff\n')
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'ignore')
        self.assertEqual(t.read(), u'abc\n\n')
        b = self.BytesIO('abc\n\xff\n')
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'replace')
        self.assertEqual(t.read(), u'abc\n\ufffd\n')

    def test_encoding_errors_writing(self):
        b = self.BytesIO()
        t = self.TextIOWrapper(b, encoding=u'ascii')
        self.assertRaises(UnicodeError, t.write, u'\xff')
        b = self.BytesIO()
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'strict')
        self.assertRaises(UnicodeError, t.write, u'\xff')
        b = self.BytesIO()
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'ignore', newline=u'\n')
        t.write(u'abc\xffdef\n')
        t.flush()
        self.assertEqual(b.getvalue(), 'abcdef\n')
        b = self.BytesIO()
        t = self.TextIOWrapper(b, encoding=u'ascii', errors=u'replace', newline=u'\n')
        t.write(u'abc\xffdef\n')
        t.flush()
        self.assertEqual(b.getvalue(), 'abc?def\n')

    def test_newlines(self):
        input_lines = [u'unix\n',
         u'windows\r\n',
         u'os9\r',
         u'last\n',
         u'nonl']
        tests = [[None, [u'unix\n',
           u'windows\n',
           u'os9\n',
           u'last\n',
           u'nonl']],
         [u'', input_lines],
         [u'\n', [u'unix\n',
           u'windows\r\n',
           u'os9\rlast\n',
           u'nonl']],
         [u'\r\n', [u'unix\nwindows\r\n', u'os9\rlast\nnonl']],
         [u'\r', [u'unix\nwindows\r', u'\nos9\r', u'last\nnonl']]]
        encodings = (u'utf-8', u'latin-1', u'utf-16', u'utf-16-le', u'utf-16-be', u'utf-32', u'utf-32-le', u'utf-32-be')
        for encoding in encodings:
            data = bytes(u''.join(input_lines).encode(encoding))
            for do_reads in (False, True):
                for bufsize in range(1, 10):
                    for newline, exp_lines in tests:
                        bufio = self.BufferedReader(self.BytesIO(data), bufsize)
                        textio = self.TextIOWrapper(bufio, newline=newline, encoding=encoding)
                        if do_reads:
                            got_lines = []
                            while True:
                                c2 = textio.read(2)
                                if c2 == u'':
                                    break
                                self.assertEqual(len(c2), 2)
                                got_lines.append(c2 + textio.readline())

                        else:
                            got_lines = list(textio)
                        for got_line, exp_line in zip(got_lines, exp_lines):
                            self.assertEqual(got_line, exp_line)

                        self.assertEqual(len(got_lines), len(exp_lines))

        return

    def test_newlines_input(self):
        testdata = 'AAA\nBB\x00B\nCCC\rDDD\rEEE\r\nFFF\r\nGGG'
        normalized = testdata.replace('\r\n', '\n').replace('\r', '\n')
        for newline, expected in [(None, normalized.decode(u'ascii').splitlines(True)),
         (u'', testdata.decode(u'ascii').splitlines(True)),
         (u'\n', [u'AAA\n',
           u'BB\x00B\n',
           u'CCC\rDDD\rEEE\r\n',
           u'FFF\r\n',
           u'GGG']),
         (u'\r\n', [u'AAA\nBB\x00B\nCCC\rDDD\rEEE\r\n', u'FFF\r\n', u'GGG']),
         (u'\r', [u'AAA\nBB\x00B\nCCC\r',
           u'DDD\r',
           u'EEE\r',
           u'\nFFF\r',
           u'\nGGG'])]:
            buf = self.BytesIO(testdata)
            txt = self.TextIOWrapper(buf, encoding=u'ascii', newline=newline)
            self.assertEqual(txt.readlines(), expected)
            txt.seek(0)
            self.assertEqual(txt.read(), u''.join(expected))

        return

    def test_newlines_output(self):
        testdict = {u'': 'AAA\nBBB\nCCC\nX\rY\r\nZ',
         u'\n': 'AAA\nBBB\nCCC\nX\rY\r\nZ',
         u'\r': 'AAA\rBBB\rCCC\rX\rY\r\rZ',
         u'\r\n': 'AAA\r\nBBB\r\nCCC\r\nX\rY\r\r\nZ'}
        tests = [(None, testdict[os.linesep])] + sorted(testdict.items())
        for newline, expected in tests:
            buf = self.BytesIO()
            txt = self.TextIOWrapper(buf, encoding=u'ascii', newline=newline)
            txt.write(u'AAA\nB')
            txt.write(u'BB\nCCC\n')
            txt.write(u'X\rY\r\nZ')
            txt.flush()
            self.assertEqual(buf.closed, False)
            self.assertEqual(buf.getvalue(), expected)

        return

    def test_destructor(self):
        l = []
        base = self.BytesIO

        class MyBytesIO(base):

            def close(self):
                l.append(self.getvalue())
                base.close(self)

        b = MyBytesIO()
        t = self.TextIOWrapper(b, encoding=u'ascii')
        t.write(u'abc')
        del t
        support.gc_collect()
        self.assertEqual(['abc'], l)

    def test_override_destructor(self):
        record = []

        class MyTextIO(self.TextIOWrapper):

            def __del__(self):
                record.append(1)
                try:
                    f = super(MyTextIO, self).__del__
                except AttributeError:
                    pass
                else:
                    f()

            def close(self):
                record.append(2)
                super(MyTextIO, self).close()

            def flush(self):
                record.append(3)
                super(MyTextIO, self).flush()

        b = self.BytesIO()
        t = MyTextIO(b, encoding=u'ascii')
        del t
        support.gc_collect()
        self.assertEqual(record, [1, 2, 3])

    def test_error_through_destructor(self):
        rawio = self.CloseFailureIO()

        def f():
            self.TextIOWrapper(rawio).xyzzy

        with support.captured_output(u'stderr') as s:
            self.assertRaises(AttributeError, f)
        s = s.getvalue().strip()
        if s:
            self.assertEqual(len(s.splitlines()), 1)
            self.assertTrue(s.startswith(u'Exception IOError: '), s)
            self.assertTrue(s.endswith(u' ignored'), s)

    def test_basic_io(self):
        for chunksize in (1, 2, 3, 4, 5, 15, 16, 17, 31, 32, 33, 63, 64, 65):
            for enc in (u'ascii', u'latin1', u'utf8'):
                f = self.open(support.TESTFN, u'w+', encoding=enc)
                f._CHUNK_SIZE = chunksize
                self.assertEqual(f.write(u'abc'), 3)
                f.close()
                f = self.open(support.TESTFN, u'r+', encoding=enc)
                f._CHUNK_SIZE = chunksize
                self.assertEqual(f.tell(), 0)
                self.assertEqual(f.read(), u'abc')
                cookie = f.tell()
                self.assertEqual(f.seek(0), 0)
                self.assertEqual(f.read(None), u'abc')
                f.seek(0)
                self.assertEqual(f.read(2), u'ab')
                self.assertEqual(f.read(1), u'c')
                self.assertEqual(f.read(1), u'')
                self.assertEqual(f.read(), u'')
                self.assertEqual(f.tell(), cookie)
                self.assertEqual(f.seek(0), 0)
                self.assertEqual(f.seek(0, 2), cookie)
                self.assertEqual(f.write(u'def'), 3)
                self.assertEqual(f.seek(cookie), cookie)
                self.assertEqual(f.read(), u'def')
                if enc.startswith(u'utf'):
                    self.multi_line_test(f, enc)
                f.close()

        return

    def multi_line_test(self, f, enc):
        f.seek(0)
        f.truncate()
        sample = u's\xff\u0fff\uffff'
        wlines = []
        for size in (0, 1, 2, 3, 4, 5, 30, 31, 32, 33, 62, 63, 64, 65, 1000):
            chars = []
            for i in range(size):
                chars.append(sample[i % len(sample)])

            line = u''.join(chars) + u'\n'
            wlines.append((f.tell(), line))
            f.write(line)

        f.seek(0)
        rlines = []
        while True:
            pos = f.tell()
            line = f.readline()
            if not line:
                break
            rlines.append((pos, line))

        self.assertEqual(rlines, wlines)

    def test_telling(self):
        f = self.open(support.TESTFN, u'w+', encoding=u'utf8')
        p0 = f.tell()
        f.write(u'\xff\n')
        p1 = f.tell()
        f.write(u'\xff\n')
        p2 = f.tell()
        f.seek(0)
        self.assertEqual(f.tell(), p0)
        self.assertEqual(f.readline(), u'\xff\n')
        self.assertEqual(f.tell(), p1)
        self.assertEqual(f.readline(), u'\xff\n')
        self.assertEqual(f.tell(), p2)
        f.seek(0)
        for line in f:
            self.assertEqual(line, u'\xff\n')
            self.assertRaises(IOError, f.tell)

        self.assertEqual(f.tell(), p2)
        f.close()

    def test_seeking(self):
        chunk_size = _default_chunk_size()
        prefix_size = chunk_size - 2
        u_prefix = u'a' * prefix_size
        prefix = bytes(u_prefix.encode(u'utf-8'))
        self.assertEqual(len(u_prefix), len(prefix))
        u_suffix = u'\u8888\n'
        suffix = bytes(u_suffix.encode(u'utf-8'))
        line = prefix + suffix
        f = self.open(support.TESTFN, u'wb')
        f.write(line * 2)
        f.close()
        f = self.open(support.TESTFN, u'r', encoding=u'utf-8')
        s = f.read(prefix_size)
        self.assertEqual(s, prefix.decode(u'ascii'))
        self.assertEqual(f.tell(), prefix_size)
        self.assertEqual(f.readline(), u_suffix)

    def test_seeking_too(self):
        data = '\xe0\xbf\xbf\n'
        f = self.open(support.TESTFN, u'wb')
        f.write(data)
        f.close()
        f = self.open(support.TESTFN, u'r', encoding=u'utf-8')
        f._CHUNK_SIZE
        f._CHUNK_SIZE = 2
        f.readline()
        f.tell()

    def test_seek_and_tell(self):
        CHUNK_SIZE = 128

        def test_seek_and_tell_with_data(data, min_pos = 0):
            u"""Tell/seek to various points within a data stream and ensure
            that the decoded data returned by read() is consistent."""
            f = self.open(support.TESTFN, u'wb')
            f.write(data)
            f.close()
            f = self.open(support.TESTFN, encoding=u'test_decoder')
            f._CHUNK_SIZE = CHUNK_SIZE
            decoded = f.read()
            f.close()
            for i in range(min_pos, len(decoded) + 1):
                for j in [1, 5, len(decoded) - i]:
                    f = self.open(support.TESTFN, encoding=u'test_decoder')
                    self.assertEqual(f.read(i), decoded[:i])
                    cookie = f.tell()
                    self.assertEqual(f.read(j), decoded[i:i + j])
                    f.seek(cookie)
                    self.assertEqual(f.read(), decoded[i:])
                    f.close()

        StatefulIncrementalDecoder.codecEnabled = 1
        try:
            for input, _, _ in StatefulIncrementalDecoderTest.test_cases:
                test_seek_and_tell_with_data(input)

            for input, _, _ in StatefulIncrementalDecoderTest.test_cases:
                offset = CHUNK_SIZE - len(input) // 2
                prefix = '.' * offset
                min_pos = offset * 2
                test_seek_and_tell_with_data(prefix + input, min_pos)

        finally:
            StatefulIncrementalDecoder.codecEnabled = 0

    def test_encoded_writes(self):
        data = u'1234567890'
        tests = (u'utf-16', u'utf-16-le', u'utf-16-be', u'utf-32', u'utf-32-le', u'utf-32-be')
        for encoding in tests:
            buf = self.BytesIO()
            f = self.TextIOWrapper(buf, encoding=encoding)
            f.write(data)
            f.write(data)
            f.seek(0)
            self.assertEqual(f.read(), data * 2)
            f.seek(0)
            self.assertEqual(f.read(), data * 2)
            self.assertEqual(buf.getvalue(), (data * 2).encode(encoding))

    def test_unreadable(self):

        class UnReadable(self.BytesIO):

            def readable(self):
                return False

        txt = self.TextIOWrapper(UnReadable())
        self.assertRaises(IOError, txt.read)

    def test_read_one_by_one(self):
        txt = self.TextIOWrapper(self.BytesIO('AA\r\nBB'))
        reads = u''
        while True:
            c = txt.read(1)
            if not c:
                break
            reads += c

        self.assertEqual(reads, u'AA\nBB')

    def test_readlines(self):
        txt = self.TextIOWrapper(self.BytesIO('AA\nBB\nCC'))
        self.assertEqual(txt.readlines(), [u'AA\n', u'BB\n', u'CC'])
        txt.seek(0)
        self.assertEqual(txt.readlines(None), [u'AA\n', u'BB\n', u'CC'])
        txt.seek(0)
        self.assertEqual(txt.readlines(5), [u'AA\n', u'BB\n'])
        return

    def test_read_by_chunk(self):
        txt = self.TextIOWrapper(self.BytesIO('A' * 127 + '\r\nB'))
        reads = u''
        while True:
            c = txt.read(128)
            if not c:
                break
            reads += c

        self.assertEqual(reads, u'A' * 127 + u'\nB')

    def test_issue1395_1(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        reads = u''
        while True:
            c = txt.read(1)
            if not c:
                break
            reads += c

        self.assertEqual(reads, self.normalized)

    def test_issue1395_2(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        txt._CHUNK_SIZE = 4
        reads = u''
        while True:
            c = txt.read(4)
            if not c:
                break
            reads += c

        self.assertEqual(reads, self.normalized)

    def test_issue1395_3(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        txt._CHUNK_SIZE = 4
        reads = txt.read(4)
        reads += txt.read(4)
        reads += txt.readline()
        reads += txt.readline()
        reads += txt.readline()
        self.assertEqual(reads, self.normalized)

    def test_issue1395_4(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        txt._CHUNK_SIZE = 4
        reads = txt.read(4)
        reads += txt.read()
        self.assertEqual(reads, self.normalized)

    def test_issue1395_5(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        txt._CHUNK_SIZE = 4
        reads = txt.read(4)
        pos = txt.tell()
        txt.seek(0)
        txt.seek(pos)
        self.assertEqual(txt.read(4), u'BBB\n')

    def test_issue2282(self):
        buffer = self.BytesIO(self.testdata)
        txt = self.TextIOWrapper(buffer, encoding=u'ascii')
        self.assertEqual(buffer.seekable(), txt.seekable())

    def test_append_bom(self):
        filename = support.TESTFN
        for charset in (u'utf-8-sig', u'utf-16', u'utf-32'):
            with self.open(filename, u'w', encoding=charset) as f:
                f.write(u'aaa')
                pos = f.tell()
            with self.open(filename, u'rb') as f:
                self.assertEqual(f.read(), u'aaa'.encode(charset))
            with self.open(filename, u'a', encoding=charset) as f:
                f.write(u'xxx')
            with self.open(filename, u'rb') as f:
                self.assertEqual(f.read(), u'aaaxxx'.encode(charset))

    def test_seek_bom(self):
        filename = support.TESTFN
        for charset in (u'utf-8-sig', u'utf-16', u'utf-32'):
            with self.open(filename, u'w', encoding=charset) as f:
                f.write(u'aaa')
                pos = f.tell()
            with self.open(filename, u'r+', encoding=charset) as f:
                f.seek(pos)
                f.write(u'zzz')
                f.seek(0)
                f.write(u'bbb')
            with self.open(filename, u'rb') as f:
                self.assertEqual(f.read(), u'bbbzzz'.encode(charset))

    def test_errors_property(self):
        with self.open(support.TESTFN, u'w') as f:
            self.assertEqual(f.errors, u'strict')
        with self.open(support.TESTFN, u'w', errors=u'replace') as f:
            self.assertEqual(f.errors, u'replace')

    @unittest.skipUnless(threading, u'Threading required for this test.')
    def test_threads_write(self):
        event = threading.Event()
        with self.open(support.TESTFN, u'w', buffering=1) as f:

            def run(n):
                text = u'Thread%03d\n' % n
                event.wait()
                f.write(text)

            threads = [ threading.Thread(target=lambda n = x: run(n)) for x in range(20) ]
            for t in threads:
                t.start()

            time.sleep(0.02)
            event.set()
            for t in threads:
                t.join()

        with self.open(support.TESTFN) as f:
            content = f.read()
            for n in range(20):
                self.assertEqual(content.count(u'Thread%03d\n' % n), 1)

    def test_flush_error_on_close(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')

        def bad_flush():
            raise IOError()

        txt.flush = bad_flush
        self.assertRaises(IOError, txt.close)

    def test_multi_close(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        txt.close()
        txt.close()
        txt.close()
        self.assertRaises(ValueError, txt.flush)

    def test_readonly_attributes(self):
        txt = self.TextIOWrapper(self.BytesIO(self.testdata), encoding=u'ascii')
        buf = self.BytesIO(self.testdata)
        with self.assertRaises((AttributeError, TypeError)):
            txt.buffer = buf


class CTextIOWrapperTest(TextIOWrapperTest):

    def test_initialization(self):
        r = self.BytesIO('\xc3\xa9\n\n')
        b = self.BufferedReader(r, 1000)
        t = self.TextIOWrapper(b)
        self.assertRaises(TypeError, t.__init__, b, newline=42)
        self.assertRaises(ValueError, t.read)
        self.assertRaises(ValueError, t.__init__, b, newline=u'xyzzy')
        self.assertRaises(ValueError, t.read)

    def test_garbage_collection(self):
        rawio = io.FileIO(support.TESTFN, u'wb')
        b = self.BufferedWriter(rawio)
        t = self.TextIOWrapper(b, encoding=u'ascii')
        t.write(u'456def')
        t.x = t
        wr = weakref.ref(t)
        del t
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        with self.open(support.TESTFN, u'rb') as f:
            self.assertEqual(f.read(), '456def')
        return

    def test_rwpair_cleared_before_textio(self):
        for i in range(1000):
            b1 = self.BufferedRWPair(self.MockRawIO(), self.MockRawIO())
            t1 = self.TextIOWrapper(b1, encoding=u'ascii')
            b2 = self.BufferedRWPair(self.MockRawIO(), self.MockRawIO())
            t2 = self.TextIOWrapper(b2, encoding=u'ascii')
            t1.buddy = t2
            t2.buddy = t1

        support.gc_collect()


class PyTextIOWrapperTest(TextIOWrapperTest):
    pass


class IncrementalNewlineDecoderTest(unittest.TestCase):

    def check_newline_decoding_utf8(self, decoder):

        def _check_decode(b, s, **kwargs):
            state = decoder.getstate()
            self.assertEqual(decoder.decode(b, **kwargs), s)
            decoder.setstate(state)
            self.assertEqual(decoder.decode(b, **kwargs), s)

        _check_decode('\xe8\xa2\x88', u'\u8888')
        _check_decode('\xe8', u'')
        _check_decode('\xa2', u'')
        _check_decode('\x88', u'\u8888')
        _check_decode('\xe8', u'')
        _check_decode('\xa2', u'')
        _check_decode('\x88', u'\u8888')
        _check_decode('\xe8', u'')
        self.assertRaises(UnicodeDecodeError, decoder.decode, '', final=True)
        decoder.reset()
        _check_decode('\n', u'\n')
        _check_decode('\r', u'')
        _check_decode('', u'\n', final=True)
        _check_decode('\r', u'\n', final=True)
        _check_decode('\r', u'')
        _check_decode('a', u'\na')
        _check_decode('\r\r\n', u'\n\n')
        _check_decode('\r', u'')
        _check_decode('\r', u'\n')
        _check_decode('\na', u'\na')
        _check_decode('\xe8\xa2\x88\r\n', u'\u8888\n')
        _check_decode('\xe8\xa2\x88', u'\u8888')
        _check_decode('\n', u'\n')
        _check_decode('\xe8\xa2\x88\r', u'\u8888')
        _check_decode('\n', u'\n')

    def check_newline_decoding(self, decoder, encoding):
        result = []
        if encoding is not None:
            encoder = codecs.getincrementalencoder(encoding)()

            def _decode_bytewise(s):
                for b in encoder.encode(s):
                    result.append(decoder.decode(b))

        else:
            encoder = None

            def _decode_bytewise(s):
                for c in s:
                    result.append(decoder.decode(c))

        self.assertEqual(decoder.newlines, None)
        _decode_bytewise(u'abc\n\r')
        self.assertEqual(decoder.newlines, u'\n')
        _decode_bytewise(u'\nabc')
        self.assertEqual(decoder.newlines, (u'\n', u'\r\n'))
        _decode_bytewise(u'abc\r')
        self.assertEqual(decoder.newlines, (u'\n', u'\r\n'))
        _decode_bytewise(u'abc')
        self.assertEqual(decoder.newlines, (u'\r', u'\n', u'\r\n'))
        _decode_bytewise(u'abc\r')
        self.assertEqual(u''.join(result), u'abc\n\nabcabc\nabcabc')
        decoder.reset()
        input = u'abc'
        if encoder is not None:
            encoder.reset()
            input = encoder.encode(input)
        self.assertEqual(decoder.decode(input), u'abc')
        self.assertEqual(decoder.newlines, None)
        return

    def test_newline_decoder(self):
        encodings = (None, u'utf-8', u'latin-1', u'utf-16', u'utf-16-le', u'utf-16-be', u'utf-32', u'utf-32-le', u'utf-32-be')
        for enc in encodings:
            decoder = enc and codecs.getincrementaldecoder(enc)()
            decoder = self.IncrementalNewlineDecoder(decoder, translate=True)
            self.check_newline_decoding(decoder, enc)

        decoder = codecs.getincrementaldecoder(u'utf-8')()
        decoder = self.IncrementalNewlineDecoder(decoder, translate=True)
        self.check_newline_decoding_utf8(decoder)
        return None

    def test_newline_bytes(self):

        def _check(dec):
            self.assertEqual(dec.newlines, None)
            self.assertEqual(dec.decode(u'\u0d00'), u'\u0d00')
            self.assertEqual(dec.newlines, None)
            self.assertEqual(dec.decode(u'\u0a00'), u'\u0a00')
            self.assertEqual(dec.newlines, None)
            return

        dec = self.IncrementalNewlineDecoder(None, translate=False)
        _check(dec)
        dec = self.IncrementalNewlineDecoder(None, translate=True)
        _check(dec)
        return


class CIncrementalNewlineDecoderTest(IncrementalNewlineDecoderTest):
    pass


class PyIncrementalNewlineDecoderTest(IncrementalNewlineDecoderTest):
    pass


class MiscIOTest(unittest.TestCase):

    def tearDown(self):
        support.unlink(support.TESTFN)

    def test___all__(self):
        for name in self.io.__all__:
            obj = getattr(self.io, name, None)
            self.assertTrue(obj is not None, name)
            if name == u'open':
                continue
            elif u'error' in name.lower() or name == u'UnsupportedOperation':
                self.assertTrue(issubclass(obj, Exception), name)
            elif not name.startswith(u'SEEK_'):
                self.assertTrue(issubclass(obj, self.IOBase))

        return

    def test_attributes(self):
        f = self.open(support.TESTFN, u'wb', buffering=0)
        self.assertEqual(f.mode, u'wb')
        f.close()
        f = self.open(support.TESTFN, u'U')
        self.assertEqual(f.name, support.TESTFN)
        self.assertEqual(f.buffer.name, support.TESTFN)
        self.assertEqual(f.buffer.raw.name, support.TESTFN)
        self.assertEqual(f.mode, u'U')
        self.assertEqual(f.buffer.mode, u'rb')
        self.assertEqual(f.buffer.raw.mode, u'rb')
        f.close()
        f = self.open(support.TESTFN, u'w+')
        self.assertEqual(f.mode, u'w+')
        self.assertEqual(f.buffer.mode, u'rb+')
        self.assertEqual(f.buffer.raw.mode, u'rb+')
        g = self.open(f.fileno(), u'wb', closefd=False)
        self.assertEqual(g.mode, u'wb')
        self.assertEqual(g.raw.mode, u'wb')
        self.assertEqual(g.name, f.fileno())
        self.assertEqual(g.raw.name, f.fileno())
        f.close()
        g.close()

    def test_io_after_close(self):
        for kwargs in [{u'mode': u'w'},
         {u'mode': u'wb'},
         {u'mode': u'w',
          u'buffering': 1},
         {u'mode': u'w',
          u'buffering': 2},
         {u'mode': u'wb',
          u'buffering': 0},
         {u'mode': u'r'},
         {u'mode': u'rb'},
         {u'mode': u'r',
          u'buffering': 1},
         {u'mode': u'r',
          u'buffering': 2},
         {u'mode': u'rb',
          u'buffering': 0},
         {u'mode': u'w+'},
         {u'mode': u'w+b'},
         {u'mode': u'w+',
          u'buffering': 1},
         {u'mode': u'w+',
          u'buffering': 2},
         {u'mode': u'w+b',
          u'buffering': 0}]:
            f = self.open(support.TESTFN, **kwargs)
            f.close()
            self.assertRaises(ValueError, f.flush)
            self.assertRaises(ValueError, f.fileno)
            self.assertRaises(ValueError, f.isatty)
            self.assertRaises(ValueError, f.__iter__)
            if hasattr(f, u'peek'):
                self.assertRaises(ValueError, f.peek, 1)
            self.assertRaises(ValueError, f.read)
            if hasattr(f, u'read1'):
                self.assertRaises(ValueError, f.read1, 1024)
            if hasattr(f, u'readall'):
                self.assertRaises(ValueError, f.readall)
            if hasattr(f, u'readinto'):
                self.assertRaises(ValueError, f.readinto, bytearray(1024))
            self.assertRaises(ValueError, f.readline)
            self.assertRaises(ValueError, f.readlines)
            self.assertRaises(ValueError, f.seek, 0)
            self.assertRaises(ValueError, f.tell)
            self.assertRaises(ValueError, f.truncate)
            self.assertRaises(ValueError, f.write, '' if u'b' in kwargs[u'mode'] else u'')
            self.assertRaises(ValueError, f.writelines, [])
            self.assertRaises(ValueError, next, f)

    def test_blockingioerror(self):
        self.assertRaises(TypeError, self.BlockingIOError)
        self.assertRaises(TypeError, self.BlockingIOError, 1)
        self.assertRaises(TypeError, self.BlockingIOError, 1, 2, 3, 4)
        self.assertRaises(TypeError, self.BlockingIOError, 1, u'', None)
        b = self.BlockingIOError(1, u'')
        self.assertEqual(b.characters_written, 0)

        class C(unicode):
            pass

        c = C(u'')
        b = self.BlockingIOError(1, c)
        c.b = b
        b.c = c
        wr = weakref.ref(c)
        del c
        del b
        support.gc_collect()
        self.assertTrue(wr() is None, wr)
        return

    def test_abcs(self):
        self.assertIsInstance(self.IOBase, abc.ABCMeta)
        self.assertIsInstance(self.RawIOBase, abc.ABCMeta)
        self.assertIsInstance(self.BufferedIOBase, abc.ABCMeta)
        self.assertIsInstance(self.TextIOBase, abc.ABCMeta)

    def _check_abc_inheritance(self, abcmodule):
        with self.open(support.TESTFN, u'wb', buffering=0) as f:
            self.assertIsInstance(f, abcmodule.IOBase)
            self.assertIsInstance(f, abcmodule.RawIOBase)
            self.assertNotIsInstance(f, abcmodule.BufferedIOBase)
            self.assertNotIsInstance(f, abcmodule.TextIOBase)
        with self.open(support.TESTFN, u'wb') as f:
            self.assertIsInstance(f, abcmodule.IOBase)
            self.assertNotIsInstance(f, abcmodule.RawIOBase)
            self.assertIsInstance(f, abcmodule.BufferedIOBase)
            self.assertNotIsInstance(f, abcmodule.TextIOBase)
        with self.open(support.TESTFN, u'w') as f:
            self.assertIsInstance(f, abcmodule.IOBase)
            self.assertNotIsInstance(f, abcmodule.RawIOBase)
            self.assertNotIsInstance(f, abcmodule.BufferedIOBase)
            self.assertIsInstance(f, abcmodule.TextIOBase)

    def test_abc_inheritance(self):
        self._check_abc_inheritance(self)

    def test_abc_inheritance_official(self):
        self._check_abc_inheritance(io)

    @unittest.skipUnless(fcntl, u'fcntl required for this test')
    def test_nonblock_pipe_write_bigbuf(self):
        self._test_nonblock_pipe_write(16384)

    @unittest.skipUnless(fcntl, u'fcntl required for this test')
    def test_nonblock_pipe_write_smallbuf(self):
        self._test_nonblock_pipe_write(1024)

    def _set_non_blocking(self, fd):
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        self.assertNotEqual(flags, -1)
        res = fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        self.assertEqual(res, 0)

    def _test_nonblock_pipe_write(self, bufsize):
        sent = []
        received = []
        r, w = os.pipe()
        self._set_non_blocking(r)
        self._set_non_blocking(w)
        rf = self.open(r, mode=u'rb', closefd=True, buffering=bufsize)
        wf = self.open(w, mode=u'wb', closefd=True, buffering=bufsize)
        with rf:
            with wf:
                for N in (9999, 73, 7574):
                    try:
                        i = 0
                        while True:
                            msg = bytes([i % 26 + 97]) * N
                            sent.append(msg)
                            wf.write(msg)
                            i += 1

                    except self.BlockingIOError as e:
                        self.assertEqual(e.args[0], errno.EAGAIN)
                        sent[-1] = sent[-1][:e.characters_written]
                        received.append(rf.read())
                        msg = 'BLOCKED'
                        wf.write(msg)
                        sent.append(msg)

                while True:
                    try:
                        wf.flush()
                        break
                    except self.BlockingIOError as e:
                        self.assertEqual(e.args[0], errno.EAGAIN)
                        self.assertEqual(e.characters_written, 0)
                        received.append(rf.read())

                received += iter(rf.read, None)
        sent, received = ''.join(sent), ''.join(received)
        self.assertTrue(sent == received)
        self.assertTrue(wf.closed)
        self.assertTrue(rf.closed)
        return


class CMiscIOTest(MiscIOTest):
    io = io


class PyMiscIOTest(MiscIOTest):
    io = pyio


@unittest.skipIf(os.name == u'nt', u'POSIX signals required for this test.')

class SignalsTest(unittest.TestCase):

    def setUp(self):
        self.oldalrm = signal.signal(signal.SIGALRM, self.alarm_interrupt)

    def tearDown(self):
        signal.signal(signal.SIGALRM, self.oldalrm)

    def alarm_interrupt(self, sig, frame):
        1 // 0

    @unittest.skipUnless(threading, u'Threading required for this test.')
    @unittest.skipIf(sys.platform in (u'freebsd5', u'freebsd6', u'freebsd7'), u'issue #12429: skip test on FreeBSD <= 7')
    def check_interrupted_write(self, item, bytes, **fdopen_kwargs):
        u"""Check that a partial write, when it gets interrupted, properly
        invokes the signal handler, and bubbles up the exception raised
        in the latter."""
        read_results = []

        def _read():
            s = os.read(r, 1)
            read_results.append(s)

        t = threading.Thread(target=_read)
        t.daemon = True
        r, w = os.pipe()
        try:
            wio = self.io.open(w, **fdopen_kwargs)
            t.start()
            signal.alarm(1)
            self.assertRaises(ZeroDivisionError, wio.write, item * 1048576)
            t.join()
            read_results.append(os.read(r, 1))
            self.assertEqual(read_results, [bytes[0:1], bytes[1:2]])
        finally:
            os.close(w)
            os.close(r)
            try:
                wio.close()
            except IOError as e:
                if e.errno != errno.EBADF:
                    raise

    def test_interrupted_write_unbuffered(self):
        self.check_interrupted_write('xy', 'xy', mode=u'wb', buffering=0)

    def test_interrupted_write_buffered(self):
        self.check_interrupted_write('xy', 'xy', mode=u'wb')

    def test_interrupted_write_text(self):
        self.check_interrupted_write(u'xy', 'xy', mode=u'w', encoding=u'ascii')

    def check_reentrant_write--- This code section failed: ---

0	LOAD_CLOSURE      'data'
3	LOAD_CLOSURE      'wio'
9	LOAD_CONST        '<code_object on_alarm>'
12	MAKE_CLOSURE_0    None
15	STORE_FAST        'on_alarm'

18	LOAD_GLOBAL       'signal'
21	LOAD_ATTR         'signal'
24	LOAD_GLOBAL       'signal'
27	LOAD_ATTR         'SIGALRM'
30	LOAD_FAST         'on_alarm'
33	CALL_FUNCTION_2   None
36	POP_TOP           None

37	LOAD_GLOBAL       'os'
40	LOAD_ATTR         'pipe'
43	CALL_FUNCTION_0   None
46	UNPACK_SEQUENCE_2 None
49	STORE_FAST        'r'
52	STORE_FAST        'w'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'io'
61	LOAD_ATTR         'open'
64	LOAD_FAST         'w'
67	LOAD_FAST         'fdopen_kwargs'
70	CALL_FUNCTION_KW_1 None
73	STORE_DEREF       'wio'

76	SETUP_FINALLY     '269'

79	LOAD_GLOBAL       'signal'
82	LOAD_ATTR         'alarm'
85	LOAD_CONST        1
88	CALL_FUNCTION_1   None
91	POP_TOP           None

92	LOAD_FAST         'self'
95	LOAD_ATTR         'assertRaises'
98	LOAD_GLOBAL       'ZeroDivisionError'
101	LOAD_GLOBAL       'RuntimeError'
104	BUILD_TUPLE_2     None
107	CALL_FUNCTION_1   None
110	SETUP_WITH        '199'
113	STORE_FAST        'cm'

116	SETUP_LOOP        '195'

119	SETUP_LOOP        '165'
122	LOAD_GLOBAL       'range'
125	LOAD_CONST        100
128	CALL_FUNCTION_1   None
131	GET_ITER          None
132	FOR_ITER          '164'
135	STORE_FAST        'i'

138	LOAD_DEREF        'wio'
141	LOAD_ATTR         'write'
144	LOAD_DEREF        'data'
147	CALL_FUNCTION_1   None
150	POP_TOP           None

151	LOAD_DEREF        'wio'
154	LOAD_ATTR         'flush'
157	CALL_FUNCTION_0   None
160	POP_TOP           None
161	JUMP_BACK         '132'
164	POP_BLOCK         None
165_0	COME_FROM         '119'

165	LOAD_GLOBAL       'os'
168	LOAD_ATTR         'read'
171	LOAD_FAST         'r'
174	LOAD_GLOBAL       'len'
177	LOAD_DEREF        'data'
180	CALL_FUNCTION_1   None
183	LOAD_CONST        100
186	BINARY_MULTIPLY   None
187	CALL_FUNCTION_2   None
190	POP_TOP           None
191	JUMP_BACK         '119'
194	POP_BLOCK         None
195_0	COME_FROM         '116'
195	POP_BLOCK         None
196	LOAD_CONST        None
199_0	COME_FROM         '110'
199	WITH_CLEANUP      None
200	END_FINALLY       None

201	LOAD_FAST         'cm'
204	LOAD_ATTR         'exception'
207	STORE_FAST        'exc'

210	LOAD_GLOBAL       'isinstance'
213	LOAD_FAST         'exc'
216	LOAD_GLOBAL       'RuntimeError'
219	CALL_FUNCTION_2   None
222	POP_JUMP_IF_FALSE '265'

225	LOAD_FAST         'self'
228	LOAD_ATTR         'assertTrue'
231	LOAD_GLOBAL       'str'
234	LOAD_FAST         'exc'
237	CALL_FUNCTION_1   None
240	LOAD_ATTR         'startswith'
243	LOAD_CONST        u'reentrant call'
246	CALL_FUNCTION_1   None
249	LOAD_GLOBAL       'str'
252	LOAD_FAST         'exc'
255	CALL_FUNCTION_1   None
258	CALL_FUNCTION_2   None
261	POP_TOP           None
262	JUMP_FORWARD      '265'
265_0	COME_FROM         '262'
265	POP_BLOCK         None
266	LOAD_CONST        None
269_0	COME_FROM         '76'

269	LOAD_DEREF        'wio'
272	LOAD_ATTR         'close'
275	CALL_FUNCTION_0   None
278	POP_TOP           None

279	LOAD_GLOBAL       'os'
282	LOAD_ATTR         'close'
285	LOAD_FAST         'r'
288	CALL_FUNCTION_1   None
291	POP_TOP           None
292	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 194

    def test_reentrant_write_buffered(self):
        self.check_reentrant_write('xy', mode=u'wb')

    def test_reentrant_write_text(self):
        self.check_reentrant_write(u'xy', mode=u'w', encoding=u'ascii')

    def check_interrupted_read_retry(self, decode, **fdopen_kwargs):
        u"""Check that a buffered read, when it gets interrupted (either
        returning a partial result or EINTR), properly invokes the signal
        handler and retries if the latter returned successfully."""
        r, w = os.pipe()
        fdopen_kwargs[u'closefd'] = False

        def alarm_handler(sig, frame):
            os.write(w, 'bar')

        signal.signal(signal.SIGALRM, alarm_handler)
        try:
            rio = self.io.open(r, **fdopen_kwargs)
            os.write(w, 'foo')
            signal.alarm(1)
            self.assertEqual(decode(rio.read(6)), u'foobar')
        finally:
            rio.close()
            os.close(w)
            os.close(r)

    def test_interrupterd_read_retry_buffered(self):
        self.check_interrupted_read_retry(lambda x: x.decode(u'latin1'), mode=u'rb')

    def test_interrupterd_read_retry_text(self):
        self.check_interrupted_read_retry(lambda x: x, mode=u'r')

    @unittest.skipUnless(threading, u'Threading required for this test.')
    def check_interrupted_write_retry(self, item, **fdopen_kwargs):
        u"""Check that a buffered write, when it gets interrupted (either
        returning a partial result or EINTR), properly invokes the signal
        handler and retries if the latter returned successfully."""
        select = support.import_module(u'select')
        N = 1048576
        r, w = os.pipe()
        fdopen_kwargs[u'closefd'] = False
        read_results = []
        write_finished = False

        def _read():
            while not write_finished:
                while r in select.select([r], [], [], 1.0)[0]:
                    s = os.read(r, 1024)
                    read_results.append(s)

        t = threading.Thread(target=_read)
        t.daemon = True

        def alarm1(sig, frame):
            signal.signal(signal.SIGALRM, alarm2)
            signal.alarm(1)

        def alarm2(sig, frame):
            t.start()

        signal.signal(signal.SIGALRM, alarm1)
        try:
            wio = self.io.open(w, **fdopen_kwargs)
            signal.alarm(1)
            self.assertEqual(N, wio.write(item * N))
            wio.flush()
            write_finished = True
            t.join()
            self.assertEqual(N, sum((len(x) for x in read_results)))
        finally:
            write_finished = True
            os.close(w)
            os.close(r)
            try:
                wio.close()
            except IOError as e:
                if e.errno != errno.EBADF:
                    raise

    def test_interrupterd_write_retry_buffered(self):
        self.check_interrupted_write_retry('x', mode=u'wb')

    def test_interrupterd_write_retry_text(self):
        self.check_interrupted_write_retry(u'x', mode=u'w', encoding=u'latin1')


class CSignalsTest(SignalsTest):
    io = io


class PySignalsTest(SignalsTest):
    io = pyio
    test_reentrant_write_buffered = None
    test_reentrant_write_text = None


def test_main():
    tests = (CIOTest,
     PyIOTest,
     CBufferedReaderTest,
     PyBufferedReaderTest,
     CBufferedWriterTest,
     PyBufferedWriterTest,
     CBufferedRWPairTest,
     PyBufferedRWPairTest,
     CBufferedRandomTest,
     PyBufferedRandomTest,
     StatefulIncrementalDecoderTest,
     CIncrementalNewlineDecoderTest,
     PyIncrementalNewlineDecoderTest,
     CTextIOWrapperTest,
     PyTextIOWrapperTest,
     CMiscIOTest,
     PyMiscIOTest,
     CSignalsTest,
     PySignalsTest)
    mocks = (MockRawIO,
     MisbehavedRawIO,
     MockFileIO,
     CloseFailureIO,
     MockNonBlockWriterIO,
     MockRawIOWithoutRead)
    all_members = io.__all__ + [u'IncrementalNewlineDecoder']
    c_io_ns = dict(((name, getattr(io, name)) for name in all_members))
    py_io_ns = dict(((name, getattr(pyio, name)) for name in all_members))
    globs = globals()
    c_io_ns.update(((x.__name__, globs[u'C' + x.__name__]) for x in mocks))
    py_io_ns.update(((x.__name__, globs[u'Py' + x.__name__]) for x in mocks))
    py_io_ns[u'open'] = pyio.OpenWrapper
    for test in tests:
        if test.__name__.startswith(u'C'):
            for name, obj in c_io_ns.items():
                setattr(test, name, obj)

        elif test.__name__.startswith(u'Py'):
            for name, obj in py_io_ns.items():
                setattr(test, name, obj)

    support.run_unittest(*tests)


if __name__ == u'__main__':
    test_main()