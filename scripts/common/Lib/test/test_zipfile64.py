# Embedded file name: scripts/common/Lib/test/test_zipfile64.py
from test import test_support
test_support.requires('extralargefile', 'test requires loads of disk-space bytes and a long time to run')
try:
    import zlib
except ImportError:
    zlib = None

import zipfile, os, unittest
import time
import sys
from tempfile import TemporaryFile
from test.test_support import TESTFN, run_unittest
TESTFN2 = TESTFN + '2'
_PRINT_WORKING_MSG_INTERVAL = 300

class TestsWithSourceFile(unittest.TestCase):

    def setUp(self):
        line_gen = ('Test of zipfile line %d.' % i for i in xrange(1000000))
        self.data = '\n'.join(line_gen)
        fp = open(TESTFN, 'wb')
        fp.write(self.data)
        fp.close()

    def zipTest(self, f, compression):
        zipfp = zipfile.ZipFile(f, 'w', compression, allowZip64=True)
        filecount = 6 * 1073741824 // len(self.data)
        next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
        for num in range(filecount):
            zipfp.writestr('testfn%d' % num, self.data)
            if next_time <= time.time():
                next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
                print >> sys.__stdout__, '  zipTest still writing %d of %d, be patient...' % (num, filecount)
                sys.__stdout__.flush()

        zipfp.close()
        zipfp = zipfile.ZipFile(f, 'r', compression)
        for num in range(filecount):
            self.assertEqual(zipfp.read('testfn%d' % num), self.data)
            if next_time <= time.time():
                next_time = time.time() + _PRINT_WORKING_MSG_INTERVAL
                print >> sys.__stdout__, '  zipTest still reading %d of %d, be patient...' % (num, filecount)
                sys.__stdout__.flush()

        zipfp.close()

    def testStored(self):
        for f in (TemporaryFile(), TESTFN2):
            self.zipTest(f, zipfile.ZIP_STORED)

    if zlib:

        def testDeflated(self):
            for f in (TemporaryFile(), TESTFN2):
                self.zipTest(f, zipfile.ZIP_DEFLATED)

    def tearDown(self):
        for fname in (TESTFN, TESTFN2):
            if os.path.exists(fname):
                os.remove(fname)


class OtherTests(unittest.TestCase):

    def testMoreThan64kFiles(self):
        zipf = zipfile.ZipFile(TESTFN, mode='w')
        zipf.debug = 100
        numfiles = 196608 / 2
        for i in xrange(numfiles):
            zipf.writestr('foo%08d' % i, '%d' % (i ** 3 % 57))

        self.assertEqual(len(zipf.namelist()), numfiles)
        zipf.close()
        zipf2 = zipfile.ZipFile(TESTFN, mode='r')
        self.assertEqual(len(zipf2.namelist()), numfiles)
        for i in xrange(numfiles):
            self.assertEqual(zipf2.read('foo%08d' % i), '%d' % (i ** 3 % 57))

        zipf.close()

    def tearDown(self):
        test_support.unlink(TESTFN)
        test_support.unlink(TESTFN2)


def test_main():
    run_unittest(TestsWithSourceFile, OtherTests)


if __name__ == '__main__':
    test_main()