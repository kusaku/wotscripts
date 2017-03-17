# Embedded file name: scripts/common/Lib/test/test_int_literal.py
"""Test correct treatment of hex/oct constants.

This is complex because of changes due to PEP 237.
"""
import unittest
from test import test_support

class TestHexOctBin(unittest.TestCase):

    def test_hex_baseline(self):
        self.assertEqual(0, 0)
        self.assertEqual(1, 1)
        self.assertEqual(81985529216486895L, 81985529216486895L)
        self.assertEqual(0, 0)
        self.assertEqual(16, 16)
        self.assertEqual(2147483647, 2147483647)
        self.assertEqual(9223372036854775807L, 9223372036854775807L)
        self.assertEqual(-0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)
        self.assertEqual(0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)

    def test_hex_unsigned(self):
        self.assertEqual(2147483648L, 2147483648L)
        self.assertEqual(4294967295L, 4294967295L)
        self.assertEqual(-2147483648L, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(-0x80000000, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(9223372036854775808L, 9223372036854775808L)
        self.assertEqual(18446744073709551615L, 18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)

    def test_oct_baseline(self):
        self.assertEqual(0, 0)
        self.assertEqual(16, 16)
        self.assertEqual(2147483647, 2147483647)
        self.assertEqual(9223372036854775807L, 9223372036854775807L)
        self.assertEqual(-0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)
        self.assertEqual(0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)

    def test_oct_baseline_new(self):
        self.assertEqual(0, 0)
        self.assertEqual(1, 1)
        self.assertEqual(342391, 342391)
        self.assertEqual(0, 0)
        self.assertEqual(16, 16)
        self.assertEqual(2147483647, 2147483647)
        self.assertEqual(9223372036854775807L, 9223372036854775807L)
        self.assertEqual(-0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)
        self.assertEqual(0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)

    def test_oct_unsigned(self):
        self.assertEqual(2147483648L, 2147483648L)
        self.assertEqual(4294967295L, 4294967295L)
        self.assertEqual(-2147483648L, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(-0x80000000, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(9223372036854775808L, 9223372036854775808L)
        self.assertEqual(18446744073709551615L, 18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)

    def test_oct_unsigned_new(self):
        self.assertEqual(2147483648L, 2147483648L)
        self.assertEqual(4294967295L, 4294967295L)
        self.assertEqual(-2147483648L, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(-0x80000000, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(9223372036854775808L, 9223372036854775808L)
        self.assertEqual(18446744073709551615L, 18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)

    def test_bin_baseline(self):
        self.assertEqual(0, 0)
        self.assertEqual(1, 1)
        self.assertEqual(1365, 1365)
        self.assertEqual(0, 0)
        self.assertEqual(16, 16)
        self.assertEqual(2147483647, 2147483647)
        self.assertEqual(9223372036854775807L, 9223372036854775807L)
        self.assertEqual(-0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)
        self.assertEqual(0, 0)
        self.assertEqual(-16, -16)
        self.assertEqual(-2147483647, -2147483647)
        self.assertEqual(-9223372036854775807L, -9223372036854775807L)

    def test_bin_unsigned(self):
        self.assertEqual(2147483648L, 2147483648L)
        self.assertEqual(4294967295L, 4294967295L)
        self.assertEqual(-2147483648L, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(-0x80000000, -2147483648L)
        self.assertEqual(-4294967295L, -4294967295L)
        self.assertEqual(9223372036854775808L, 9223372036854775808L)
        self.assertEqual(18446744073709551615L, 18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)
        self.assertEqual(-9223372036854775808L, -9223372036854775808L)
        self.assertEqual(-18446744073709551615L, -18446744073709551615L)


def test_main():
    test_support.run_unittest(TestHexOctBin)


if __name__ == '__main__':
    test_main()