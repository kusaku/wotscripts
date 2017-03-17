# Embedded file name: scripts/common/Lib/test/test_bytes.py
"""Unit tests for the bytes and bytearray types.

XXX This is a mess.  Common tests should be moved to buffer_tests.py,
which itself ought to be unified with string_tests.py (and the latter
should be modernized).
"""
import os
import re
import sys
import copy
import functools
import pickle
import tempfile
import unittest
import test.test_support
import test.string_tests
import test.buffer_tests
if sys.flags.bytes_warning:

    def check_bytes_warnings(func):

        @functools.wraps(func)
        def wrapper(*args, **kw):
            with test.test_support.check_warnings(('', BytesWarning)):
                return func(*args, **kw)

        return wrapper


else:

    def check_bytes_warnings(func):
        return func


class Indexable():

    def __init__(self, value = 0):
        self.value = value

    def __index__(self):
        return self.value


class BaseBytesTest(unittest.TestCase):

    def test_basics(self):
        b = self.type2test()
        self.assertEqual(type(b), self.type2test)
        self.assertEqual(b.__class__, self.type2test)

    def test_empty_sequence(self):
        b = self.type2test()
        self.assertEqual(len(b), 0)
        self.assertRaises(IndexError, lambda : b[0])
        self.assertRaises(IndexError, lambda : b[1])
        self.assertRaises(IndexError, lambda : b[sys.maxint])
        self.assertRaises(IndexError, lambda : b[sys.maxint + 1])
        self.assertRaises(IndexError, lambda : b[10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L])
        self.assertRaises(IndexError, lambda : b[-1])
        self.assertRaises(IndexError, lambda : b[-2])
        self.assertRaises(IndexError, lambda : b[-sys.maxint])
        self.assertRaises(IndexError, lambda : b[-sys.maxint - 1])
        self.assertRaises(IndexError, lambda : b[-sys.maxint - 2])
        self.assertRaises(IndexError, lambda : b[-10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L])

    def test_from_list(self):
        ints = list(range(256))
        b = self.type2test((i for i in ints))
        self.assertEqual(len(b), 256)
        self.assertEqual(list(b), ints)

    def test_from_index(self):
        b = self.type2test([Indexable(),
         Indexable(1),
         Indexable(254),
         Indexable(255)])
        self.assertEqual(list(b), [0,
         1,
         254,
         255])
        self.assertRaises(ValueError, self.type2test, [Indexable(-1)])
        self.assertRaises(ValueError, self.type2test, [Indexable(256)])

    def test_from_ssize(self):
        self.assertEqual(self.type2test(0), '')
        self.assertEqual(self.type2test(1), '\x00')
        self.assertEqual(self.type2test(5), '\x00\x00\x00\x00\x00')
        self.assertRaises(ValueError, self.type2test, -1)
        self.assertEqual(self.type2test('0', 'ascii'), '0')
        self.assertEqual(self.type2test('0'), '0')
        self.assertRaises(OverflowError, self.type2test, sys.maxsize + 1)

    def test_constructor_type_errors(self):
        self.assertRaises(TypeError, self.type2test, 0.0)

        class C:
            pass

        self.assertRaises(TypeError, self.type2test, [0.0])
        self.assertRaises(TypeError, self.type2test, [None])
        self.assertRaises(TypeError, self.type2test, [C()])
        return

    def test_constructor_value_errors(self):
        self.assertRaises(ValueError, self.type2test, [-1])
        self.assertRaises(ValueError, self.type2test, [-sys.maxint])
        self.assertRaises(ValueError, self.type2test, [-sys.maxint - 1])
        self.assertRaises(ValueError, self.type2test, [-sys.maxint - 2])
        self.assertRaises(ValueError, self.type2test, [-10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L])
        self.assertRaises(ValueError, self.type2test, [256])
        self.assertRaises(ValueError, self.type2test, [257])
        self.assertRaises(ValueError, self.type2test, [sys.maxint])
        self.assertRaises(ValueError, self.type2test, [sys.maxint + 1])
        self.assertRaises(ValueError, self.type2test, [10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000L])

    def test_compare(self):
        b1 = self.type2test([1, 2, 3])
        b2 = self.type2test([1, 2, 3])
        b3 = self.type2test([1, 3])
        self.assertEqual(b1, b2)
        self.assertTrue(b2 != b3)
        self.assertTrue(b1 <= b2)
        self.assertTrue(b1 <= b3)
        self.assertTrue(b1 < b3)
        self.assertTrue(b1 >= b2)
        self.assertTrue(b3 >= b2)
        self.assertTrue(b3 > b2)
        self.assertFalse(b1 != b2)
        self.assertFalse(b2 == b3)
        self.assertFalse(b1 > b2)
        self.assertFalse(b1 > b3)
        self.assertFalse(b1 >= b3)
        self.assertFalse(b1 < b2)
        self.assertFalse(b3 < b2)
        self.assertFalse(b3 <= b2)

    @check_bytes_warnings
    def test_compare_to_str(self):
        self.assertEqual(self.type2test('\x00a\x00b\x00c') == u'abc', False)
        self.assertEqual(self.type2test('\x00\x00\x00a\x00\x00\x00b\x00\x00\x00c') == u'abc', False)
        self.assertEqual(self.type2test('a\x00b\x00c\x00') == u'abc', False)
        self.assertEqual(self.type2test('a\x00\x00\x00b\x00\x00\x00c\x00\x00\x00') == u'abc', False)
        self.assertEqual(self.type2test() == unicode(), False)
        self.assertEqual(self.type2test() != unicode(), True)

    def test_reversed(self):
        input = list(map(ord, 'Hello'))
        b = self.type2test(input)
        output = list(reversed(b))
        input.reverse()
        self.assertEqual(output, input)

    def test_getslice(self):

        def by(s):
            return self.type2test(map(ord, s))

        b = by('Hello, world')
        self.assertEqual(b[:5], by('Hello'))
        self.assertEqual(b[1:5], by('ello'))
        self.assertEqual(b[5:7], by(', '))
        self.assertEqual(b[7:], by('world'))
        self.assertEqual(b[7:12], by('world'))
        self.assertEqual(b[7:100], by('world'))
        self.assertEqual(b[:-7], by('Hello'))
        self.assertEqual(b[-11:-7], by('ello'))
        self.assertEqual(b[-7:-5], by(', '))
        self.assertEqual(b[-5:], by('world'))
        self.assertEqual(b[-5:12], by('world'))
        self.assertEqual(b[-5:100], by('world'))
        self.assertEqual(b[-100:5], by('Hello'))

    def test_extended_getslice(self):
        L = list(range(255))
        b = self.type2test(L)
        indices = (0, None, 1, 3, 19, 100, -1, -2, -31, -100)
        for start in indices:
            for stop in indices:
                for step in indices[1:]:
                    self.assertEqual(b[start:stop:step], self.type2test(L[start:stop:step]))

        return None

    def test_encoding(self):
        sample = u'Hello world\n\u1234\u5678\u9abc\udef0'
        for enc in ('utf8', 'utf16'):
            b = self.type2test(sample, enc)
            self.assertEqual(b, self.type2test(sample.encode(enc)))

        self.assertRaises(UnicodeEncodeError, self.type2test, sample, 'latin1')
        b = self.type2test(sample, 'latin1', 'ignore')
        self.assertEqual(b, self.type2test(sample[:-4], 'utf-8'))

    def test_decode(self):
        sample = u'Hello world\n\u1234\u5678\u9abc\\def0\\def0'
        for enc in ('utf8', 'utf16'):
            b = self.type2test(sample, enc)
            self.assertEqual(b.decode(enc), sample)

        sample = u'Hello world\n\x80\x81\xfe\xff'
        b = self.type2test(sample, 'latin1')
        self.assertRaises(UnicodeDecodeError, b.decode, 'utf8')
        self.assertEqual(b.decode('utf8', 'ignore'), 'Hello world\n')
        self.assertEqual(b.decode(errors='ignore', encoding='utf8'), 'Hello world\n')

    def test_from_int(self):
        b = self.type2test(0)
        self.assertEqual(b, self.type2test())
        b = self.type2test(10)
        self.assertEqual(b, self.type2test([0] * 10))
        b = self.type2test(10000)
        self.assertEqual(b, self.type2test([0] * 10000))

    def test_concat(self):
        b1 = self.type2test('abc')
        b2 = self.type2test('def')
        self.assertEqual(b1 + b2, 'abcdef')
        self.assertEqual(b1 + bytes('def'), 'abcdef')
        self.assertEqual(bytes('def') + b1, 'defabc')
        self.assertRaises(TypeError, lambda : b1 + u'def')
        self.assertRaises(TypeError, lambda : u'abc' + b2)

    def test_repeat(self):
        for b in ('abc', self.type2test('abc')):
            self.assertEqual(b * 3, 'abcabcabc')
            self.assertEqual(b * 0, '')
            self.assertEqual(b * -1, '')
            self.assertRaises(TypeError, lambda : b * 3.14)
            self.assertRaises(TypeError, lambda : 3.14 * b)
            self.assertRaises((OverflowError, MemoryError), lambda : b * sys.maxsize)

    def test_repeat_1char(self):
        self.assertEqual(self.type2test('x') * 100, self.type2test([ord('x')] * 100))

    def test_contains(self):
        b = self.type2test('abc')
        self.assertIn(ord('a'), b)
        self.assertIn(int(ord('a')), b)
        self.assertNotIn(200, b)
        self.assertRaises(ValueError, lambda : 300 in b)
        self.assertRaises(ValueError, lambda : -1 in b)
        self.assertRaises(TypeError, lambda : None in b)
        self.assertRaises(TypeError, lambda : float(ord('a')) in b)
        self.assertRaises(TypeError, lambda : u'a' in b)
        for f in (bytes, bytearray):
            self.assertIn(f(''), b)
            self.assertIn(f('a'), b)
            self.assertIn(f('b'), b)
            self.assertIn(f('c'), b)
            self.assertIn(f('ab'), b)
            self.assertIn(f('bc'), b)
            self.assertIn(f('abc'), b)
            self.assertNotIn(f('ac'), b)
            self.assertNotIn(f('d'), b)
            self.assertNotIn(f('dab'), b)
            self.assertNotIn(f('abd'), b)

    def test_fromhex(self):
        self.assertRaises(TypeError, self.type2test.fromhex)
        self.assertRaises(TypeError, self.type2test.fromhex, 1)
        self.assertEqual(self.type2test.fromhex(u''), self.type2test())
        b = bytearray([26, 43, 48])
        self.assertEqual(self.type2test.fromhex(u'1a2B30'), b)
        self.assertEqual(self.type2test.fromhex(u'  1A 2B  30   '), b)
        self.assertEqual(self.type2test.fromhex(u'0000'), '\x00\x00')
        self.assertRaises(ValueError, self.type2test.fromhex, u'a')
        self.assertRaises(ValueError, self.type2test.fromhex, u'rt')
        self.assertRaises(ValueError, self.type2test.fromhex, u'1a b cd')
        self.assertRaises(ValueError, self.type2test.fromhex, u'\x00')
        self.assertRaises(ValueError, self.type2test.fromhex, u'12   \x00   34')

    def test_join(self):
        self.assertEqual(self.type2test('').join([]), '')
        self.assertEqual(self.type2test('').join(['']), '')
        for lst in [['abc'],
         ['a', 'bc'],
         ['ab', 'c'],
         ['a', 'b', 'c']]:
            lst = list(map(self.type2test, lst))
            self.assertEqual(self.type2test('').join(lst), 'abc')
            self.assertEqual(self.type2test('').join(tuple(lst)), 'abc')
            self.assertEqual(self.type2test('').join(iter(lst)), 'abc')

        self.assertEqual(self.type2test('.').join(['ab', 'cd']), 'ab.cd')

    def test_count(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.count('i'), 4)
        self.assertEqual(b.count('ss'), 2)
        self.assertEqual(b.count('w'), 0)

    def test_startswith(self):
        b = self.type2test('hello')
        self.assertFalse(self.type2test().startswith('anything'))
        self.assertTrue(b.startswith('hello'))
        self.assertTrue(b.startswith('hel'))
        self.assertTrue(b.startswith('h'))
        self.assertFalse(b.startswith('hellow'))
        self.assertFalse(b.startswith('ha'))

    def test_endswith(self):
        b = self.type2test('hello')
        self.assertFalse(bytearray().endswith('anything'))
        self.assertTrue(b.endswith('hello'))
        self.assertTrue(b.endswith('llo'))
        self.assertTrue(b.endswith('o'))
        self.assertFalse(b.endswith('whello'))
        self.assertFalse(b.endswith('no'))

    def test_find(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.find('ss'), 2)
        self.assertEqual(b.find('ss', 3), 5)
        self.assertEqual(b.find('ss', 1, 7), 2)
        self.assertEqual(b.find('ss', 1, 3), -1)
        self.assertEqual(b.find('w'), -1)
        self.assertEqual(b.find('mississippian'), -1)

    def test_rfind(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.rfind('ss'), 5)
        self.assertEqual(b.rfind('ss', 3), 5)
        self.assertEqual(b.rfind('ss', 0, 6), 2)
        self.assertEqual(b.rfind('w'), -1)
        self.assertEqual(b.rfind('mississippian'), -1)

    def test_index(self):
        b = self.type2test('world')
        self.assertEqual(b.index('w'), 0)
        self.assertEqual(b.index('orl'), 1)
        self.assertRaises(ValueError, b.index, 'worm')
        self.assertRaises(ValueError, b.index, 'ldo')

    def test_rindex(self):
        b = self.type2test('world')
        self.assertEqual(b.rindex('w'), 0)
        self.assertEqual(b.rindex('orl'), 1)
        self.assertRaises(ValueError, b.rindex, 'worm')
        self.assertRaises(ValueError, b.rindex, 'ldo')

    def test_replace(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.replace('i', 'a'), 'massassappa')
        self.assertEqual(b.replace('ss', 'x'), 'mixixippi')

    def test_split(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.split('i'), ['m',
         'ss',
         'ss',
         'pp',
         ''])
        self.assertEqual(b.split('ss'), ['mi', 'i', 'ippi'])
        self.assertEqual(b.split('w'), [b])

    def test_split_whitespace(self):
        for b in ('  arf  barf  ', 'arf\tbarf', 'arf\nbarf', 'arf\rbarf', 'arf\x0cbarf', 'arf\x0bbarf'):
            b = self.type2test(b)
            self.assertEqual(b.split(), ['arf', 'barf'])
            self.assertEqual(b.split(None), ['arf', 'barf'])
            self.assertEqual(b.split(None, 2), ['arf', 'barf'])

        for b in ('a\x1cb', 'a\x1db', 'a\x1eb', 'a\x1fb'):
            b = self.type2test(b)
            self.assertEqual(b.split(), [b])

        self.assertEqual(self.type2test('  a  bb  c  ').split(None, 0), ['a  bb  c  '])
        self.assertEqual(self.type2test('  a  bb  c  ').split(None, 1), ['a', 'bb  c  '])
        self.assertEqual(self.type2test('  a  bb  c  ').split(None, 2), ['a', 'bb', 'c  '])
        self.assertEqual(self.type2test('  a  bb  c  ').split(None, 3), ['a', 'bb', 'c'])
        return

    def test_split_string_error(self):
        self.assertRaises(TypeError, self.type2test('a b').split, u' ')

    def test_split_unicodewhitespace(self):
        b = self.type2test('\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f')
        self.assertEqual(b.split(), ['\x1c\x1d\x1e\x1f'])

    def test_rsplit(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.rsplit('i'), ['m',
         'ss',
         'ss',
         'pp',
         ''])
        self.assertEqual(b.rsplit('ss'), ['mi', 'i', 'ippi'])
        self.assertEqual(b.rsplit('w'), [b])

    def test_rsplit_whitespace(self):
        for b in ('  arf  barf  ', 'arf\tbarf', 'arf\nbarf', 'arf\rbarf', 'arf\x0cbarf', 'arf\x0bbarf'):
            b = self.type2test(b)
            self.assertEqual(b.rsplit(), ['arf', 'barf'])
            self.assertEqual(b.rsplit(None), ['arf', 'barf'])
            self.assertEqual(b.rsplit(None, 2), ['arf', 'barf'])

        self.assertEqual(self.type2test('  a  bb  c  ').rsplit(None, 0), ['  a  bb  c'])
        self.assertEqual(self.type2test('  a  bb  c  ').rsplit(None, 1), ['  a  bb', 'c'])
        self.assertEqual(self.type2test('  a  bb  c  ').rsplit(None, 2), ['  a', 'bb', 'c'])
        self.assertEqual(self.type2test('  a  bb  c  ').rsplit(None, 3), ['a', 'bb', 'c'])
        return

    def test_rsplit_string_error(self):
        self.assertRaises(TypeError, self.type2test('a b').rsplit, u' ')

    def test_rsplit_unicodewhitespace(self):
        b = self.type2test('\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f')
        self.assertEqual(b.rsplit(), ['\x1c\x1d\x1e\x1f'])

    def test_partition(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.partition('ss'), ('mi', 'ss', 'issippi'))
        self.assertEqual(b.partition('w'), ('mississippi', '', ''))

    def test_rpartition(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.rpartition('ss'), ('missi', 'ss', 'ippi'))
        self.assertEqual(b.rpartition('i'), ('mississipp', 'i', ''))
        self.assertEqual(b.rpartition('w'), ('', '', 'mississippi'))

    def test_pickling(self):
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            for b in ('', 'a', 'abc', '\xffab\x80', '\x00\x00\xff\x00\x00'):
                b = self.type2test(b)
                ps = pickle.dumps(b, proto)
                q = pickle.loads(ps)
                self.assertEqual(b, q)

    def test_strip(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.strip('i'), 'mississipp')
        self.assertEqual(b.strip('m'), 'ississippi')
        self.assertEqual(b.strip('pi'), 'mississ')
        self.assertEqual(b.strip('im'), 'ssissipp')
        self.assertEqual(b.strip('pim'), 'ssiss')
        self.assertEqual(b.strip(b), '')

    def test_lstrip(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.lstrip('i'), 'mississippi')
        self.assertEqual(b.lstrip('m'), 'ississippi')
        self.assertEqual(b.lstrip('pi'), 'mississippi')
        self.assertEqual(b.lstrip('im'), 'ssissippi')
        self.assertEqual(b.lstrip('pim'), 'ssissippi')

    def test_rstrip(self):
        b = self.type2test('mississippi')
        self.assertEqual(b.rstrip('i'), 'mississipp')
        self.assertEqual(b.rstrip('m'), 'mississippi')
        self.assertEqual(b.rstrip('pi'), 'mississ')
        self.assertEqual(b.rstrip('im'), 'mississipp')
        self.assertEqual(b.rstrip('pim'), 'mississ')

    def test_strip_whitespace(self):
        b = self.type2test(' \t\n\r\x0c\x0babc \t\n\r\x0c\x0b')
        self.assertEqual(b.strip(), 'abc')
        self.assertEqual(b.lstrip(), 'abc \t\n\r\x0c\x0b')
        self.assertEqual(b.rstrip(), ' \t\n\r\x0c\x0babc')

    def test_strip_bytearray(self):
        self.assertEqual(self.type2test('abc').strip(memoryview('ac')), 'b')
        self.assertEqual(self.type2test('abc').lstrip(memoryview('ac')), 'bc')
        self.assertEqual(self.type2test('abc').rstrip(memoryview('ac')), 'ab')

    def test_strip_string_error(self):
        self.assertRaises(TypeError, self.type2test('abc').strip, u'b')
        self.assertRaises(TypeError, self.type2test('abc').lstrip, u'b')
        self.assertRaises(TypeError, self.type2test('abc').rstrip, u'b')

    def test_ord(self):
        b = self.type2test('\x00A\x7f\x80\xff')
        self.assertEqual([ ord(b[i:i + 1]) for i in range(len(b)) ], [0,
         65,
         127,
         128,
         255])

    def test_none_arguments(self):
        b = self.type2test('hello')
        l = self.type2test('l')
        h = self.type2test('h')
        x = self.type2test('x')
        o = self.type2test('o')
        self.assertEqual(2, b.find(l, None))
        self.assertEqual(3, b.find(l, -2, None))
        self.assertEqual(2, b.find(l, None, -2))
        self.assertEqual(0, b.find(h, None, None))
        self.assertEqual(3, b.rfind(l, None))
        self.assertEqual(3, b.rfind(l, -2, None))
        self.assertEqual(2, b.rfind(l, None, -2))
        self.assertEqual(0, b.rfind(h, None, None))
        self.assertEqual(2, b.index(l, None))
        self.assertEqual(3, b.index(l, -2, None))
        self.assertEqual(2, b.index(l, None, -2))
        self.assertEqual(0, b.index(h, None, None))
        self.assertEqual(3, b.rindex(l, None))
        self.assertEqual(3, b.rindex(l, -2, None))
        self.assertEqual(2, b.rindex(l, None, -2))
        self.assertEqual(0, b.rindex(h, None, None))
        self.assertEqual(2, b.count(l, None))
        self.assertEqual(1, b.count(l, -2, None))
        self.assertEqual(1, b.count(l, None, -2))
        self.assertEqual(0, b.count(x, None, None))
        self.assertEqual(True, b.endswith(o, None))
        self.assertEqual(True, b.endswith(o, -2, None))
        self.assertEqual(True, b.endswith(l, None, -2))
        self.assertEqual(False, b.endswith(x, None, None))
        self.assertEqual(True, b.startswith(h, None))
        self.assertEqual(True, b.startswith(l, -2, None))
        self.assertEqual(True, b.startswith(h, None, -2))
        self.assertEqual(False, b.startswith(x, None, None))
        return

    def test_find_etc_raise_correct_error_messages(self):
        b = self.type2test('hello')
        x = self.type2test('x')
        self.assertRaisesRegexp(TypeError, '\\bfind\\b', b.find, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\brfind\\b', b.rfind, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\bindex\\b', b.index, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\brindex\\b', b.rindex, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\bcount\\b', b.count, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\bstartswith\\b', b.startswith, x, None, None, None)
        self.assertRaisesRegexp(TypeError, '\\bendswith\\b', b.endswith, x, None, None, None)
        return


class ByteArrayTest(BaseBytesTest):
    type2test = bytearray

    def test_nohash(self):
        self.assertRaises(TypeError, hash, bytearray())

    def test_bytearray_api(self):
        short_sample = 'Hello world\n'
        sample = short_sample + '\x00' * (20 - len(short_sample))
        tfn = tempfile.mktemp()
        try:
            with open(tfn, 'wb') as f:
                f.write(short_sample)
            with open(tfn, 'rb') as f:
                b = bytearray(20)
                n = f.readinto(b)
            self.assertEqual(n, len(short_sample))
            b_sample = (ord(s) for s in sample)
            self.assertEqual(list(b), list(b_sample))
            with open(tfn, 'wb') as f:
                f.write(b)
            with open(tfn, 'rb') as f:
                self.assertEqual(f.read(), sample)
        finally:
            try:
                os.remove(tfn)
            except os.error:
                pass

    def test_reverse(self):
        b = bytearray('hello')
        self.assertEqual(b.reverse(), None)
        self.assertEqual(b, 'olleh')
        b = bytearray('hello1')
        b.reverse()
        self.assertEqual(b, '1olleh')
        b = bytearray()
        b.reverse()
        self.assertFalse(b)
        return

    def test_regexps(self):

        def by(s):
            return bytearray(map(ord, s))

        b = by('Hello, world')
        self.assertEqual(re.findall('\\w+', b), [by('Hello'), by('world')])

    def test_setitem(self):
        b = bytearray([1, 2, 3])
        b[1] = 100
        self.assertEqual(b, bytearray([1, 100, 3]))
        b[-1] = 200
        self.assertEqual(b, bytearray([1, 100, 200]))
        b[0] = Indexable(10)
        self.assertEqual(b, bytearray([10, 100, 200]))
        try:
            b[3] = 0
            self.fail("Didn't raise IndexError")
        except IndexError:
            pass

        try:
            b[-10] = 0
            self.fail("Didn't raise IndexError")
        except IndexError:
            pass

        try:
            b[0] = 256
            self.fail("Didn't raise ValueError")
        except ValueError:
            pass

        try:
            b[0] = Indexable(-1)
            self.fail("Didn't raise ValueError")
        except ValueError:
            pass

        try:
            b[0] = None
            self.fail("Didn't raise TypeError")
        except TypeError:
            pass

        return

    def test_delitem(self):
        b = bytearray(range(10))
        del b[0]
        self.assertEqual(b, bytearray(range(1, 10)))
        del b[-1]
        self.assertEqual(b, bytearray(range(1, 9)))
        del b[4]
        self.assertEqual(b, bytearray([1,
         2,
         3,
         4,
         6,
         7,
         8]))

    def test_setslice(self):
        b = bytearray(range(10))
        self.assertEqual(list(b), list(range(10)))
        b[0:5] = bytearray([1,
         1,
         1,
         1,
         1])
        self.assertEqual(b, bytearray([1,
         1,
         1,
         1,
         1,
         5,
         6,
         7,
         8,
         9]))
        del b[0:-5]
        self.assertEqual(b, bytearray([5,
         6,
         7,
         8,
         9]))
        b[0:0] = bytearray([0,
         1,
         2,
         3,
         4])
        self.assertEqual(b, bytearray(range(10)))
        b[-7:-3] = bytearray([100, 101])
        self.assertEqual(b, bytearray([0,
         1,
         2,
         100,
         101,
         7,
         8,
         9]))
        b[3:5] = [3,
         4,
         5,
         6]
        self.assertEqual(b, bytearray(range(10)))
        b[3:0] = [42, 42, 42]
        self.assertEqual(b, bytearray([0,
         1,
         2,
         42,
         42,
         42,
         3,
         4,
         5,
         6,
         7,
         8,
         9]))

    def test_extended_set_del_slice(self):
        indices = (0,
         None,
         1,
         3,
         19,
         300,
         17498005798264095394980017816940970922825355447145699491406164851279623993595007385788105416184430592L,
         -1,
         -2,
         -31,
         -300)
        for start in indices:
            for stop in indices:
                for step in indices[1:]:
                    L = list(range(255))
                    b = bytearray(L)
                    data = L[start:stop:step]
                    data.reverse()
                    L[start:stop:step] = data
                    b[start:stop:step] = data
                    self.assertEqual(b, bytearray(L))
                    del L[start:stop:step]
                    del b[start:stop:step]
                    self.assertEqual(b, bytearray(L))

        return

    def test_setslice_trap(self):
        b = bytearray(range(256))
        b[8:] = b
        self.assertEqual(b, bytearray(list(range(8)) + list(range(256))))

    def test_iconcat(self):
        b = bytearray('abc')
        b1 = b
        b += 'def'
        self.assertEqual(b, 'abcdef')
        self.assertEqual(b, b1)
        self.assertTrue(b is b1)
        b += 'xyz'
        self.assertEqual(b, 'abcdefxyz')
        try:
            b += u''
        except TypeError:
            pass
        else:
            self.fail("bytes += unicode didn't raise TypeError")

    def test_irepeat(self):
        b = bytearray('abc')
        b1 = b
        b *= 3
        self.assertEqual(b, 'abcabcabc')
        self.assertEqual(b, b1)
        self.assertTrue(b is b1)

    def test_irepeat_1char(self):
        b = bytearray('x')
        b1 = b
        b *= 100
        self.assertEqual(b, 'x' * 100)
        self.assertEqual(b, b1)
        self.assertTrue(b is b1)

    def test_alloc(self):
        b = bytearray()
        alloc = b.__alloc__()
        self.assertTrue(alloc >= 0)
        seq = [alloc]
        for i in range(100):
            b += 'x'
            alloc = b.__alloc__()
            self.assertTrue(alloc >= len(b))
            if alloc not in seq:
                seq.append(alloc)

    def test_extend(self):
        orig = 'hello'
        a = bytearray(orig)
        a.extend(a)
        self.assertEqual(a, orig + orig)
        self.assertEqual(a[5:], orig)
        a = bytearray('')
        a.extend(map(ord, orig * 25))
        a.extend((ord(x) for x in orig * 25))
        self.assertEqual(a, orig * 50)
        self.assertEqual(a[-5:], orig)
        a = bytearray('')
        a.extend(iter(map(ord, orig * 50)))
        self.assertEqual(a, orig * 50)
        self.assertEqual(a[-5:], orig)
        a = bytearray('')
        a.extend(list(map(ord, orig * 50)))
        self.assertEqual(a, orig * 50)
        self.assertEqual(a[-5:], orig)
        a = bytearray('')
        self.assertRaises(ValueError, a.extend, [0,
         1,
         2,
         256])
        self.assertRaises(ValueError, a.extend, [0,
         1,
         2,
         -1])
        self.assertEqual(len(a), 0)
        a = bytearray('')
        a.extend([Indexable(ord('a'))])
        self.assertEqual(a, 'a')

    def test_remove(self):
        b = bytearray('hello')
        b.remove(ord('l'))
        self.assertEqual(b, 'helo')
        b.remove(ord('l'))
        self.assertEqual(b, 'heo')
        self.assertRaises(ValueError, lambda : b.remove(ord('l')))
        self.assertRaises(ValueError, lambda : b.remove(400))
        self.assertRaises(TypeError, lambda : b.remove(u'e'))
        b.remove(ord('o'))
        b.remove(ord('h'))
        self.assertEqual(b, 'e')
        self.assertRaises(TypeError, lambda : b.remove(u'e'))
        b.remove(Indexable(ord('e')))
        self.assertEqual(b, '')

    def test_pop(self):
        b = bytearray('world')
        self.assertEqual(b.pop(), ord('d'))
        self.assertEqual(b.pop(0), ord('w'))
        self.assertEqual(b.pop(-2), ord('r'))
        self.assertRaises(IndexError, lambda : b.pop(10))
        self.assertRaises(IndexError, lambda : bytearray().pop())
        self.assertEqual(bytearray('\xff').pop(), 255)

    def test_nosort(self):
        self.assertRaises(AttributeError, lambda : bytearray().sort())

    def test_append(self):
        b = bytearray('hell')
        b.append(ord('o'))
        self.assertEqual(b, 'hello')
        self.assertEqual(b.append(100), None)
        b = bytearray()
        b.append(ord('A'))
        self.assertEqual(len(b), 1)
        self.assertRaises(TypeError, lambda : b.append(u'o'))
        b = bytearray()
        b.append(Indexable(ord('A')))
        self.assertEqual(b, 'A')
        return

    def test_insert(self):
        b = bytearray('msssspp')
        b.insert(1, ord('i'))
        b.insert(4, ord('i'))
        b.insert(-2, ord('i'))
        b.insert(1000, ord('i'))
        self.assertEqual(b, 'mississippi')
        b = bytearray()
        b.insert(0, Indexable(ord('A')))
        self.assertEqual(b, 'A')

    def test_copied(self):
        b = bytearray('abc')
        self.assertFalse(b is b.replace('abc', 'cde', 0))
        t = bytearray([ i for i in range(256) ])
        x = bytearray('')
        self.assertFalse(x is x.translate(t))

    def test_partition_bytearray_doesnt_share_nullstring(self):
        a, b, c = bytearray('x').partition('y')
        self.assertEqual(b, '')
        self.assertEqual(c, '')
        self.assertTrue(b is not c)
        b += '!'
        self.assertEqual(c, '')
        a, b, c = bytearray('x').partition('y')
        self.assertEqual(b, '')
        self.assertEqual(c, '')
        b, c, a = bytearray('x').rpartition('y')
        self.assertEqual(b, '')
        self.assertEqual(c, '')
        self.assertTrue(b is not c)
        b += '!'
        self.assertEqual(c, '')
        c, b, a = bytearray('x').rpartition('y')
        self.assertEqual(b, '')
        self.assertEqual(c, '')

    def test_resize_forbidden(self):
        b = bytearray(range(10))
        v = memoryview(b)

        def resize(n):
            b[1:-1] = range(n + 1, 2 * n - 1)

        resize(10)
        orig = b[:]
        self.assertRaises(BufferError, resize, 11)
        self.assertEqual(b, orig)
        self.assertRaises(BufferError, resize, 9)
        self.assertEqual(b, orig)
        self.assertRaises(BufferError, resize, 0)
        self.assertEqual(b, orig)
        self.assertRaises(BufferError, b.pop, 0)
        self.assertEqual(b, orig)
        self.assertRaises(BufferError, b.remove, b[1])
        self.assertEqual(b, orig)

        def delitem():
            del b[1]

        self.assertRaises(BufferError, delitem)
        self.assertEqual(b, orig)

        def delslice():
            b[1:-1:2] = ''

        self.assertRaises(BufferError, delslice)
        self.assertEqual(b, orig)

    def test_empty_bytearray(self):
        self.assertRaises(ValueError, int, bytearray(''))


class AssortedBytesTest(unittest.TestCase):

    @check_bytes_warnings
    def test_repr_str(self):
        for f in (str, repr):
            self.assertEqual(f(bytearray()), "bytearray(b'')")
            self.assertEqual(f(bytearray([0])), "bytearray(b'\\x00')")
            self.assertEqual(f(bytearray([0,
             1,
             254,
             255])), "bytearray(b'\\x00\\x01\\xfe\\xff')")
            self.assertEqual(f('abc'), "b'abc'")
            self.assertEqual(f("'"), 'b"\'"')
            self.assertEqual(f('\'"'), 'b\'\\\'"\'')

    def test_compare_bytes_to_bytearray(self):
        self.assertEqual('abc' == bytes('abc'), True)
        self.assertEqual('ab' != bytes('abc'), True)
        self.assertEqual('ab' <= bytes('abc'), True)
        self.assertEqual('ab' < bytes('abc'), True)
        self.assertEqual('abc' >= bytes('ab'), True)
        self.assertEqual('abc' > bytes('ab'), True)
        self.assertEqual('abc' != bytes('abc'), False)
        self.assertEqual('ab' == bytes('abc'), False)
        self.assertEqual('ab' > bytes('abc'), False)
        self.assertEqual('ab' >= bytes('abc'), False)
        self.assertEqual('abc' < bytes('ab'), False)
        self.assertEqual('abc' <= bytes('ab'), False)
        self.assertEqual(bytes('abc') == 'abc', True)
        self.assertEqual(bytes('ab') != 'abc', True)
        self.assertEqual(bytes('ab') <= 'abc', True)
        self.assertEqual(bytes('ab') < 'abc', True)
        self.assertEqual(bytes('abc') >= 'ab', True)
        self.assertEqual(bytes('abc') > 'ab', True)
        self.assertEqual(bytes('abc') != 'abc', False)
        self.assertEqual(bytes('ab') == 'abc', False)
        self.assertEqual(bytes('ab') > 'abc', False)
        self.assertEqual(bytes('ab') >= 'abc', False)
        self.assertEqual(bytes('abc') < 'ab', False)
        self.assertEqual(bytes('abc') <= 'ab', False)

    def test_doc(self):
        self.assertIsNotNone(bytearray.__doc__)
        self.assertTrue(bytearray.__doc__.startswith('bytearray('), bytearray.__doc__)
        self.assertIsNotNone(bytes.__doc__)
        self.assertTrue(bytes.__doc__.startswith('bytes('), bytes.__doc__)

    def test_from_bytearray(self):
        sample = bytes('Hello world\n\x80\x81\xfe\xff')
        buf = memoryview(sample)
        b = bytearray(buf)
        self.assertEqual(b, bytearray(sample))

    @check_bytes_warnings
    def test_to_str(self):
        self.assertEqual(str(''), "b''")
        self.assertEqual(str('x'), "b'x'")
        self.assertEqual(str('\x80'), "b'\\x80'")
        self.assertEqual(str(bytearray('')), "bytearray(b'')")
        self.assertEqual(str(bytearray('x')), "bytearray(b'x')")
        self.assertEqual(str(bytearray('\x80')), "bytearray(b'\\x80')")

    def test_literal(self):
        tests = [('Wonderful spam', 'Wonderful spam'),
         ('Wonderful spam too', 'Wonderful spam too'),
         ('\xaa\x00\x00\x80', '\xaa\x00\x00\x80'),
         ('\\xaa\\x00\\000\\200', '\\xaa\\x00\\000\\200')]
        for b, s in tests:
            self.assertEqual(b, bytearray(s, 'latin-1'))

        for c in range(128, 256):
            self.assertRaises(SyntaxError, eval, 'b"%s"' % chr(c))

    def test_translate(self):
        b = 'hello'
        ba = bytearray(b)
        rosetta = bytearray(range(0, 256))
        rosetta[ord('o')] = ord('e')
        c = b.translate(rosetta, 'l')
        self.assertEqual(b, 'hello')
        self.assertEqual(c, 'hee')
        c = ba.translate(rosetta, 'l')
        self.assertEqual(ba, 'hello')
        self.assertEqual(c, 'hee')
        c = b.translate(None, 'e')
        self.assertEqual(c, 'hllo')
        c = ba.translate(None, 'e')
        self.assertEqual(c, 'hllo')
        self.assertRaises(TypeError, b.translate, None, None)
        self.assertRaises(TypeError, ba.translate, None, None)
        return

    def test_split_bytearray(self):
        self.assertEqual('a b'.split(memoryview(' ')), ['a', 'b'])

    def test_rsplit_bytearray(self):
        self.assertEqual('a b'.rsplit(memoryview(' ')), ['a', 'b'])


class BytearrayPEP3137Test(unittest.TestCase, test.buffer_tests.MixinBytesBufferCommonTests):

    def marshal(self, x):
        return bytearray(x)

    def test_returns_new_copy(self):
        val = self.marshal('1234')
        for methname in ('zfill', 'rjust', 'ljust', 'center'):
            method = getattr(val, methname)
            newval = method(3)
            self.assertEqual(val, newval)
            self.assertTrue(val is not newval, methname + ' returned self on a mutable object')

        for expr in ('val.split()[0]', 'val.rsplit()[0]', 'val.partition(".")[0]', 'val.rpartition(".")[2]', 'val.splitlines()[0]', 'val.replace("", "")'):
            newval = eval(expr)
            self.assertEqual(val, newval)
            self.assertTrue(val is not newval, expr + ' returned val on a mutable object')


class FixedStringTest(test.string_tests.BaseTest):

    def fixtype(self, obj):
        if isinstance(obj, str):
            return obj.encode('utf-8')
        return super(FixedStringTest, self).fixtype(obj)

    def test_contains(self):
        pass

    def test_expandtabs(self):
        pass

    def test_upper(self):
        pass

    def test_lower(self):
        pass

    def test_hash(self):
        pass


class ByteArrayAsStringTest(FixedStringTest):
    type2test = bytearray


class ByteArraySubclass(bytearray):
    pass


class ByteArraySubclassTest(unittest.TestCase):

    def test_basic(self):
        self.assertTrue(issubclass(ByteArraySubclass, bytearray))
        self.assertIsInstance(ByteArraySubclass(), bytearray)
        a, b = ('abcd', 'efgh')
        _a, _b = ByteArraySubclass(a), ByteArraySubclass(b)
        self.assertTrue(_a == _a)
        self.assertTrue(_a != _b)
        self.assertTrue(_a < _b)
        self.assertTrue(_a <= _b)
        self.assertTrue(_b >= _a)
        self.assertTrue(_b > _a)
        self.assertTrue(_a is not a)
        self.assertEqual(a + b, _a + _b)
        self.assertEqual(a + b, a + _b)
        self.assertEqual(a + b, _a + b)
        self.assertTrue(a * 5 == _a * 5)

    def test_join(self):
        s1 = ByteArraySubclass('abcd')
        s2 = bytearray().join([s1])
        self.assertTrue(s1 is not s2)
        self.assertTrue(type(s2) is bytearray, type(s2))
        s3 = s1.join(['abcd'])
        self.assertTrue(type(s3) is bytearray)

    def test_pickle(self):
        a = ByteArraySubclass('abcd')
        a.x = 10
        a.y = ByteArraySubclass('efgh')
        for proto in range(pickle.HIGHEST_PROTOCOL + 1):
            b = pickle.loads(pickle.dumps(a, proto))
            self.assertNotEqual(id(a), id(b))
            self.assertEqual(a, b)
            self.assertEqual(a.x, b.x)
            self.assertEqual(a.y, b.y)
            self.assertEqual(type(a), type(b))
            self.assertEqual(type(a.y), type(b.y))

    def test_copy(self):
        a = ByteArraySubclass('abcd')
        a.x = 10
        a.y = ByteArraySubclass('efgh')
        for copy_method in (copy.copy, copy.deepcopy):
            b = copy_method(a)
            self.assertNotEqual(id(a), id(b))
            self.assertEqual(a, b)
            self.assertEqual(a.x, b.x)
            self.assertEqual(a.y, b.y)
            self.assertEqual(type(a), type(b))
            self.assertEqual(type(a.y), type(b.y))

    def test_init_override(self):

        class subclass(bytearray):

            def __init__(self, newarg = 1, *args, **kwargs):
                bytearray.__init__(self, *args, **kwargs)

        x = subclass(4, source='abcd')
        self.assertEqual(x, 'abcd')
        x = subclass(newarg=4, source='abcd')
        self.assertEqual(x, 'abcd')


def test_main():
    test.test_support.run_unittest(ByteArrayTest, ByteArrayAsStringTest, ByteArraySubclassTest, BytearrayPEP3137Test)


if __name__ == '__main__':
    test_main()