# Embedded file name: scripts/common/Lib/test/test_bufio.py
import unittest
from test import test_support as support
import io
import _pyio as pyio
lengths = list(range(1, 257)) + [512,
 1000,
 1024,
 2048,
 4096,
 8192,
 10000,
 16384,
 32768,
 65536,
 1000000]

class BufferSizeTest(unittest.TestCase):

    def try_one(self, s):
        support.unlink(support.TESTFN)
        f = self.open(support.TESTFN, 'wb')
        try:
            f.write(s)
            f.write('\n')
            f.write(s)
            f.close()
            f = open(support.TESTFN, 'rb')
            line = f.readline()
            self.assertEqual(line, s + '\n')
            line = f.readline()
            self.assertEqual(line, s)
            line = f.readline()
            self.assertTrue(not line)
            f.close()
        finally:
            support.unlink(support.TESTFN)

    def drive_one(self, pattern):
        for length in lengths:
            q, r = divmod(length, len(pattern))
            teststring = pattern * q + pattern[:r]
            self.assertEqual(len(teststring), length)
            self.try_one(teststring)
            self.try_one(teststring + 'x')
            self.try_one(teststring[:-1])

    def test_primepat(self):
        self.drive_one('1234567890\x00\x01\x02\x03\x04\x05\x06')

    def test_nullpat(self):
        self.drive_one(bytes(1000))


class CBufferSizeTest(BufferSizeTest):
    open = io.open


class PyBufferSizeTest(BufferSizeTest):
    open = staticmethod(pyio.open)


class BuiltinBufferSizeTest(BufferSizeTest):
    open = open


def test_main():
    support.run_unittest(CBufferSizeTest, PyBufferSizeTest, BuiltinBufferSizeTest)


if __name__ == '__main__':
    test_main()