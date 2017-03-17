# Embedded file name: scripts/common/Lib/test/test_codecencodings_iso2022.py
from test import test_support
from test import test_multibytecodec_support
import unittest
COMMON_CODEC_TESTS = (('ab\xffcd', 'replace', u'ab\ufffdcd'), ('ab\x1bdef', 'replace', u'ab\x1bdef'), ('ab\x1b$def', 'replace', u'ab\ufffd'))

class Test_ISO2022_JP(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_jp'
    tstring = test_multibytecodec_support.load_teststring('iso2022_jp')
    codectests = COMMON_CODEC_TESTS + (('ab\x1bNdef', 'replace', u'ab\x1bNdef'),)


class Test_ISO2022_JP2(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_jp_2'
    tstring = test_multibytecodec_support.load_teststring('iso2022_jp')
    codectests = COMMON_CODEC_TESTS + (('ab\x1bNdef', 'replace', u'abdef'),)


class Test_ISO2022_KR(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'iso2022_kr'
    tstring = test_multibytecodec_support.load_teststring('iso2022_kr')
    codectests = COMMON_CODEC_TESTS + (('ab\x1bNdef', 'replace', u'ab\x1bNdef'),)

    def test_chunkcoding(self):
        pass


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()