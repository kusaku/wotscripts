# Embedded file name: scripts/common/Lib/test/test_file.py
from __future__ import print_function
import sys
import os
import unittest
from array import array
from weakref import proxy
import io
import _pyio as pyio
from test.test_support import TESTFN, run_unittest
from UserList import UserList

class AutoFileTests(unittest.TestCase):

    def setUp(self):
        self.f = self.open(TESTFN, 'wb')

    def tearDown(self):
        if self.f:
            self.f.close()
        os.remove(TESTFN)

    def testWeakRefs(self):
        p = proxy(self.f)
        p.write('teststring')
        self.assertEqual(self.f.tell(), p.tell())
        self.f.close()
        self.f = None
        self.assertRaises(ReferenceError, getattr, p, 'tell')
        return

    def testAttributes(self):
        f = self.f
        f.name
        f.mode
        f.closed

    def testReadinto(self):
        self.f.write('12')
        self.f.close()
        a = array('b', 'xxxxxxxxxx')
        self.f = self.open(TESTFN, 'rb')
        n = self.f.readinto(a)
        self.assertEqual('12', a.tostring()[:n])

    def testReadinto_text(self):
        a = array('b', 'xxxxxxxxxx')
        self.f.close()
        self.f = self.open(TESTFN, 'r')
        if hasattr(self.f, 'readinto'):
            self.assertRaises(TypeError, self.f.readinto, a)

    def testWritelinesUserList(self):
        l = UserList(['1', '2'])
        self.f.writelines(l)
        self.f.close()
        self.f = self.open(TESTFN, 'rb')
        buf = self.f.read()
        self.assertEqual(buf, '12')

    def testWritelinesIntegers(self):
        self.assertRaises(TypeError, self.f.writelines, [1, 2, 3])

    def testWritelinesIntegersUserList(self):
        l = UserList([1, 2, 3])
        self.assertRaises(TypeError, self.f.writelines, l)

    def testWritelinesNonString(self):

        class NonString:
            pass

        self.assertRaises(TypeError, self.f.writelines, [NonString(), NonString()])

    def testErrors(self):
        f = self.f
        self.assertEqual(f.name, TESTFN)
        self.assertTrue(not f.isatty())
        self.assertTrue(not f.closed)
        if hasattr(f, 'readinto'):
            self.assertRaises((IOError, TypeError), f.readinto, '')
        f.close()
        self.assertTrue(f.closed)

    def testMethods(self):
        methods = [('fileno', ()),
         ('flush', ()),
         ('isatty', ()),
         ('next', ()),
         ('read', ()),
         ('write', ('',)),
         ('readline', ()),
         ('readlines', ()),
         ('seek', (0,)),
         ('tell', ()),
         ('write', ('',)),
         ('writelines', ([],)),
         ('__iter__', ())]
        if not sys.platform.startswith('atheos'):
            methods.append(('truncate', ()))
        self.f.__exit__(None, None, None)
        self.assertTrue(self.f.closed)
        for methodname, args in methods:
            method = getattr(self.f, methodname)
            self.assertRaises(ValueError, method, *args)

        self.assertEqual(self.f.__exit__(None, None, None), None)
        try:
            1 // 0
        except:
            self.assertEqual(self.f.__exit__(*sys.exc_info()), None)

        return

    def testReadWhenWriting(self):
        self.assertRaises(IOError, self.f.read)


class CAutoFileTests(AutoFileTests):
    open = io.open


class PyAutoFileTests(AutoFileTests):
    open = staticmethod(pyio.open)


class OtherFileTests(unittest.TestCase):

    def testModeStrings(self):
        for mode in ('', 'aU', 'wU+'):
            try:
                f = self.open(TESTFN, mode)
            except ValueError:
                pass
            else:
                f.close()
                self.fail('%r is an invalid file mode' % mode)

    def testStdin(self):
        if sys.platform != 'osf1V5':
            self.assertRaises((IOError, ValueError), sys.stdin.seek, -1)
        else:
            print('  Skipping sys.stdin.seek(-1), it may crash the interpreter. Test manually.', file=sys.__stdout__)
        self.assertRaises((IOError, ValueError), sys.stdin.truncate)

    def testBadModeArgument(self):
        bad_mode = 'qwerty'
        try:
            f = self.open(TESTFN, bad_mode)
        except ValueError as msg:
            if msg.args[0] != 0:
                s = str(msg)
                if TESTFN in s or bad_mode not in s:
                    self.fail('bad error message for invalid mode: %s' % s)
        else:
            f.close()
            self.fail('no error for invalid mode: %s' % bad_mode)

    def testSetBufferSize(self):
        for s in (-1, 0, 1, 512):
            try:
                f = self.open(TESTFN, 'wb', s)
                f.write(str(s).encode('ascii'))
                f.close()
                f.close()
                f = self.open(TESTFN, 'rb', s)
                d = int(f.read().decode('ascii'))
                f.close()
                f.close()
            except IOError as msg:
                self.fail('error setting buffer size %d: %s' % (s, str(msg)))

            self.assertEqual(d, s)

    def testTruncateOnWindows(self):
        os.unlink(TESTFN)
        f = self.open(TESTFN, 'wb')
        try:
            f.write('12345678901')
            f.close()
            f = self.open(TESTFN, 'rb+')
            data = f.read(5)
            if data != '12345':
                self.fail('Read on file opened for update failed %r' % data)
            if f.tell() != 5:
                self.fail('File pos after read wrong %d' % f.tell())
            f.truncate()
            if f.tell() != 5:
                self.fail('File pos after ftruncate wrong %d' % f.tell())
            f.close()
            size = os.path.getsize(TESTFN)
            if size != 5:
                self.fail('File size after ftruncate wrong %d' % size)
        finally:
            f.close()
            os.unlink(TESTFN)

    def testIteration(self):
        dataoffset = 16384
        filler = 'ham\n'
        raise not dataoffset % len(filler) or AssertionError('dataoffset must be multiple of len(filler)')
        nchunks = dataoffset // len(filler)
        testlines = ['spam, spam and eggs\n',
         'eggs, spam, ham and spam\n',
         'saussages, spam, spam and eggs\n',
         'spam, ham, spam and eggs\n',
         'spam, spam, spam, spam, spam, ham, spam\n',
         'wonderful spaaaaaam.\n']
        methods = [('readline', ()),
         ('read', ()),
         ('readlines', ()),
         ('readinto', (array('b', ' ' * 100),))]
        try:
            bag = self.open(TESTFN, 'wb')
            bag.write(filler * nchunks)
            bag.writelines(testlines)
            bag.close()
            for methodname, args in methods:
                f = self.open(TESTFN, 'rb')
                if next(f) != filler:
                    (self.fail, 'Broken testfile')
                meth = getattr(f, methodname)
                meth(*args)
                f.close()

            f = self.open(TESTFN, 'rb')
            for i in range(nchunks):
                next(f)

            testline = testlines.pop(0)
            try:
                line = f.readline()
            except ValueError:
                self.fail('readline() after next() with supposedly empty iteration-buffer failed anyway')

            if line != testline:
                self.fail('readline() after next() with empty buffer failed. Got %r, expected %r' % (line, testline))
            testline = testlines.pop(0)
            buf = array('b', '\x00' * len(testline))
            try:
                f.readinto(buf)
            except ValueError:
                self.fail('readinto() after next() with supposedly empty iteration-buffer failed anyway')

            line = buf.tostring()
            if line != testline:
                self.fail('readinto() after next() with empty buffer failed. Got %r, expected %r' % (line, testline))
            testline = testlines.pop(0)
            try:
                line = f.read(len(testline))
            except ValueError:
                self.fail('read() after next() with supposedly empty iteration-buffer failed anyway')

            if line != testline:
                self.fail('read() after next() with empty buffer failed. Got %r, expected %r' % (line, testline))
            try:
                lines = f.readlines()
            except ValueError:
                self.fail('readlines() after next() with supposedly empty iteration-buffer failed anyway')

            if lines != testlines:
                self.fail('readlines() after next() with empty buffer failed. Got %r, expected %r' % (line, testline))
            f = self.open(TESTFN, 'rb')
            try:
                for line in f:
                    pass

                try:
                    f.readline()
                    f.readinto(buf)
                    f.read()
                    f.readlines()
                except ValueError:
                    self.fail('read* failed after next() consumed file')

            finally:
                f.close()

        finally:
            os.unlink(TESTFN)


class COtherFileTests(OtherFileTests):
    open = io.open


class PyOtherFileTests(OtherFileTests):
    open = staticmethod(pyio.open)


def test_main():
    try:
        run_unittest(CAutoFileTests, PyAutoFileTests, COtherFileTests, PyOtherFileTests)
    finally:
        if os.path.exists(TESTFN):
            os.unlink(TESTFN)


if __name__ == '__main__':
    test_main()