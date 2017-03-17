# Embedded file name: scripts/common/Lib/test/test_xmllib.py
"""Test module to thest the xmllib module.
   Sjoerd Mullender
"""
testdoc = '<?xml version="1.0" encoding="UTF-8" standalone=\'yes\' ?>\n<!-- comments aren\'t allowed before the <?xml?> tag,\n     but they are allowed before the <!DOCTYPE> tag -->\n<?processing instructions are allowed in the same places as comments ?>\n<!DOCTYPE greeting [\n  <!ELEMENT greeting (#PCDATA)>\n]>\n<greeting>Hello, world!</greeting>\n'
nsdoc = "<foo xmlns='URI' attr='val'/>"
from test import test_support
import unittest
xmllib = test_support.import_module('xmllib', deprecated=True)

class XMLParserTestCase(unittest.TestCase):

    def test_simple(self):
        parser = xmllib.XMLParser()
        for c in testdoc:
            parser.feed(c)

        parser.close()

    def test_default_namespace(self):

        class H(xmllib.XMLParser):

            def unknown_starttag(self, name, attr):
                self.name, self.attr = name, attr

        h = H()
        h.feed(nsdoc)
        h.close()
        self.assertEqual(h.name, 'URI foo')
        self.assertEqual(h.attr, {'attr': 'val'})


def test_main():
    test_support.run_unittest(XMLParserTestCase)


if __name__ == '__main__':
    test_main()