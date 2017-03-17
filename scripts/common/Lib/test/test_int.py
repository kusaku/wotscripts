# Embedded file name: scripts/common/Lib/test/test_int.py
import sys
import unittest
from test.test_support import run_unittest, have_unicode
import math
L = [('0', 0),
 ('1', 1),
 ('9', 9),
 ('10', 10),
 ('99', 99),
 ('100', 100),
 ('314', 314),
 (' 314', 314),
 ('314 ', 314),
 ('  \t\t  314  \t\t  ', 314),
 (repr(sys.maxint), sys.maxint),
 ('  1x', ValueError),
 ('  1  ', 1),
 ('  1\x02  ', ValueError),
 ('', ValueError),
 (' ', ValueError),
 ('  \t\t  ', ValueError)]
if have_unicode:
    L += [(unicode('0'), 0),
     (unicode('1'), 1),
     (unicode('9'), 9),
     (unicode('10'), 10),
     (unicode('99'), 99),
     (unicode('100'), 100),
     (unicode('314'), 314),
     (unicode(' 314'), 314),
     (unicode('\\u0663\\u0661\\u0664 ', 'raw-unicode-escape'), 314),
     (unicode('  \t\t  314  \t\t  '), 314),
     (unicode('  1x'), ValueError),
     (unicode('  1  '), 1),
     (unicode('  1\x02  '), ValueError),
     (unicode(''), ValueError),
     (unicode(' '), ValueError),
     (unicode('  \t\t  '), ValueError),
     (unichr(512), ValueError)]

class IntTestCases(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(int(314), 314)
        self.assertEqual(int(3.14), 3)
        self.assertEqual(int(314L), 314)
        self.assertEqual(int(-3.14), -3)
        self.assertEqual(int(3.9), 3)
        self.assertEqual(int(-3.9), -3)
        self.assertEqual(int(3.5), 3)
        self.assertEqual(int(-3.5), -3)
        self.assertEqual(int('10', 16), 16L)
        if have_unicode:
            self.assertEqual(int(unicode('10'), 16), 16L)
        for s, v in L:
            for sign in ('', '+', '-'):
                for prefix in ('', ' ', '\t', '  \t\t  '):
                    ss = prefix + sign + s
                    vv = v
                    if sign == '-' and v is not ValueError:
                        vv = -v
                    try:
                        self.assertEqual(int(ss), vv)
                    except v:
                        pass

        s = repr(-1 - sys.maxint)
        x = int(s)
        self.assertEqual(x + 1, -sys.maxint)
        self.assertIsInstance(x, int)
        self.assertEqual(int(s[1:]), sys.maxint + 1)
        x = int(1e+100)
        self.assertIsInstance(x, long)
        x = int(-1e+100)
        self.assertIsInstance(x, long)
        x = -1 - sys.maxint
        self.assertEqual(x >> 1, x // 2)
        self.assertRaises(ValueError, int, '123\x00')
        self.assertRaises(ValueError, int, '53', 40)
        self.assertRaises(ValueError, int, '123\x00', 10)
        self.assertRaises(ValueError, int, '123\x00 245', 20)
        x = int('1' * 600)
        self.assertIsInstance(x, long)
        if have_unicode:
            x = int(unichr(1633) * 600)
            self.assertIsInstance(x, long)
        self.assertRaises(TypeError, int, 1, 12)
        self.assertEqual(int('0123', 0), 83)
        self.assertEqual(int('0x123', 16), 291)
        self.assertRaises(ValueError, int, '0x', 16)
        self.assertRaises(ValueError, int, '0x', 0)
        self.assertRaises(ValueError, int, '0o', 8)
        self.assertRaises(ValueError, int, '0o', 0)
        self.assertRaises(ValueError, int, '0b', 2)
        self.assertRaises(ValueError, int, '0b', 0)
        self.assertEqual(int('100000000000000000000000000000000', 2), 4294967296L)
        self.assertEqual(int('102002022201221111211', 3), 4294967296L)
        self.assertEqual(int('10000000000000000', 4), 4294967296L)
        self.assertEqual(int('32244002423141', 5), 4294967296L)
        self.assertEqual(int('1550104015504', 6), 4294967296L)
        self.assertEqual(int('211301422354', 7), 4294967296L)
        self.assertEqual(int('40000000000', 8), 4294967296L)
        self.assertEqual(int('12068657454', 9), 4294967296L)
        self.assertEqual(int('4294967296', 10), 4294967296L)
        self.assertEqual(int('1904440554', 11), 4294967296L)
        self.assertEqual(int('9ba461594', 12), 4294967296L)
        self.assertEqual(int('535a79889', 13), 4294967296L)
        self.assertEqual(int('2ca5b7464', 14), 4294967296L)
        self.assertEqual(int('1a20dcd81', 15), 4294967296L)
        self.assertEqual(int('100000000', 16), 4294967296L)
        self.assertEqual(int('a7ffda91', 17), 4294967296L)
        self.assertEqual(int('704he7g4', 18), 4294967296L)
        self.assertEqual(int('4f5aff66', 19), 4294967296L)
        self.assertEqual(int('3723ai4g', 20), 4294967296L)
        self.assertEqual(int('281d55i4', 21), 4294967296L)
        self.assertEqual(int('1fj8b184', 22), 4294967296L)
        self.assertEqual(int('1606k7ic', 23), 4294967296L)
        self.assertEqual(int('mb994ag', 24), 4294967296L)
        self.assertEqual(int('hek2mgl', 25), 4294967296L)
        self.assertEqual(int('dnchbnm', 26), 4294967296L)
        self.assertEqual(int('b28jpdm', 27), 4294967296L)
        self.assertEqual(int('8pfgih4', 28), 4294967296L)
        self.assertEqual(int('76beigg', 29), 4294967296L)
        self.assertEqual(int('5qmcpqg', 30), 4294967296L)
        self.assertEqual(int('4q0jto4', 31), 4294967296L)
        self.assertEqual(int('4000000', 32), 4294967296L)
        self.assertEqual(int('3aokq94', 33), 4294967296L)
        self.assertEqual(int('2qhxjli', 34), 4294967296L)
        self.assertEqual(int('2br45qb', 35), 4294967296L)
        self.assertEqual(int('1z141z4', 36), 4294967296L)
        self.assertEqual(int(' 0123  ', 0), 83)
        self.assertEqual(int(' 0123  ', 0), 83)
        self.assertEqual(int('000', 0), 0)
        self.assertEqual(int('0o123', 0), 83)
        self.assertEqual(int('0x123', 0), 291)
        self.assertEqual(int('0b100', 0), 4)
        self.assertEqual(int(' 0O123   ', 0), 83)
        self.assertEqual(int(' 0X123  ', 0), 291)
        self.assertEqual(int(' 0B100 ', 0), 4)
        self.assertEqual(int('0', 0), 0)
        self.assertEqual(int('+0', 0), 0)
        self.assertEqual(int('-0', 0), 0)
        self.assertEqual(int('00', 0), 0)
        self.assertRaises(ValueError, int, '08', 0)
        self.assertRaises(ValueError, int, '-012395', 0)
        self.assertEqual(int('0123'), 123)
        self.assertEqual(int('0123', 10), 123)
        self.assertEqual(int('0x123', 16), 291)
        self.assertEqual(int('0o123', 8), 83)
        self.assertEqual(int('0b100', 2), 4)
        self.assertEqual(int('0X123', 16), 291)
        self.assertEqual(int('0O123', 8), 83)
        self.assertEqual(int('0B100', 2), 4)
        self.assertRaises(ValueError, int, '0b2', 2)
        self.assertRaises(ValueError, int, '0b02', 2)
        self.assertRaises(ValueError, int, '0B2', 2)
        self.assertRaises(ValueError, int, '0B02', 2)
        self.assertRaises(ValueError, int, '0o8', 8)
        self.assertRaises(ValueError, int, '0o08', 8)
        self.assertRaises(ValueError, int, '0O8', 8)
        self.assertRaises(ValueError, int, '0O08', 8)
        self.assertRaises(ValueError, int, '0xg', 16)
        self.assertRaises(ValueError, int, '0x0g', 16)
        self.assertRaises(ValueError, int, '0Xg', 16)
        self.assertRaises(ValueError, int, '0X0g', 16)
        self.assertEqual(int('100000000000000000000000000000001', 2), 4294967297L)
        self.assertEqual(int('102002022201221111212', 3), 4294967297L)
        self.assertEqual(int('10000000000000001', 4), 4294967297L)
        self.assertEqual(int('32244002423142', 5), 4294967297L)
        self.assertEqual(int('1550104015505', 6), 4294967297L)
        self.assertEqual(int('211301422355', 7), 4294967297L)
        self.assertEqual(int('40000000001', 8), 4294967297L)
        self.assertEqual(int('12068657455', 9), 4294967297L)
        self.assertEqual(int('4294967297', 10), 4294967297L)
        self.assertEqual(int('1904440555', 11), 4294967297L)
        self.assertEqual(int('9ba461595', 12), 4294967297L)
        self.assertEqual(int('535a7988a', 13), 4294967297L)
        self.assertEqual(int('2ca5b7465', 14), 4294967297L)
        self.assertEqual(int('1a20dcd82', 15), 4294967297L)
        self.assertEqual(int('100000001', 16), 4294967297L)
        self.assertEqual(int('a7ffda92', 17), 4294967297L)
        self.assertEqual(int('704he7g5', 18), 4294967297L)
        self.assertEqual(int('4f5aff67', 19), 4294967297L)
        self.assertEqual(int('3723ai4h', 20), 4294967297L)
        self.assertEqual(int('281d55i5', 21), 4294967297L)
        self.assertEqual(int('1fj8b185', 22), 4294967297L)
        self.assertEqual(int('1606k7id', 23), 4294967297L)
        self.assertEqual(int('mb994ah', 24), 4294967297L)
        self.assertEqual(int('hek2mgm', 25), 4294967297L)
        self.assertEqual(int('dnchbnn', 26), 4294967297L)
        self.assertEqual(int('b28jpdn', 27), 4294967297L)
        self.assertEqual(int('8pfgih5', 28), 4294967297L)
        self.assertEqual(int('76beigh', 29), 4294967297L)
        self.assertEqual(int('5qmcpqh', 30), 4294967297L)
        self.assertEqual(int('4q0jto5', 31), 4294967297L)
        self.assertEqual(int('4000001', 32), 4294967297L)
        self.assertEqual(int('3aokq95', 33), 4294967297L)
        self.assertEqual(int('2qhxjlj', 34), 4294967297L)
        self.assertEqual(int('2br45qc', 35), 4294967297L)
        self.assertEqual(int('1z141z5', 36), 4294967297L)

    def test_bit_length(self):
        tiny = 1e-10
        for x in xrange(-65000, 65000):
            k = x.bit_length()
            self.assertEqual(k, len(bin(x).lstrip('-0b')))
            if x != 0:
                self.assertTrue(2 ** (k - 1) <= abs(x) < 2 ** k)
            else:
                self.assertEqual(k, 0)
            if x != 0:
                self.assertEqual(k, 1 + math.floor(math.log(abs(x)) / math.log(2) + tiny))

        self.assertEqual(0.bit_length(), 0)
        self.assertEqual(1.bit_length(), 1)
        self.assertEqual((-1).bit_length(), 1)
        self.assertEqual(2.bit_length(), 2)
        self.assertEqual((-2).bit_length(), 2)
        for i in [2,
         3,
         15,
         16,
         17,
         31,
         32,
         33,
         63,
         64]:
            a = 2 ** i
            self.assertEqual((a - 1).bit_length(), i)
            self.assertEqual((1 - a).bit_length(), i)
            self.assertEqual(a.bit_length(), i + 1)
            self.assertEqual((-a).bit_length(), i + 1)
            self.assertEqual((a + 1).bit_length(), i + 1)
            self.assertEqual((-a - 1).bit_length(), i + 1)

    @unittest.skipUnless(float.__getformat__('double').startswith('IEEE'), 'test requires IEEE 754 doubles')
    def test_float_conversion(self):
        exact_values = [-2,
         -1,
         0,
         1,
         2,
         4503599627370496L,
         9007199254740991L,
         9007199254740992L,
         9007199254740994L,
         9007199254740996L,
         18014398509481980L,
         18014398509481982L,
         9223372036854775808L,
         -9223372036854775808L,
         18446744073709551616L,
         -18446744073709551616L,
         100000000000000000000L,
         1000000000000000000000L,
         10000000000000000000000L]
        for value in exact_values:
            self.assertEqual(int(float(int(value))), value)

        self.assertEqual(int(float(9007199254740993L)), 9007199254740992L)
        self.assertEqual(int(float(9007199254740994L)), 9007199254740994L)
        self.assertEqual(int(float(9007199254740995L)), 9007199254740996L)
        self.assertEqual(int(float(9007199254740997L)), 9007199254740996L)
        self.assertEqual(int(float(9007199254740998L)), 9007199254740998L)
        self.assertEqual(int(float(9007199254740999L)), 9007199254741000L)
        self.assertEqual(int(float(-9007199254740993L)), -9007199254740992L)
        self.assertEqual(int(float(-9007199254740994L)), -9007199254740994L)
        self.assertEqual(int(float(-9007199254740995L)), -9007199254740996L)
        self.assertEqual(int(float(-9007199254740997L)), -9007199254740996L)
        self.assertEqual(int(float(-9007199254740998L)), -9007199254740998L)
        self.assertEqual(int(float(-9007199254740999L)), -9007199254741000L)
        self.assertEqual(int(float(18014398509481982L)), 18014398509481982L)
        self.assertEqual(int(float(18014398509481983L)), 18014398509481984L)
        self.assertEqual(int(float(18014398509481986L)), 18014398509481984L)
        self.assertEqual(int(float(18014398509481987L)), 18014398509481988L)
        self.assertEqual(int(float(18014398509481989L)), 18014398509481988L)
        self.assertEqual(int(float(18014398509481990L)), 18014398509481992L)
        self.assertEqual(int(float(18014398509481994L)), 18014398509481992L)
        self.assertEqual(int(float(18014398509481995L)), 18014398509481996L)

    def test_intconversion(self):

        class ClassicMissingMethods:
            pass

        self.assertRaises(AttributeError, int, ClassicMissingMethods())

        class MissingMethods(object):
            pass

        self.assertRaises(TypeError, int, MissingMethods())

        class Foo0:

            def __int__(self):
                return 42

        class Foo1(object):

            def __int__(self):
                return 42

        class Foo2(int):

            def __int__(self):
                return 42

        class Foo3(int):

            def __int__(self):
                return self

        class Foo4(int):

            def __int__(self):
                return 42L

        class Foo5(int):

            def __int__(self):
                return 42.0

        self.assertEqual(int(Foo0()), 42)
        self.assertEqual(int(Foo1()), 42)
        self.assertEqual(int(Foo2()), 42)
        self.assertEqual(int(Foo3()), 0)
        self.assertEqual(int(Foo4()), 42L)
        self.assertRaises(TypeError, int, Foo5())

        class Classic:
            pass

        for base in (object, Classic):

            class IntOverridesTrunc(base):

                def __int__(self):
                    return 42

                def __trunc__(self):
                    return -12

            self.assertEqual(int(IntOverridesTrunc()), 42)

            class JustTrunc(base):

                def __trunc__(self):
                    return 42

            self.assertEqual(int(JustTrunc()), 42)
            for trunc_result_base in (object, Classic):

                class Integral(trunc_result_base):

                    def __int__(self):
                        return 42

                class TruncReturnsNonInt(base):

                    def __trunc__(self):
                        return Integral()

                self.assertEqual(int(TruncReturnsNonInt()), 42)

                class NonIntegral(trunc_result_base):

                    def __trunc__(self):
                        return NonIntegral()

                class TruncReturnsNonIntegral(base):

                    def __trunc__(self):
                        return NonIntegral()

                try:
                    int(TruncReturnsNonIntegral())
                except TypeError as e:
                    self.assertEqual(str(e), '__trunc__ returned non-Integral (type NonIntegral)')
                else:
                    self.fail('Failed to raise TypeError with %s' % ((base, trunc_result_base),))


def test_main():
    run_unittest(IntTestCases)


if __name__ == '__main__':
    test_main()