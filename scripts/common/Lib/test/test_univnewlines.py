# Embedded file name: scripts/common/Lib/test/test_univnewlines.py
from __future__ import print_function
from __future__ import unicode_literals
import io
import _pyio as pyio
import unittest
import os
import sys
from test import test_support as support
if not hasattr(sys.stdin, u'newlines'):
    raise unittest.SkipTest(u'This Python does not have universal newline support')
FATX = u'x' * 16384
DATA_TEMPLATE = [u'line1=1',
 u"line2='this is a very long line designed to go past any default " + u'buffer limits that exist in io.py but we also want to test ' + u"the uncommon case, naturally.'",
 u'def line3():pass',
 u"line4 = '%s'" % FATX]
DATA_LF = u'\n'.join(DATA_TEMPLATE) + u'\n'
DATA_CR = u'\r'.join(DATA_TEMPLATE) + u'\r'
DATA_CRLF = u'\r\n'.join(DATA_TEMPLATE) + u'\r\n'
DATA_MIXED = u'\n'.join(DATA_TEMPLATE) + u'\r'
DATA_SPLIT = [ x + u'\n' for x in DATA_TEMPLATE ]

class TestGenericUnivNewlines(unittest.TestCase):
    READMODE = u'r'
    WRITEMODE = u'wb'

    def setUp(self):
        data = self.DATA
        if u'b' in self.WRITEMODE:
            data = data.encode(u'ascii')
        with self.open(support.TESTFN, self.WRITEMODE) as fp:
            fp.write(data)

    def tearDown(self):
        try:
            os.unlink(support.TESTFN)
        except:
            pass

    def test_read(self):
        with self.open(support.TESTFN, self.READMODE) as fp:
            data = fp.read()
        self.assertEqual(data, DATA_LF)
        self.assertEqual(set(fp.newlines), set(self.NEWLINE))

    def test_readlines(self):
        with self.open(support.TESTFN, self.READMODE) as fp:
            data = fp.readlines()
        self.assertEqual(data, DATA_SPLIT)
        self.assertEqual(set(fp.newlines), set(self.NEWLINE))

    def test_readline(self):
        with self.open(support.TESTFN, self.READMODE) as fp:
            data = []
            d = fp.readline()
            while d:
                data.append(d)
                d = fp.readline()

        self.assertEqual(data, DATA_SPLIT)
        self.assertEqual(set(fp.newlines), set(self.NEWLINE))

    def test_seek(self):
        with self.open(support.TESTFN, self.READMODE) as fp:
            fp.readline()
            pos = fp.tell()
            data = fp.readlines()
            self.assertEqual(data, DATA_SPLIT[1:])
            fp.seek(pos)
            data = fp.readlines()
        self.assertEqual(data, DATA_SPLIT[1:])


class TestCRNewlines(TestGenericUnivNewlines):
    NEWLINE = u'\r'
    DATA = DATA_CR


class TestLFNewlines(TestGenericUnivNewlines):
    NEWLINE = u'\n'
    DATA = DATA_LF


class TestCRLFNewlines(TestGenericUnivNewlines):
    NEWLINE = u'\r\n'
    DATA = DATA_CRLF

    def test_tell(self):
        with self.open(support.TESTFN, self.READMODE) as fp:
            self.assertEqual(repr(fp.newlines), repr(None))
            data = fp.readline()
            pos = fp.tell()
        self.assertEqual(repr(fp.newlines), repr(self.NEWLINE))
        return


class TestMixedNewlines(TestGenericUnivNewlines):
    NEWLINE = (u'\r', u'\n')
    DATA = DATA_MIXED


def test_main():
    base_tests = (TestCRNewlines,
     TestLFNewlines,
     TestCRLFNewlines,
     TestMixedNewlines)
    tests = []
    for test in base_tests:

        class CTest(test):
            open = io.open

        CTest.__name__ = str(u'C' + test.__name__)

        class PyTest(test):
            open = staticmethod(pyio.open)

        PyTest.__name__ = str(u'Py' + test.__name__)
        tests.append(CTest)
        tests.append(PyTest)

    support.run_unittest(*tests)


if __name__ == u'__main__':
    test_main()