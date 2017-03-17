# Embedded file name: scripts/common/Lib/test/test_htmllib.py
import formatter
import unittest
from test import test_support
htmllib = test_support.import_module('htmllib', deprecated=True)

class AnchorCollector(htmllib.HTMLParser):

    def __init__(self, *args, **kw):
        self.__anchors = []
        htmllib.HTMLParser.__init__(self, *args, **kw)

    def get_anchor_info(self):
        return self.__anchors

    def anchor_bgn(self, *args):
        self.__anchors.append(args)


class DeclCollector(htmllib.HTMLParser):

    def __init__(self, *args, **kw):
        self.__decls = []
        htmllib.HTMLParser.__init__(self, *args, **kw)

    def get_decl_info(self):
        return self.__decls

    def unknown_decl(self, data):
        self.__decls.append(data)


class HTMLParserTestCase(unittest.TestCase):

    def test_anchor_collection(self):
        parser = AnchorCollector(formatter.NullFormatter(), verbose=1)
        parser.feed("<a href='http://foo.org/' name='splat'> </a>\n            <a href='http://www.python.org/'> </a>\n            <a name='frob'> </a>\n            ")
        parser.close()
        self.assertEqual(parser.get_anchor_info(), [('http://foo.org/', 'splat', ''), ('http://www.python.org/', '', ''), ('', 'frob', '')])

    def test_decl_collection(self):
        parser = DeclCollector(formatter.NullFormatter(), verbose=1)
        parser.feed('<html>\n            <body>\n            hallo\n            <![if !supportEmptyParas]>&nbsp;<![endif]>\n            </body>\n            </html>\n            ')
        parser.close()
        self.assertEqual(parser.get_decl_info(), ['if !supportEmptyParas', 'endif'])


def test_main():
    test_support.run_unittest(HTMLParserTestCase)


if __name__ == '__main__':
    test_main()