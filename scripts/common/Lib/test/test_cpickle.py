# Embedded file name: scripts/common/Lib/test/test_cpickle.py
import cPickle, unittest
from cStringIO import StringIO
from test.pickletester import AbstractPickleTests, AbstractPickleModuleTests
from test.pickletester import AbstractPicklerUnpicklerObjectTests
from test import test_support

class cPickleTests(AbstractPickleTests, AbstractPickleModuleTests):

    def setUp(self):
        self.dumps = cPickle.dumps
        self.loads = cPickle.loads

    error = cPickle.BadPickleGet
    module = cPickle


class cPicklePicklerTests(AbstractPickleTests):

    def dumps(self, arg, proto = 0):
        f = StringIO()
        p = cPickle.Pickler(f, proto)
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, buf):
        f = StringIO(buf)
        p = cPickle.Unpickler(f)
        return p.load()

    error = cPickle.BadPickleGet


class cPickleListPicklerTests(AbstractPickleTests):

    def dumps(self, arg, proto = 0):
        p = cPickle.Pickler(proto)
        p.dump(arg)
        return p.getvalue()

    def loads(self, *args):
        f = StringIO(args[0])
        p = cPickle.Unpickler(f)
        return p.load()

    error = cPickle.BadPickleGet


class cPickleFastPicklerTests(AbstractPickleTests):

    def dumps(self, arg, proto = 0):
        f = StringIO()
        p = cPickle.Pickler(f, proto)
        p.fast = 1
        p.dump(arg)
        f.seek(0)
        return f.read()

    def loads(self, *args):
        f = StringIO(args[0])
        p = cPickle.Unpickler(f)
        return p.load()

    error = cPickle.BadPickleGet

    def test_recursive_list(self):
        self.assertRaises(ValueError, AbstractPickleTests.test_recursive_list, self)

    def test_recursive_tuple(self):
        self.assertRaises(ValueError, AbstractPickleTests.test_recursive_tuple, self)

    def test_recursive_inst(self):
        self.assertRaises(ValueError, AbstractPickleTests.test_recursive_inst, self)

    def test_recursive_dict(self):
        self.assertRaises(ValueError, AbstractPickleTests.test_recursive_dict, self)

    def test_recursive_multi(self):
        self.assertRaises(ValueError, AbstractPickleTests.test_recursive_multi, self)

    def test_nonrecursive_deep(self):
        a = []
        for i in range(60):
            a = [a]

        b = self.loads(self.dumps(a))
        self.assertEqual(a, b)


class cPicklePicklerUnpicklerObjectTests(AbstractPicklerUnpicklerObjectTests):
    pickler_class = cPickle.Pickler
    unpickler_class = cPickle.Unpickler


class Node(object):
    pass


class cPickleDeepRecursive(unittest.TestCase):

    def test_issue2702(self):
        nodes = [ Node() for i in range(500) ]
        for n in nodes:
            n.connections = list(nodes)
            n.connections.remove(n)

        self.assertRaises((AttributeError, RuntimeError), cPickle.dumps, n)

    def test_issue3179(self):
        res = []
        for x in range(1, 2000):
            res.append(dict(doc=x, similar=[]))

        cPickle.dumps(res)


def test_main():
    test_support.run_unittest(cPickleTests, cPicklePicklerTests, cPickleListPicklerTests, cPickleFastPicklerTests, cPickleDeepRecursive, cPicklePicklerUnpicklerObjectTests)


if __name__ == '__main__':
    test_main()