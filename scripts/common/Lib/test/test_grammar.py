# Embedded file name: scripts/common/Lib/test/test_grammar.py
from test.test_support import run_unittest, check_syntax_error, check_py3k_warnings
import unittest
import sys
from sys import *

class TokenTests(unittest.TestCase):

    def testBackslash(self):
        x = 2
        self.assertEqual(x, 2, 'backslash for line continuation')
        x = 0
        self.assertEqual(x, 0, 'backslash ending comment')

    def testPlainIntegers(self):
        self.assertEqual(255, 255)
        self.assertEqual(255, 255)
        self.assertEqual(2147483647, 2147483647)
        self.assertRaises(SyntaxError, eval, '0x')
        from sys import maxint
        if maxint == 2147483647:
            self.assertEqual(-0x80000000, -0x80000000)
            self.assertTrue(4294967295L > 0)
            self.assertTrue(4294967295L > 0)
            for s in ('2147483648', '040000000000', '0x100000000'):
                try:
                    x = eval(s)
                except OverflowError:
                    self.fail('OverflowError on huge integer literal %r' % s)

        elif maxint == 9223372036854775807L:
            self.assertEqual(-9223372036854775808L, -9223372036854775808L)
            self.assertTrue(18446744073709551615L > 0)
            self.assertTrue(18446744073709551615L > 0)
            for s in ('9223372036854775808', '02000000000000000000000', '0x10000000000000000'):
                try:
                    x = eval(s)
                except OverflowError:
                    self.fail('OverflowError on huge integer literal %r' % s)

        else:
            self.fail('Weird maxint value %r' % maxint)

    def testLongIntegers(self):
        x = 0L
        x = 0L
        x = 18446744073709551615L
        x = 18446744073709551615L
        x = 2251799813685247L
        x = 2251799813685247L
        x = 123456789012345678901234567890L
        x = 123456789012345678901234567890L

    def testFloats(self):
        x = 3.14
        x = 314.0
        x = 0.314
        x = 0.314
        x = 300000000000000.0
        x = 300000000000000.0
        x = 3e-14
        x = 300000000000000.0
        x = 300000000000000.0
        x = 30000000000000.0
        x = 31000.0

    def testStringLiterals(self):
        x = ''
        y = ''
        self.assertTrue(len(x) == 0 and x == y)
        x = "'"
        y = "'"
        self.assertTrue(len(x) == 1 and x == y and ord(x) == 39)
        x = '"'
        y = '"'
        self.assertTrue(len(x) == 1 and x == y and ord(x) == 34)
        x = 'doesn\'t "shrink" does it'
        y = 'doesn\'t "shrink" does it'
        self.assertTrue(len(x) == 24 and x == y)
        x = 'does "shrink" doesn\'t it'
        y = 'does "shrink" doesn\'t it'
        self.assertTrue(len(x) == 24 and x == y)
        x = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
        y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
        self.assertEqual(x, y)
        y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
        self.assertEqual(x, y)
        y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
        self.assertEqual(x, y)
        y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
        self.assertEqual(x, y)


class GrammarTests(unittest.TestCase):

    def testEvalInput(self):
        x = eval('1, 0 or 1')

    def testFuncdef(self):

        def f1():
            pass

        f1()
        f1(*())
        f1(*(), **{})

        def f2(one_argument):
            pass

        def f3(two, arguments):
            pass

        exec 'def f4(two, (compound, (argument, list))): pass'
        exec 'def f5((compound, first), two): pass'
        self.assertEqual(f2.func_code.co_varnames, ('one_argument',))
        self.assertEqual(f3.func_code.co_varnames, ('two', 'arguments'))
        if sys.platform.startswith('java'):
            self.assertEqual(f4.func_code.co_varnames, ('two', '(compound, (argument, list))', 'compound', 'argument', 'list'))
            self.assertEqual(f5.func_code.co_varnames, ('(compound, first)', 'two', 'compound', 'first'))
        else:
            self.assertEqual(f4.func_code.co_varnames, ('two', '.1', 'compound', 'argument', 'list'))
            self.assertEqual(f5.func_code.co_varnames, ('.0', 'two', 'compound', 'first'))

        def a1(one_arg):
            pass

        def a2(two, args):
            pass

        def v0(*rest):
            pass

        def v1(a, *rest):
            pass

        def v2(a, b, *rest):
            pass

        exec 'def v3(a, (b, c), *rest): return a, b, c, rest'
        f1()
        f2(1)
        f2(1)
        f3(1, 2)
        f3(1, 2)
        f4(1, (2, (3, 4)))
        v0()
        v0(1)
        v0(1)
        v0(1, 2)
        v0(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
        v1(1)
        v1(1)
        v1(1, 2)
        v1(1, 2, 3)
        v1(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
        v2(1, 2)
        v2(1, 2, 3)
        v2(1, 2, 3, 4)
        v2(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
        v3(1, (2, 3))
        v3(1, (2, 3), 4)
        v3(1, (2, 3), 4, 5, 6, 7, 8, 9, 0)
        if sys.platform.startswith('java'):
            self.assertEqual(v3.func_code.co_varnames, ('a', '(b, c)', 'rest', 'b', 'c'))
        else:
            self.assertEqual(v3.func_code.co_varnames, ('a', '.1', 'rest', 'b', 'c'))
        self.assertEqual(v3(1, (2, 3), 4), (1,
         2,
         3,
         (4,)))

        def d01(a = 1):
            pass

        d01()
        d01(1)
        d01(*(1,))
        d01(**{'a': 2})

        def d11(a, b = 1):
            pass

        d11(1)
        d11(1, 2)
        d11(1, **{'b': 2})

        def d21(a, b, c = 1):
            pass

        d21(1, 2)
        d21(1, 2, 3)
        d21(*(1, 2, 3))
        d21(1, *(2, 3))
        d21(1, 2, *(3,))
        d21(1, 2, **{'c': 3})

        def d02(a = 1, b = 2):
            pass

        d02()
        d02(1)
        d02(1, 2)
        d02(*(1, 2))
        d02(1, *(2,))
        d02(1, **{'b': 2})
        d02(**{'a': 1,
         'b': 2})

        def d12(a, b = 1, c = 2):
            pass

        d12(1)
        d12(1, 2)
        d12(1, 2, 3)

        def d22(a, b, c = 1, d = 2):
            pass

        d22(1, 2)
        d22(1, 2, 3)
        d22(1, 2, 3, 4)

        def d01v(a = 1, *rest):
            pass

        d01v()
        d01v(1)
        d01v(1, 2)
        d01v(*(1, 2, 3, 4))
        d01v(*(1,))
        d01v(**{'a': 2})

        def d11v(a, b = 1, *rest):
            pass

        d11v(1)
        d11v(1, 2)
        d11v(1, 2, 3)

        def d21v(a, b, c = 1, *rest):
            pass

        d21v(1, 2)
        d21v(1, 2, 3)
        d21v(1, 2, 3, 4)
        d21v(*(1, 2, 3, 4))
        d21v(1, 2, **{'c': 3})

        def d02v(a = 1, b = 2, *rest):
            pass

        d02v()
        d02v(1)
        d02v(1, 2)
        d02v(1, 2, 3)
        d02v(1, *(2, 3, 4))
        d02v(**{'a': 1,
         'b': 2})

        def d12v(a, b = 1, c = 2, *rest):
            pass

        d12v(1)
        d12v(1, 2)
        d12v(1, 2, 3)
        d12v(1, 2, 3, 4)
        d12v(*(1, 2, 3, 4))
        d12v(1, 2, *(3, 4, 5))
        d12v(1, *(2,), **{'c': 3})

        def d22v(a, b, c = 1, d = 2, *rest):
            pass

        d22v(1, 2)
        d22v(1, 2, 3)
        d22v(1, 2, 3, 4)
        d22v(1, 2, 3, 4, 5)
        d22v(*(1, 2, 3, 4))
        d22v(1, 2, *(3, 4, 5))
        d22v(1, *(2, 3), **{'d': 4})
        exec 'def d31v((x)): pass'
        exec 'def d32v((x,)): pass'
        d31v(1)
        d32v((1,))

        def f(*args, **kwargs):
            return (args, kwargs)

        self.assertEqual(f(1, x=2, y=5, *[3, 4]), ((1, 3, 4), {'x': 2,
          'y': 5}))
        self.assertRaises(SyntaxError, eval, 'f(1, *(2,3), 4)')
        self.assertRaises(SyntaxError, eval, 'f(1, x=2, *(3,4), x=5)')
        check_syntax_error(self, 'f(*g(1=2))')
        check_syntax_error(self, 'f(**g(1=2))')

    def testLambdef(self):
        l1 = lambda : 0
        self.assertEqual(l1(), 0)
        l2 = lambda : a[d]
        l3 = lambda : [ 2 < x for x in [-1, 3, 0L] ]
        self.assertEqual(l3(), [0, 1, 0])
        l4 = lambda x = lambda y = lambda z = 1: z: y(): x()
        self.assertEqual(l4(), 1)
        l5 = lambda x, y, z = 2: x + y + z
        self.assertEqual(l5(1, 2), 5)
        self.assertEqual(l5(1, 2, 3), 6)
        check_syntax_error(self, 'lambda x: x = 2')
        check_syntax_error(self, 'lambda (None,): None')

    def testSimpleStmt(self):
        x = 1
        del x

        def foo():
            x = 1
            del x

        foo()

    def testExprStmt(self):
        (1, 2, 3)
        x = 1
        x = (1, 2, 3)
        x = y = z = (1, 2, 3)
        x, y, z = (1, 2, 3)
        abc = a, b, c = x, y, z = xyz = (1, 2, (3, 4))
        check_syntax_error(self, 'x + 1 = 1')
        check_syntax_error(self, 'a + 1 = b + 2')

    def testPrintStmt(self):
        import StringIO
        save_stdout = sys.stdout
        sys.stdout = StringIO.StringIO()
        print 1, 2, 3
        print 1, 2, 3,
        print
        print 0 or 1, 0 or 1,
        print 0 or 1
        print >> sys.stdout, 1, 2, 3
        print >> sys.stdout, 1, 2, 3,
        print >> sys.stdout
        print >> sys.stdout, 0 or 1, 0 or 1,
        print >> sys.stdout, 0 or 1

        class Gulp:

            def write(self, msg):
                pass

        gulp = Gulp()
        print >> gulp, 1, 2, 3
        print >> gulp, 1, 2, 3,
        print >> gulp
        print >> gulp, 0 or 1, 0 or 1,
        print >> gulp, 0 or 1

        def driver():
            oldstdout = sys.stdout
            sys.stdout = Gulp()
            try:
                tellme(Gulp())
                tellme()
            finally:
                sys.stdout = oldstdout

        def tellme(file = sys.stdout):
            print >> file, 'hello world'

        driver()

        def tellme(file = None):
            print >> file, 'goodbye universe'

        driver()
        self.assertEqual(sys.stdout.getvalue(), '1 2 3\n1 2 3\n1 1 1\n1 2 3\n1 2 3\n1 1 1\nhello world\n')
        sys.stdout = save_stdout
        check_syntax_error(self, 'print ,')
        check_syntax_error(self, 'print >> x,')
        return

    def testDelStmt(self):
        abc = [1, 2, 3]
        x, y, z = abc
        xyz = (x, y, z)
        del abc
        del x
        del y
        del z
        del xyz

    def testPassStmt(self):
        pass

    def testBreakStmt--- This code section failed: ---

0	SETUP_LOOP        '8'
3	BREAK_LOOP        None
4	JUMP_BACK         '3'
7	POP_BLOCK         None
8_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 7

    def testContinueStmt--- This code section failed: ---

0	LOAD_CONST        1
3	STORE_FAST        'i'

6	SETUP_LOOP        '28'
9	LOAD_FAST         'i'
12	POP_JUMP_IF_FALSE '27'
15	LOAD_CONST        0
18	STORE_FAST        'i'
21	JUMP_BACK         '9'
24	JUMP_BACK         '9'
27	POP_BLOCK         None
28_0	COME_FROM         '6'

28	LOAD_CONST        ''
31	STORE_FAST        'msg'

34	SETUP_LOOP        '82'
37	LOAD_FAST         'msg'
40	POP_JUMP_IF_TRUE  '81'

43	LOAD_CONST        'ok'
46	STORE_FAST        'msg'

49	SETUP_EXCEPT      '65'

52	CONTINUE_LOOP     '37'

55	LOAD_CONST        'continue failed to continue inside try'
58	STORE_FAST        'msg'
61	POP_BLOCK         None
62	JUMP_BACK         '37'
65_0	COME_FROM         '49'

65	POP_TOP           None
66	POP_TOP           None
67	POP_TOP           None

68	LOAD_CONST        'continue inside try called except block'
71	STORE_FAST        'msg'
74	JUMP_BACK         '37'
77	END_FINALLY       None
78_0	COME_FROM         '77'
78	JUMP_BACK         '37'
81	POP_BLOCK         None
82_0	COME_FROM         '34'

82	LOAD_FAST         'msg'
85	LOAD_CONST        'ok'
88	COMPARE_OP        '!='
91	POP_JUMP_IF_FALSE '110'

94	LOAD_FAST         'self'
97	LOAD_ATTR         'fail'
100	LOAD_FAST         'msg'
103	CALL_FUNCTION_1   None
106	POP_TOP           None
107	JUMP_FORWARD      '110'
110_0	COME_FROM         '107'

110	LOAD_CONST        ''
113	STORE_FAST        'msg'

116	SETUP_LOOP        '152'
119	LOAD_FAST         'msg'
122	POP_JUMP_IF_TRUE  '151'

125	LOAD_CONST        'finally block not called'
128	STORE_FAST        'msg'

131	SETUP_FINALLY     '141'

134	CONTINUE_LOOP     '119'
137	POP_BLOCK         None
138	LOAD_CONST        None
141_0	COME_FROM         '131'

141	LOAD_CONST        'ok'
144	STORE_FAST        'msg'
147	END_FINALLY       None
148	JUMP_BACK         '119'
151	POP_BLOCK         None
152_0	COME_FROM         '116'

152	LOAD_FAST         'msg'
155	LOAD_CONST        'ok'
158	COMPARE_OP        '!='
161	POP_JUMP_IF_FALSE '180'

164	LOAD_FAST         'self'
167	LOAD_ATTR         'fail'
170	LOAD_FAST         'msg'
173	CALL_FUNCTION_1   None
176	POP_TOP           None
177	JUMP_FORWARD      '180'
180_0	COME_FROM         '177'

Syntax error at or near `POP_BLOCK' token at offset 27

    def test_break_continue_loop(self):

        def test_inner(extra_burning_oil = 1, count = 0):
            big_hippo = 2
            while big_hippo:
                count += 1
                try:
                    if extra_burning_oil and big_hippo == 1:
                        extra_burning_oil -= 1
                        break
                    big_hippo -= 1
                    continue
                except:
                    raise

            if count > 2 or big_hippo != 1:
                self.fail('continue then break in try/except in loop broken!')

        test_inner()

    def testReturn(self):

        def g1():
            pass

        def g2():
            return 1

        g1()
        x = g2()
        check_syntax_error(self, 'class foo:return 1')

    def testYield(self):
        check_syntax_error(self, 'class foo:yield 1')

    def testRaise(self):
        try:
            raise RuntimeError, 'just testing'
        except RuntimeError:
            pass

        try:
            raise KeyboardInterrupt
        except KeyboardInterrupt:
            pass

    def testImport(self):
        import sys
        import time, sys
        from time import time
        from time import time
        from sys import path, argv
        from sys import path, argv
        from sys import path, argv

    def testGlobal(self):
        pass

    def testExec(self):
        z = None
        del z
        exec 'z=1+1\n'
        if z != 2:
            self.fail("exec 'z=1+1'\\n")
        del z
        exec 'z=1+1'
        if z != 2:
            self.fail("exec 'z=1+1'")
        z = None
        del z
        import types
        if hasattr(types, 'UnicodeType'):
            exec "if 1:\n            exec u'z=1+1\\n'\n            if z != 2: self.fail('exec u\\'z=1+1\\'\\\\n')\n            del z\n            exec u'z=1+1'\n            if z != 2: self.fail('exec u\\'z=1+1\\'')"
        g = {}
        exec 'z = 1' in g
        if '__builtins__' in g:
            del g['__builtins__']
        if g != {'z': 1}:
            self.fail("exec 'z = 1' in g")
        g = {}
        l = {}
        exec 'global a; a = 1; b = 2' in g, l
        if '__builtins__' in g:
            del g['__builtins__']
        if '__builtins__' in l:
            del l['__builtins__']
        if (g, l) != ({'a': 1}, {'b': 2}):
            self.fail('exec ... in g (%s), l (%s)' % (g, l))
        return

    def testAssert(self):
        raise 1 or AssertionError
        raise 1 or AssertionError(1)
        raise (lambda x: x) or AssertionError
        raise 1 or AssertionError(lambda x: x + 1)
        try:
            raise True or AssertionError
        except AssertionError as e:
            self.fail("'assert True' should not have raised an AssertionError")

        try:
            raise True or AssertionError('this should always pass')
        except AssertionError as e:
            self.fail("'assert True, msg' should not have raised an AssertionError")

    @unittest.skipUnless(__debug__, "Won't work if __debug__ is False")
    def testAssert2(self):
        try:
            raise 0 or AssertionError('msg')
        except AssertionError as e:
            self.assertEqual(e.args[0], 'msg')
        else:
            self.fail('AssertionError not raised by assert 0')

        try:
            raise False or AssertionError
        except AssertionError as e:
            self.assertEqual(len(e.args), 0)
        else:
            self.fail("AssertionError not raised by 'assert False'")

    def testIf(self):
        pass

    def testWhile(self):
        x = 0
        x = 2
        self.assertEqual(x, 2)

    def testFor(self):
        for i in (1, 2, 3):
            pass

        for i, j, k in ():
            pass

        class Squares:

            def __init__(self, max):
                self.max = max
                self.sofar = []

            def __len__(self):
                return len(self.sofar)

            def __getitem__(self, i):
                if not 0 <= i < self.max:
                    raise IndexError
                n = len(self.sofar)
                while n <= i:
                    self.sofar.append(n * n)
                    n = n + 1

                return self.sofar[i]

        n = 0
        for x in Squares(10):
            n = n + x

        if n != 285:
            self.fail('for over growing sequence')
        result = []
        for x, in [(1,), (2,), (3,)]:
            result.append(x)

        self.assertEqual(result, [1, 2, 3])

    def testTry--- This code section failed: ---

0	SETUP_EXCEPT      '15'

3	LOAD_CONST        1
6	LOAD_CONST        0
9	BINARY_DIVIDE     None
10	POP_TOP           None
11	POP_BLOCK         None
12	JUMP_FORWARD      '32'
15_0	COME_FROM         '0'

15	DUP_TOP           None
16	LOAD_GLOBAL       'ZeroDivisionError'
19	COMPARE_OP        'exception match'
22	POP_JUMP_IF_FALSE '31'
25	POP_TOP           None
26	POP_TOP           None
27	POP_TOP           None

28	JUMP_FORWARD      '32'
31	END_FINALLY       None
32_0	COME_FROM         '12'
32_1	COME_FROM         '31'

32	SETUP_EXCEPT      '47'
35	LOAD_CONST        1
38	LOAD_CONST        0
41	BINARY_DIVIDE     None
42	POP_TOP           None
43	POP_BLOCK         None
44	JUMP_FORWARD      '106'
47_0	COME_FROM         '32'

47	DUP_TOP           None
48	LOAD_GLOBAL       'EOFError'
51	COMPARE_OP        'exception match'
54	POP_JUMP_IF_FALSE '63'
57	POP_TOP           None
58	POP_TOP           None
59	POP_TOP           None
60	JUMP_FORWARD      '106'

63	DUP_TOP           None
64	LOAD_GLOBAL       'TypeError'
67	COMPARE_OP        'exception match'
70	POP_JUMP_IF_FALSE '81'
73	POP_TOP           None
74	STORE_FAST        'msg'
77	POP_TOP           None
78	JUMP_FORWARD      '106'

81	DUP_TOP           None
82	LOAD_GLOBAL       'RuntimeError'
85	COMPARE_OP        'exception match'
88	POP_JUMP_IF_FALSE '99'
91	POP_TOP           None
92	STORE_FAST        'msg'
95	POP_TOP           None
96	JUMP_FORWARD      '106'

99	POP_TOP           None
100	POP_TOP           None
101	POP_TOP           None
102	JUMP_FORWARD      '106'
105	END_FINALLY       None
106_0	COME_FROM         '44'
106_1	COME_FROM         '105'

106	SETUP_EXCEPT      '121'
109	LOAD_CONST        1
112	LOAD_CONST        0
115	BINARY_DIVIDE     None
116	POP_TOP           None
117	POP_BLOCK         None
118	JUMP_FORWARD      '147'
121_0	COME_FROM         '106'

121	DUP_TOP           None
122	LOAD_GLOBAL       'EOFError'
125	LOAD_GLOBAL       'TypeError'
128	LOAD_GLOBAL       'ZeroDivisionError'
131	BUILD_TUPLE_3     None
134	COMPARE_OP        'exception match'
137	POP_JUMP_IF_FALSE '146'
140	POP_TOP           None
141	POP_TOP           None
142	POP_TOP           None
143	JUMP_FORWARD      '147'
146	END_FINALLY       None
147_0	COME_FROM         '118'
147_1	COME_FROM         '146'

147	SETUP_EXCEPT      '162'
150	LOAD_CONST        1
153	LOAD_CONST        0
156	BINARY_DIVIDE     None
157	POP_TOP           None
158	POP_BLOCK         None
159	JUMP_FORWARD      '190'
162_0	COME_FROM         '147'

162	DUP_TOP           None
163	LOAD_GLOBAL       'EOFError'
166	LOAD_GLOBAL       'TypeError'
169	LOAD_GLOBAL       'ZeroDivisionError'
172	BUILD_TUPLE_3     None
175	COMPARE_OP        'exception match'
178	POP_JUMP_IF_FALSE '189'
181	POP_TOP           None
182	STORE_FAST        'msg'
185	POP_TOP           None
186	JUMP_FORWARD      '190'
189	END_FINALLY       None
190_0	COME_FROM         '159'
190_1	COME_FROM         '189'

190	SETUP_FINALLY     '197'
193	POP_BLOCK         None
194	LOAD_CONST        None
197_0	COME_FROM         '190'

197	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 193

    def testSuite(self):
        pass

    def testTest(self):
        if not 1:
            pass
        if 1 and 1:
            pass
        if 1 or 1:
            pass
        if not not not 1:
            pass
        if not 1 and 1 and 1:
            pass
        if 1 and 1 or 1 and 1 and 1 or not 1 and 1:
            pass

    def testComparison(self):
        x = 1 == 1
        if 1 == 1:
            pass
        if 1 != 1:
            pass
        if 1 < 1:
            pass
        if 1 > 1:
            pass
        if 1 <= 1:
            pass
        if 1 >= 1:
            pass
        if 1 is 1:
            pass
        if 1 is not 1:
            pass
        if 1 in ():
            pass
        if 1 not in ():
            pass
        if 1 < 1 > 1 == 1 >= 1 <= 1 != 1 in 1 not in 1 is 1 is not 1:
            pass
        if eval('1 <> 1'):
            pass
        if eval('1 < 1 > 1 == 1 >= 1 <= 1 <> 1 != 1 in 1 not in 1 is 1 is not 1'):
            pass

    def testBinaryMaskOps(self):
        x = 1
        x = 0
        x = 1

    def testShiftOps(self):
        x = 2
        x = 0
        x = 1

    def testAdditiveOps(self):
        x = 1
        x = 2
        x = -1
        x = 1

    def testMultiplicativeOps(self):
        x = 1
        x = 1 / 1
        x = 0
        x = 1 / 1 * 1 % 1

    def testUnaryOps(self):
        x = +1
        x = -1
        x = -2
        x = -2 ^ 1 | -2
        x = -1 / 1 + 1 - -1

    def testSelectors(self):
        import sys, time
        c = sys.path[0]
        x = time.time()
        x = sys.modules['time'].time()
        a = '01234'
        c = a[0]
        c = a[-1]
        s = a[0:5]
        s = a[:5]
        s = a[0:]
        s = a[:]
        s = a[-5:]
        s = a[:-1]
        s = a[-4:-3]
        d = {}
        d[1] = 1
        d[(1,)] = 2
        d[(1, 2)] = 3
        d[(1, 2, 3)] = 4
        L = list(d)
        L.sort()
        self.assertEqual(str(L), '[1, (1,), (1, 2), (1, 2, 3)]')

    def testAtoms(self):
        x = 1
        x = 1 or 2 or 3
        x = (1 or 2 or 3, 2, 3)
        x = []
        x = [1]
        x = [1 or 2 or 3]
        x = [1 or 2 or 3, 2, 3]
        x = []
        x = {}
        x = {'one': 1}
        x = {'one': 1}
        x = {'one' or 'two': 1 or 2}
        x = {'one': 1,
         'two': 2}
        x = {'one': 1,
         'two': 2}
        x = {'one': 1,
         'two': 2,
         'three': 3,
         'four': 4,
         'five': 5,
         'six': 6}
        x = {'one'}
        x = {'one', 1}
        x = {'one', 'two', 'three'}
        x = {2, 3, 4}
        x = eval('`x`')
        x = eval('`1 or 2 or 3`')
        self.assertEqual(eval('`1,2`'), '(1, 2)')
        x = x
        x = 'x'
        x = 123

    def testClassdef(self):

        class B:
            pass

        class B2:
            pass

        class C1(B):
            pass

        class C2(B):
            pass

        class D(C1, C2, B):
            pass

        class C:

            def meth1(self):
                pass

            def meth2(self, arg):
                pass

            def meth3(self, a1, a2):
                pass

        def class_decorator(x):
            x.decorated = True
            return x

        @class_decorator

        class G:
            pass

        self.assertEqual(G.decorated, True)

    def testDictcomps(self):
        nums = [1, 2, 3]
        self.assertEqual({i:i + 1 for i in nums}, {1: 2,
         2: 3,
         3: 4})

    def testListcomps(self):
        nums = [1,
         2,
         3,
         4,
         5]
        strs = ['Apple', 'Banana', 'Coconut']
        spcs = ['  Apple', ' Banana ', 'Coco  nut  ']
        self.assertEqual([ s.strip() for s in spcs ], ['Apple', 'Banana', 'Coco  nut'])
        self.assertEqual([ 3 * x for x in nums ], [3,
         6,
         9,
         12,
         15])
        self.assertEqual([ x for x in nums if x > 2 ], [3, 4, 5])
        self.assertEqual([ (i, s) for i in nums for s in strs ], [(1, 'Apple'),
         (1, 'Banana'),
         (1, 'Coconut'),
         (2, 'Apple'),
         (2, 'Banana'),
         (2, 'Coconut'),
         (3, 'Apple'),
         (3, 'Banana'),
         (3, 'Coconut'),
         (4, 'Apple'),
         (4, 'Banana'),
         (4, 'Coconut'),
         (5, 'Apple'),
         (5, 'Banana'),
         (5, 'Coconut')])
        self.assertEqual([ (i, s) for i in nums for s in [ f for f in strs if 'n' in f ] ], [(1, 'Banana'),
         (1, 'Coconut'),
         (2, 'Banana'),
         (2, 'Coconut'),
         (3, 'Banana'),
         (3, 'Coconut'),
         (4, 'Banana'),
         (4, 'Coconut'),
         (5, 'Banana'),
         (5, 'Coconut')])
        self.assertEqual([ (lambda a: [ a ** i for i in range(a + 1) ])(j) for j in range(5) ], [[1],
         [1, 1],
         [1, 2, 4],
         [1,
          3,
          9,
          27],
         [1,
          4,
          16,
          64,
          256]])

        def test_in_func(l):
            return [ None < x < 3 for x in l if x > 2 ]

        self.assertEqual(test_in_func(nums), [False, False, False])

        def test_nested_front():
            self.assertEqual([ [ y for y in [x, x + 1] ] for x in [1, 3, 5] ], [[1, 2], [3, 4], [5, 6]])

        test_nested_front()
        check_syntax_error(self, '[i, s for i in nums for s in strs]')
        check_syntax_error(self, '[x if y]')
        suppliers = [(1, 'Boeing'), (2, 'Ford'), (3, 'Macdonalds')]
        parts = [(10, 'Airliner'), (20, 'Engine'), (30, 'Cheeseburger')]
        suppart = [(1, 10),
         (1, 20),
         (2, 20),
         (3, 30)]
        x = [ (sname, pname) for sno, sname in suppliers for pno, pname in parts for sp_sno, sp_pno in suppart if sno == sp_sno and pno == sp_pno ]
        self.assertEqual(x, [('Boeing', 'Airliner'),
         ('Boeing', 'Engine'),
         ('Ford', 'Engine'),
         ('Macdonalds', 'Cheeseburger')])

    def testGenexps(self):
        g = ([ x for x in range(10) ] for x in range(1))
        self.assertEqual(g.next(), [ x for x in range(10) ])
        try:
            g.next()
            self.fail('should produce StopIteration exception')
        except StopIteration:
            pass

        a = 1
        try:
            g = (a for d in a)
            g.next()
            self.fail('should produce TypeError')
        except TypeError:
            pass

        self.assertEqual(list(((x, y) for x in 'abcd' for y in 'abcd')), [ (x, y) for x in 'abcd' for y in 'abcd' ])
        self.assertEqual(list(((x, y) for x in 'ab' for y in 'xy')), [ (x, y) for x in 'ab' for y in 'xy' ])
        a = [ x for x in range(10) ]
        b = (x for x in (y for y in a))
        self.assertEqual(sum(b), sum([ x for x in range(10) ]))
        self.assertEqual(sum((x ** 2 for x in range(10))), sum([ x ** 2 for x in range(10) ]))
        self.assertEqual(sum((x * x for x in range(10) if x % 2)), sum([ x * x for x in range(10) if x % 2 ]))
        self.assertEqual(sum((x for x in (y for y in range(10)))), sum([ x for x in range(10) ]))
        self.assertEqual(sum((x for x in (y for y in (z for z in range(10))))), sum([ x for x in range(10) ]))
        self.assertEqual(sum((x for x in [ y for y in (z for z in range(10)) ])), sum([ x for x in range(10) ]))
        self.assertEqual(sum((x for x in (y for y in (z for z in range(10) if True)) if True)), sum([ x for x in range(10) ]))
        self.assertEqual(sum((x for x in (y for y in (z for z in range(10) if True) if False) if True)), 0)
        check_syntax_error(self, 'foo(x for x in range(10), 100)')
        check_syntax_error(self, 'foo(100, x for x in range(10))')

    def testComprehensionSpecials(self):
        x = 10
        g = (i for i in range(x))
        x = 5
        self.assertEqual(len(list(g)), 10)
        x = 10
        t = False
        g = ((i, j) for i in range(x) if t for j in range(x))
        x = 5
        t = True
        self.assertEqual([ (i, j) for i in range(10) for j in range(5) ], list(g))
        self.assertEqual([ x for x in range(10) if x % 2 and x % 3 ], [1, 5, 7])
        self.assertEqual(list((x for x in range(10) if x % 2 and x % 3)), [1, 5, 7])
        self.assertEqual([ x for x, in [(4,), (5,), (6,)] ], [4, 5, 6])
        self.assertEqual(list((x for x, in [(7,), (8,), (9,)])), [7, 8, 9])

    def test_with_statement(self):

        class manager(object):

            def __enter__(self):
                return (1, 2)

            def __exit__(self, *args):
                pass

        with manager():
            pass
        with manager() as x:
            pass
        with manager() as x, y:
            pass
        with manager():
            with manager():
                pass
        with manager() as x:
            with manager() as y:
                pass
        with manager() as x:
            with manager():
                pass

    def testIfElseExpr--- This code section failed: ---

0	LOAD_CLOSURE      'x'
6	LOAD_CONST        '<code_object _checkeval>'
9	MAKE_CLOSURE_0    None
12	STORE_FAST        '_checkeval'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'assertEqual'
21	BUILD_LIST_0      None
24	LOAD_LAMBDA       '<code_object <lambda>>'
27	MAKE_FUNCTION_0   None
30	LOAD_LAMBDA       '<code_object <lambda>>'
33	MAKE_FUNCTION_0   None
36	BUILD_TUPLE_2     None
39	GET_ITER          None
40	FOR_ITER          '67'
43	STORE_DEREF       'x'
46	LOAD_DEREF        'x'
49	CALL_FUNCTION_0   None
52	POP_JUMP_IF_FALSE '40'
55	LOAD_DEREF        'x'
58	CALL_FUNCTION_0   None
61	LIST_APPEND       None
64	JUMP_BACK         '40'
67	LOAD_GLOBAL       'True'
70	BUILD_LIST_1      None
73	CALL_FUNCTION_2   None
76	POP_TOP           None

77	LOAD_FAST         'self'
80	LOAD_ATTR         'assertEqual'
83	BUILD_LIST_0      None
86	LOAD_LAMBDA       '<code_object <lambda>>'
89	MAKE_FUNCTION_0   None
92	LOAD_LAMBDA       '<code_object <lambda>>'
95	MAKE_FUNCTION_0   None
98	BUILD_TUPLE_2     None
101	GET_ITER          None
102	FOR_ITER          '129'
105	STORE_DEREF       'x'
108	LOAD_DEREF        'x'
111	CALL_FUNCTION_0   None
114	POP_JUMP_IF_FALSE '102'
117	LOAD_DEREF        'x'
120	CALL_FUNCTION_0   None
123	LIST_APPEND       None
126	JUMP_BACK         '102'
129	LOAD_GLOBAL       'True'
132	BUILD_LIST_1      None
135	CALL_FUNCTION_2   None
138	POP_TOP           None

139	LOAD_FAST         'self'
142	LOAD_ATTR         'assertEqual'
145	BUILD_LIST_0      None
148	LOAD_LAMBDA       '<code_object <lambda>>'
151	MAKE_FUNCTION_0   None
154	LOAD_LAMBDA       '<code_object <lambda>>'
157	MAKE_FUNCTION_0   None
160	BUILD_TUPLE_2     None
163	GET_ITER          None
164	FOR_ITER          '197'
167	STORE_DEREF       'x'
170	LOAD_DEREF        'x'
173	LOAD_GLOBAL       'False'
176	CALL_FUNCTION_1   None
179	POP_JUMP_IF_FALSE '164'
182	LOAD_DEREF        'x'
185	LOAD_GLOBAL       'False'
188	CALL_FUNCTION_1   None
191	LIST_APPEND       None
194	JUMP_BACK         '164'
197	LOAD_GLOBAL       'True'
200	BUILD_LIST_1      None
203	CALL_FUNCTION_2   None
206	POP_TOP           None

207	LOAD_FAST         'self'
210	LOAD_ATTR         'assertEqual'
213	LOAD_CONST        5
216	JUMP_FORWARD      '231'
219	LOAD_FAST         '_checkeval'
222	LOAD_CONST        'check 1'
225	LOAD_CONST        0
228	CALL_FUNCTION_2   None
231_0	COME_FROM         '216'
231	LOAD_CONST        5
234	CALL_FUNCTION_2   None
237	POP_TOP           None

238	LOAD_FAST         'self'
241	LOAD_ATTR         'assertEqual'
244	LOAD_CONST        0
247	POP_JUMP_IF_FALSE '265'
250	LOAD_FAST         '_checkeval'
253	LOAD_CONST        'check 2'
256	LOAD_CONST        0
259	CALL_FUNCTION_2   None
262	JUMP_FORWARD      '268'
265	LOAD_CONST        5
268_0	COME_FROM         '262'
268	LOAD_CONST        5
271	CALL_FUNCTION_2   None
274	POP_TOP           None

275	LOAD_FAST         'self'
278	LOAD_ATTR         'assertEqual'
281	LOAD_CONST        0
284	POP_JUMP_IF_FALSE '299'
287	LOAD_CONST        5
290	JUMP_IF_FALSE_OR_POP '302'
293	LOAD_CONST        6
296_0	COME_FROM         '290'
296	JUMP_FORWARD      '302'
299	LOAD_CONST        1
302_0	COME_FROM         '296'
302	LOAD_CONST        1
305	CALL_FUNCTION_2   None
308	POP_TOP           None

309	LOAD_FAST         'self'
312	LOAD_ATTR         'assertEqual'
315	LOAD_CONST        0
318	POP_JUMP_IF_FALSE '333'
321	LOAD_CONST        5
324	JUMP_IF_FALSE_OR_POP '336'
327	LOAD_CONST        6
330_0	COME_FROM         '324'
330	JUMP_FORWARD      '336'
333	LOAD_CONST        1
336_0	COME_FROM         '330'
336	LOAD_CONST        1
339	CALL_FUNCTION_2   None
342	POP_TOP           None

343	LOAD_FAST         'self'
346	LOAD_ATTR         'assertEqual'
349	LOAD_CONST        5
352	JUMP_IF_FALSE_OR_POP '364'
355	LOAD_CONST        6
358	JUMP_FORWARD      '364'
361	LOAD_CONST        1
364_0	COME_FROM         '352'
364_1	COME_FROM         '358'
364	LOAD_CONST        6
367	CALL_FUNCTION_2   None
370	POP_TOP           None

371	LOAD_FAST         'self'
374	LOAD_ATTR         'assertEqual'
377	LOAD_CONST        0
380	POP_JUMP_IF_FALSE '404'
383	LOAD_CONST        0
386	JUMP_IF_TRUE_OR_POP '407'
389	LOAD_FAST         '_checkeval'
392	LOAD_CONST        'check 3'
395	LOAD_CONST        2
398	CALL_FUNCTION_2   None
401_0	COME_FROM         '386'
401	JUMP_FORWARD      '407'
404	LOAD_CONST        3
407_0	COME_FROM         '401'
407	LOAD_CONST        3
410	CALL_FUNCTION_2   None
413	POP_TOP           None

414	LOAD_FAST         'self'
417	LOAD_ATTR         'assertEqual'
420	LOAD_CONST        1
423	JUMP_IF_TRUE_OR_POP '453'
426	LOAD_FAST         '_checkeval'
429	LOAD_CONST        'check 4'
432	LOAD_CONST        2
435	CALL_FUNCTION_2   None
438	JUMP_FORWARD      '453'
441	LOAD_FAST         '_checkeval'
444	LOAD_CONST        'check 5'
447	LOAD_CONST        3
450	CALL_FUNCTION_2   None
453_0	COME_FROM         '423'
453_1	COME_FROM         '438'
453	LOAD_CONST        1
456	CALL_FUNCTION_2   None
459	POP_TOP           None

460	LOAD_FAST         'self'
463	LOAD_ATTR         'assertEqual'
466	LOAD_CONST        0
469	JUMP_IF_TRUE_OR_POP '490'
472	LOAD_CONST        5
475	JUMP_FORWARD      '490'
478	LOAD_FAST         '_checkeval'
481	LOAD_CONST        'check 6'
484	LOAD_CONST        3
487	CALL_FUNCTION_2   None
490_0	COME_FROM         '469'
490_1	COME_FROM         '475'
490	LOAD_CONST        5
493	CALL_FUNCTION_2   None
496	POP_TOP           None

497	LOAD_FAST         'self'
500	LOAD_ATTR         'assertEqual'
503	LOAD_CONST        5
506	UNARY_NOT         None
507	JUMP_FORWARD      '513'
510	LOAD_CONST        1
513_0	COME_FROM         '507'
513	LOAD_GLOBAL       'False'
516	CALL_FUNCTION_2   None
519	POP_TOP           None

520	LOAD_FAST         'self'
523	LOAD_ATTR         'assertEqual'
526	LOAD_CONST        0
529	POP_JUMP_IF_FALSE '539'
532	LOAD_CONST        5
535	UNARY_NOT         None
536	JUMP_FORWARD      '542'
539	LOAD_CONST        1
542_0	COME_FROM         '536'
542	LOAD_CONST        1
545	CALL_FUNCTION_2   None
548	POP_TOP           None

549	LOAD_FAST         'self'
552	LOAD_ATTR         'assertEqual'
555	LOAD_CONST        7
558	JUMP_FORWARD      '564'
561	LOAD_CONST        2
564_0	COME_FROM         '558'
564	LOAD_CONST        7
567	CALL_FUNCTION_2   None
570	POP_TOP           None

571	LOAD_FAST         'self'
574	LOAD_ATTR         'assertEqual'
577	LOAD_CONST        5
580	JUMP_FORWARD      '586'
583	LOAD_CONST        2
586_0	COME_FROM         '580'
586	LOAD_CONST        5
589	CALL_FUNCTION_2   None
592	POP_TOP           None

593	LOAD_FAST         'self'
596	LOAD_ATTR         'assertEqual'
599	LOAD_CONST        12
602	JUMP_FORWARD      '608'
605	LOAD_CONST        4
608_0	COME_FROM         '602'
608	LOAD_CONST        12
611	CALL_FUNCTION_2   None
614	POP_TOP           None

615	LOAD_FAST         'self'
618	LOAD_ATTR         'assertEqual'
621	LOAD_CONST        6
624	LOAD_CONST        2
627	BINARY_DIVIDE     None
628	JUMP_FORWARD      '634'
631	LOAD_CONST        3
634_0	COME_FROM         '628'
634	LOAD_CONST        3
637	CALL_FUNCTION_2   None
640	POP_TOP           None

641	LOAD_FAST         'self'
644	LOAD_ATTR         'assertEqual'
647	LOAD_CONST        0
650	POP_JUMP_IF_FALSE '665'
653	LOAD_CONST        6
656	LOAD_CONST        4
659	COMPARE_OP        '<'
662	JUMP_FORWARD      '668'
665	LOAD_CONST        2
668_0	COME_FROM         '662'
668	LOAD_CONST        2
671	CALL_FUNCTION_2   None
674	POP_TOP           None

Syntax error at or near `LOAD_FAST' token at offset 219

    def test_paren_evaluation(self):
        self.assertEqual(16 // 2, 8)
        self.assertEqual(2, 2)
        self.assertEqual(2, 2)
        self.assertTrue(False is (2 is 3))
        self.assertFalse((False is 2) is 3)
        self.assertFalse(False is 2 is 3)


def test_main():
    with check_py3k_warnings(('backquote not supported', SyntaxWarning), ('tuple parameter unpacking has been removed', SyntaxWarning), ('parenthesized argument names are invalid', SyntaxWarning), ('classic int division', DeprecationWarning), ('.+ not supported in 3.x', DeprecationWarning)):
        run_unittest(TokenTests, GrammarTests)


if __name__ == '__main__':
    test_main()