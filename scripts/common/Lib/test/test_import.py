# Embedded file name: scripts/common/Lib/test/test_import.py
import errno
import imp
import marshal
import os
import py_compile
import random
import stat
import sys
import unittest
from test.test_support import unlink, TESTFN, unload, run_unittest, rmtree, is_jython, check_warnings, EnvironmentVarGuard
import textwrap
from test import script_helper

def remove_files(name):
    for f in (name + os.extsep + 'py',
     name + os.extsep + 'pyc',
     name + os.extsep + 'pyo',
     name + os.extsep + 'pyw',
     name + '$py.class'):
        unlink(f)


class ImportTests(unittest.TestCase):

    def tearDown(self):
        unload(TESTFN)

    setUp = tearDown

    def test_case_sensitivity(self):
        try:
            import RAnDoM
        except ImportError:
            pass
        else:
            self.fail('import of RAnDoM should have failed (case mismatch)')

    def test_double_const(self):
        from test import double_const

    def test_import(self):

        def test_with_extension(ext):
            source = TESTFN + ext
            pyo = TESTFN + os.extsep + 'pyo'
            if is_jython:
                pyc = TESTFN + '$py.class'
            else:
                pyc = TESTFN + os.extsep + 'pyc'
            with open(source, 'w') as f:
                print >> f, ("# This tests Python's ability to import a", ext, 'file.')
                a = random.randrange(1000)
                b = random.randrange(1000)
                print >> f, 'a =', a
                print >> f, 'b =', b
            try:
                mod = __import__(TESTFN)
            except ImportError as err:
                self.fail('import from %s failed: %s' % (ext, err))
            else:
                self.assertEqual(mod.a, a, 'module loaded (%s) but contents invalid' % mod)
                self.assertEqual(mod.b, b, 'module loaded (%s) but contents invalid' % mod)
            finally:
                unlink(source)

            try:
                imp.reload(mod)
            except ImportError as err:
                self.fail('import from .pyc/.pyo failed: %s' % err)
            finally:
                unlink(pyc)
                unlink(pyo)
                unload(TESTFN)

        sys.path.insert(0, os.curdir)
        try:
            test_with_extension(os.extsep + 'py')
            if sys.platform.startswith('win'):
                for ext in ['.PY',
                 '.Py',
                 '.pY',
                 '.pyw',
                 '.PYW',
                 '.pYw']:
                    test_with_extension(ext)

        finally:
            del sys.path[0]

    @unittest.skipUnless(os.name == 'posix', 'test meaningful only on posix systems')
    def test_execute_bit_not_copied(self):
        oldmask = os.umask(18)
        sys.path.insert(0, os.curdir)
        try:
            fname = TESTFN + os.extsep + 'py'
            f = open(fname, 'w').close()
            os.chmod(fname, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            __import__(TESTFN)
            fn = fname + 'c'
            if not os.path.exists(fn):
                fn = fname + 'o'
                if not os.path.exists(fn):
                    self.fail('__import__ did not result in creation of either a .pyc or .pyo file')
            s = os.stat(fn)
            self.assertEqual(stat.S_IMODE(s.st_mode), stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        finally:
            os.umask(oldmask)
            remove_files(TESTFN)
            unload(TESTFN)
            del sys.path[0]

    def test_imp_module(self):
        orig_path = os.path
        orig_getenv = os.getenv
        with EnvironmentVarGuard():
            x = imp.find_module('os')
            new_os = imp.load_module('os', *x)
            self.assertIs(os, new_os)
            self.assertIs(orig_path, new_os.path)
            self.assertIsNot(orig_getenv, new_os.getenv)

    def test_module_with_large_stack(self, module = 'longlist'):
        filename = module + os.extsep + 'py'
        with open(filename, 'w+') as f:
            f.write('d = [\n')
            for i in range(65000):
                f.write('"",\n')

            f.write(']')
        with open(filename, 'r') as f:
            py_compile.compile(filename)
        unlink(filename)
        sys.path.append('')
        exec 'import ' + module
        del sys.path[-1]
        unlink(filename + 'c')
        unlink(filename + 'o')

    def test_failing_import_sticks(self):
        source = TESTFN + os.extsep + 'py'
        with open(source, 'w') as f:
            print >> f, 'a = 1 // 0'
        sys.path.insert(0, os.curdir)
        try:
            for i in [1, 2, 3]:
                self.assertRaises(ZeroDivisionError, __import__, TESTFN)
                self.assertNotIn(TESTFN, sys.modules, 'damaged module in sys.modules on %i try' % i)

        finally:
            del sys.path[0]
            remove_files(TESTFN)

    def test_failing_reload(self):
        source = TESTFN + os.extsep + 'py'
        with open(source, 'w') as f:
            print >> f, 'a = 1'
            print >> f, 'b = 2'
        sys.path.insert(0, os.curdir)
        try:
            mod = __import__(TESTFN)
            self.assertIn(TESTFN, sys.modules)
            self.assertEqual(mod.a, 1, 'module has wrong attribute values')
            self.assertEqual(mod.b, 2, 'module has wrong attribute values')
            remove_files(TESTFN)
            with open(source, 'w') as f:
                print >> f, 'a = 10'
                print >> f, 'b = 20//0'
            self.assertRaises(ZeroDivisionError, imp.reload, mod)
            mod = sys.modules.get(TESTFN)
            self.assertIsNot(mod, None, 'expected module to be in sys.modules')
            self.assertEqual(mod.a, 10, 'module has wrong attribute values')
            self.assertEqual(mod.b, 2, 'module has wrong attribute values')
        finally:
            del sys.path[0]
            remove_files(TESTFN)
            unload(TESTFN)

        return

    def test_infinite_reload(self):
        sys.path.insert(0, os.path.dirname(__file__))
        try:
            import infinite_reload
        finally:
            del sys.path[0]

    def test_import_name_binding(self):
        import test as x
        import test.test_support
        self.assertIs(x, test, x.__name__)
        self.assertTrue(hasattr(test.test_support, '__file__'))
        import test.test_support as y
        self.assertIs(y, test.test_support, y.__name__)

    def test_import_initless_directory_warning(self):
        with check_warnings(('', ImportWarning)):
            self.assertRaises(ImportError, __import__, 'site-packages')

    def test_import_by_filename(self):
        path = os.path.abspath(TESTFN)
        with self.assertRaises(ImportError) as c:
            __import__(path)
        self.assertEqual('Import by filename is not supported.', c.exception.args[0])

    def test_import_in_del_does_not_crash(self):
        testfn = script_helper.make_script('', TESTFN, textwrap.dedent('            import sys\n            class C:\n               def __del__(self):\n                  import imp\n            sys.argv.insert(0, C())\n            '))
        try:
            script_helper.assert_python_ok(testfn)
        finally:
            unlink(testfn)

    def test_bug7732(self):
        source = TESTFN + '.py'
        os.mkdir(source)
        try:
            self.assertRaises((ImportError, IOError), imp.find_module, TESTFN, ['.'])
        finally:
            os.rmdir(source)

    def test_timestamp_overflow(self):
        sys.path.insert(0, os.curdir)
        try:
            source = TESTFN + '.py'
            compiled = source + ('c' if __debug__ else 'o')
            with open(source, 'w') as f:
                pass
            try:
                os.utime(source, (8589934587L, 8589934587L))
            except OverflowError:
                self.skipTest('cannot set modification time to large integer')
            except OSError as e:
                if e.errno != getattr(errno, 'EOVERFLOW', None):
                    raise
                self.skipTest('cannot set modification time to large integer ({})'.format(e))

            __import__(TESTFN)
            os.stat(compiled)
        finally:
            del sys.path[0]
            remove_files(TESTFN)

        return


class PycRewritingTests(unittest.TestCase):
    module_name = 'unlikely_module_name'
    module_source = '\nimport sys\ncode_filename = sys._getframe().f_code.co_filename\nmodule_filename = __file__\nconstant = 1\ndef func():\n    pass\nfunc_filename = func.func_code.co_filename\n'
    dir_name = os.path.abspath(TESTFN)
    file_name = os.path.join(dir_name, module_name) + os.extsep + 'py'
    compiled_name = file_name + ('c' if __debug__ else 'o')

    def setUp(self):
        self.sys_path = sys.path[:]
        self.orig_module = sys.modules.pop(self.module_name, None)
        os.mkdir(self.dir_name)
        with open(self.file_name, 'w') as f:
            f.write(self.module_source)
        sys.path.insert(0, self.dir_name)
        return

    def tearDown(self):
        sys.path[:] = self.sys_path
        if self.orig_module is not None:
            sys.modules[self.module_name] = self.orig_module
        else:
            unload(self.module_name)
        unlink(self.file_name)
        unlink(self.compiled_name)
        rmtree(self.dir_name)
        return

    def import_module(self):
        ns = globals()
        __import__(self.module_name, ns, ns)
        return sys.modules[self.module_name]

    def test_basics(self):
        mod = self.import_module()
        self.assertEqual(mod.module_filename, self.file_name)
        self.assertEqual(mod.code_filename, self.file_name)
        self.assertEqual(mod.func_filename, self.file_name)
        del sys.modules[self.module_name]
        mod = self.import_module()
        self.assertEqual(mod.module_filename, self.compiled_name)
        self.assertEqual(mod.code_filename, self.file_name)
        self.assertEqual(mod.func_filename, self.file_name)

    def test_incorrect_code_name(self):
        py_compile.compile(self.file_name, dfile='another_module.py')
        mod = self.import_module()
        self.assertEqual(mod.module_filename, self.compiled_name)
        self.assertEqual(mod.code_filename, self.file_name)
        self.assertEqual(mod.func_filename, self.file_name)

    def test_module_without_source(self):
        target = 'another_module.py'
        py_compile.compile(self.file_name, dfile=target)
        os.remove(self.file_name)
        mod = self.import_module()
        self.assertEqual(mod.module_filename, self.compiled_name)
        self.assertEqual(mod.code_filename, target)
        self.assertEqual(mod.func_filename, target)

    def test_foreign_code(self):
        py_compile.compile(self.file_name)
        with open(self.compiled_name, 'rb') as f:
            header = f.read(8)
            code = marshal.load(f)
        constants = list(code.co_consts)
        foreign_code = test_main.func_code
        pos = constants.index(1)
        constants[pos] = foreign_code
        code = type(code)(code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags, code.co_code, tuple(constants), code.co_names, code.co_varnames, code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab, code.co_freevars, code.co_cellvars)
        with open(self.compiled_name, 'wb') as f:
            f.write(header)
            marshal.dump(code, f)
        mod = self.import_module()
        self.assertEqual(mod.constant.co_filename, foreign_code.co_filename)


class PathsTests(unittest.TestCase):
    path = TESTFN

    def setUp(self):
        os.mkdir(self.path)
        self.syspath = sys.path[:]

    def tearDown(self):
        rmtree(self.path)
        sys.path[:] = self.syspath

    def test_trailing_slash(self):
        with open(os.path.join(self.path, 'test_trailing_slash.py'), 'w') as f:
            f.write("testdata = 'test_trailing_slash'")
        sys.path.append(self.path + '/')
        mod = __import__('test_trailing_slash')
        self.assertEqual(mod.testdata, 'test_trailing_slash')
        unload('test_trailing_slash')

    def _test_UNC_path(self):
        with open(os.path.join(self.path, 'test_trailing_slash.py'), 'w') as f:
            f.write("testdata = 'test_trailing_slash'")
        path = os.path.abspath(self.path)
        import socket
        hn = socket.gethostname()
        drive = path[0]
        unc = '\\\\%s\\%s$' % (hn, drive)
        unc += path[2:]
        sys.path.append(path)
        mod = __import__('test_trailing_slash')
        self.assertEqual(mod.testdata, 'test_trailing_slash')
        unload('test_trailing_slash')

    if sys.platform == 'win32':
        test_UNC_path = _test_UNC_path


class RelativeImportTests(unittest.TestCase):

    def tearDown(self):
        unload('test.relimport')

    setUp = tearDown

    def test_relimport_star(self):
        from . import relimport
        self.assertTrue(hasattr(relimport, 'RelativeImportTests'))

    def test_issue3221(self):

        def check_absolute():
            exec 'from os import path' in ns

        def check_relative():
            exec 'from . import relimport' in ns

        ns = dict(__package__='test', __name__='test.notarealmodule')
        check_absolute()
        check_relative()
        ns = dict(__package__='test', __name__='notarealpkg.notarealmodule')
        check_absolute()
        check_relative()
        ns = dict(__package__='foo', __name__='test.notarealmodule')
        with check_warnings(('.+foo', RuntimeWarning)):
            check_absolute()
        self.assertRaises(SystemError, check_relative)
        ns = dict(__package__='foo', __name__='notarealpkg.notarealmodule')
        with check_warnings(('.+foo', RuntimeWarning)):
            check_absolute()
        self.assertRaises(SystemError, check_relative)
        ns = dict(__package__=object())
        self.assertRaises(ValueError, check_absolute)
        self.assertRaises(ValueError, check_relative)

    def test_absolute_import_without_future(self):
        with self.assertRaises(ImportError):
            from .os import sep
            self.fail('explicit relative import triggered an implicit absolute import')


def test_main(verbose = None):
    run_unittest(ImportTests, PycRewritingTests, PathsTests, RelativeImportTests)


if __name__ == '__main__':
    from test.test_import import test_main
    test_main()