# Embedded file name: scripts/common/Lib/test/test_pep263.py
import unittest
from test import test_support

class PEP263Test(unittest.TestCase):

    def test_pep263(self):
        self.assertEqual(u'\u041f\u0438\u0442\u043e\u043d'.encode('utf-8'), '\xd0\x9f\xd0\xb8\xd1\x82\xd0\xbe\xd0\xbd')
        self.assertEqual(u'\\\u041f'.encode('utf-8'), '\\\xd0\x9f')

    def test_compilestring(self):
        c = compile("\n# coding: utf-8\nu = u'\xc3\xb3'\n", 'dummy', 'exec')
        d = {}
        exec c in d
        self.assertEqual(d['u'], u'\xf3')

    def test_issue3297(self):
        c = compile("a, b = '\\U0001010F', '\\U0001010F'", 'dummy', 'exec')
        d = {}
        exec c in d
        self.assertEqual(d['a'], d['b'])
        self.assertEqual(len(d['a']), len(d['b']))

    def test_issue7820(self):
        self.assertRaises(SyntaxError, eval, '\xff ')
        self.assertRaises(SyntaxError, eval, '\xef\xbb ')


def test_main():
    test_support.run_unittest(PEP263Test)


if __name__ == '__main__':
    test_main()