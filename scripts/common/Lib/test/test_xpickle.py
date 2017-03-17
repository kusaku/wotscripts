# Embedded file name: scripts/common/Lib/test/test_xpickle.py
import cPickle
import os
import os.path
import pickle
import subprocess
import sys
import types
import unittest
from test import test_support
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'pickletester.py'))
pickletester = types.ModuleType('test.pickletester')
exec compile(open(mod_path).read(), mod_path, 'exec') in pickletester.__dict__
AbstractPickleTests = pickletester.AbstractPickleTests
if pickletester.__name__ in sys.modules:
    raise RuntimeError('Did not expect to find test.pickletester loaded')
sys.modules[pickletester.__name__] = pickletester

class DumpCPickle_LoadPickle(AbstractPickleTests):
    error = KeyError

    def dumps(self, arg, proto = 0, fast = False):
        return cPickle.dumps(arg, proto)

    def loads(self, buf):
        return pickle.loads(buf)


class DumpPickle_LoadCPickle(AbstractPickleTests):
    error = cPickle.BadPickleGet

    def dumps(self, arg, proto = 0, fast = False):
        return pickle.dumps(arg, proto)

    def loads(self, buf):
        return cPickle.loads(buf)


def have_python_version(name):
    """Check whether the given name is a valid Python binary and has
    test.test_support.
    
    This respects your PATH.
    
    Args:
        name: short string name of a Python binary such as "python2.4".
    
    Returns:
        True if the name is valid, False otherwise.
    """
    return os.system(name + " -c 'import test.test_support'") == 0


class AbstractCompatTests(AbstractPickleTests):
    module = None
    python = None
    error = None

    def setUp(self):
        self.assertTrue(self.python)
        self.assertTrue(self.module)
        self.assertTrue(self.error)

    def send_to_worker(self, python, obj, proto):
        """Bounce a pickled object through another version of Python.
        
        This will pickle the object, send it to a child process where it will be
        unpickled, then repickled and sent back to the parent process.
        
        Args:
            python: the name of the Python binary to start.
            obj: object to pickle.
            proto: pickle protocol number to use.
        
        Returns:
            The pickled data received from the child process.
        """
        target = __file__
        if target[-1] in ('c', 'o'):
            target = target[:-1]
        data = self.module.dumps((proto, obj), proto)
        worker = subprocess.Popen([python, target, 'worker'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = worker.communicate(data)
        if worker.returncode != 0:
            raise RuntimeError(stderr)
        return stdout

    def dumps(self, arg, proto = 0, fast = False):
        return self.send_to_worker(self.python, arg, proto)

    def loads(self, input):
        return self.module.loads(input)

    def test_global_ext1(self):
        pass

    def test_global_ext2(self):
        pass

    def test_global_ext4(self):
        pass

    def test_float(self):
        for_bin_protos = [5e-324, 1e-310]
        neg_for_bin_protos = [ -x for x in for_bin_protos ]
        test_values = [0.0,
         7e-308,
         6.626e-34,
         0.1,
         0.5,
         3.14,
         263.44582062374053,
         6.022e+23,
         1e+30]
        test_proto0_values = test_values + [ -x for x in test_values ]
        test_values = test_proto0_values + for_bin_protos + neg_for_bin_protos
        for value in test_proto0_values:
            pickle = self.dumps(value, 0)
            got = self.loads(pickle)
            self.assertEqual(value, got)

        for proto in pickletester.protocols[1:]:
            for value in test_values:
                pickle = self.dumps(value, proto)
                got = self.loads(pickle)
                self.assertEqual(value, got)

    def test_unicode_high_plane(self):
        pass

    def test_dynamic_class(self):
        pass

    if test_support.have_unicode:

        def test_unicode(self):
            endcases = [u'',
             u'<\\u>',
             u'<\\\u1234>',
             u'<\n>',
             u'<\\>']
            for proto in pickletester.protocols:
                for u in endcases:
                    p = self.dumps(u, proto)
                    u2 = self.loads(p)
                    self.assertEqual(u2, u)


def run_compat_test(python_name):
    return test_support.is_resource_enabled('xpickle') and have_python_version(python_name)


if not run_compat_test('python2.4'):

    class CPicklePython24Compat(unittest.TestCase):
        pass


else:

    class CPicklePython24Compat(AbstractCompatTests):
        module = cPickle
        python = 'python2.4'
        error = cPickle.BadPickleGet

        def test_reduce_calls_base(self):
            pass

        def test_reduce_ex_calls_base(self):
            pass


class PicklePython24Compat(CPicklePython24Compat):
    module = pickle
    error = KeyError


if not run_compat_test('python2.5'):

    class CPicklePython25Compat(unittest.TestCase):
        pass


else:

    class CPicklePython25Compat(AbstractCompatTests):
        module = cPickle
        python = 'python2.5'
        error = cPickle.BadPickleGet


class PicklePython25Compat(CPicklePython25Compat):
    module = pickle
    error = KeyError


if not run_compat_test('python2.6'):

    class CPicklePython26Compat(unittest.TestCase):
        pass


else:

    class CPicklePython26Compat(AbstractCompatTests):
        module = cPickle
        python = 'python2.6'
        error = cPickle.BadPickleGet


class PicklePython26Compat(CPicklePython26Compat):
    module = pickle
    error = KeyError


def worker_main(in_stream, out_stream):
    message = cPickle.load(in_stream)
    protocol, obj = message
    cPickle.dump(obj, out_stream, protocol)


def test_main():
    if not test_support.is_resource_enabled('xpickle'):
        print >> sys.stderr, 'test_xpickle -- skipping backwards compat tests.'
        print >> sys.stderr, "Use 'regrtest.py -u xpickle' to run them."
        sys.stderr.flush()
    test_support.run_unittest(DumpCPickle_LoadPickle, DumpPickle_LoadCPickle, CPicklePython24Compat, CPicklePython25Compat, CPicklePython26Compat, PicklePython24Compat, PicklePython25Compat, PicklePython26Compat)


if __name__ == '__main__':
    if 'worker' in sys.argv:
        worker_main(sys.stdin, sys.stdout)
    else:
        test_main()