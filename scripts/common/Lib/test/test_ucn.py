# Embedded file name: scripts/common/Lib/test/test_ucn.py
""" Test script for the Unicode implementation.

Written by Bill Tutt.
Modified for Python 2.0 by Fredrik Lundh (fredrik@pythonware.com)

(c) Copyright CNRI, All Rights Reserved. NO WARRANTY.

"""
import unittest
from test import test_support

class UnicodeNamesTest(unittest.TestCase):

    def checkletter(self, name, code):
        res = eval(u'u"\\N{%s}"' % name)
        self.assertEqual(res, code)
        return res

    def test_general(self):
        chars = ['LATIN CAPITAL LETTER T',
         'LATIN SMALL LETTER H',
         'LATIN SMALL LETTER E',
         'SPACE',
         'LATIN SMALL LETTER R',
         'LATIN CAPITAL LETTER E',
         'LATIN SMALL LETTER D',
         'SPACE',
         'LATIN SMALL LETTER f',
         'LATIN CAPITAL LeTtEr o',
         'LATIN SMaLl LETTER x',
         'SPACE',
         'LATIN SMALL LETTER A',
         'LATIN SMALL LETTER T',
         'LATIN SMALL LETTER E',
         'SPACE',
         'LATIN SMALL LETTER T',
         'LATIN SMALL LETTER H',
         'LATIN SMALL LETTER E',
         'SpAcE',
         'LATIN SMALL LETTER S',
         'LATIN SMALL LETTER H',
         'LATIN small LETTER e',
         'LATIN small LETTER e',
         'LATIN SMALL LETTER P',
         'FULL STOP']
        string = u'The rEd fOx ate the sheep.'
        self.assertEqual(u''.join([ self.checkletter(*args) for args in zip(chars, string) ]), string)

    def test_ascii_letters(self):
        import unicodedata
        for char in ''.join(map(chr, xrange(ord('a'), ord('z')))):
            name = 'LATIN SMALL LETTER %s' % char.upper()
            code = unicodedata.lookup(name)
            self.assertEqual(unicodedata.name(code), name)

    def test_hangul_syllables(self):
        self.checkletter('HANGUL SYLLABLE GA', u'\uac00')
        self.checkletter('HANGUL SYLLABLE GGWEOSS', u'\uafe8')
        self.checkletter('HANGUL SYLLABLE DOLS', u'\ub3d0')
        self.checkletter('HANGUL SYLLABLE RYAN', u'\ub7b8')
        self.checkletter('HANGUL SYLLABLE MWIK', u'\ubba0')
        self.checkletter('HANGUL SYLLABLE BBWAEM', u'\ubf88')
        self.checkletter('HANGUL SYLLABLE SSEOL', u'\uc370')
        self.checkletter('HANGUL SYLLABLE YI', u'\uc758')
        self.checkletter('HANGUL SYLLABLE JJYOSS', u'\ucb40')
        self.checkletter('HANGUL SYLLABLE KYEOLS', u'\ucf28')
        self.checkletter('HANGUL SYLLABLE PAN', u'\ud310')
        self.checkletter('HANGUL SYLLABLE HWEOK', u'\ud6f8')
        self.checkletter('HANGUL SYLLABLE HIH', u'\ud7a3')
        import unicodedata
        self.assertRaises(ValueError, unicodedata.name, u'\ud7a4')

    def test_cjk_unified_ideographs(self):
        self.checkletter('CJK UNIFIED IDEOGRAPH-3400', u'\u3400')
        self.checkletter('CJK UNIFIED IDEOGRAPH-4DB5', u'\u4db5')
        self.checkletter('CJK UNIFIED IDEOGRAPH-4E00', u'\u4e00')
        self.checkletter('CJK UNIFIED IDEOGRAPH-9FA5', u'\u9fa5')
        self.checkletter('CJK UNIFIED IDEOGRAPH-20000', u'\U00020000')
        self.checkletter('CJK UNIFIED IDEOGRAPH-2A6D6', u'\U0002a6d6')

    def test_bmp_characters(self):
        import unicodedata
        count = 0
        for code in xrange(65536):
            char = unichr(code)
            name = unicodedata.name(char, None)
            if name is not None:
                self.assertEqual(unicodedata.lookup(name), char)
                count += 1

        return

    def test_misc_symbols(self):
        self.checkletter('PILCROW SIGN', u'\xb6')
        self.checkletter('REPLACEMENT CHARACTER', u'\ufffd')
        self.checkletter('HALFWIDTH KATAKANA SEMI-VOICED SOUND MARK', u'\uff9f')
        self.checkletter('FULLWIDTH LATIN SMALL LETTER A', u'\uff41')

    def test_errors(self):
        import unicodedata
        self.assertRaises(TypeError, unicodedata.name)
        self.assertRaises(TypeError, unicodedata.name, u'xx')
        self.assertRaises(TypeError, unicodedata.lookup)
        self.assertRaises(KeyError, unicodedata.lookup, u'unknown')

    def test_strict_eror_handling(self):
        self.assertRaises(UnicodeError, unicode, '\\N{blah}', 'unicode-escape', 'strict')
        self.assertRaises(UnicodeError, unicode, '\\N{%s}' % ('x' * 100000), 'unicode-escape', 'strict')
        self.assertRaises(UnicodeError, unicode, '\\N{SPACE', 'unicode-escape', 'strict')
        self.assertRaises(UnicodeError, unicode, '\\NSPACE', 'unicode-escape', 'strict')


def test_main():
    test_support.run_unittest(UnicodeNamesTest)


if __name__ == '__main__':
    test_main()