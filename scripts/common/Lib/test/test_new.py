# Embedded file name: scripts/common/Lib/test/test_new.py
import unittest
from test import test_support
import sys
new = test_support.import_module('new', deprecated=True)

class NewTest(unittest.TestCase):

    def test_spam(self):

        class Eggs:

            def get_yolks(self):
                return self.yolks

        m = new.module('Spam')
        m.Eggs = Eggs
        sys.modules['Spam'] = m
        import Spam

        def get_more_yolks(self):
            return self.yolks + 3

        C = new.classobj('Spam', (Spam.Eggs,), {'get_more_yolks': get_more_yolks})
        c = new.instance(C, {'yolks': 3})
        o = new.instance(C)
        self.assertEqual(o.__dict__, {}, 'new __dict__ should be empty')
        del o
        o = new.instance(C, None)
        self.assertEqual(o.__dict__, {}, 'new __dict__ should be empty')
        del o

        def break_yolks(self):
            self.yolks = self.yolks - 2

        im = new.instancemethod(break_yolks, c, C)
        self.assertEqual(c.get_yolks(), 3, 'Broken call of hand-crafted class instance')
        self.assertEqual(c.get_more_yolks(), 6, 'Broken call of hand-crafted class instance')
        im()
        self.assertEqual(c.get_yolks(), 1, 'Broken call of hand-crafted instance method')
        self.assertEqual(c.get_more_yolks(), 4, 'Broken call of hand-crafted instance method')
        im = new.instancemethod(break_yolks, c)
        im()
        self.assertEqual(c.get_yolks(), -1)
        self.assertRaises(TypeError, new.instancemethod, break_yolks, None)
        self.assertRaises(TypeError, new.instancemethod, break_yolks, c, kw=1)
        return

    def test_scope(self):
        codestr = '\n        global c\n        a = 1\n        b = 2\n        c = a + b\n        '
        codestr = '\n'.join((l.strip() for l in codestr.splitlines()))
        ccode = compile(codestr, '<string>', 'exec')
        import __builtin__
        g = {'c': 0,
         '__builtins__': __builtin__}
        func = new.function(ccode, g)
        func()
        self.assertEqual(g['c'], 3, 'Could not create a proper function object')

    def test_function(self):

        def f(x):

            def g(y):
                return x + y

            return g

        g = f(4)
        new.function(f.func_code, {}, 'blah')
        g2 = new.function(g.func_code, {}, 'blah', (2,), g.func_closure)
        self.assertEqual(g2(), 6)
        g3 = new.function(g.func_code, {}, 'blah', None, g.func_closure)
        self.assertEqual(g3(5), 9)

        def test_closure(func, closure, exc):
            self.assertRaises(exc, new.function, func.func_code, {}, '', None, closure)
            return

        test_closure(g, None, TypeError)
        test_closure(g, (1,), TypeError)
        test_closure(g, (1, 1), ValueError)
        test_closure(f, g.func_closure, ValueError)
        return

    if hasattr(new, 'code'):

        def test_code(self):

            def f(a):
                pass

            c = f.func_code
            argcount = c.co_argcount
            nlocals = c.co_nlocals
            stacksize = c.co_stacksize
            flags = c.co_flags
            codestring = c.co_code
            constants = c.co_consts
            names = c.co_names
            varnames = c.co_varnames
            filename = c.co_filename
            name = c.co_name
            firstlineno = c.co_firstlineno
            lnotab = c.co_lnotab
            freevars = c.co_freevars
            cellvars = c.co_cellvars
            d = new.code(argcount, nlocals, stacksize, flags, codestring, constants, names, varnames, filename, name, firstlineno, lnotab, freevars, cellvars)
            d = new.code(argcount, nlocals, stacksize, flags, codestring, constants, names, varnames, filename, name, firstlineno, lnotab)
            self.assertRaises(ValueError, new.code, -argcount, nlocals, stacksize, flags, codestring, constants, names, varnames, filename, name, firstlineno, lnotab)
            self.assertRaises(ValueError, new.code, argcount, -nlocals, stacksize, flags, codestring, constants, names, varnames, filename, name, firstlineno, lnotab)
            self.assertRaises(TypeError, new.code, argcount, nlocals, stacksize, flags, codestring, constants, (5,), varnames, filename, name, firstlineno, lnotab)

            class S(str):
                pass

            t = (S('ab'),)
            d = new.code(argcount, nlocals, stacksize, flags, codestring, constants, t, varnames, filename, name, firstlineno, lnotab)
            self.assertTrue(type(t[0]) is S, 'eek, tuple changed under us!')


def test_main():
    test_support.run_unittest(NewTest)


if __name__ == '__main__':
    test_main()