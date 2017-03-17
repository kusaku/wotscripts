# Embedded file name: scripts/common/Lib/test/test_future_builtins.py
import test.test_support, unittest
from future_builtins import hex, oct, map, zip, filter

class BuiltinTest(unittest.TestCase):

    def test_hex(self):
        self.assertEqual(hex(0), '0x0')
        self.assertEqual(hex(16), '0x10')
        self.assertEqual(hex(16L), '0x10')
        self.assertEqual(hex(-16), '-0x10')
        self.assertEqual(hex(-16L), '-0x10')
        self.assertRaises(TypeError, hex, {})

    def test_oct(self):
        self.assertEqual(oct(0), '0o0')
        self.assertEqual(oct(100), '0o144')
        self.assertEqual(oct(100L), '0o144')
        self.assertEqual(oct(-100), '-0o144')
        self.assertEqual(oct(-100L), '-0o144')
        self.assertRaises(TypeError, oct, ())

    def test_itertools(self):
        from itertools import imap, izip, ifilter
        self.assertEqual(map, imap)
        self.assertEqual(zip, izip)
        self.assertEqual(filter, ifilter)


def test_main(verbose = None):
    test.test_support.run_unittest(BuiltinTest)


if __name__ == '__main__':
    test_main(verbose=True)