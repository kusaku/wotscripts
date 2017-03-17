# Embedded file name: scripts/common/Lib/test/test_codecencodings_jp.py
from test import test_support
from test import test_multibytecodec_support
import unittest

class Test_CP932(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'cp932'
    tstring = test_multibytecodec_support.load_teststring('shift_jis')
    codectests = (('abc\x81\x00\x81\x00\x82\x84', 'strict', None),
     ('abc\xf8', 'strict', None),
     ('abc\x81\x00\x82\x84', 'replace', u'abc\ufffd\uff44'),
     ('abc\x81\x00\x82\x84\x88', 'replace', u'abc\ufffd\uff44\ufffd'),
     ('abc\x81\x00\x82\x84', 'ignore', u'abc\uff44'),
     ('\\~', 'replace', u'\\~'),
     ('\x81_\x81a\x81|', 'replace', u'\uff3c\u2225\uff0d'))


class Test_EUC_JISX0213(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'euc_jisx0213'
    tstring = test_multibytecodec_support.load_teststring('euc_jisx0213')
    codectests = (('abc\x80\x80\xc1\xc4', 'strict', None),
     ('abc\xc8', 'strict', None),
     ('abc\x80\x80\xc1\xc4', 'replace', u'abc\ufffd\u7956'),
     ('abc\x80\x80\xc1\xc4\xc8', 'replace', u'abc\ufffd\u7956\ufffd'),
     ('abc\x80\x80\xc1\xc4', 'ignore', u'abc\u7956'),
     ('abc\x8f\x83\x83', 'replace', u'abc\ufffd'),
     ('\xc1d', 'strict', None),
     ('\xa1\xc0', 'strict', u'\uff3c'))
    xmlcharnametest = (u'\xab\u211c\xbb = \u2329\u1234\u232a', '\xa9\xa8&real;\xa9\xb2 = &lang;&#4660;&rang;')


eucjp_commontests = (('abc\x80\x80\xc1\xc4', 'strict', None),
 ('abc\xc8', 'strict', None),
 ('abc\x80\x80\xc1\xc4', 'replace', u'abc\ufffd\u7956'),
 ('abc\x80\x80\xc1\xc4\xc8', 'replace', u'abc\ufffd\u7956\ufffd'),
 ('abc\x80\x80\xc1\xc4', 'ignore', u'abc\u7956'),
 ('abc\x8f\x83\x83', 'replace', u'abc\ufffd'),
 ('\xc1d', 'strict', None))

class Test_EUC_JP_COMPAT(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'euc_jp'
    tstring = test_multibytecodec_support.load_teststring('euc_jp')
    codectests = eucjp_commontests + (('\xa1\xc0\\', 'strict', u'\uff3c\\'), (u'\xa5', 'strict', '\\'), (u'\u203e', 'strict', '~'))


shiftjis_commonenctests = (('abc\x80\x80\x82\x84', 'strict', None),
 ('abc\xf8', 'strict', None),
 ('abc\x80\x80\x82\x84', 'replace', u'abc\ufffd\uff44'),
 ('abc\x80\x80\x82\x84\x88', 'replace', u'abc\ufffd\uff44\ufffd'),
 ('abc\x80\x80\x82\x84def', 'ignore', u'abc\uff44def'))

class Test_SJIS_COMPAT(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'shift_jis'
    tstring = test_multibytecodec_support.load_teststring('shift_jis')
    codectests = shiftjis_commonenctests + (('\\~', 'strict', u'\\~'), ('\x81_\x81a\x81|', 'strict', u'\uff3c\u2016\u2212'))


class Test_SJISX0213(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'shift_jisx0213'
    tstring = test_multibytecodec_support.load_teststring('shift_jisx0213')
    codectests = (('abc\x80\x80\x82\x84', 'strict', None),
     ('abc\xf8', 'strict', None),
     ('abc\x80\x80\x82\x84', 'replace', u'abc\ufffd\uff44'),
     ('abc\x80\x80\x82\x84\x88', 'replace', u'abc\ufffd\uff44\ufffd'),
     ('abc\x80\x80\x82\x84def', 'ignore', u'abc\uff44def'),
     ('\\~', 'replace', u'\xa5\u203e'),
     ('\x81_\x81a\x81|', 'replace', u'\\\u2016\u2212'))
    xmlcharnametest = (u'\xab\u211c\xbb = \u2329\u1234\u232a', '\x85G&real;\x85Q = &lang;&#4660;&rang;')


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()