# Embedded file name: scripts/common/Lib/test/test_charmapcodec.py
""" Python character mapping codec test

This uses the test codec in testcodec.py and thus also tests the
encodings package lookup scheme.

Written by Marc-Andre Lemburg (mal@lemburg.com).

(c) Copyright 2000 Guido van Rossum.

"""
import test.test_support, unittest
import codecs

def codec_search_function(encoding):
    if encoding == 'testcodec':
        from test import testcodec
        return tuple(testcodec.getregentry())
    else:
        return None


codecs.register(codec_search_function)
codecname = 'testcodec'

class CharmapCodecTest(unittest.TestCase):

    def test_constructorx(self):
        self.assertEqual(unicode('abc', codecname), u'abc')
        self.assertEqual(unicode('xdef', codecname), u'abcdef')
        self.assertEqual(unicode('defx', codecname), u'defabc')
        self.assertEqual(unicode('dxf', codecname), u'dabcf')
        self.assertEqual(unicode('dxfx', codecname), u'dabcfabc')

    def test_encodex(self):
        self.assertEqual(u'abc'.encode(codecname), 'abc')
        self.assertEqual(u'xdef'.encode(codecname), 'abcdef')
        self.assertEqual(u'defx'.encode(codecname), 'defabc')
        self.assertEqual(u'dxf'.encode(codecname), 'dabcf')
        self.assertEqual(u'dxfx'.encode(codecname), 'dabcfabc')

    def test_constructory(self):
        self.assertEqual(unicode('ydef', codecname), u'def')
        self.assertEqual(unicode('defy', codecname), u'def')
        self.assertEqual(unicode('dyf', codecname), u'df')
        self.assertEqual(unicode('dyfy', codecname), u'df')

    def test_maptoundefined(self):
        self.assertRaises(UnicodeError, unicode, 'abc\x01', codecname)


def test_main():
    test.test_support.run_unittest(CharmapCodecTest)


if __name__ == '__main__':
    test_main()