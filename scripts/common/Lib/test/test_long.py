# Embedded file name: scripts/common/Lib/test/test_long.py
import unittest
from test import test_support
import sys
import random
import math

class Frm(object):

    def __init__(self, format, *args):
        self.format = format
        self.args = args

    def __str__(self):
        return self.format % self.args


SHIFT = sys.long_info.bits_per_digit
BASE = 2 ** SHIFT
MASK = BASE - 1
KARATSUBA_CUTOFF = 70
MAXDIGITS = 15
special = map(long, [0,
 1,
 2,
 BASE,
 BASE >> 1])
special.append(6148914691236517205L)
special.append(12297829382473034410L)
p2 = 4L
for i in range(2 * SHIFT):
    special.append(p2 - 1)
    p2 = p2 << 1

del p2
special = special + map(lambda x: ~x, special) + map(lambda x: -x, special)
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
if test_support.have_unicode:
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

class LongTest(unittest.TestCase):

    def getran(self, ndigits):
        self.assertTrue(ndigits > 0)
        nbits_hi = ndigits * SHIFT
        nbits_lo = nbits_hi - SHIFT + 1
        answer = 0L
        nbits = 0
        r = int(random.random() * (SHIFT * 2)) | 1
        while nbits < nbits_lo:
            bits = (r >> 1) + 1
            bits = min(bits, nbits_hi - nbits)
            self.assertTrue(1 <= bits <= SHIFT)
            nbits = nbits + bits
            answer = answer << bits
            if r & 1:
                answer = answer | (1 << bits) - 1
            r = int(random.random() * (SHIFT * 2))

        self.assertTrue(nbits_lo <= nbits <= nbits_hi)
        if random.random() < 0.5:
            answer = -answer
        return answer

    def getran2(ndigits):
        answer = 0L
        for i in xrange(ndigits):
            answer = answer << SHIFT | random.randint(0, MASK)

        if random.random() < 0.5:
            answer = -answer
        return answer

    def check_division(self, x, y):
        eq = self.assertEqual
        q, r = divmod(x, y)
        q2, r2 = x // y, x % y
        pab, pba = x * y, y * x
        eq(pab, pba, Frm('multiplication does not commute for %r and %r', x, y))
        eq(q, q2, Frm('divmod returns different quotient than / for %r and %r', x, y))
        eq(r, r2, Frm('divmod returns different mod than %% for %r and %r', x, y))
        eq(x, q * y + r, Frm('x != q*y + r after divmod on x=%r, y=%r', x, y))
        if y > 0:
            self.assertTrue(0 <= r < y, Frm('bad mod from divmod on %r and %r', x, y))
        else:
            self.assertTrue(y < r <= 0, Frm('bad mod from divmod on %r and %r', x, y))

    def test_division(self):
        digits = range(1, MAXDIGITS + 1) + range(KARATSUBA_CUTOFF, KARATSUBA_CUTOFF + 14)
        digits.append(KARATSUBA_CUTOFF * 3)
        for lenx in digits:
            x = self.getran(lenx)
            for leny in digits:
                y = self.getran(leny) or 1L
                self.check_division(x, y)

        self.check_division(1231948412290879395966702881L, 1147341367131428698L)
        self.check_division(815427756481275430342312021515587883L, 707270836069027745L)
        self.check_division(627976073697012820849443363563599041L, 643588798496057020L)
        self.check_division(1115141373653752303710932756325578065L, 1038556335171453937726882627L)
        self.check_division(922498905405436751940989320930368494L, 949985870686786135626943396L)
        self.check_division(768235853328091167204009652174031844L, 1091555541180371554426545266L)
        self.check_division(20172188947443L, 615611397L)
        self.check_division(1020908530270155025L, 950795710L)
        self.check_division(128589565723112408L, 736393718L)
        self.check_division(609919780285761575L, 18613274546784L)
        self.check_division(710031681576388032L, 26769404391308L)
        self.check_division(1933622614268221L, 30212853348836L)

    def test_karatsuba(self):
        digits = range(1, 5) + range(KARATSUBA_CUTOFF, KARATSUBA_CUTOFF + 10)
        digits.extend([KARATSUBA_CUTOFF * 10, KARATSUBA_CUTOFF * 100])
        bits = [ digit * SHIFT for digit in digits ]
        for abits in bits:
            a = (1L << abits) - 1
            for bbits in bits:
                if bbits < abits:
                    continue
                b = (1L << bbits) - 1
                x = a * b
                y = (1L << abits + bbits) - (1L << abits) - (1L << bbits) + 1
                self.assertEqual(x, y, Frm('bad result for a*b: a=%r, b=%r, x=%r, y=%r', a, b, x, y))

    def check_bitop_identities_1(self, x):
        eq = self.assertEqual
        eq(x & 0, 0, Frm('x & 0 != 0 for x=%r', x))
        eq(x | 0, x, Frm('x | 0 != x for x=%r', x))
        eq(x ^ 0, x, Frm('x ^ 0 != x for x=%r', x))
        eq(x & -1, x, Frm('x & -1 != x for x=%r', x))
        eq(x | -1, -1, Frm('x | -1 != -1 for x=%r', x))
        eq(x ^ -1, ~x, Frm('x ^ -1 != ~x for x=%r', x))
        eq(x, ~~x, Frm('x != ~~x for x=%r', x))
        eq(x & x, x, Frm('x & x != x for x=%r', x))
        eq(x | x, x, Frm('x | x != x for x=%r', x))
        eq(x ^ x, 0, Frm('x ^ x != 0 for x=%r', x))
        eq(x & ~x, 0, Frm('x & ~x != 0 for x=%r', x))
        eq(x | ~x, -1, Frm('x | ~x != -1 for x=%r', x))
        eq(x ^ ~x, -1, Frm('x ^ ~x != -1 for x=%r', x))
        eq(-x, 1 + ~x, Frm('not -x == 1 + ~x for x=%r', x))
        eq(-x, ~(x - 1), Frm('not -x == ~(x-1) forx =%r', x))
        for n in xrange(2 * SHIFT):
            p2 = 2L ** n
            eq(x << n >> n, x, Frm('x << n >> n != x for x=%r, n=%r', (x, n)))
            eq(x // p2, x >> n, Frm('x // p2 != x >> n for x=%r n=%r p2=%r', (x, n, p2)))
            eq(x * p2, x << n, Frm('x * p2 != x << n for x=%r n=%r p2=%r', (x, n, p2)))
            eq(x & -p2, x >> n << n, Frm('not x & -p2 == x >> n << n for x=%r n=%r p2=%r', (x, n, p2)))
            eq(x & -p2, x & ~(p2 - 1), Frm('not x & -p2 == x & ~(p2 - 1) for x=%r n=%r p2=%r', (x, n, p2)))

    def check_bitop_identities_2(self, x, y):
        eq = self.assertEqual
        eq(x & y, y & x, Frm('x & y != y & x for x=%r, y=%r', (x, y)))
        eq(x | y, y | x, Frm('x | y != y | x for x=%r, y=%r', (x, y)))
        eq(x ^ y, y ^ x, Frm('x ^ y != y ^ x for x=%r, y=%r', (x, y)))
        eq(x ^ y ^ x, y, Frm('x ^ y ^ x != y for x=%r, y=%r', (x, y)))
        eq(x & y, ~(~x | ~y), Frm('x & y != ~(~x | ~y) for x=%r, y=%r', (x, y)))
        eq(x | y, ~(~x & ~y), Frm('x | y != ~(~x & ~y) for x=%r, y=%r', (x, y)))
        eq(x ^ y, (x | y) & ~(x & y), Frm('x ^ y != (x | y) & ~(x & y) for x=%r, y=%r', (x, y)))
        eq(x ^ y, x & ~y | ~x & y, Frm('x ^ y == (x & ~y) | (~x & y) for x=%r, y=%r', (x, y)))
        eq(x ^ y, (x | y) & (~x | ~y), Frm('x ^ y == (x | y) & (~x | ~y) for x=%r, y=%r', (x, y)))

    def check_bitop_identities_3(self, x, y, z):
        eq = self.assertEqual
        eq(x & y & z, x & (y & z), Frm('(x & y) & z != x & (y & z) for x=%r, y=%r, z=%r', (x, y, z)))
        eq(x | y | z, x | (y | z), Frm('(x | y) | z != x | (y | z) for x=%r, y=%r, z=%r', (x, y, z)))
        eq(x ^ y ^ z, x ^ (y ^ z), Frm('(x ^ y) ^ z != x ^ (y ^ z) for x=%r, y=%r, z=%r', (x, y, z)))
        eq(x & (y | z), x & y | x & z, Frm('x & (y | z) != (x & y) | (x & z) for x=%r, y=%r, z=%r', (x, y, z)))
        eq(x | y & z, (x | y) & (x | z), Frm('x | (y & z) != (x | y) & (x | z) for x=%r, y=%r, z=%r', (x, y, z)))

    def test_bitop_identities(self):
        for x in special:
            self.check_bitop_identities_1(x)

        digits = xrange(1, MAXDIGITS + 1)
        for lenx in digits:
            x = self.getran(lenx)
            self.check_bitop_identities_1(x)
            for leny in digits:
                y = self.getran(leny)
                self.check_bitop_identities_2(x, y)
                self.check_bitop_identities_3(x, y, self.getran((lenx + leny) // 2))

    def slow_format(self, x, base):
        if (x, base) == (0, 8):
            return '0L'
        digits = []
        sign = 0
        if x < 0:
            sign, x = 1, -x
        while x:
            x, r = divmod(x, base)
            digits.append(int(r))

        digits.reverse()
        digits = digits or [0]
        return '-'[:sign] + {8: '0',
         10: '',
         16: '0x'}[base] + ''.join(map(lambda i: '0123456789abcdef'[i], digits)) + 'L'

    def check_format_1(self, x):
        for base, mapper in ((8, oct), (10, repr), (16, hex)):
            got = mapper(x)
            expected = self.slow_format(x, base)
            msg = Frm('%s returned %r but expected %r for %r', mapper.__name__, got, expected, x)
            self.assertEqual(got, expected, msg)
            self.assertEqual(long(got, 0), x, Frm('long("%s", 0) != %r', got, x))

        got = str(x)
        expected = self.slow_format(x, 10)[:-1]
        msg = Frm('%s returned %r but expected %r for %r', mapper.__name__, got, expected, x)
        self.assertEqual(got, expected, msg)

    def test_format(self):
        for x in special:
            self.check_format_1(x)

        for i in xrange(10):
            for lenx in xrange(1, MAXDIGITS + 1):
                x = self.getran(lenx)
                self.check_format_1(x)

    def test_long(self):
        self.assertEqual(long(314), 314L)
        self.assertEqual(long(3.14), 3L)
        self.assertEqual(long(314L), 314L)
        self.assertEqual(type(long(314)), long)
        self.assertEqual(type(long(3.14)), long)
        self.assertEqual(type(long(314L)), long)
        self.assertEqual(long(-3.14), -3L)
        self.assertEqual(long(3.9), 3L)
        self.assertEqual(long(-3.9), -3L)
        self.assertEqual(long(3.5), 3L)
        self.assertEqual(long(-3.5), -3L)
        self.assertEqual(long('-3'), -3L)
        self.assertEqual(long('0b10', 2), 2L)
        self.assertEqual(long('0o10', 8), 8L)
        self.assertEqual(long('0x10', 16), 16L)
        if test_support.have_unicode:
            self.assertEqual(long(unicode('-3')), -3L)
        self.assertEqual(long('10', 16), 16L)
        if test_support.have_unicode:
            self.assertEqual(long(unicode('10'), 16), 16L)
        LL = [('1' + '00000000000000000000', 100000000000000000000L), ('1' + '0' * 100, 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L)]
        L2 = L[:]
        if test_support.have_unicode:
            L2 += [(unicode('1') + unicode('0') * 20, 100000000000000000000L), (unicode('1') + unicode('0') * 100, 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L)]
        for s, v in L2 + LL:
            for sign in ('', '+', '-'):
                for prefix in ('', ' ', '\t', '  \t\t  '):
                    ss = prefix + sign + s
                    vv = v
                    if sign == '-' and v is not ValueError:
                        vv = -v
                    try:
                        self.assertEqual(long(ss), long(vv))
                    except v:
                        pass

        self.assertRaises(ValueError, long, '123\x00')
        self.assertRaises(ValueError, long, '53', 40)
        self.assertRaises(TypeError, long, 1, 12)
        self.assertEqual(long(' 0123  ', 0), 83)
        self.assertEqual(long(' 0123  ', 0), 83)
        self.assertEqual(long('000', 0), 0)
        self.assertEqual(long('0o123', 0), 83)
        self.assertEqual(long('0x123', 0), 291)
        self.assertEqual(long('0b100', 0), 4)
        self.assertEqual(long(' 0O123   ', 0), 83)
        self.assertEqual(long(' 0X123  ', 0), 291)
        self.assertEqual(long(' 0B100 ', 0), 4)
        self.assertEqual(long('0', 0), 0)
        self.assertEqual(long('+0', 0), 0)
        self.assertEqual(long('-0', 0), 0)
        self.assertEqual(long('00', 0), 0)
        self.assertRaises(ValueError, long, '08', 0)
        self.assertRaises(ValueError, long, '-012395', 0)
        self.assertRaises(ValueError, long, '123\x00', 10)
        self.assertRaises(ValueError, long, '123\x00 245', 20)
        self.assertEqual(long('100000000000000000000000000000000', 2), 4294967296L)
        self.assertEqual(long('102002022201221111211', 3), 4294967296L)
        self.assertEqual(long('10000000000000000', 4), 4294967296L)
        self.assertEqual(long('32244002423141', 5), 4294967296L)
        self.assertEqual(long('1550104015504', 6), 4294967296L)
        self.assertEqual(long('211301422354', 7), 4294967296L)
        self.assertEqual(long('40000000000', 8), 4294967296L)
        self.assertEqual(long('12068657454', 9), 4294967296L)
        self.assertEqual(long('4294967296', 10), 4294967296L)
        self.assertEqual(long('1904440554', 11), 4294967296L)
        self.assertEqual(long('9ba461594', 12), 4294967296L)
        self.assertEqual(long('535a79889', 13), 4294967296L)
        self.assertEqual(long('2ca5b7464', 14), 4294967296L)
        self.assertEqual(long('1a20dcd81', 15), 4294967296L)
        self.assertEqual(long('100000000', 16), 4294967296L)
        self.assertEqual(long('a7ffda91', 17), 4294967296L)
        self.assertEqual(long('704he7g4', 18), 4294967296L)
        self.assertEqual(long('4f5aff66', 19), 4294967296L)
        self.assertEqual(long('3723ai4g', 20), 4294967296L)
        self.assertEqual(long('281d55i4', 21), 4294967296L)
        self.assertEqual(long('1fj8b184', 22), 4294967296L)
        self.assertEqual(long('1606k7ic', 23), 4294967296L)
        self.assertEqual(long('mb994ag', 24), 4294967296L)
        self.assertEqual(long('hek2mgl', 25), 4294967296L)
        self.assertEqual(long('dnchbnm', 26), 4294967296L)
        self.assertEqual(long('b28jpdm', 27), 4294967296L)
        self.assertEqual(long('8pfgih4', 28), 4294967296L)
        self.assertEqual(long('76beigg', 29), 4294967296L)
        self.assertEqual(long('5qmcpqg', 30), 4294967296L)
        self.assertEqual(long('4q0jto4', 31), 4294967296L)
        self.assertEqual(long('4000000', 32), 4294967296L)
        self.assertEqual(long('3aokq94', 33), 4294967296L)
        self.assertEqual(long('2qhxjli', 34), 4294967296L)
        self.assertEqual(long('2br45qb', 35), 4294967296L)
        self.assertEqual(long('1z141z4', 36), 4294967296L)
        self.assertEqual(long('100000000000000000000000000000001', 2), 4294967297L)
        self.assertEqual(long('102002022201221111212', 3), 4294967297L)
        self.assertEqual(long('10000000000000001', 4), 4294967297L)
        self.assertEqual(long('32244002423142', 5), 4294967297L)
        self.assertEqual(long('1550104015505', 6), 4294967297L)
        self.assertEqual(long('211301422355', 7), 4294967297L)
        self.assertEqual(long('40000000001', 8), 4294967297L)
        self.assertEqual(long('12068657455', 9), 4294967297L)
        self.assertEqual(long('4294967297', 10), 4294967297L)
        self.assertEqual(long('1904440555', 11), 4294967297L)
        self.assertEqual(long('9ba461595', 12), 4294967297L)
        self.assertEqual(long('535a7988a', 13), 4294967297L)
        self.assertEqual(long('2ca5b7465', 14), 4294967297L)
        self.assertEqual(long('1a20dcd82', 15), 4294967297L)
        self.assertEqual(long('100000001', 16), 4294967297L)
        self.assertEqual(long('a7ffda92', 17), 4294967297L)
        self.assertEqual(long('704he7g5', 18), 4294967297L)
        self.assertEqual(long('4f5aff67', 19), 4294967297L)
        self.assertEqual(long('3723ai4h', 20), 4294967297L)
        self.assertEqual(long('281d55i5', 21), 4294967297L)
        self.assertEqual(long('1fj8b185', 22), 4294967297L)
        self.assertEqual(long('1606k7id', 23), 4294967297L)
        self.assertEqual(long('mb994ah', 24), 4294967297L)
        self.assertEqual(long('hek2mgm', 25), 4294967297L)
        self.assertEqual(long('dnchbnn', 26), 4294967297L)
        self.assertEqual(long('b28jpdn', 27), 4294967297L)
        self.assertEqual(long('8pfgih5', 28), 4294967297L)
        self.assertEqual(long('76beigh', 29), 4294967297L)
        self.assertEqual(long('5qmcpqh', 30), 4294967297L)
        self.assertEqual(long('4q0jto5', 31), 4294967297L)
        self.assertEqual(long('4000001', 32), 4294967297L)
        self.assertEqual(long('3aokq95', 33), 4294967297L)
        self.assertEqual(long('2qhxjlj', 34), 4294967297L)
        self.assertEqual(long('2br45qc', 35), 4294967297L)
        self.assertEqual(long('1z141z5', 36), 4294967297L)

    def test_conversion(self):

        class ClassicMissingMethods:
            pass

        self.assertRaises(AttributeError, long, ClassicMissingMethods())

        class MissingMethods(object):
            pass

        self.assertRaises(TypeError, long, MissingMethods())

        class Foo0:

            def __long__(self):
                return 42L

        class Foo1(object):

            def __long__(self):
                return 42L

        class Foo2(long):

            def __long__(self):
                return 42L

        class Foo3(long):

            def __long__(self):
                return self

        class Foo4(long):

            def __long__(self):
                return 42

        class Foo5(long):

            def __long__(self):
                return 42.0

        self.assertEqual(long(Foo0()), 42L)
        self.assertEqual(long(Foo1()), 42L)
        self.assertEqual(long(Foo2()), 42L)
        self.assertEqual(long(Foo3()), 0)
        self.assertEqual(long(Foo4()), 42)
        self.assertRaises(TypeError, long, Foo5())

        class Classic:
            pass

        for base in (object, Classic):

            class LongOverridesTrunc(base):

                def __long__(self):
                    return 42

                def __trunc__(self):
                    return -12

            self.assertEqual(long(LongOverridesTrunc()), 42)

            class JustTrunc(base):

                def __trunc__(self):
                    return 42

            self.assertEqual(long(JustTrunc()), 42)
            for trunc_result_base in (object, Classic):

                class Integral(trunc_result_base):

                    def __int__(self):
                        return 42

                class TruncReturnsNonLong(base):

                    def __trunc__(self):
                        return Integral()

                self.assertEqual(long(TruncReturnsNonLong()), 42)

                class NonIntegral(trunc_result_base):

                    def __trunc__(self):
                        return NonIntegral()

                class TruncReturnsNonIntegral(base):

                    def __trunc__(self):
                        return NonIntegral()

                try:
                    long(TruncReturnsNonIntegral())
                except TypeError as e:
                    self.assertEqual(str(e), '__trunc__ returned non-Integral (type NonIntegral)')
                else:
                    self.fail('Failed to raise TypeError with %s' % ((base, trunc_result_base),))

    def test_misc(self):
        hugepos = sys.maxint
        hugeneg = -hugepos - 1
        hugepos_aslong = long(hugepos)
        hugeneg_aslong = long(hugeneg)
        self.assertEqual(hugepos, hugepos_aslong, 'long(sys.maxint) != sys.maxint')
        self.assertEqual(hugeneg, hugeneg_aslong, 'long(-sys.maxint-1) != -sys.maxint-1')
        x = int(hugepos_aslong)
        try:
            self.assertEqual(x, hugepos, 'converting sys.maxint to long and back to int fails')
        except OverflowError:
            self.fail('int(long(sys.maxint)) overflowed!')

        if not isinstance(x, int):
            self.fail('int(long(sys.maxint)) should have returned int')
        x = int(hugeneg_aslong)
        try:
            self.assertEqual(x, hugeneg, 'converting -sys.maxint-1 to long and back to int fails')
        except OverflowError:
            self.fail('int(long(-sys.maxint-1)) overflowed!')

        if not isinstance(x, int):
            self.fail('int(long(-sys.maxint-1)) should have returned int')
        x = hugepos_aslong + 1
        try:
            y = int(x)
        except OverflowError:
            self.fail("int(long(sys.maxint) + 1) mustn't overflow")

        self.assertIsInstance(y, long, 'int(long(sys.maxint) + 1) should have returned long')
        x = hugeneg_aslong - 1
        try:
            y = int(x)
        except OverflowError:
            self.fail("int(long(-sys.maxint-1) - 1) mustn't overflow")

        self.assertIsInstance(y, long, 'int(long(-sys.maxint-1) - 1) should have returned long')

        class long2(long):
            pass

        x = long2(1267650600228229401496703205376L)
        y = int(x)
        self.assertTrue(type(y) is long, 'overflowing int conversion must return long not long subtype')

        class X(object):

            def __getslice__(self, i, j):
                return (i, j)

        with test_support.check_py3k_warnings():
            self.assertEqual(X()[-5L:7L], (-5, 7))
            slicemin, slicemax = X()[-1267650600228229401496703205376L:1267650600228229401496703205376L]
            self.assertEqual(X()[slicemin:slicemax], (slicemin, slicemax))

    def test_issue9869(self):

        class BadLong(object):

            def __long__(self):
                return 1000000

        class MyLong(long):
            pass

        x = MyLong(BadLong())
        self.assertIsInstance(x, long)
        self.assertEqual(x, 1000000)

    def test_auto_overflow(self):
        special = [0,
         1,
         2,
         3,
         sys.maxint - 1,
         sys.maxint,
         sys.maxint + 1]
        sqrt = int(math.sqrt(sys.maxint))
        special.extend([sqrt - 1, sqrt, sqrt + 1])
        special.extend([ -i for i in special ])

        def checkit(*args):
            self.assertEqual(got, expected, Frm('for %r expected %r got %r', args, expected, got))

        for x in special:
            longx = long(x)
            expected = -longx
            got = -x
            checkit('-', x)
            for y in special:
                longy = long(y)
                expected = longx + longy
                got = x + y
                checkit(x, '+', y)
                expected = longx - longy
                got = x - y
                checkit(x, '-', y)
                expected = longx * longy
                got = x * y
                checkit(x, '*', y)
                if y:
                    with test_support.check_py3k_warnings():
                        expected = longx / longy
                        got = x / y
                    checkit(x, '/', y)
                    expected = longx // longy
                    got = x // y
                    checkit(x, '//', y)
                    expected = divmod(longx, longy)
                    got = divmod(longx, longy)
                    checkit(x, 'divmod', y)
                if abs(y) < 5 and not (x == 0 and y < 0):
                    expected = longx ** longy
                    got = x ** y
                    checkit(x, '**', y)
                    for z in special:
                        if z != 0:
                            if y >= 0:
                                expected = pow(longx, longy, long(z))
                                got = pow(x, y, z)
                                checkit('pow', x, y, '%', z)
                            else:
                                self.assertRaises(TypeError, pow, longx, longy, long(z))

    @unittest.skipUnless(float.__getformat__('double').startswith('IEEE'), 'test requires IEEE 754 doubles')
    def test_float_conversion(self):
        import sys
        DBL_MAX = sys.float_info.max
        DBL_MAX_EXP = sys.float_info.max_exp
        DBL_MANT_DIG = sys.float_info.mant_dig
        exact_values = [0L,
         1L,
         2L,
         long(9007199254740989L),
         long(9007199254740990L),
         long(9007199254740991L),
         long(9007199254740992L),
         long(9007199254740994L),
         long(18014398509481980L),
         long(18014398509481982L),
         long(18014398509481984L),
         long(18014398509481988L)]
        for x in exact_values:
            self.assertEqual(long(float(x)), x)
            self.assertEqual(long(float(-x)), -x)

        for x, y in [(1, 0),
         (2, 2),
         (3, 4),
         (4, 4),
         (5, 4),
         (6, 6),
         (7, 8)]:
            for p in xrange(15):
                self.assertEqual(long(float(2L ** p * (9007199254740992L + x))), 2L ** p * (9007199254740992L + y))

        for x, y in [(0, 0),
         (1, 0),
         (2, 0),
         (3, 4),
         (4, 4),
         (5, 4),
         (6, 8),
         (7, 8),
         (8, 8),
         (9, 8),
         (10, 8),
         (11, 12),
         (12, 12),
         (13, 12),
         (14, 16),
         (15, 16)]:
            for p in xrange(15):
                self.assertEqual(long(float(2L ** p * (18014398509481984L + x))), 2L ** p * (18014398509481984L + y))

        long_dbl_max = long(DBL_MAX)
        top_power = 2 ** DBL_MAX_EXP
        halfway = (long_dbl_max + top_power) // 2
        self.assertEqual(float(long_dbl_max), DBL_MAX)
        self.assertEqual(float(long_dbl_max + 1), DBL_MAX)
        self.assertEqual(float(halfway - 1), DBL_MAX)
        self.assertRaises(OverflowError, float, halfway)
        self.assertEqual(float(1 - halfway), -DBL_MAX)
        self.assertRaises(OverflowError, float, -halfway)
        self.assertRaises(OverflowError, float, top_power - 1)
        self.assertRaises(OverflowError, float, top_power)
        self.assertRaises(OverflowError, float, top_power + 1)
        self.assertRaises(OverflowError, float, 2 * top_power - 1)
        self.assertRaises(OverflowError, float, 2 * top_power)
        self.assertRaises(OverflowError, float, top_power * top_power)
        for p in xrange(100):
            x = long(2 ** p * 9007199254740993L + 1)
            y = long(2 ** p * 9007199254740994L)
            self.assertEqual(long(float(x)), y)
            x = long(2 ** p * 9007199254740993L)
            y = long(2 ** p * 9007199254740992L)
            self.assertEqual(long(float(x)), y)

    def test_float_overflow(self):
        for x in (-2.0, -1.0, 0.0, 1.0, 2.0):
            self.assertEqual(float(long(x)), x)

        shuge = '12345' * 120
        huge = 7940903519132960324132517843492702513993728125208692855608343385791937317443908783509203179530892191987155926623978283105489921384424923263573391363734522382231742028063376725759936388639366060309563838895747548705834901470733791335653266902911839098782447109218743196966760157998340228043734553776187051118620709439579947093508401401631712073916879445638849346437187368000288168434884333847925762236847628855418907650698624898277065152326488047315941120701839655677173867549336208651066198963223290589867846485132811671585188249558469966534679356622663014517463255220325474870240326369687171527575053114352298945393524403254488026713532705619878245336270252062774783554202422698010972274190731058780728665028820297377514920071911925316084153056162480126388256580805608668574098316652608084771381953279181807157124713495613535424964215087630579096416669412630963986266552255718328160093117171637176650461295905567798132566281830354760366845352847955988129319896463854644608371823052534475141787679872786514159114921739708002617255270132388918811410977435895396248451768654187319563238686283969523236598937575074075134832047015519967296117865059672408654143498300165797510261969248336086014507694880004991778986415235204301660350334495307361712887960284632677139787048917393643287459305474248980105673159828131668823017101082986585062392365948205090959113071881041827910955350953704544370610472951070584567122153134386488507931897347896476243074931121650906482288868176150253025211895156520637042141877938782162689974142535856811409350797999956935841304870462808561495898333508472825831608841541629774755125749727159621742064615698362754332703890081287850192279465994174027123241887841355700008797695827617585094166714681343934267814915983302899637208486895379003478260404794370190915279231820733870379611984486892305385547891658035957444915773234512895626653324329822236838347833347687425757461860385229811346853592062462047018996231044691628755849499236009150479879605728979573172369124457634185102981264603566083370978970799101089027836554440382819472118601458401918643928069876406542406071118615806625085824456854863979645899966637153209552212396640437943772545570483804997716243538941179327354233526696713020947472416870994670783011051712327870774436583319125031316426803072026069142645544005733014128831146765979494598139825459105864907583965881882621065226983702618061228442756431769122964613617375193603363395778677616863258776074909714481159472483656638636883905929561817009023225704494931649580244483067442895448116590200567862439843508757338874305666064020338586615494230869950377610901426952558555290754646731084712315377291685221486683802783173117977276188840040275281110684283769640407214107271547786283887632689107752753390160523083386097747662361270177689418705527656522586458191862673847072061569739104492290520198683038902176982310753849809395320886639517634536158200806471259521049539727943187963197268440224844191407585128461076820807297787167383627575728041411301362585409493415870308423212193521149493260116945970404112377639493777243891271756621388699383660092483378247137837404268181140483370799330162426982827657152251244197941017192462061402979725739794687203586057387049201328340740887613387447373950100364897993316703441609904410822270956774058525196895813450925460655992776458785696356096538719329635647435239637380987498860439974395381303640979706981047664449092837741423437750637398558006767405145577627845832442613424523401175851345000125719849355699508871872809722871771728920574635057754539704808256398258021657181631646653858218142294843188825332270943094773719052109024064741171772477805603508257036674300294772683042759362219623448371538133982379930047191809206227921208700106982255244604098915930509977374486881810265642413314768183921252265575687635855689358364488784569782073768095310083723171411494279585407016158164945621505763617207893409944262618402965931873079670095015733617746877300750509712879507227799458469597736523821060866640083030773506593703498958271459509635430714515996165957316860755452659887380754883726465754562084009757807676742841540915231452746388930155368777969302149196612427015257866224609809635545481432467055079781718688694625568390291242476874334496646167840811344038616912036262677898752353137617932464426938533068149594397330418793795121451178296619780889116946269720756453197797175630467028831811767694924026443309816620034415671299267529082859608565046302314480222041155660138589746509861360513578781207262965589567494651373413182425009104839730190149937947622089525920708952014849827703025335438184057214637609601759797823298934525394090047984591262655321980211610728487690126512120377208077136664007624578448120627230396424410042374844009670652260318316136052064907073435701629756724920584736158928924278934883719667988746713618906882417265966338374439287540631235652183805585782577155016112920519870327732380836637193766632802136294403009176925679245705047676377488689151940988044538779620569126246914623230622550873833016216386563851328799259238499209999554275144036829640523748021401728023122244307347992671576527851754613176709861868141311926931354304172823126246339384547648330807215813145604886297539405314289438215407049391797179642618840408152005708840007039063560129359925732830917411892757772809818575096784644565715760330894450126391162364208544862724738685623480831213673235809909380477161451584643843568534938096246268595494491365840517011400827280642612038747802019218876411298166730081425354989926655512260424077683575852034407693008704791720595633742513869707262524626017377493164287304819460043078664039641036775279542417209435165675567825046032886316406129631936546931605479637395114227232190652680872356798895146260947715560593392445186984236956570815352503866425684731286029621371987843983873934202001834098493770340755884933421197354319996162927798822953001886866626905634079645276444343953882636459987016836014105836047428179943564602344815587492558221783493716856715822173632068059947551285269563622335522991489745734282255801862901539307877621890762534259395955994265498441398061542138034565251317948280490260333910701284702637378217580300519778821654757373607001758665360274942735667175469786830514617316799788829828488595159136082781420787173940977589036643699445988900111463504091118505957731531122881013656096713848503207213801429450347652261701703797452710816893657403894575437034934309359118706773291294149609820409223114512957520662826447436712867350827763314329955554198056499593324617110997418473591698243750929034579737043373422295332799624460483435014107165058059680662756509294186127896780339588928295545567048648137777388824658242865273549421647865095857398123831625977971274399024570969728319426236983475449696817501513013923092811160488701020981223217638134870238330785987777362107900870220566117625369732484685079573905971412010869204851929675105202526462440450843331477591337504677466560247802932519058064669736932026506218065518053804099470058672554881957334239171945470128328111118154219248709276771964468934141432065279835956804758479020506175634676314795774377756781619147787644127864326395955719541635424625005330931654336931776693662159112848110480538382283610794193466885074933882258128230814880496958689388480616019325410776127163363865400356822111134438394432428391432135839292661553803106862931835006288173627261324100173990865286349533830063091557567956830696284020826665435848602925945339374112474445787390743846224660527423380047536181832382852749004482639132488012423772632872567611837956509727738665319125833435486837183884662511338560958654837653843605981267354569271666682256876436360004085720878438365292520427632066423329003200404292501117164412280016866913720423748205122496830626503634357509731013181992464259628431617164036515488291676782170317826525643681591655990081992152832281532788807385136544281343581225957439747570626419144498020442835012520333597010650792505163588284469813745780712765859388127933246124890834158661340828624389473858924747755262424780692268948813094438604009655040806473697307373869826808819809241641401202736133330433499401052488323809427280113231657969181497898455075395595987717599255810574111896611381295446449094360605719953456587602255949355196532488359097463064531159681099827588754339376178603572206993104116724005865677519296398159948715473178534023839748776968930959359430050467682338953460003719728316579187691878697698768262029532555154453385626292655405747586784964721828435123748874036892336467993833313566351099012062133708330659839945835334408003540883710466685587003017166599283017074947301584414988865004786028293285499770491180405306064801835537732617278174051627839185610787636744236037208733359089934980863639140305262357999304049578253805867435072383872118239392509532576937965747681037411189244456427767218969226659923736338685936365229374852506760977484949718096704779139202025385886007539531005659537317072283913313695763253184409898181120428466758352325450311576982995045335286929880973682790673015037574198678081581095988135833790694215909376L
        mhuge = -huge
        namespace = {'huge': huge,
         'mhuge': mhuge,
         'shuge': shuge,
         'math': math}
        for test in ['float(huge)',
         'float(mhuge)',
         'complex(huge)',
         'complex(mhuge)',
         'complex(huge, 1)',
         'complex(mhuge, 1)',
         'complex(1, huge)',
         'complex(1, mhuge)',
         '1. + huge',
         'huge + 1.',
         '1. + mhuge',
         'mhuge + 1.',
         '1. - huge',
         'huge - 1.',
         '1. - mhuge',
         'mhuge - 1.',
         '1. * huge',
         'huge * 1.',
         '1. * mhuge',
         'mhuge * 1.',
         '1. // huge',
         'huge // 1.',
         '1. // mhuge',
         'mhuge // 1.',
         '1. / huge',
         'huge / 1.',
         '1. / mhuge',
         'mhuge / 1.',
         '1. ** huge',
         'huge ** 1.',
         '1. ** mhuge',
         'mhuge ** 1.',
         'math.sin(huge)',
         'math.sin(mhuge)',
         'math.sqrt(huge)',
         'math.sqrt(mhuge)',
         'math.floor(huge)',
         'math.floor(mhuge)']:
            self.assertRaises(OverflowError, eval, test, namespace)
            self.assertNotEqual(float(shuge), int(shuge), 'float(shuge) should not equal int(shuge)')

    def test_logs(self):
        LOG10E = math.log10(math.e)
        for exp in range(10) + [100, 1000, 10000]:
            value = 10 ** exp
            log10 = math.log10(value)
            self.assertAlmostEqual(log10, exp)
            expected = exp / LOG10E
            log = math.log(value)
            self.assertAlmostEqual(log, expected)

        for bad in (-19950631168807583848837421626835850838234968318861924548520089498529438830221946631919961684036194597899331129423209124271556491349413781117593785932096323957855730046793794526765246551266059895520550086918193311542508608460618104685509074866089624888090489894838009253941633257850621568309473902556912388065225096643874441046759871626985453222868538161694315775629640762836880760732228535091641476183956381458969463899410840960536267821064621427333394036525565649530603142680234969400335934316651459297773279665775606172582031407994198179607378245683762280037302885487251900834464581454650557929601414833921615734588139257095379769119277800826957735674444123062018757836325502728323789270710373802866393031428133241401624195671690574061419654342324638801248856147305207431992259611796250130992860241708340807605932320161268492288496255841312844061536738951487114256315111089745514203313820202931640957596464756010405845841566072044962867016515061920631004186422275908670900574606417856951911456055068251250406007519842261898059237118054444788072906395242548339221982707404473162376760846613033778706039803413197133493654622700563169937455508241780972810983291314403571877524768509857276937926433221599399876886660808368837838027643282775172273657572744784112294389733810861607423253291974813120197604178281965697475898164531258434135959862784130128185406283476649088690521047580882615823961985770122407044330583075869039319604603404973156583208672105913300903752823415539745394397715257455290510212310947321610753474825740775273986348298498340756937955646638621874569499279016572103701364433135817214311791398222983845847334440270964182851005072927748364550578634501100852987812389473928699540834346158807043959118985815145779177143619698728131459483783202081474982171858011389071228250905826817436220577475921417653715687725614904582904992461028630081535583308130101987675856234343538955409175623400844887526162643568648833519463720377293240094456246923254350400678027273837755376406726898636241037491410966718557050759098100246789880178271925953381282421954028302759408448955014676668389697996886241636313376393903373455801407636741877711055384225739499110186468219696581651485130494222369947714763069155468217682876200362777257723781365331611196811280792669481887201298643660768551639860534602297871557517947385246369446923087894265948217008051120322365496288169035739121368338393591756418733850510970271613915439590991598154654417336311656936031122249937969999226781732358023111862644575299135758175008199839236284615249881088960232244362173771618086357015468484058622329792853875623486556440536962622018963571028812361567512543338303270029097668650568557157505516727518899194129711337690149916181315171544007728650573189557450920330185304847113818315407324053319038462084036421763703911550639789000742853672196280903477974533320468368795868580237952218629120080742819551317948157624448298518461509704888027274721574688131594750409732115080498190455803416826949787141316063210686391511681774304792596709376L, -2L, 0L):
            self.assertRaises(ValueError, math.log, bad)
            self.assertRaises(ValueError, math.log10, bad)

    def test_mixed_compares(self):
        eq = self.assertEqual

        class Rat:

            def __init__(self, value):
                if isinstance(value, (int, long)):
                    self.n = value
                    self.d = 1
                else:
                    if isinstance(value, float):
                        f, e = math.frexp(abs(value))
                        if not (f == 0 or 0.5) <= f < 1.0:
                            raise AssertionError
                            CHUNK = 28
                            top = 0
                            while f:
                                f = math.ldexp(f, CHUNK)
                                digit = int(f)
                                raise digit >> CHUNK == 0 or AssertionError
                                top = top << CHUNK | digit
                                f -= digit
                                raise 0.0 <= f < 1.0 or AssertionError
                                e -= CHUNK

                            n = e >= 0 and top << e
                            d = 1
                        else:
                            n = top
                            d = 1 << -e
                        n = value < 0 and -n
                    self.n = n
                    self.d = d
                    if not float(n) / float(d) == value:
                        raise AssertionError
                    else:
                        raise TypeError("can't deal with %r" % value)

            def __cmp__(self, other):
                if not isinstance(other, Rat):
                    other = Rat(other)
                return cmp(self.n * other.d, self.d * other.n)

        cases = [0,
         0.001,
         0.99,
         1.0,
         1.5,
         1e+20,
         1e+200]
        for t in (281474976710656.0, 1125899906842624.0, 9007199254740992.0):
            cases.extend([t - 1.0,
             t - 0.3,
             t,
             t + 0.3,
             t + 1.0,
             long(t - 1),
             long(t),
             long(t + 1)])

        cases.extend([0,
         1,
         2,
         sys.maxint,
         float(sys.maxint)])
        t = long(1e+200)
        cases.extend([0L,
         1L,
         2L,
         398027684033796659235430720619120245370477278049242593871342686565238635974930057042676009749975595510836461137504912702831400376935319143621753470415827025981215282426893498224826615977707595539466961019588699726772279731941315198182787264034852821200164566127930390710398182979935327718016873784821349516406114982916691867361875370024545872140793827277482562824192439237801588697814168520338650090909697535966525032757049430286459482977357373598020450589927318365663076719136934132593126761906696003770385305284570331119691001526584347722012386381881779425549210851696458253943578557699072154639655630793883941961378971846841113804188730258903839103669626086974468150655710480841592465655211805257863007811676888839555017536731758113448656752514158601444051645154665514388431619042396106716755762338728183461369854648923972904427556158821823778729193111453445844216979095435045778144571378954652122396061615147642540250745857228893999875491625014946013839340891326060933901036249999238637827577774666644809734033861619420363936465178730919233673114244563915058438996625834112132967998495576249320462871747777012165543887156255858358784852335060574881876552025685704823768078710818951860741379429242110855644973977420413810373514584504006896392675854997866870818564207239083874324953871276375716101506575153205747363963740749867514682619756775534507006871485887812402927738227576635284174246988540785975240020481266853076127172228024330561550120182008777598230542033702463408316671120886169260934006805799864598636311179787776738608992346063063099659648279663878174074787179237169752957046404584525301384153358344055908219695854852185210739761460551596658211013159915409566145426809737550417578228465835830890294497535463112081537672664056891624345779311524560019984315456142126282898486728345004767873499752683471409587367450593302392307908004590644754012537113320493601682133709318222647489080531644015321391157387178232154126828007760313716872242209614200967522180475716199973689467714010404673961454146466045855232217196687665143147612199151921277432309700460321430381533385245877431330533479476152339364503436322919665631042328740463612565842560411947020174006507893396276103834436233140915025391014386119201176462659556388343058600326710618903683746516577021214276933289179021059956925949717956040857979165914170970056212869933593589268626151996676594370800885093048230687152803213254735594741799076039453057272319884322341883241036382617598401889439130301876975498681736174215711287053447013711596004574803562701388246822510391522419061320663740921321754344166744899588160649291823535983386025904942040724581017615968429577015808090360968544059204594200069304612417366398776831532265596224715750301792207725607932534543693758772262010387360435567635232718343420679693057360004073679493008945813961012439574397373178636054628207647520675194420244271036343729318858430871461978866964772362057290577326080664463129657590249859748544101333842092713653096656066266827446079145590196644643417403723220085696202719321533233027169599734928971588850348415000070034027025298183104148343980297663148971586607903771717880683175436445585810610546882073571556162324659351310326560804448974229349743425637164834242799991427145050899469511954834774847172360693568437689147399455672090773686782511054291185172381917008889957645311339950993044779783607140593766508017935992581357858306525303783231752425242008347844867988333025417249944092118578113687403158162707075154006053416374075765162668533127078605316562826337193606242535290683224423660462222408680300498714149607265550441220738075941633988435051594487256802874182264814425923111193188280632013127802897889605338783089532740877202304122498193625454768343775535498872821099981620497070810489137457106892573248498734243717184800822956334469415666818858073218653977954309023182851723246522042792401461382001601920501284439325214084210736400630884929942272982943613708123011355260915545831043160243523599372006226150289664982113944898886610710824955096724626895416484521819026132177640598691658035986285376355033719094568083122219345722063613609779158338084375331431276527548482566210071347744541292871876134764249704859840950276227627328897424208932988115108907187647698491814375639614313178092528678007370045871748218421786396197284213209022623762734630836006864192414605237248983289006905268988475197599781524158913583701325199090352274252608342971303907669363045656232183978755853064004010895030834921988601355201181158877254807798058635127708445592064519563115094749276606697559529332807221414021024905241788974917755034700510432039890197393691722911126889174394312127254793141624975830429097997705531781908242083922068769027355129212617244130640289994777413026624013157329948333586377955103195844817163822484232700763859290253400376515701986753596890075818544485475785780031843579065754095099970940504640212850809997051128976563880886392410766321449987529690463262182894272302749154535447233331028841215215533602398281107050696017507827602761547816324743297938177204183765821117818869959795031848201322436053103778993541384779857262311465895754085538371969040922420936915076653500310175006188572019017358300979056992161958286882575984331858170857303361269891312794369244896540323192451678830668180455059289743580640736076233561935888109525845803125912388965524166819855977061399043499229843517930169118036812460794615667808961600389778306540324849286501515292799391304510997298128228258006156017389878086272789993321416349205921635696963703558971391123174877353757536774013315034956942784403824181551741629180658414081905650333672638983416786388095026169496605199749691595798835947189777822765198767949699778106683862989103096006505865271003566346191382406011673958404009194852110016915222433459641787170917872140367871023596464051647947388580570774462304347896201676197195521428782313608583714399238092208362933211302942806480175589402387976531080436906856834377344137698180789562645974374155400497754843905032231188252125802180353577510519869570675234892321663406309376L,
         t - 1,
         t,
         t + 1])
        cases.extend([ -x for x in cases ])
        for x in cases:
            Rx = Rat(x)
            for y in cases:
                Ry = Rat(y)
                Rcmp = cmp(Rx, Ry)
                xycmp = cmp(x, y)
                eq(Rcmp, xycmp, Frm('%r %r %d %d', x, y, Rcmp, xycmp))
                eq(x == y, Rcmp == 0, Frm('%r == %r %d', x, y, Rcmp))
                eq(x != y, Rcmp != 0, Frm('%r != %r %d', x, y, Rcmp))
                eq(x < y, Rcmp < 0, Frm('%r < %r %d', x, y, Rcmp))
                eq(x <= y, Rcmp <= 0, Frm('%r <= %r %d', x, y, Rcmp))
                eq(x > y, Rcmp > 0, Frm('%r > %r %d', x, y, Rcmp))
                eq(x >= y, Rcmp >= 0, Frm('%r >= %r %d', x, y, Rcmp))

    def test_nan_inf(self):
        self.assertRaises(OverflowError, long, float('inf'))
        self.assertRaises(OverflowError, long, float('-inf'))
        self.assertRaises(ValueError, long, float('nan'))

    def test_bit_length(self):
        tiny = 1e-10
        for x in xrange(-65000, 65000):
            x = long(x)
            k = x.bit_length()
            self.assertEqual(k, len(bin(x).lstrip('-0b')))
            if x != 0:
                self.assertTrue(2 ** (k - 1) <= abs(x) < 2 ** k)
            else:
                self.assertEqual(k, 0)
            if x != 0:
                self.assertEqual(k, 1 + math.floor(math.log(abs(x)) / math.log(2) + tiny))

        self.assertEqual(0L.bit_length(), 0)
        self.assertEqual(1L.bit_length(), 1)
        self.assertEqual((-1L).bit_length(), 1)
        self.assertEqual(2L.bit_length(), 2)
        self.assertEqual((-2L).bit_length(), 2)
        for i in [2,
         3,
         15,
         16,
         17,
         31,
         32,
         33,
         63,
         64,
         234]:
            a = 2L ** i
            self.assertEqual((a - 1).bit_length(), i)
            self.assertEqual((1 - a).bit_length(), i)
            self.assertEqual(a.bit_length(), i + 1)
            self.assertEqual((-a).bit_length(), i + 1)
            self.assertEqual((a + 1).bit_length(), i + 1)
            self.assertEqual((-a - 1).bit_length(), i + 1)


def test_main():
    test_support.run_unittest(LongTest)


if __name__ == '__main__':
    test_main()