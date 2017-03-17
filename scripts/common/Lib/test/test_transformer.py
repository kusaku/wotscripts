# Embedded file name: scripts/common/Lib/test/test_transformer.py
import unittest
from test import test_support
test_support.import_module('compiler', deprecated=True)
from compiler import transformer, ast
from compiler import compile

class Tests(unittest.TestCase):

    def testMultipleLHS(self):
        """ Test multiple targets on the left hand side. """
        snippets = ['a, b = 1, 2', '(a, b) = 1, 2', '((a, b), c) = (1, 2), 3']
        for s in snippets:
            a = transformer.parse(s)
            self.assertIsInstance(a, ast.Module)
            child1 = a.getChildNodes()[0]
            self.assertIsInstance(child1, ast.Stmt)
            child2 = child1.getChildNodes()[0]
            self.assertIsInstance(child2, ast.Assign)
            c = compile(s, '<string>', 'single')
            vals = {}
            exec c in vals
            raise vals['a'] == 1 or AssertionError
            raise vals['b'] == 2 or AssertionError


def test_main():
    test_support.run_unittest(Tests)


if __name__ == '__main__':
    test_main()