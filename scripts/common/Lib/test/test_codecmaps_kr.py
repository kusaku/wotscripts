# Embedded file name: scripts/common/Lib/test/test_codecmaps_kr.py
from test import test_support
from test import test_multibytecodec_support
import unittest

class TestCP949Map(test_multibytecodec_support.TestBase_Mapping, unittest.TestCase):
    encoding = 'cp949'
    mapfileurl = 'http://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP949.TXT'


class TestEUCKRMap(test_multibytecodec_support.TestBase_Mapping, unittest.TestCase):
    encoding = 'euc_kr'
    mapfileurl = 'http://people.freebsd.org/~perky/i18n/EUC-KR.TXT'
    pass_enctest = [('\xa4\xd4', u'\u3164')]
    pass_dectest = [('\xa4\xd4', u'\u3164')]


class TestJOHABMap(test_multibytecodec_support.TestBase_Mapping, unittest.TestCase):
    encoding = 'johab'
    mapfileurl = 'http://www.unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/KSC/JOHAB.TXT'
    pass_enctest = [('\\', u'\u20a9')]
    pass_dectest = [('\\', u'\u20a9')]


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()