# Embedded file name: scripts/common/Lib/test/test_strop.py
import warnings
warnings.filterwarnings('ignore', 'strop functions are obsolete;', DeprecationWarning, 'test.test_strop|unittest')
import strop
import unittest
from test import test_support

class StropFunctionTestCase(unittest.TestCase):

    def test_atoi(self):
        self.assertTrue(strop.atoi(' 1 ') == 1)
        self.assertRaises(ValueError, strop.atoi, ' 1x')
        self.assertRaises(ValueError, strop.atoi, ' x1 ')

    def test_atol(self):
        self.assertTrue(strop.atol(' 1 ') == 1L)
        self.assertRaises(ValueError, strop.atol, ' 1x')
        self.assertRaises(ValueError, strop.atol, ' x1 ')

    def test_atof(self):
        self.assertTrue(strop.atof(' 1 ') == 1.0)
        self.assertRaises(ValueError, strop.atof, ' 1x')
        self.assertRaises(ValueError, strop.atof, ' x1 ')

    def test_capitalize(self):
        self.assertTrue(strop.capitalize(' hello ') == ' hello ')
        self.assertTrue(strop.capitalize('hello ') == 'Hello ')

    def test_find(self):
        self.assertTrue(strop.find('abcdefghiabc', 'abc') == 0)
        self.assertTrue(strop.find('abcdefghiabc', 'abc', 1) == 9)
        self.assertTrue(strop.find('abcdefghiabc', 'def', 4) == -1)

    def test_rfind(self):
        self.assertTrue(strop.rfind('abcdefghiabc', 'abc') == 9)

    def test_lower(self):
        self.assertTrue(strop.lower('HeLLo') == 'hello')

    def test_upper(self):
        self.assertTrue(strop.upper('HeLLo') == 'HELLO')

    def test_swapcase(self):
        self.assertTrue(strop.swapcase('HeLLo cOmpUteRs') == 'hEllO CoMPuTErS')

    def test_strip(self):
        self.assertTrue(strop.strip(' \t\n hello \t\n ') == 'hello')

    def test_lstrip(self):
        self.assertTrue(strop.lstrip(' \t\n hello \t\n ') == 'hello \t\n ')

    def test_rstrip(self):
        self.assertTrue(strop.rstrip(' \t\n hello \t\n ') == ' \t\n hello')

    def test_replace(self):
        replace = strop.replace
        self.assertTrue(replace('one!two!three!', '!', '@', 1) == 'one@two!three!')
        self.assertTrue(replace('one!two!three!', '!', '@', 2) == 'one@two@three!')
        self.assertTrue(replace('one!two!three!', '!', '@', 3) == 'one@two@three@')
        self.assertTrue(replace('one!two!three!', '!', '@', 4) == 'one@two@three@')
        self.assertTrue(replace('one!two!three!', '!', '@', 0) == 'one@two@three@')
        self.assertTrue(replace('one!two!three!', '!', '@') == 'one@two@three@')
        self.assertTrue(replace('one!two!three!', 'x', '@') == 'one!two!three!')
        self.assertTrue(replace('one!two!three!', 'x', '@', 2) == 'one!two!three!')

    def test_split(self):
        split = strop.split
        self.assertTrue(split('this is the split function') == ['this',
         'is',
         'the',
         'split',
         'function'])
        self.assertTrue(split('a|b|c|d', '|') == ['a',
         'b',
         'c',
         'd'])
        self.assertTrue(split('a|b|c|d', '|', 2) == ['a', 'b', 'c|d'])
        self.assertTrue(split('a b c d', None, 1) == ['a', 'b c d'])
        self.assertTrue(split('a b c d', None, 2) == ['a', 'b', 'c d'])
        self.assertTrue(split('a b c d', None, 3) == ['a',
         'b',
         'c',
         'd'])
        self.assertTrue(split('a b c d', None, 4) == ['a',
         'b',
         'c',
         'd'])
        self.assertTrue(split('a b c d', None, 0) == ['a',
         'b',
         'c',
         'd'])
        self.assertTrue(split('a  b  c  d', None, 2) == ['a', 'b', 'c  d'])
        return

    def test_join(self):
        self.assertTrue(strop.join(['a',
         'b',
         'c',
         'd']) == 'a b c d')
        self.assertTrue(strop.join(('a', 'b', 'c', 'd'), '') == 'abcd')
        self.assertTrue(strop.join(Sequence()) == 'w x y z')
        self.assertTrue(strop.join(['x' * 100] * 100, ':') == ('x' * 100 + ':') * 99 + 'x' * 100)
        self.assertTrue(strop.join(('x' * 100,) * 100, ':') == ('x' * 100 + ':') * 99 + 'x' * 100)

    def test_maketrans(self):
        self.assertTrue(strop.maketrans('abc', 'xyz') == transtable)
        self.assertRaises(ValueError, strop.maketrans, 'abc', 'xyzq')

    def test_translate(self):
        self.assertTrue(strop.translate('xyzabcdef', transtable, 'def') == 'xyzxyz')

    def test_data_attributes(self):
        strop.lowercase
        strop.uppercase
        strop.whitespace

    @test_support.precisionbigmemtest(size=test_support._2G - 1, memuse=5)
    def test_stropjoin_huge_list(self, size):
        a = 'A' * size
        try:
            r = strop.join([a, a], a)
        except OverflowError:
            pass
        else:
            self.assertEqual(len(r), len(a) * 3)

    @test_support.precisionbigmemtest(size=test_support._2G - 1, memuse=1)
    def test_stropjoin_huge_tup(self, size):
        a = 'A' * size
        try:
            r = strop.join((a, a), a)
        except OverflowError:
            pass
        else:
            self.assertEqual(len(r), len(a) * 3)


transtable = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`xyzdefghijklmnopqrstuvwxyz{|}~\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff'

class Sequence:

    def __init__(self):
        self.seq = 'wxyz'

    def __len__(self):
        return len(self.seq)

    def __getitem__(self, i):
        return self.seq[i]


def test_main():
    test_support.run_unittest(StropFunctionTestCase)


if __name__ == '__main__':
    test_main()