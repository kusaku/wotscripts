# Embedded file name: scripts/common/Lib/test/test_memoryio.py
u"""Unit tests for memory-based file-like objects.
StringIO -- for unicode strings
BytesIO -- for bytes
"""
from __future__ import unicode_literals
from __future__ import print_function
import unittest
from test import test_support as support
import io
import _pyio as pyio
import pickle

class MemorySeekTestMixin():

    def testInit(self):
        buf = self.buftype(u'1234567890')
        bytesIo = self.ioclass(buf)

    def testRead(self):
        buf = self.buftype(u'1234567890')
        bytesIo = self.ioclass(buf)
        self.assertEqual(buf[:1], bytesIo.read(1))
        self.assertEqual(buf[1:5], bytesIo.read(4))
        self.assertEqual(buf[5:], bytesIo.read(900))
        self.assertEqual(self.EOF, bytesIo.read())

    def testReadNoArgs(self):
        buf = self.buftype(u'1234567890')
        bytesIo = self.ioclass(buf)
        self.assertEqual(buf, bytesIo.read())
        self.assertEqual(self.EOF, bytesIo.read())

    def testSeek(self):
        buf = self.buftype(u'1234567890')
        bytesIo = self.ioclass(buf)
        bytesIo.read(5)
        bytesIo.seek(0)
        self.assertEqual(buf, bytesIo.read())
        bytesIo.seek(3)
        self.assertEqual(buf[3:], bytesIo.read())
        self.assertRaises(TypeError, bytesIo.seek, 0.0)

    def testTell(self):
        buf = self.buftype(u'1234567890')
        bytesIo = self.ioclass(buf)
        self.assertEqual(0, bytesIo.tell())
        bytesIo.seek(5)
        self.assertEqual(5, bytesIo.tell())
        bytesIo.seek(10000)
        self.assertEqual(10000, bytesIo.tell())


class MemoryTestMixin():

    def test_detach(self):
        buf = self.ioclass()
        self.assertRaises(self.UnsupportedOperation, buf.detach)

    def write_ops(self, f, t):
        self.assertEqual(f.write(t(u'blah.')), 5)
        self.assertEqual(f.seek(0), 0)
        self.assertEqual(f.write(t(u'Hello.')), 6)
        self.assertEqual(f.tell(), 6)
        self.assertEqual(f.seek(5), 5)
        self.assertEqual(f.tell(), 5)
        self.assertEqual(f.write(t(u' world\n\n\n')), 9)
        self.assertEqual(f.seek(0), 0)
        self.assertEqual(f.write(t(u'h')), 1)
        self.assertEqual(f.truncate(12), 12)
        self.assertEqual(f.tell(), 1)

    def test_write(self):
        buf = self.buftype(u'hello world\n')
        memio = self.ioclass(buf)
        self.write_ops(memio, self.buftype)
        self.assertEqual(memio.getvalue(), buf)
        memio = self.ioclass()
        self.write_ops(memio, self.buftype)
        self.assertEqual(memio.getvalue(), buf)
        self.assertRaises(TypeError, memio.write, None)
        memio.close()
        self.assertRaises(ValueError, memio.write, self.buftype(u''))
        return

    def test_writelines(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass()
        self.assertEqual(memio.writelines([buf] * 100), None)
        self.assertEqual(memio.getvalue(), buf * 100)
        memio.writelines([])
        self.assertEqual(memio.getvalue(), buf * 100)
        memio = self.ioclass()
        self.assertRaises(TypeError, memio.writelines, [buf] + [1])
        self.assertEqual(memio.getvalue(), buf)
        self.assertRaises(TypeError, memio.writelines, None)
        memio.close()
        self.assertRaises(ValueError, memio.writelines, [])
        return

    def test_writelines_error(self):
        memio = self.ioclass()

        def error_gen():
            yield self.buftype(u'spam')
            raise KeyboardInterrupt

        self.assertRaises(KeyboardInterrupt, memio.writelines, error_gen())

    def test_truncate(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertRaises(ValueError, memio.truncate, -1)
        memio.seek(6)
        self.assertEqual(memio.truncate(), 6)
        self.assertEqual(memio.getvalue(), buf[:6])
        self.assertEqual(memio.truncate(4), 4)
        self.assertEqual(memio.getvalue(), buf[:4])
        self.assertEqual(memio.truncate(4L), 4)
        self.assertEqual(memio.getvalue(), buf[:4])
        self.assertEqual(memio.tell(), 6)
        memio.seek(0, 2)
        memio.write(buf)
        self.assertEqual(memio.getvalue(), buf[:4] + buf)
        pos = memio.tell()
        self.assertEqual(memio.truncate(None), pos)
        self.assertEqual(memio.tell(), pos)
        self.assertRaises(TypeError, memio.truncate, u'0')
        memio.close()
        self.assertRaises(ValueError, memio.truncate, 0)
        return

    def test_init(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.getvalue(), buf)
        memio = self.ioclass(None)
        self.assertEqual(memio.getvalue(), self.EOF)
        memio.__init__(buf * 2)
        self.assertEqual(memio.getvalue(), buf * 2)
        memio.__init__(buf)
        self.assertEqual(memio.getvalue(), buf)
        return

    def test_read(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.read(0), self.EOF)
        self.assertEqual(memio.read(1), buf[:1])
        self.assertEqual(memio.read(4L), buf[1:5])
        self.assertEqual(memio.read(900), buf[5:])
        self.assertEqual(memio.read(), self.EOF)
        memio.seek(0)
        self.assertEqual(memio.read(), buf)
        self.assertEqual(memio.read(), self.EOF)
        self.assertEqual(memio.tell(), 10)
        memio.seek(0)
        self.assertEqual(memio.read(-1), buf)
        memio.seek(0)
        self.assertEqual(type(memio.read()), type(buf))
        memio.seek(100)
        self.assertEqual(type(memio.read()), type(buf))
        memio.seek(0)
        self.assertEqual(memio.read(None), buf)
        self.assertRaises(TypeError, memio.read, u'')
        memio.close()
        self.assertRaises(ValueError, memio.read)
        return

    def test_readline(self):
        buf = self.buftype(u'1234567890\n')
        memio = self.ioclass(buf * 2)
        self.assertEqual(memio.readline(0), self.EOF)
        self.assertEqual(memio.readline(), buf)
        self.assertEqual(memio.readline(), buf)
        self.assertEqual(memio.readline(), self.EOF)
        memio.seek(0)
        self.assertEqual(memio.readline(5), buf[:5])
        self.assertEqual(memio.readline(5L), buf[5:10])
        self.assertEqual(memio.readline(5), buf[10:15])
        memio.seek(0)
        self.assertEqual(memio.readline(-1), buf)
        memio.seek(0)
        self.assertEqual(memio.readline(0), self.EOF)
        buf = self.buftype(u'1234567890\n')
        memio = self.ioclass((buf * 3)[:-1])
        self.assertEqual(memio.readline(), buf)
        self.assertEqual(memio.readline(), buf)
        self.assertEqual(memio.readline(), buf[:-1])
        self.assertEqual(memio.readline(), self.EOF)
        memio.seek(0)
        self.assertEqual(type(memio.readline()), type(buf))
        self.assertEqual(memio.readline(), buf)
        self.assertRaises(TypeError, memio.readline, u'')
        memio.close()
        self.assertRaises(ValueError, memio.readline)

    def test_readlines(self):
        buf = self.buftype(u'1234567890\n')
        memio = self.ioclass(buf * 10)
        self.assertEqual(memio.readlines(), [buf] * 10)
        memio.seek(5)
        self.assertEqual(memio.readlines(), [buf[5:]] + [buf] * 9)
        memio.seek(0)
        self.assertEqual(memio.readlines(15L), [buf] * 2)
        memio.seek(0)
        self.assertEqual(memio.readlines(-1), [buf] * 10)
        memio.seek(0)
        self.assertEqual(memio.readlines(0), [buf] * 10)
        memio.seek(0)
        self.assertEqual(type(memio.readlines()[0]), type(buf))
        memio.seek(0)
        self.assertEqual(memio.readlines(None), [buf] * 10)
        self.assertRaises(TypeError, memio.readlines, u'')
        memio.close()
        self.assertRaises(ValueError, memio.readlines)
        return

    def test_iterator(self):
        buf = self.buftype(u'1234567890\n')
        memio = self.ioclass(buf * 10)
        self.assertEqual(iter(memio), memio)
        self.assertTrue(hasattr(memio, u'__iter__'))
        self.assertTrue(hasattr(memio, u'next'))
        i = 0
        for line in memio:
            self.assertEqual(line, buf)
            i += 1

        self.assertEqual(i, 10)
        memio.seek(0)
        i = 0
        for line in memio:
            self.assertEqual(line, buf)
            i += 1

        self.assertEqual(i, 10)
        memio = self.ioclass(buf * 2)
        memio.close()
        self.assertRaises(ValueError, next, memio)

    def test_getvalue(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.getvalue(), buf)
        memio.read()
        self.assertEqual(memio.getvalue(), buf)
        self.assertEqual(type(memio.getvalue()), type(buf))
        memio = self.ioclass(buf * 1000)
        self.assertEqual(memio.getvalue()[-3:], self.buftype(u'890'))
        memio = self.ioclass(buf)
        memio.close()
        self.assertRaises(ValueError, memio.getvalue)

    def test_seek(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        memio.read(5)
        self.assertRaises(ValueError, memio.seek, -1)
        self.assertRaises(ValueError, memio.seek, 1, -1)
        self.assertRaises(ValueError, memio.seek, 1, 3)
        self.assertEqual(memio.seek(0), 0)
        self.assertEqual(memio.seek(0, 0), 0)
        self.assertEqual(memio.read(), buf)
        self.assertEqual(memio.seek(3), 3)
        self.assertEqual(memio.seek(3L), 3)
        self.assertEqual(memio.seek(0, 1), 3)
        self.assertEqual(memio.read(), buf[3:])
        self.assertEqual(memio.seek(len(buf)), len(buf))
        self.assertEqual(memio.read(), self.EOF)
        memio.seek(len(buf) + 1)
        self.assertEqual(memio.read(), self.EOF)
        self.assertEqual(memio.seek(0, 2), len(buf))
        self.assertEqual(memio.read(), self.EOF)
        memio.close()
        self.assertRaises(ValueError, memio.seek, 0)

    def test_overseek(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.seek(len(buf) + 1), 11)
        self.assertEqual(memio.read(), self.EOF)
        self.assertEqual(memio.tell(), 11)
        self.assertEqual(memio.getvalue(), buf)
        memio.write(self.EOF)
        self.assertEqual(memio.getvalue(), buf)
        memio.write(buf)
        self.assertEqual(memio.getvalue(), buf + self.buftype(u'\x00') + buf)

    def test_tell(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.tell(), 0)
        memio.seek(5)
        self.assertEqual(memio.tell(), 5)
        memio.seek(10000)
        self.assertEqual(memio.tell(), 10000)
        memio.close()
        self.assertRaises(ValueError, memio.tell)

    def test_flush(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.flush(), None)
        return

    def test_flags(self):
        memio = self.ioclass()
        self.assertEqual(memio.writable(), True)
        self.assertEqual(memio.readable(), True)
        self.assertEqual(memio.seekable(), True)
        self.assertEqual(memio.isatty(), False)
        self.assertEqual(memio.closed, False)
        memio.close()
        self.assertEqual(memio.writable(), True)
        self.assertEqual(memio.readable(), True)
        self.assertEqual(memio.seekable(), True)
        self.assertRaises(ValueError, memio.isatty)
        self.assertEqual(memio.closed, True)

    def test_subclassing(self):
        buf = self.buftype(u'1234567890')

        def test1():

            class MemIO(self.ioclass):
                pass

            m = MemIO(buf)
            return m.getvalue()

        def test2():

            class MemIO(self.ioclass):

                def __init__(me, a, b):
                    self.ioclass.__init__(me, a)

            m = MemIO(buf, None)
            return m.getvalue()

        self.assertEqual(test1(), buf)
        self.assertEqual(test2(), buf)

    def test_instance_dict_leak(self):
        for _ in range(100):
            memio = self.ioclass()
            memio.foo = 1

    def test_pickling(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        memio.foo = 42
        memio.seek(2)

        class PickleTestMemIO(self.ioclass):

            def __init__(me, initvalue, foo):
                self.ioclass.__init__(me, initvalue)
                me.foo = foo

        import __main__
        PickleTestMemIO.__module__ = u'__main__'
        __main__.PickleTestMemIO = PickleTestMemIO
        submemio = PickleTestMemIO(buf, 80)
        submemio.seek(2)
        for proto in range(2, pickle.HIGHEST_PROTOCOL):
            for obj in (memio, submemio):
                obj2 = pickle.loads(pickle.dumps(obj, protocol=proto))
                self.assertEqual(obj.getvalue(), obj2.getvalue())
                self.assertEqual(obj.__class__, obj2.__class__)
                self.assertEqual(obj.foo, obj2.foo)
                self.assertEqual(obj.tell(), obj2.tell())
                obj.close()
                self.assertRaises(ValueError, pickle.dumps, obj, proto)

        del __main__.PickleTestMemIO


class PyBytesIOTest(MemoryTestMixin, MemorySeekTestMixin, unittest.TestCase):
    UnsupportedOperation = pyio.UnsupportedOperation

    @staticmethod
    def buftype(s):
        return s.encode(u'ascii')

    ioclass = pyio.BytesIO
    EOF = ''

    def test_read1(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertRaises(TypeError, memio.read1)
        self.assertEqual(memio.read(), buf)

    def test_readinto(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        b = bytearray('hello')
        self.assertEqual(memio.readinto(b), 5)
        self.assertEqual(b, '12345')
        self.assertEqual(memio.readinto(b), 5)
        self.assertEqual(b, '67890')
        self.assertEqual(memio.readinto(b), 0)
        self.assertEqual(b, '67890')
        b = bytearray('hello world')
        memio.seek(0)
        self.assertEqual(memio.readinto(b), 10)
        self.assertEqual(b, '1234567890d')
        b = bytearray('')
        memio.seek(0)
        self.assertEqual(memio.readinto(b), 0)
        self.assertEqual(b, '')
        self.assertRaises(TypeError, memio.readinto, u'')
        import array
        a = array.array('b', 'hello world')
        memio = self.ioclass(buf)
        memio.readinto(a)
        self.assertEqual(a.tostring(), '1234567890d')
        memio.close()
        self.assertRaises(ValueError, memio.readinto, b)
        memio = self.ioclass('123')
        b = bytearray()
        memio.seek(42)
        memio.readinto(b)
        self.assertEqual(b, '')

    def test_relative_seek(self):
        buf = self.buftype(u'1234567890')
        memio = self.ioclass(buf)
        self.assertEqual(memio.seek(-1, 1), 0)
        self.assertEqual(memio.seek(3, 1), 3)
        self.assertEqual(memio.seek(-4, 1), 0)
        self.assertEqual(memio.seek(-1, 2), 9)
        self.assertEqual(memio.seek(1, 1), 10)
        self.assertEqual(memio.seek(1, 2), 11)
        memio.seek(-3, 2)
        self.assertEqual(memio.read(), buf[-3:])
        memio.seek(0)
        memio.seek(1, 1)
        self.assertEqual(memio.read(), buf[1:])

    def test_unicode(self):
        memio = self.ioclass()
        self.assertRaises(TypeError, self.ioclass, u'1234567890')
        self.assertRaises(TypeError, memio.write, u'1234567890')
        self.assertRaises(TypeError, memio.writelines, [u'1234567890'])

    def test_bytes_array(self):
        buf = '1234567890'
        import array
        a = array.array('b', buf)
        memio = self.ioclass(a)
        self.assertEqual(memio.getvalue(), buf)
        self.assertEqual(memio.write(a), 10)
        self.assertEqual(memio.getvalue(), buf)

    def test_issue5449(self):
        buf = self.buftype(u'1234567890')
        self.ioclass(initial_bytes=buf)
        self.assertRaises(TypeError, self.ioclass, buf, foo=None)
        return


class TextIOTestMixin():

    def test_newlines_property(self):
        memio = self.ioclass(newline=None)

        def force_decode():
            memio.seek(0)
            memio.read()

        self.assertEqual(memio.newlines, None)
        memio.write(u'a\n')
        force_decode()
        self.assertEqual(memio.newlines, u'\n')
        memio.write(u'b\r\n')
        force_decode()
        self.assertEqual(memio.newlines, (u'\n', u'\r\n'))
        memio.write(u'c\rd')
        force_decode()
        self.assertEqual(memio.newlines, (u'\r', u'\n', u'\r\n'))
        return

    def test_relative_seek(self):
        memio = self.ioclass()
        self.assertRaises(IOError, memio.seek, -1, 1)
        self.assertRaises(IOError, memio.seek, 3, 1)
        self.assertRaises(IOError, memio.seek, -3, 1)
        self.assertRaises(IOError, memio.seek, -1, 2)
        self.assertRaises(IOError, memio.seek, 1, 1)
        self.assertRaises(IOError, memio.seek, 1, 2)

    def test_textio_properties(self):
        memio = self.ioclass()
        self.assertIsNone(memio.encoding)
        self.assertIsNone(memio.errors)
        self.assertFalse(memio.line_buffering)

    def test_newline_none(self):
        memio = self.ioclass(u'a\nb\r\nc\rd', newline=None)
        self.assertEqual(list(memio), [u'a\n',
         u'b\n',
         u'c\n',
         u'd'])
        memio.seek(0)
        self.assertEqual(memio.read(1), u'a')
        self.assertEqual(memio.read(2), u'\nb')
        self.assertEqual(memio.read(2), u'\nc')
        self.assertEqual(memio.read(1), u'\n')
        memio = self.ioclass(newline=None)
        self.assertEqual(2, memio.write(u'a\n'))
        self.assertEqual(3, memio.write(u'b\r\n'))
        self.assertEqual(3, memio.write(u'c\rd'))
        memio.seek(0)
        self.assertEqual(memio.read(), u'a\nb\nc\nd')
        memio = self.ioclass(u'a\r\nb', newline=None)
        self.assertEqual(memio.read(3), u'a\nb')
        return

    def test_newline_empty(self):
        memio = self.ioclass(u'a\nb\r\nc\rd', newline=u'')
        self.assertEqual(list(memio), [u'a\n',
         u'b\r\n',
         u'c\r',
         u'd'])
        memio.seek(0)
        self.assertEqual(memio.read(4), u'a\nb\r')
        self.assertEqual(memio.read(2), u'\nc')
        self.assertEqual(memio.read(1), u'\r')
        memio = self.ioclass(newline=u'')
        self.assertEqual(2, memio.write(u'a\n'))
        self.assertEqual(2, memio.write(u'b\r'))
        self.assertEqual(2, memio.write(u'\nc'))
        self.assertEqual(2, memio.write(u'\rd'))
        memio.seek(0)
        self.assertEqual(list(memio), [u'a\n',
         u'b\r\n',
         u'c\r',
         u'd'])

    def test_newline_lf(self):
        memio = self.ioclass(u'a\nb\r\nc\rd')
        self.assertEqual(list(memio), [u'a\n', u'b\r\n', u'c\rd'])

    def test_newline_cr(self):
        memio = self.ioclass(u'a\nb\r\nc\rd', newline=u'\r')
        self.assertEqual(memio.read(), u'a\rb\r\rc\rd')
        memio.seek(0)
        self.assertEqual(list(memio), [u'a\r',
         u'b\r',
         u'\r',
         u'c\r',
         u'd'])

    def test_newline_crlf(self):
        memio = self.ioclass(u'a\nb\r\nc\rd', newline=u'\r\n')
        self.assertEqual(memio.read(), u'a\r\nb\r\r\nc\rd')
        memio.seek(0)
        self.assertEqual(list(memio), [u'a\r\n', u'b\r\r\n', u'c\rd'])

    def test_issue5265(self):
        memio = self.ioclass(u'a\r\nb\r\n', newline=None)
        self.assertEqual(memio.read(5), u'a\nb\n')
        return


class PyStringIOTest(MemoryTestMixin, MemorySeekTestMixin, TextIOTestMixin, unittest.TestCase):
    buftype = unicode
    ioclass = pyio.StringIO
    UnsupportedOperation = pyio.UnsupportedOperation
    EOF = u''


class PyStringIOPickleTest(TextIOTestMixin, unittest.TestCase):
    u"""Test if pickle restores properly the internal state of StringIO.
    """
    buftype = unicode
    UnsupportedOperation = pyio.UnsupportedOperation
    EOF = u''

    class ioclass(pyio.StringIO):

        def __new__(cls, *args, **kwargs):
            return pickle.loads(pickle.dumps(pyio.StringIO(*args, **kwargs)))

        def __init__(self, *args, **kwargs):
            pass


class CBytesIOTest(PyBytesIOTest):
    ioclass = io.BytesIO
    UnsupportedOperation = io.UnsupportedOperation
    test_bytes_array = unittest.skip(u'array.array() does not have the new buffer API')(PyBytesIOTest.test_bytes_array)

    def test_getstate(self):
        memio = self.ioclass()
        state = memio.__getstate__()
        self.assertEqual(len(state), 3)
        bytearray(state[0])
        self.assertIsInstance(state[1], int)
        self.assertTrue(isinstance(state[2], dict) or state[2] is None)
        memio.close()
        self.assertRaises(ValueError, memio.__getstate__)
        return

    def test_setstate(self):
        memio = self.ioclass()
        memio.__setstate__(('no error', 0, None))
        memio.__setstate__((bytearray('no error'), 0, None))
        memio.__setstate__(('no error', 0, {u'spam': 3}))
        self.assertRaises(ValueError, memio.__setstate__, ('', -1, None))
        self.assertRaises(TypeError, memio.__setstate__, (u'unicode', 0, None))
        self.assertRaises(TypeError, memio.__setstate__, ('', 0.0, None))
        self.assertRaises(TypeError, memio.__setstate__, ('', 0, 0))
        self.assertRaises(TypeError, memio.__setstate__, ('len-test', 0))
        self.assertRaises(TypeError, memio.__setstate__)
        self.assertRaises(TypeError, memio.__setstate__, 0)
        memio.close()
        self.assertRaises(ValueError, memio.__setstate__, ('closed', 0, None))
        return


class CStringIOTest(PyStringIOTest):
    ioclass = io.StringIO
    UnsupportedOperation = io.UnsupportedOperation

    def test_widechar(self):
        buf = self.buftype(u'\U0002030a\U00020347')
        memio = self.ioclass(buf)
        self.assertEqual(memio.getvalue(), buf)
        self.assertEqual(memio.write(buf), len(buf))
        self.assertEqual(memio.tell(), len(buf))
        self.assertEqual(memio.getvalue(), buf)
        self.assertEqual(memio.write(buf), len(buf))
        self.assertEqual(memio.tell(), len(buf) * 2)
        self.assertEqual(memio.getvalue(), buf + buf)

    def test_getstate(self):
        memio = self.ioclass()
        state = memio.__getstate__()
        self.assertEqual(len(state), 4)
        self.assertIsInstance(state[0], unicode)
        self.assertIsInstance(state[1], str)
        self.assertIsInstance(state[2], int)
        self.assertTrue(isinstance(state[3], dict) or state[3] is None)
        memio.close()
        self.assertRaises(ValueError, memio.__getstate__)
        return

    def test_setstate(self):
        memio = self.ioclass()
        memio.__setstate__((u'no error', u'\n', 0, None))
        memio.__setstate__((u'no error',
         u'',
         0,
         {u'spam': 3}))
        self.assertRaises(ValueError, memio.__setstate__, (u'', u'f', 0, None))
        self.assertRaises(ValueError, memio.__setstate__, (u'', u'', -1, None))
        self.assertRaises(TypeError, memio.__setstate__, ('', u'', 0, None))
        self.assertRaises(TypeError, memio.__setstate__, (u'', u'', 0.0, None))
        self.assertRaises(TypeError, memio.__setstate__, (u'', u'', 0, 0))
        self.assertRaises(TypeError, memio.__setstate__, (u'len-test', 0))
        self.assertRaises(TypeError, memio.__setstate__)
        self.assertRaises(TypeError, memio.__setstate__, 0)
        memio.close()
        self.assertRaises(ValueError, memio.__setstate__, (u'closed', u'', 0, None))
        return None


class CStringIOPickleTest(PyStringIOPickleTest):
    UnsupportedOperation = io.UnsupportedOperation

    class ioclass(io.StringIO):

        def __new__(cls, *args, **kwargs):
            return pickle.loads(pickle.dumps(io.StringIO(*args, **kwargs), protocol=2))

        def __init__(self, *args, **kwargs):
            pass


def test_main():
    tests = [PyBytesIOTest,
     PyStringIOTest,
     CBytesIOTest,
     CStringIOTest,
     PyStringIOPickleTest,
     CStringIOPickleTest]
    support.run_unittest(*tests)


if __name__ == u'__main__':
    test_main()