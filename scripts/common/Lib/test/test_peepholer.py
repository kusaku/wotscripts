# Embedded file name: scripts/common/Lib/test/test_peepholer.py
import dis
import sys
from cStringIO import StringIO
import unittest

def disassemble(func):
    f = StringIO()
    tmp = sys.stdout
    sys.stdout = f
    dis.dis(func)
    sys.stdout = tmp
    result = f.getvalue()
    f.close()
    return result


def dis_single(line):
    return disassemble(compile(line, '', 'single'))


class TestTranforms(unittest.TestCase):

    def test_unot(self):

        def unot(x):
            if not x == 2:
                del x

        asm = disassemble(unot)
        for elem in ('UNARY_NOT', 'POP_JUMP_IF_FALSE'):
            self.assertNotIn(elem, asm)

        self.assertIn('POP_JUMP_IF_TRUE', asm)

    def test_elim_inversion_of_is_or_in(self):
        for line, elem in (('not a is b', '(is not)'),
         ('not a in b', '(not in)'),
         ('not a is not b', '(is)'),
         ('not a not in b', '(in)')):
            asm = dis_single(line)
            self.assertIn(elem, asm)

    def test_none_as_constant(self):

        def f(x):
            None
            return x

        asm = disassemble(f)
        for elem in ('LOAD_GLOBAL',):
            self.assertNotIn(elem, asm)

        for elem in ('LOAD_CONST', '(None)'):
            self.assertIn(elem, asm)

        def f():
            """Adding a docstring made this test fail in Py2.5.0"""
            return None

        self.assertIn('LOAD_CONST', disassemble(f))
        self.assertNotIn('LOAD_GLOBAL', disassemble(f))

    def test_while_one(self):

        def f--- This code section failed: ---

0	SETUP_LOOP        '7'

3	JUMP_ABSOLUTE     '3'
6	POP_BLOCK         None
7_0	COME_FROM         '0'

7	LOAD_GLOBAL       'list'
10	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 6

        asm = disassemble(f)
        for elem in ('LOAD_CONST', 'POP_JUMP_IF_FALSE'):
            self.assertNotIn(elem, asm)

        for elem in ('JUMP_ABSOLUTE',):
            self.assertIn(elem, asm)

    def test_pack_unpack(self):
        for line, elem in (('a, = a,', 'LOAD_CONST'), ('a, b = a, b', 'ROT_TWO'), ('a, b, c = a, b, c', 'ROT_THREE')):
            asm = dis_single(line)
            self.assertIn(elem, asm)
            self.assertNotIn('BUILD_TUPLE', asm)
            self.assertNotIn('UNPACK_TUPLE', asm)

    def test_folding_of_tuples_of_constants(self):
        for line, elem in (('a = 1,2,3', '((1, 2, 3))'),
         ('("a","b","c")', "(('a', 'b', 'c'))"),
         ('a,b,c = 1,2,3', '((1, 2, 3))'),
         ('(None, 1, None)', '((None, 1, None))'),
         ('((1, 2), 3, 4)', '(((1, 2), 3, 4))')):
            asm = dis_single(line)
            self.assertIn(elem, asm)
            self.assertNotIn('BUILD_TUPLE', asm)

        def crater():
            (~[0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              0,
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9],)

    def test_folding_of_binops_on_constants(self):
        for line, elem in (('a = 2+3+4', '(9)'),
         ('"@"*4', "('@@@@')"),
         ('a="abc" + "def"', "('abcdef')"),
         ('a = 3**4', '(81)'),
         ('a = 3*4', '(12)'),
         ('a = 13//4', '(3)'),
         ('a = 14%4', '(2)'),
         ('a = 2+3', '(5)'),
         ('a = 13-4', '(9)'),
         ('a = (12,13)[1]', '(13)'),
         ('a = 13 << 2', '(52)'),
         ('a = 13 >> 2', '(3)'),
         ('a = 13 & 7', '(5)'),
         ('a = 13 ^ 7', '(10)'),
         ('a = 13 | 7', '(15)')):
            asm = dis_single(line)
            self.assertIn(elem, asm, asm)
            self.assertNotIn('BINARY_', asm)

        asm = dis_single('a=2+"b"')
        self.assertIn('(2)', asm)
        self.assertIn("('b')", asm)
        asm = dis_single('a="x"*1000')
        self.assertIn('(1000)', asm)

    def test_binary_subscr_on_unicode(self):
        asm = dis_single('u"foo"[0]')
        self.assertIn("(u'f')", asm)
        self.assertNotIn('BINARY_SUBSCR', asm)
        asm = dis_single('u"\\u0061\\uffff"[1]')
        self.assertIn("(u'\\uffff')", asm)
        self.assertNotIn('BINARY_SUBSCR', asm)
        asm = dis_single('u"fuu"[10]')
        self.assertIn('BINARY_SUBSCR', asm)
        asm = dis_single('u"\\U00012345"[0]')
        self.assertIn('BINARY_SUBSCR', asm)

    def test_folding_of_unaryops_on_constants(self):
        for line, elem in (('`1`', "('1')"), ('-0.5', '(-0.5)'), ('~-2', '(1)')):
            asm = dis_single(line)
            self.assertIn(elem, asm, asm)
            self.assertNotIn('UNARY_', asm)

        for line, elem in (('-"abc"', "('abc')"), ('~"abc"', "('abc')")):
            asm = dis_single(line)
            self.assertIn(elem, asm, asm)
            self.assertIn('UNARY_', asm)

    def test_elim_extra_return(self):

        def f(x):
            return x

        asm = disassemble(f)
        self.assertNotIn('LOAD_CONST', asm)
        self.assertNotIn('(None)', asm)
        self.assertEqual(asm.split().count('RETURN_VALUE'), 1)

    def test_elim_jump_to_return(self):

        def f(cond, true_value, false_value):
            if cond:
                return true_value
            return false_value

        asm = disassemble(f)
        self.assertNotIn('JUMP_FORWARD', asm)
        self.assertNotIn('JUMP_ABSOLUTE', asm)
        self.assertEqual(asm.split().count('RETURN_VALUE'), 2)

    def test_elim_jump_after_return1(self):

        def f--- This code section failed: ---

0	LOAD_FAST         'cond1'
3	POP_JUMP_IF_FALSE '10'
6	LOAD_CONST        1
9	RETURN_END_IF     None

10	LOAD_FAST         'cond2'
13	POP_JUMP_IF_FALSE '20'
16	LOAD_CONST        2
19	RETURN_END_IF     None

20	SETUP_LOOP        '28'

23	LOAD_CONST        3
26	RETURN_VALUE      None
27	POP_BLOCK         None
28_0	COME_FROM         '20'

28	SETUP_LOOP        '46'

31	LOAD_FAST         'cond1'
34	POP_JUMP_IF_FALSE '41'
37	LOAD_CONST        4
40	RETURN_END_IF     None

41	LOAD_CONST        5
44	RETURN_VALUE      None
45	POP_BLOCK         None
46_0	COME_FROM         '28'

46	LOAD_CONST        6
49	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 27

        asm = disassemble(f)
        self.assertNotIn('JUMP_FORWARD', asm)
        self.assertNotIn('JUMP_ABSOLUTE', asm)
        self.assertEqual(asm.split().count('RETURN_VALUE'), 6)

    def test_elim_jump_after_return2(self):

        def f--- This code section failed: ---

0	SETUP_LOOP        '17'

3	LOAD_FAST         'cond1'
6	POP_JUMP_IF_FALSE '3'
9	LOAD_CONST        4
12	RETURN_END_IF     None
13	JUMP_BACK         '3'
16	POP_BLOCK         None
17_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 16

        asm = disassemble(f)
        self.assertNotIn('JUMP_FORWARD', asm)
        self.assertEqual(asm.split().count('JUMP_ABSOLUTE'), 1)
        self.assertEqual(asm.split().count('RETURN_VALUE'), 2)


def test_main(verbose = None):
    import sys
    from test import test_support
    test_classes = (TestTranforms,)
    with test_support.check_py3k_warnings(('backquote not supported', SyntaxWarning)):
        test_support.run_unittest(*test_classes)
        if verbose and hasattr(sys, 'gettotalrefcount'):
            import gc
            counts = [None] * 5
            for i in xrange(len(counts)):
                test_support.run_unittest(*test_classes)
                gc.collect()
                counts[i] = sys.gettotalrefcount()

            print counts
    return


if __name__ == '__main__':
    test_main(verbose=True)