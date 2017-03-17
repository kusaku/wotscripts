# Embedded file name: scripts/common/Lib/test/test_multibytecodec.py
from test import test_support
from test.test_support import TESTFN
import unittest, StringIO, codecs, sys, os
import _multibytecodec
ALL_CJKENCODINGS = ['gb2312',
 'gbk',
 'gb18030',
 'hz',
 'big5hkscs',
 'cp932',
 'shift_jis',
 'euc_jp',
 'euc_jisx0213',
 'shift_jisx0213',
 'euc_jis_2004',
 'shift_jis_2004',
 'cp949',
 'euc_kr',
 'johab',
 'big5',
 'cp950',
 'iso2022_jp',
 'iso2022_jp_1',
 'iso2022_jp_2',
 'iso2022_jp_2004',
 'iso2022_jp_3',
 'iso2022_jp_ext',
 'iso2022_kr']

class Test_MultibyteCodec(unittest.TestCase):

    def test_nullcoding(self):
        for enc in ALL_CJKENCODINGS:
            self.assertEqual(''.decode(enc), u'')
            self.assertEqual(unicode('', enc), u'')
            self.assertEqual(u''.encode(enc), '')

    def test_str_decode(self):
        for enc in ALL_CJKENCODINGS:
            self.assertEqual('abcd'.encode(enc), 'abcd')

    def test_errorcallback_longindex(self):
        dec = codecs.getdecoder('euc-kr')
        myreplace = lambda exc: (u'', sys.maxint + 1)
        codecs.register_error('test.cjktest', myreplace)
        self.assertRaises(IndexError, dec, 'apple\x92ham\x93spam', 'test.cjktest')

    def test_codingspec(self):
        for enc in ALL_CJKENCODINGS:
            code = '# coding: {}\n'.format(enc)
            exec code

    def test_init_segfault(self):
        self.assertRaises(AttributeError, _multibytecodec.MultibyteStreamReader, None)
        self.assertRaises(AttributeError, _multibytecodec.MultibyteStreamWriter, None)
        return


class Test_IncrementalEncoder(unittest.TestCase):

    def test_stateless(self):
        encoder = codecs.getincrementalencoder('cp949')()
        self.assertEqual(encoder.encode(u'\ud30c\uc774\uc36c \ub9c8\uc744'), '\xc6\xc4\xc0\xcc\xbd\xe3 \xb8\xb6\xc0\xbb')
        self.assertEqual(encoder.reset(), None)
        self.assertEqual(encoder.encode(u'\u2606\u223c\u2606', True), '\xa1\xd9\xa1\xad\xa1\xd9')
        self.assertEqual(encoder.reset(), None)
        self.assertEqual(encoder.encode(u'', True), '')
        self.assertEqual(encoder.encode(u'', False), '')
        self.assertEqual(encoder.reset(), None)
        return

    def test_stateful(self):
        encoder = codecs.getincrementalencoder('jisx0213')()
        self.assertEqual(encoder.encode(u'\xe6\u0300'), '\xab\xc4')
        self.assertEqual(encoder.encode(u'\xe6'), '')
        self.assertEqual(encoder.encode(u'\u0300'), '\xab\xc4')
        self.assertEqual(encoder.encode(u'\xe6', True), '\xa9\xdc')
        self.assertEqual(encoder.reset(), None)
        self.assertEqual(encoder.encode(u'\u0300'), '\xab\xdc')
        self.assertEqual(encoder.encode(u'\xe6'), '')
        self.assertEqual(encoder.encode('', True), '\xa9\xdc')
        self.assertEqual(encoder.encode('', True), '')
        return

    def test_stateful_keep_buffer(self):
        encoder = codecs.getincrementalencoder('jisx0213')()
        self.assertEqual(encoder.encode(u'\xe6'), '')
        self.assertRaises(UnicodeEncodeError, encoder.encode, u'\u0123')
        self.assertEqual(encoder.encode(u'\u0300\xe6'), '\xab\xc4')
        self.assertRaises(UnicodeEncodeError, encoder.encode, u'\u0123')
        self.assertEqual(encoder.reset(), None)
        self.assertEqual(encoder.encode(u'\u0300'), '\xab\xdc')
        self.assertEqual(encoder.encode(u'\xe6'), '')
        self.assertRaises(UnicodeEncodeError, encoder.encode, u'\u0123')
        self.assertEqual(encoder.encode(u'', True), '\xa9\xdc')
        return

    def test_issue5640(self):
        encoder = codecs.getincrementalencoder('shift-jis')('backslashreplace')
        self.assertEqual(encoder.encode(u'\xff'), '\\xff')
        self.assertEqual(encoder.encode(u'\n'), '\n')


class Test_IncrementalDecoder(unittest.TestCase):

    def test_dbcs(self):
        decoder = codecs.getincrementaldecoder('cp949')()
        self.assertEqual(decoder.decode('\xc6\xc4\xc0\xcc\xbd'), u'\ud30c\uc774')
        self.assertEqual(decoder.decode('\xe3 \xb8\xb6\xc0\xbb'), u'\uc36c \ub9c8\uc744')
        self.assertEqual(decoder.decode(''), u'')

    def test_dbcs_keep_buffer(self):
        decoder = codecs.getincrementaldecoder('cp949')()
        self.assertEqual(decoder.decode('\xc6\xc4\xc0'), u'\ud30c')
        self.assertRaises(UnicodeDecodeError, decoder.decode, '', True)
        self.assertEqual(decoder.decode('\xcc'), u'\uc774')
        self.assertEqual(decoder.decode('\xc6\xc4\xc0'), u'\ud30c')
        self.assertRaises(UnicodeDecodeError, decoder.decode, '\xcc\xbd', True)
        self.assertEqual(decoder.decode('\xcc'), u'\uc774')

    def test_iso2022(self):
        decoder = codecs.getincrementaldecoder('iso2022-jp')()
        ESC = '\x1b'
        self.assertEqual(decoder.decode(ESC + '('), u'')
        self.assertEqual(decoder.decode('B', True), u'')
        self.assertEqual(decoder.decode(ESC + '$'), u'')
        self.assertEqual(decoder.decode('B@$'), u'\u4e16')
        self.assertEqual(decoder.decode('@$@'), u'\u4e16')
        self.assertEqual(decoder.decode('$', True), u'\u4e16')
        self.assertEqual(decoder.reset(), None)
        self.assertEqual(decoder.decode('@$'), u'@$')
        self.assertEqual(decoder.decode(ESC + '$'), u'')
        self.assertRaises(UnicodeDecodeError, decoder.decode, '', True)
        self.assertEqual(decoder.decode('B@$'), u'\u4e16')
        return


class Test_StreamReader(unittest.TestCase):

    def test_bug1728403(self):
        try:
            open(TESTFN, 'w').write('\xa1')
            f = codecs.open(TESTFN, encoding='cp949')
            self.assertRaises(UnicodeDecodeError, f.read, 2)
        finally:
            try:
                f.close()
            except:
                pass

            os.unlink(TESTFN)


class Test_StreamWriter(unittest.TestCase):
    if len(u'\U00012345') == 2:

        def test_gb18030(self):
            s = StringIO.StringIO()
            c = codecs.getwriter('gb18030')(s)
            c.write(u'123')
            self.assertEqual(s.getvalue(), '123')
            c.write(u'\U00012345')
            self.assertEqual(s.getvalue(), '123\x907\x959')
            c.write(u'\U00012345'[0])
            self.assertEqual(s.getvalue(), '123\x907\x959')
            c.write(u'\U00012345'[1] + u'\U00012345' + u'\uac00\xac')
            self.assertEqual(s.getvalue(), '123\x907\x959\x907\x959\x907\x959\x827\xcf5\x810\x851')
            c.write(u'\U00012345'[0])
            self.assertEqual(s.getvalue(), '123\x907\x959\x907\x959\x907\x959\x827\xcf5\x810\x851')
            self.assertRaises(UnicodeError, c.reset)
            self.assertEqual(s.getvalue(), '123\x907\x959\x907\x959\x907\x959\x827\xcf5\x810\x851')

        def test_utf_8(self):
            s = StringIO.StringIO()
            c = codecs.getwriter('utf-8')(s)
            c.write(u'123')
            self.assertEqual(s.getvalue(), '123')
            c.write(u'\U00012345')
            self.assertEqual(s.getvalue(), '123\xf0\x92\x8d\x85')

    def test_streamwriter_strwrite(self):
        s = StringIO.StringIO()
        wr = codecs.getwriter('gb18030')(s)
        wr.write('abcd')
        self.assertEqual(s.getvalue(), 'abcd')


class Test_ISO2022(unittest.TestCase):

    def test_g2(self):
        iso2022jp2 = '\x1b(B:hu4:unit\x1b.A\x1bNi de famille'
        uni = u':hu4:unit\xe9 de famille'
        self.assertEqual(iso2022jp2.decode('iso2022-jp-2'), uni)

    def test_iso2022_jp_g0(self):
        self.assertNotIn('\x0e', u'\xad'.encode('iso-2022-jp-2'))
        for encoding in ('iso-2022-jp-2004', 'iso-2022-jp-3'):
            e = u'\u3406'.encode(encoding)
            self.assertFalse(filter(lambda x: x >= '\x80', e))

    def test_bug1572832(self):
        if sys.maxunicode >= 65536:
            myunichr = unichr
        else:
            myunichr = lambda x: unichr(55232 + (x >> 10)) + unichr(56320 + (x & 1023))
        for x in xrange(65536, 1114112):
            myunichr(x).encode('iso_2022_jp', 'ignore')


class TestStateful(unittest.TestCase):
    text = u'\u4e16\u4e16'
    encoding = 'iso-2022-jp'
    expected = '\x1b$B@$@$'
    expected_reset = '\x1b$B@$@$\x1b(B'

    def test_encode(self):
        self.assertEqual(self.text.encode(self.encoding), self.expected_reset)

    def test_incrementalencoder(self):
        encoder = codecs.getincrementalencoder(self.encoding)()
        output = ''.join((encoder.encode(char) for char in self.text))
        self.assertEqual(output, self.expected)

    def test_incrementalencoder_final(self):
        encoder = codecs.getincrementalencoder(self.encoding)()
        last_index = len(self.text) - 1
        output = ''.join((encoder.encode(char, index == last_index) for index, char in enumerate(self.text)))
        self.assertEqual(output, self.expected_reset)


class TestHZStateful(TestStateful):
    text = u'\u804a\u804a'
    encoding = 'hz'
    expected = '~{ADAD'
    expected_reset = '~{ADAD~}'


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()