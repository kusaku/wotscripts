# Embedded file name: scripts/common/Lib/test/test_codecencodings_cn.py
from test import test_support
from test import test_multibytecodec_support
import unittest

class Test_GB2312(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'gb2312'
    tstring = test_multibytecodec_support.load_teststring('gb2312')
    codectests = (('abc\x81\x81\xc1\xc4', 'strict', None),
     ('abc\xc8', 'strict', None),
     ('abc\x81\x81\xc1\xc4', 'replace', u'abc\ufffd\u804a'),
     ('abc\x81\x81\xc1\xc4\xc8', 'replace', u'abc\ufffd\u804a\ufffd'),
     ('abc\x81\x81\xc1\xc4', 'ignore', u'abc\u804a'),
     ('\xc1d', 'strict', None))


class Test_GBK(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'gbk'
    tstring = test_multibytecodec_support.load_teststring('gbk')
    codectests = (('abc\x80\x80\xc1\xc4', 'strict', None),
     ('abc\xc8', 'strict', None),
     ('abc\x80\x80\xc1\xc4', 'replace', u'abc\ufffd\u804a'),
     ('abc\x80\x80\xc1\xc4\xc8', 'replace', u'abc\ufffd\u804a\ufffd'),
     ('abc\x80\x80\xc1\xc4', 'ignore', u'abc\u804a'),
     ('\x834\x831', 'strict', None),
     (u'\u30fb', 'strict', None))


class Test_GB18030(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'gb18030'
    tstring = test_multibytecodec_support.load_teststring('gb18030')
    codectests = (('abc\x80\x80\xc1\xc4', 'strict', None),
     ('abc\xc8', 'strict', None),
     ('abc\x80\x80\xc1\xc4', 'replace', u'abc\ufffd\u804a'),
     ('abc\x80\x80\xc1\xc4\xc8', 'replace', u'abc\ufffd\u804a\ufffd'),
     ('abc\x80\x80\xc1\xc4', 'ignore', u'abc\u804a'),
     ('abc\x849\x849\xc1\xc4', 'replace', u'abc\ufffd\u804a'),
     (u'\u30fb', 'strict', '\x819\xa79'))
    has_iso10646 = True


class Test_HZ(test_multibytecodec_support.TestBase, unittest.TestCase):
    encoding = 'hz'
    tstring = test_multibytecodec_support.load_teststring('hz')
    codectests = (('This sentence is in ASCII.\nThe next sentence is in GB.~{<:Ky2;S{#,~}~\n~{NpJ)l6HK!#~}Bye.\n', 'strict', u'This sentence is in ASCII.\nThe next sentence is in GB.\u5df1\u6240\u4e0d\u6b32\uff0c\u52ff\u65bd\u65bc\u4eba\u3002Bye.\n'),
     ('This sentence is in ASCII.\nThe next sentence is in GB.~\n~{<:Ky2;S{#,NpJ)l6HK!#~}~\nBye.\n', 'strict', u'This sentence is in ASCII.\nThe next sentence is in GB.\u5df1\u6240\u4e0d\u6b32\uff0c\u52ff\u65bd\u65bc\u4eba\u3002Bye.\n'),
     ('ab~cd', 'replace', u'ab\ufffdd'),
     ('ab\xffcd', 'replace', u'ab\ufffdcd'),
     ('ab~{\x81\x81AD~}cd', 'replace', u'ab\ufffd\ufffd\u804acd'))


def test_main():
    test_support.run_unittest(__name__)


if __name__ == '__main__':
    test_main()