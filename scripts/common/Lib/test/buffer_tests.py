# Embedded file name: scripts/common/Lib/test/buffer_tests.py
import struct
import sys

class MixinBytesBufferCommonTests(object):
    """Tests that work for both bytes and buffer objects.
    See PEP 3137.
    """

    def marshal(self, x):
        """Convert x into the appropriate type for these tests."""
        raise RuntimeError('test class must provide a marshal method')

    def test_islower(self):
        self.assertFalse(self.marshal('').islower())
        self.assertTrue(self.marshal('a').islower())
        self.assertFalse(self.marshal('A').islower())
        self.assertFalse(self.marshal('\n').islower())
        self.assertTrue(self.marshal('abc').islower())
        self.assertFalse(self.marshal('aBc').islower())
        self.assertTrue(self.marshal('abc\n').islower())
        self.assertRaises(TypeError, self.marshal('abc').islower, 42)

    def test_isupper(self):
        self.assertFalse(self.marshal('').isupper())
        self.assertFalse(self.marshal('a').isupper())
        self.assertTrue(self.marshal('A').isupper())
        self.assertFalse(self.marshal('\n').isupper())
        self.assertTrue(self.marshal('ABC').isupper())
        self.assertFalse(self.marshal('AbC').isupper())
        self.assertTrue(self.marshal('ABC\n').isupper())
        self.assertRaises(TypeError, self.marshal('abc').isupper, 42)

    def test_istitle(self):
        self.assertFalse(self.marshal('').istitle())
        self.assertFalse(self.marshal('a').istitle())
        self.assertTrue(self.marshal('A').istitle())
        self.assertFalse(self.marshal('\n').istitle())
        self.assertTrue(self.marshal('A Titlecased Line').istitle())
        self.assertTrue(self.marshal('A\nTitlecased Line').istitle())
        self.assertTrue(self.marshal('A Titlecased, Line').istitle())
        self.assertFalse(self.marshal('Not a capitalized String').istitle())
        self.assertFalse(self.marshal('Not\ta Titlecase String').istitle())
        self.assertFalse(self.marshal('Not--a Titlecase String').istitle())
        self.assertFalse(self.marshal('NOT').istitle())
        self.assertRaises(TypeError, self.marshal('abc').istitle, 42)

    def test_isspace(self):
        self.assertFalse(self.marshal('').isspace())
        self.assertFalse(self.marshal('a').isspace())
        self.assertTrue(self.marshal(' ').isspace())
        self.assertTrue(self.marshal('\t').isspace())
        self.assertTrue(self.marshal('\r').isspace())
        self.assertTrue(self.marshal('\n').isspace())
        self.assertTrue(self.marshal(' \t\r\n').isspace())
        self.assertFalse(self.marshal(' \t\r\na').isspace())
        self.assertRaises(TypeError, self.marshal('abc').isspace, 42)

    def test_isalpha(self):
        self.assertFalse(self.marshal('').isalpha())
        self.assertTrue(self.marshal('a').isalpha())
        self.assertTrue(self.marshal('A').isalpha())
        self.assertFalse(self.marshal('\n').isalpha())
        self.assertTrue(self.marshal('abc').isalpha())
        self.assertFalse(self.marshal('aBc123').isalpha())
        self.assertFalse(self.marshal('abc\n').isalpha())
        self.assertRaises(TypeError, self.marshal('abc').isalpha, 42)

    def test_isalnum(self):
        self.assertFalse(self.marshal('').isalnum())
        self.assertTrue(self.marshal('a').isalnum())
        self.assertTrue(self.marshal('A').isalnum())
        self.assertFalse(self.marshal('\n').isalnum())
        self.assertTrue(self.marshal('123abc456').isalnum())
        self.assertTrue(self.marshal('a1b3c').isalnum())
        self.assertFalse(self.marshal('aBc000 ').isalnum())
        self.assertFalse(self.marshal('abc\n').isalnum())
        self.assertRaises(TypeError, self.marshal('abc').isalnum, 42)

    def test_isdigit(self):
        self.assertFalse(self.marshal('').isdigit())
        self.assertFalse(self.marshal('a').isdigit())
        self.assertTrue(self.marshal('0').isdigit())
        self.assertTrue(self.marshal('0123456789').isdigit())
        self.assertFalse(self.marshal('0123456789a').isdigit())
        self.assertRaises(TypeError, self.marshal('abc').isdigit, 42)

    def test_lower(self):
        self.assertEqual('hello', self.marshal('HeLLo').lower())
        self.assertEqual('hello', self.marshal('hello').lower())
        self.assertRaises(TypeError, self.marshal('hello').lower, 42)

    def test_upper(self):
        self.assertEqual('HELLO', self.marshal('HeLLo').upper())
        self.assertEqual('HELLO', self.marshal('HELLO').upper())
        self.assertRaises(TypeError, self.marshal('hello').upper, 42)

    def test_capitalize(self):
        self.assertEqual(' hello ', self.marshal(' hello ').capitalize())
        self.assertEqual('Hello ', self.marshal('Hello ').capitalize())
        self.assertEqual('Hello ', self.marshal('hello ').capitalize())
        self.assertEqual('Aaaa', self.marshal('aaaa').capitalize())
        self.assertEqual('Aaaa', self.marshal('AaAa').capitalize())
        self.assertRaises(TypeError, self.marshal('hello').capitalize, 42)

    def test_ljust(self):
        self.assertEqual('abc       ', self.marshal('abc').ljust(10))
        self.assertEqual('abc   ', self.marshal('abc').ljust(6))
        self.assertEqual('abc', self.marshal('abc').ljust(3))
        self.assertEqual('abc', self.marshal('abc').ljust(2))
        self.assertEqual('abc*******', self.marshal('abc').ljust(10, '*'))
        self.assertRaises(TypeError, self.marshal('abc').ljust)

    def test_rjust(self):
        self.assertEqual('       abc', self.marshal('abc').rjust(10))
        self.assertEqual('   abc', self.marshal('abc').rjust(6))
        self.assertEqual('abc', self.marshal('abc').rjust(3))
        self.assertEqual('abc', self.marshal('abc').rjust(2))
        self.assertEqual('*******abc', self.marshal('abc').rjust(10, '*'))
        self.assertRaises(TypeError, self.marshal('abc').rjust)

    def test_center(self):
        self.assertEqual('   abc    ', self.marshal('abc').center(10))
        self.assertEqual(' abc  ', self.marshal('abc').center(6))
        self.assertEqual('abc', self.marshal('abc').center(3))
        self.assertEqual('abc', self.marshal('abc').center(2))
        self.assertEqual('***abc****', self.marshal('abc').center(10, '*'))
        self.assertRaises(TypeError, self.marshal('abc').center)

    def test_swapcase(self):
        self.assertEqual('hEllO CoMPuTErS', self.marshal('HeLLo cOmpUteRs').swapcase())
        self.assertRaises(TypeError, self.marshal('hello').swapcase, 42)

    def test_zfill(self):
        self.assertEqual('123', self.marshal('123').zfill(2))
        self.assertEqual('123', self.marshal('123').zfill(3))
        self.assertEqual('0123', self.marshal('123').zfill(4))
        self.assertEqual('+123', self.marshal('+123').zfill(3))
        self.assertEqual('+123', self.marshal('+123').zfill(4))
        self.assertEqual('+0123', self.marshal('+123').zfill(5))
        self.assertEqual('-123', self.marshal('-123').zfill(3))
        self.assertEqual('-123', self.marshal('-123').zfill(4))
        self.assertEqual('-0123', self.marshal('-123').zfill(5))
        self.assertEqual('000', self.marshal('').zfill(3))
        self.assertEqual('34', self.marshal('34').zfill(1))
        self.assertEqual('0034', self.marshal('34').zfill(4))
        self.assertRaises(TypeError, self.marshal('123').zfill)

    def test_expandtabs(self):
        self.assertEqual('abc\rab      def\ng       hi', self.marshal('abc\rab\tdef\ng\thi').expandtabs())
        self.assertEqual('abc\rab      def\ng       hi', self.marshal('abc\rab\tdef\ng\thi').expandtabs(8))
        self.assertEqual('abc\rab  def\ng   hi', self.marshal('abc\rab\tdef\ng\thi').expandtabs(4))
        self.assertEqual('abc\r\nab  def\ng   hi', self.marshal('abc\r\nab\tdef\ng\thi').expandtabs(4))
        self.assertEqual('abc\rab      def\ng       hi', self.marshal('abc\rab\tdef\ng\thi').expandtabs())
        self.assertEqual('abc\rab      def\ng       hi', self.marshal('abc\rab\tdef\ng\thi').expandtabs(8))
        self.assertEqual('abc\r\nab\r\ndef\ng\r\nhi', self.marshal('abc\r\nab\r\ndef\ng\r\nhi').expandtabs(4))
        self.assertEqual('  a\n b', self.marshal(' \ta\n\tb').expandtabs(1))
        self.assertRaises(TypeError, self.marshal('hello').expandtabs, 42, 42)
        if sys.maxint < 4294967296L and struct.calcsize('P') == 4:
            self.assertRaises(OverflowError, self.marshal('\ta\n\tb').expandtabs, sys.maxint)

    def test_title(self):
        self.assertEqual(' Hello ', self.marshal(' hello ').title())
        self.assertEqual('Hello ', self.marshal('hello ').title())
        self.assertEqual('Hello ', self.marshal('Hello ').title())
        self.assertEqual('Format This As Title String', self.marshal('fOrMaT thIs aS titLe String').title())
        self.assertEqual('Format,This-As*Title;String', self.marshal('fOrMaT,thIs-aS*titLe;String').title())
        self.assertEqual('Getint', self.marshal('getInt').title())
        self.assertRaises(TypeError, self.marshal('hello').title, 42)

    def test_splitlines(self):
        self.assertEqual(['abc',
         'def',
         '',
         'ghi'], self.marshal('abc\ndef\n\rghi').splitlines())
        self.assertEqual(['abc',
         'def',
         '',
         'ghi'], self.marshal('abc\ndef\n\r\nghi').splitlines())
        self.assertEqual(['abc', 'def', 'ghi'], self.marshal('abc\ndef\r\nghi').splitlines())
        self.assertEqual(['abc', 'def', 'ghi'], self.marshal('abc\ndef\r\nghi\n').splitlines())
        self.assertEqual(['abc',
         'def',
         'ghi',
         ''], self.marshal('abc\ndef\r\nghi\n\r').splitlines())
        self.assertEqual(['',
         'abc',
         'def',
         'ghi',
         ''], self.marshal('\nabc\ndef\r\nghi\n\r').splitlines())
        self.assertEqual(['\n',
         'abc\n',
         'def\r\n',
         'ghi\n',
         '\r'], self.marshal('\nabc\ndef\r\nghi\n\r').splitlines(1))
        self.assertRaises(TypeError, self.marshal('abc').splitlines, 42, 42)