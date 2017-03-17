# Embedded file name: scripts/common/Lib/test/test_xml_etree_c.py
from test import test_support
from test.test_support import precisionbigmemtest, _2G
import unittest
cET = test_support.import_module('xml.etree.cElementTree')

def sanity():
    """
    Import sanity.
    
    >>> from xml.etree import cElementTree
    """
    pass


class MiscTests(unittest.TestCase):

    @precisionbigmemtest(size=_2G + 100, memuse=1)
    def test_length_overflow(self, size):
        if size < _2G + 100:
            self.skipTest('not enough free memory, need at least 2 GB')
        data = 'x' * size
        parser = cET.XMLParser()
        try:
            self.assertRaises(OverflowError, parser.feed, data)
        finally:
            data = None

        return


def test_main():
    from test import test_xml_etree, test_xml_etree_c
    test_support.run_doctest(test_xml_etree_c, verbosity=True)
    pyET = test_xml_etree.ET
    py__name__ = test_xml_etree.__name__
    test_xml_etree.ET = cET
    if __name__ != '__main__':
        test_xml_etree.__name__ = __name__
    try:
        test_xml_etree.test_main(module_name='xml.etree.cElementTree')
    finally:
        test_xml_etree.ET = pyET
        test_xml_etree.__name__ = py__name__


if __name__ == '__main__':
    test_main()