# Embedded file name: scripts/common/Lib/test/test_unicodedata.py
""" Test script for the unicodedata module.

    Written by Marc-Andre Lemburg (mal@lemburg.com).

    (c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""
import sys
import unittest
import hashlib
import subprocess
import test.test_support
encoding = 'utf-8'

class UnicodeMethodsTest(unittest.TestCase):
    expectedchecksum = '4504dffd035baea02c5b9de82bebc3d65e0e0baf'

    def test_method_checksum(self):
        h = hashlib.sha1()
        for i in range(65536):
            char = unichr(i)
            data = [u'01'[char.isalnum()],
             u'01'[char.isalpha()],
             u'01'[char.isdecimal()],
             u'01'[char.isdigit()],
             u'01'[char.islower()],
             u'01'[char.isnumeric()],
             u'01'[char.isspace()],
             u'01'[char.istitle()],
             u'01'[char.isupper()],
             u'01'[(char + u'abc').isalnum()],
             u'01'[(char + u'abc').isalpha()],
             u'01'[(char + u'123').isdecimal()],
             u'01'[(char + u'123').isdigit()],
             u'01'[(char + u'abc').islower()],
             u'01'[(char + u'123').isnumeric()],
             u'01'[(char + u' \t').isspace()],
             u'01'[(char + u'abc').istitle()],
             u'01'[(char + u'ABC').isupper()],
             char.lower(),
             char.upper(),
             char.title(),
             (char + u'abc').lower(),
             (char + u'ABC').upper(),
             (char + u'abc').title(),
             (char + u'ABC').title()]
            h.update(u''.join(data).encode(encoding))

        result = h.hexdigest()
        self.assertEqual(result, self.expectedchecksum)


class UnicodeDatabaseTest(unittest.TestCase):

    def setUp(self):
        import unicodedata
        self.db = unicodedata

    def tearDown(self):
        del self.db


class UnicodeFunctionsTest(UnicodeDatabaseTest):
    expectedchecksum = '6ccf1b1a36460d2694f9b0b0f0324942fe70ede6'

    def test_function_checksum(self):
        data = []
        h = hashlib.sha1()
        for i in range(65536):
            char = unichr(i)
            data = [str(self.db.digit(char, -1)),
             str(self.db.numeric(char, -1)),
             str(self.db.decimal(char, -1)),
             self.db.category(char),
             self.db.bidirectional(char),
             self.db.decomposition(char),
             str(self.db.mirrored(char)),
             str(self.db.combining(char))]
            h.update(''.join(data))

        result = h.hexdigest()
        self.assertEqual(result, self.expectedchecksum)

    def test_digit(self):
        self.assertEqual(self.db.digit(u'A', None), None)
        self.assertEqual(self.db.digit(u'9'), 9)
        self.assertEqual(self.db.digit(u'\u215b', None), None)
        self.assertEqual(self.db.digit(u'\u2468'), 9)
        self.assertEqual(self.db.digit(u'\U00020000', None), None)
        self.assertRaises(TypeError, self.db.digit)
        self.assertRaises(TypeError, self.db.digit, u'xx')
        self.assertRaises(ValueError, self.db.digit, u'x')
        return

    def test_numeric(self):
        self.assertEqual(self.db.numeric(u'A', None), None)
        self.assertEqual(self.db.numeric(u'9'), 9)
        self.assertEqual(self.db.numeric(u'\u215b'), 0.125)
        self.assertEqual(self.db.numeric(u'\u2468'), 9.0)
        self.assertEqual(self.db.numeric(u'\ua627'), 7.0)
        self.assertEqual(self.db.numeric(u'\U00020000', None), None)
        self.assertRaises(TypeError, self.db.numeric)
        self.assertRaises(TypeError, self.db.numeric, u'xx')
        self.assertRaises(ValueError, self.db.numeric, u'x')
        return

    def test_decimal(self):
        self.assertEqual(self.db.decimal(u'A', None), None)
        self.assertEqual(self.db.decimal(u'9'), 9)
        self.assertEqual(self.db.decimal(u'\u215b', None), None)
        self.assertEqual(self.db.decimal(u'\u2468', None), None)
        self.assertEqual(self.db.decimal(u'\U00020000', None), None)
        self.assertRaises(TypeError, self.db.decimal)
        self.assertRaises(TypeError, self.db.decimal, u'xx')
        self.assertRaises(ValueError, self.db.decimal, u'x')
        return

    def test_category(self):
        self.assertEqual(self.db.category(u'\ufffe'), 'Cn')
        self.assertEqual(self.db.category(u'a'), 'Ll')
        self.assertEqual(self.db.category(u'A'), 'Lu')
        self.assertEqual(self.db.category(u'\U00020000'), 'Lo')
        self.assertRaises(TypeError, self.db.category)
        self.assertRaises(TypeError, self.db.category, u'xx')

    def test_bidirectional(self):
        self.assertEqual(self.db.bidirectional(u'\ufffe'), '')
        self.assertEqual(self.db.bidirectional(u' '), 'WS')
        self.assertEqual(self.db.bidirectional(u'A'), 'L')
        self.assertEqual(self.db.bidirectional(u'\U00020000'), 'L')
        self.assertRaises(TypeError, self.db.bidirectional)
        self.assertRaises(TypeError, self.db.bidirectional, u'xx')

    def test_decomposition(self):
        self.assertEqual(self.db.decomposition(u'\ufffe'), '')
        self.assertEqual(self.db.decomposition(u'\xbc'), '<fraction> 0031 2044 0034')
        self.assertRaises(TypeError, self.db.decomposition)
        self.assertRaises(TypeError, self.db.decomposition, u'xx')

    def test_mirrored(self):
        self.assertEqual(self.db.mirrored(u'\ufffe'), 0)
        self.assertEqual(self.db.mirrored(u'a'), 0)
        self.assertEqual(self.db.mirrored(u'\u2201'), 1)
        self.assertEqual(self.db.mirrored(u'\U00020000'), 0)
        self.assertRaises(TypeError, self.db.mirrored)
        self.assertRaises(TypeError, self.db.mirrored, u'xx')

    def test_combining(self):
        self.assertEqual(self.db.combining(u'\ufffe'), 0)
        self.assertEqual(self.db.combining(u'a'), 0)
        self.assertEqual(self.db.combining(u'\u20e1'), 230)
        self.assertEqual(self.db.combining(u'\U00020000'), 0)
        self.assertRaises(TypeError, self.db.combining)
        self.assertRaises(TypeError, self.db.combining, u'xx')

    def test_normalize(self):
        self.assertRaises(TypeError, self.db.normalize)
        self.assertRaises(ValueError, self.db.normalize, 'unknown', u'xx')
        self.assertEqual(self.db.normalize('NFKC', u''), u'')

    def test_pr29(self):
        composed = (u'\u0b47\u0300\u0b3e',
         u'\u1100\u0300\u1161',
         u'Li\u030dt-s\u1e73\u0301',
         u'\u092e\u093e\u0930\u094d\u0915 \u091c\u093c\u0941\u0915\u0947\u0930\u092c\u0930\u094d\u0917',
         u'\u0915\u093f\u0930\u094d\u0917\u093f\u091c\u093c' + 'u\\u0938\\u094d\\u0924\\u093e\\u0928')
        for text in composed:
            self.assertEqual(self.db.normalize('NFC', text), text)

    def test_issue10254(self):
        a = u'C\u0338' * 20 + u'C\u0327'
        b = u'C\u0338' * 20 + u'\xc7'
        self.assertEqual(self.db.normalize('NFC', a), b)

    def test_east_asian_width(self):
        eaw = self.db.east_asian_width
        self.assertRaises(TypeError, eaw, 'a')
        self.assertRaises(TypeError, eaw, u'')
        self.assertRaises(TypeError, eaw, u'ra')
        self.assertEqual(eaw(u'\x1e'), 'N')
        self.assertEqual(eaw(u' '), 'Na')
        self.assertEqual(eaw(u'\uc894'), 'W')
        self.assertEqual(eaw(u'\uff66'), 'H')
        self.assertEqual(eaw(u'\uff1f'), 'F')
        self.assertEqual(eaw(u'\u2010'), 'A')
        self.assertEqual(eaw(u'\U00020000'), 'W')


class UnicodeMiscTest(UnicodeDatabaseTest):

    def test_failed_import_during_compiling(self):
        code = 'import sys;sys.modules[\'unicodedata\'] = None;eval("u\'\\N{SOFT HYPHEN}\'")'
        args = [sys.executable, '-c', code]
        popen = subprocess.Popen(args, stderr=subprocess.PIPE)
        popen.wait()
        self.assertEqual(popen.returncode, 1)
        error = "SyntaxError: (unicode error) \\N escapes not supported (can't load unicodedata module)"
        self.assertIn(error, popen.stderr.read())

    def test_decimal_numeric_consistent(self):
        count = 0
        for i in xrange(65536):
            c = unichr(i)
            dec = self.db.decimal(c, -1)
            if dec != -1:
                self.assertEqual(dec, self.db.numeric(c))
                count += 1

        self.assertTrue(count >= 10)

    def test_digit_numeric_consistent(self):
        count = 0
        for i in xrange(65536):
            c = unichr(i)
            dec = self.db.digit(c, -1)
            if dec != -1:
                self.assertEqual(dec, self.db.numeric(c))
                count += 1

        self.assertTrue(count >= 10)

    def test_bug_1704793(self):
        self.assertEqual(self.db.lookup('GOTHIC LETTER FAIHU'), u'\U00010346')

    def test_ucd_510(self):
        import unicodedata
        self.assertTrue(unicodedata.mirrored(u'\u0f3a'))
        self.assertTrue(not unicodedata.ucd_3_2_0.mirrored(u'\u0f3a'))
        self.assertTrue(u'a'.upper() == u'A')
        self.assertTrue(u'\u1d79'.upper() == u'\ua77d')
        self.assertTrue(u'.'.upper() == u'.')

    def test_bug_5828(self):
        self.assertEqual(u'\u1d79'.lower(), u'\u1d79')
        self.assertEqual([ c for c in range(sys.maxunicode + 1) if u'\x00' in unichr(c).lower() + unichr(c).upper() + unichr(c).title() ], [0])

    def test_bug_4971(self):
        self.assertEqual(u'\u01c4'.title(), u'\u01c5')
        self.assertEqual(u'\u01c5'.title(), u'\u01c5')
        self.assertEqual(u'\u01c6'.title(), u'\u01c5')

    def test_linebreak_7643(self):
        for i in range(65536):
            lines = (unichr(i) + u'A').splitlines()
            if i in (10, 11, 12, 13, 133, 28, 29, 30, 8232, 8233):
                self.assertEqual(len(lines), 2, '\\u%.4x should be a linebreak' % i)
            else:
                self.assertEqual(len(lines), 1, '\\u%.4x should not be a linebreak' % i)


def test_main():
    test.test_support.run_unittest(UnicodeMiscTest, UnicodeMethodsTest, UnicodeFunctionsTest)


if __name__ == '__main__':
    test_main()