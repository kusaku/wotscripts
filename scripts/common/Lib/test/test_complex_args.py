# Embedded file name: scripts/common/Lib/test/test_complex_args.py
import unittest
from test import test_support
import textwrap

class ComplexArgsTestCase(unittest.TestCase):

    def check(self, func, expected, *args):
        self.assertEqual(func(*args), expected)

    def test_func_parens_no_unpacking(self):
        exec textwrap.dedent('\n        def f(((((x))))): return x\n        self.check(f, 1, 1)\n        # Inner parens are elided, same as: f(x,)\n        def f(((x)),): return x\n        self.check(f, 2, 2)\n        ')

    def test_func_1(self):
        exec textwrap.dedent('\n        def f(((((x),)))): return x\n        self.check(f, 3, (3,))\n        def f(((((x)),))): return x\n        self.check(f, 4, (4,))\n        def f(((((x))),)): return x\n        self.check(f, 5, (5,))\n        def f(((x),)): return x\n        self.check(f, 6, (6,))\n        ')

    def test_func_2(self):
        exec textwrap.dedent('\n        def f(((((x)),),)): return x\n        self.check(f, 2, ((2,),))\n        ')

    def test_func_3(self):
        exec textwrap.dedent('\n        def f((((((x)),),),)): return x\n        self.check(f, 3, (((3,),),))\n        ')

    def test_func_complex(self):
        exec textwrap.dedent('\n        def f((((((x)),),),), a, b, c): return x, a, b, c\n        self.check(f, (3, 9, 8, 7), (((3,),),), 9, 8, 7)\n\n        def f(((((((x)),)),),), a, b, c): return x, a, b, c\n        self.check(f, (3, 9, 8, 7), (((3,),),), 9, 8, 7)\n\n        def f(a, b, c, ((((((x)),)),),)): return a, b, c, x\n        self.check(f, (9, 8, 7, 3), 9, 8, 7, (((3,),),))\n        ')

    def test_lambda_parens_no_unpacking(self):
        exec textwrap.dedent('\n        f = lambda (((((x))))): x\n        self.check(f, 1, 1)\n        # Inner parens are elided, same as: f(x,)\n        f = lambda ((x)),: x\n        self.check(f, 2, 2)\n        ')

    def test_lambda_1(self):
        exec textwrap.dedent('\n        f = lambda (((((x),)))): x\n        self.check(f, 3, (3,))\n        f = lambda (((((x)),))): x\n        self.check(f, 4, (4,))\n        f = lambda (((((x))),)): x\n        self.check(f, 5, (5,))\n        f = lambda (((x),)): x\n        self.check(f, 6, (6,))\n        ')

    def test_lambda_2(self):
        exec textwrap.dedent('\n        f = lambda (((((x)),),)): x\n        self.check(f, 2, ((2,),))\n        ')

    def test_lambda_3(self):
        exec textwrap.dedent('\n        f = lambda ((((((x)),),),)): x\n        self.check(f, 3, (((3,),),))\n        ')

    def test_lambda_complex(self):
        exec textwrap.dedent('\n        f = lambda (((((x)),),),), a, b, c: (x, a, b, c)\n        self.check(f, (3, 9, 8, 7), (((3,),),), 9, 8, 7)\n\n        f = lambda ((((((x)),)),),), a, b, c: (x, a, b, c)\n        self.check(f, (3, 9, 8, 7), (((3,),),), 9, 8, 7)\n\n        f = lambda a, b, c, ((((((x)),)),),): (a, b, c, x)\n        self.check(f, (9, 8, 7, 3), 9, 8, 7, (((3,),),))\n        ')


def test_main():
    with test_support.check_py3k_warnings(('tuple parameter unpacking has been removed', SyntaxWarning), ('parenthesized argument names are invalid', SyntaxWarning)):
        test_support.run_unittest(ComplexArgsTestCase)


if __name__ == '__main__':
    test_main()