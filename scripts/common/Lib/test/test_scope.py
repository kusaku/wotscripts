# Embedded file name: scripts/common/Lib/test/test_scope.py
import unittest
from test.test_support import check_syntax_error, check_py3k_warnings, check_warnings, run_unittest

class ScopeTests(unittest.TestCase):

    def testSimpleNesting(self):

        def make_adder(x):

            def adder(y):
                return x + y

            return adder

        inc = make_adder(1)
        plus10 = make_adder(10)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(-2), 8)

    def testExtraNesting(self):

        def make_adder2(x):

            def extra():

                def adder(y):
                    return x + y

                return adder

            return extra()

        inc = make_adder2(1)
        plus10 = make_adder2(10)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(-2), 8)

    def testSimpleAndRebinding(self):

        def make_adder3(x):

            def adder(y):
                return x + y

            x = x + 1
            return adder

        inc = make_adder3(0)
        plus10 = make_adder3(9)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(-2), 8)

    def testNestingGlobalNoFree(self):

        def make_adder4():

            def nest():

                def nest():

                    def adder(y):
                        return global_x + y

                    return adder

                return nest()

            return nest()

        global_x = 1
        adder = make_adder4()
        self.assertEqual(adder(1), 2)
        global_x = 10
        self.assertEqual(adder(-2), 8)

    def testNestingThroughClass(self):

        def make_adder5(x):

            class Adder:

                def __call__(self, y):
                    return x + y

            return Adder()

        inc = make_adder5(1)
        plus10 = make_adder5(10)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(-2), 8)

    def testNestingPlusFreeRefToGlobal(self):

        def make_adder6(x):
            global global_nest_x

            def adder(y):
                return global_nest_x + y

            global_nest_x = x
            return adder

        inc = make_adder6(1)
        plus10 = make_adder6(10)
        self.assertEqual(inc(1), 11)
        self.assertEqual(plus10(-2), 8)

    def testNearestEnclosingScope(self):

        def f(x):

            def g(y):
                x = 42

                def h(z):
                    return x + z

                return h

            return g(2)

        test_func = f(10)
        self.assertEqual(test_func(5), 47)

    def testMixedFreevarsAndCellvars(self):

        def identity(x):
            return x

        def f(x, y, z):

            def g(a, b, c):
                a = a + x

                def h():
                    return identity(z * (b + y))

                y = c + z
                return h

            return g

        g = f(1, 2, 3)
        h = g(2, 4, 6)
        self.assertEqual(h(), 39)

    def testFreeVarInMethod(self):

        def test():
            method_and_var = 'var'

            class Test:

                def method_and_var(self):
                    return 'method'

                def test(self):
                    return method_and_var

                def actual_global(self):
                    return str('global')

                def str(self):
                    return str(self)

            return Test()

        t = test()
        self.assertEqual(t.test(), 'var')
        self.assertEqual(t.method_and_var(), 'method')
        self.assertEqual(t.actual_global(), 'global')
        method_and_var = 'var'

        class Test:

            def method_and_var(self):
                return 'method'

            def test(self):
                return method_and_var

            def actual_global(self):
                return str('global')

            def str(self):
                return str(self)

        t = Test()
        self.assertEqual(t.test(), 'var')
        self.assertEqual(t.method_and_var(), 'method')
        self.assertEqual(t.actual_global(), 'global')

    def testRecursion(self):

        def f(x):

            def fact(n):
                if n == 0:
                    return 1
                else:
                    return n * fact(n - 1)

            if x >= 0:
                return fact(x)
            raise ValueError, 'x must be >= 0'

        self.assertEqual(f(6), 720)

    def testUnoptimizedNamespaces(self):
        check_syntax_error(self, 'def unoptimized_clash1(strip):\n    def f(s):\n        from string import *\n        return strip(s) # ambiguity: free or local\n    return f\n')
        check_syntax_error(self, 'def unoptimized_clash2():\n    from string import *\n    def f(s):\n        return strip(s) # ambiguity: global or local\n    return f\n')
        check_syntax_error(self, 'def unoptimized_clash2():\n    from string import *\n    def g():\n        def f(s):\n            return strip(s) # ambiguity: global or local\n        return f\n')
        check_syntax_error(self, 'def error(y):\n    exec "a = 1"\n    def f(x):\n        return x + y\n    return f\n')
        check_syntax_error(self, "def f(x):\n    def g():\n        return x\n    del x # can't del name\n")
        check_syntax_error(self, 'def f():\n    def g():\n        from string import *\n        return strip # global or local?\n')
        exec '\ndef noproblem1():\n    from string import *\n    f = lambda x:x\n\ndef noproblem2():\n    from string import *\n    def f(x):\n        return x + 1\n\ndef noproblem3():\n    from string import *\n    def f(x):\n        global y\n        y = x\n'

    def testLambdas(self):
        f1 = lambda x: lambda y: x + y
        inc = f1(1)
        plus10 = f1(10)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(5), 15)
        f2 = lambda x: (lambda : lambda y: x + y)()
        inc = f2(1)
        plus10 = f2(10)
        self.assertEqual(inc(1), 2)
        self.assertEqual(plus10(5), 15)
        f3 = lambda x: lambda y: global_x + y
        global_x = 1
        inc = f3(None)
        self.assertEqual(inc(2), 3)
        f8 = lambda x, y, z: lambda a, b, c: lambda : z * (b + y)
        g = f8(1, 2, 3)
        h = g(2, 4, 6)
        self.assertEqual(h(), 18)
        return

    def testUnboundLocal(self):

        def errorInOuter():
            print y

            def inner():
                return y

            y = 1

        def errorInInner():

            def inner():
                return y

            inner()
            y = 1

        self.assertRaises(UnboundLocalError, errorInOuter)
        self.assertRaises(NameError, errorInInner)
        exec "\nglobal_x = 1\ndef f():\n    global_x += 1\ntry:\n    f()\nexcept UnboundLocalError:\n    pass\nelse:\n    fail('scope of global_x not correctly determined')\n" in {'fail': self.fail}

    def testComplexDefinitions(self):

        def makeReturner(*lst):

            def returner():
                return lst

            return returner

        self.assertEqual(makeReturner(1, 2, 3)(), (1, 2, 3))

        def makeReturner2(**kwargs):

            def returner():
                return kwargs

            return returner

        self.assertEqual(makeReturner2(a=11)()['a'], 11)
        with check_py3k_warnings(('tuple parameter unpacking has been removed', SyntaxWarning)):
            exec 'def makeAddPair((a, b)):\n    def addPair((c, d)):\n        return (a + c, b + d)\n    return addPair\n' in locals()
        self.assertEqual(makeAddPair((1, 2))((100, 200)), (101, 202))

    def testScopeOfGlobalStmt(self):
        exec '# I\nx = 7\ndef f():\n    x = 1\n    def g():\n        global x\n        def i():\n            def h():\n                return x\n            return h()\n        return i()\n    return g()\nself.assertEqual(f(), 7)\nself.assertEqual(x, 7)\n\n# II\nx = 7\ndef f():\n    x = 1\n    def g():\n        x = 2\n        def i():\n            def h():\n                return x\n            return h()\n        return i()\n    return g()\nself.assertEqual(f(), 2)\nself.assertEqual(x, 7)\n\n# III\nx = 7\ndef f():\n    x = 1\n    def g():\n        global x\n        x = 2\n        def i():\n            def h():\n                return x\n            return h()\n        return i()\n    return g()\nself.assertEqual(f(), 2)\nself.assertEqual(x, 2)\n\n# IV\nx = 7\ndef f():\n    x = 3\n    def g():\n        global x\n        x = 2\n        def i():\n            def h():\n                return x\n            return h()\n        return i()\n    return g()\nself.assertEqual(f(), 2)\nself.assertEqual(x, 2)\n\n# XXX what about global statements in class blocks?\n# do they affect methods?\n\nx = 12\nclass Global:\n    global x\n    x = 13\n    def set(self, val):\n        x = val\n    def get(self):\n        return x\n\ng = Global()\nself.assertEqual(g.get(), 13)\ng.set(15)\nself.assertEqual(g.get(), 13)\n'

    def testLeaks(self):

        class Foo:
            count = 0

            def __init__(self):
                Foo.count += 1

            def __del__(self):
                Foo.count -= 1

        def f1():
            x = Foo()

            def f2():
                return x

            f2()

        for i in range(100):
            f1()

        self.assertEqual(Foo.count, 0)

    def testClassAndGlobal(self):
        exec "def test(x):\n    class Foo:\n        global x\n        def __call__(self, y):\n            return x + y\n    return Foo()\n\nx = 0\nself.assertEqual(test(6)(2), 8)\nx = -1\nself.assertEqual(test(3)(2), 5)\n\nlooked_up_by_load_name = False\nclass X:\n    # Implicit globals inside classes are be looked up by LOAD_NAME, not\n    # LOAD_GLOBAL.\n    locals()['looked_up_by_load_name'] = True\n    passed = looked_up_by_load_name\n\nself.assertTrue(X.passed)\n"

    def testLocalsFunction(self):

        def f(x):

            def g(y):

                def h(z):
                    return y + z

                w = x + y
                y += 3
                return locals()

            return g

        d = f(2)(4)
        self.assertIn('h', d)
        del d['h']
        self.assertEqual(d, {'x': 2,
         'y': 7,
         'w': 6})

    def testLocalsClass(self):

        def f(x):

            class C:
                x = 12

                def m(self):
                    return x

                locals()

            return C

        self.assertEqual(f(1).x, 12)

        def f(x):

            class C:
                y = x

                def m(self):
                    return x

                z = list(locals())

            return C

        varnames = f(1).z
        self.assertNotIn('x', varnames)
        self.assertIn('y', varnames)

    def testLocalsClass_WithTrace(self):
        import sys
        sys.settrace(lambda a, b, c: None)
        try:
            x = 12

            class C:

                def f(self):
                    return x

            self.assertEqual(x, 12)
        finally:
            sys.settrace(None)

        return

    def testBoundAndFree(self):

        def f(x):

            class C:

                def m(self):
                    return x

                a = x

            return C

        inst = f(3)()
        self.assertEqual(inst.a, inst.m())

    def testInteractionWithTraceFunc(self):
        import sys

        def tracer(a, b, c):
            return tracer

        def adaptgetter(name, klass, getter):
            kind, des = getter
            if kind == 1:
                if des == '':
                    des = '_%s__%s' % (klass.__name__, name)
                return lambda obj: getattr(obj, des)

        class TestClass:
            pass

        sys.settrace(tracer)
        adaptgetter('foo', TestClass, (1, ''))
        sys.settrace(None)
        self.assertRaises(TypeError, sys.settrace)
        return

    def testEvalExecFreeVars(self):

        def f(x):
            return lambda : x + 1

        g = f(3)
        self.assertRaises(TypeError, eval, g.func_code)
        try:
            exec g.func_code in {}
        except TypeError:
            pass
        else:
            self.fail('exec should have failed, because code contained free vars')

    def testListCompLocalVars(self):
        try:
            print bad
        except NameError:
            pass
        else:
            print 'bad should not be defined'

        def x():
            [ bad for s in 'a b' for bad in s.split() ]

        x()
        try:
            print bad
        except NameError:
            pass

    def testEvalFreeVars(self):

        def f(x):

            def g():
                x
                eval('x + 1')

            return g

        f(4)()

    def testFreeingCell(self):

        class Special:

            def __del__(self):
                nestedcell_get()

        def f():
            global nestedcell_get

            def nestedcell_get():
                return c

            c = (Special(),)
            c = 2

        f()

    def testGlobalInParallelNestedFunctions(self):
        CODE = 'def f():\n    y = 1\n    def g():\n        global y\n        return y\n    def h():\n        return y + 1\n    return g, h\n\ny = 9\ng, h = f()\nresult9 = g()\nresult2 = h()\n'
        local_ns = {}
        global_ns = {}
        exec CODE in local_ns, global_ns
        self.assertEqual(2, global_ns['result2'])
        self.assertEqual(9, global_ns['result9'])

    def testTopIsNotSignificant(self):

        def top(a):
            pass

        def b():
            pass


def test_main():
    with check_warnings(('import \\* only allowed at module level', SyntaxWarning)):
        run_unittest(ScopeTests)


if __name__ == '__main__':
    test_main()