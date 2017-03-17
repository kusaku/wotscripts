# Embedded file name: scripts/common/Lib/test/test_sys.py
import unittest, test.test_support
import sys, os, cStringIO
import struct
import operator

class SysModuleTest(unittest.TestCase):

    def tearDown(self):
        test.test_support.reap_children()

    def test_original_displayhook(self):
        import __builtin__
        savestdout = sys.stdout
        out = cStringIO.StringIO()
        sys.stdout = out
        dh = sys.__displayhook__
        self.assertRaises(TypeError, dh)
        if hasattr(__builtin__, '_'):
            del __builtin__._
        dh(None)
        self.assertEqual(out.getvalue(), '')
        self.assertTrue(not hasattr(__builtin__, '_'))
        dh(42)
        self.assertEqual(out.getvalue(), '42\n')
        self.assertEqual(__builtin__._, 42)
        del sys.stdout
        self.assertRaises(RuntimeError, dh, 42)
        sys.stdout = savestdout
        return

    def test_lost_displayhook(self):
        olddisplayhook = sys.displayhook
        del sys.displayhook
        code = compile('42', '<string>', 'single')
        self.assertRaises(RuntimeError, eval, code)
        sys.displayhook = olddisplayhook

    def test_custom_displayhook(self):
        olddisplayhook = sys.displayhook

        def baddisplayhook(obj):
            raise ValueError

        sys.displayhook = baddisplayhook
        code = compile('42', '<string>', 'single')
        self.assertRaises(ValueError, eval, code)
        sys.displayhook = olddisplayhook

    def test_original_excepthook(self):
        savestderr = sys.stderr
        err = cStringIO.StringIO()
        sys.stderr = err
        eh = sys.__excepthook__
        self.assertRaises(TypeError, eh)
        try:
            raise ValueError(42)
        except ValueError as exc:
            eh(*sys.exc_info())

        sys.stderr = savestderr
        self.assertTrue(err.getvalue().endswith('ValueError: 42\n'))

    def test_exc_clear(self):
        self.assertRaises(TypeError, sys.exc_clear, 42)

        def clear_check(exc):
            typ, value, traceback = sys.exc_info()
            self.assertTrue(typ is not None)
            self.assertTrue(value is exc)
            self.assertTrue(traceback is not None)
            with test.test_support.check_py3k_warnings():
                sys.exc_clear()
            typ, value, traceback = sys.exc_info()
            self.assertTrue(typ is None)
            self.assertTrue(value is None)
            self.assertTrue(traceback is None)
            return

        def clear():
            try:
                raise ValueError, 42
            except ValueError as exc:
                clear_check(exc)

        clear()
        try:
            raise ValueError, 13
        except ValueError as exc:
            typ1, value1, traceback1 = sys.exc_info()
            clear()
            typ2, value2, traceback2 = sys.exc_info()
            self.assertTrue(typ1 is typ2)
            self.assertTrue(value1 is exc)
            self.assertTrue(value1 is value2)
            self.assertTrue(traceback1 is traceback2)

        clear_check(exc)

    def test_exit(self):
        self.assertRaises(TypeError, sys.exit, 42, 42)
        try:
            sys.exit(0)
        except SystemExit as exc:
            self.assertEqual(exc.code, 0)
        except:
            self.fail('wrong exception')
        else:
            self.fail('no exception')

        try:
            sys.exit(42)
        except SystemExit as exc:
            self.assertEqual(exc.code, 42)
        except:
            self.fail('wrong exception')
        else:
            self.fail('no exception')

        try:
            sys.exit((42,))
        except SystemExit as exc:
            self.assertEqual(exc.code, 42)
        except:
            self.fail('wrong exception')
        else:
            self.fail('no exception')

        try:
            sys.exit('exit')
        except SystemExit as exc:
            self.assertEqual(exc.code, 'exit')
        except:
            self.fail('wrong exception')
        else:
            self.fail('no exception')

        try:
            sys.exit((17, 23))
        except SystemExit as exc:
            self.assertEqual(exc.code, (17, 23))
        except:
            self.fail('wrong exception')
        else:
            self.fail('no exception')

        import subprocess
        rc = subprocess.call([sys.executable, '-c', 'raise SystemExit, 46'])
        self.assertEqual(rc, 46)
        rc = subprocess.call([sys.executable, '-c', 'raise SystemExit(47)'])
        self.assertEqual(rc, 47)

        def check_exit_message(code, expected, env = None):
            process = subprocess.Popen([sys.executable, '-c', code], stderr=subprocess.PIPE, env=env)
            stdout, stderr = process.communicate()
            self.assertEqual(process.returncode, 1)
            self.assertTrue(stderr.startswith(expected), "%s doesn't start with %s" % (repr(stderr), repr(expected)))

        check_exit_message('import sys; sys.stderr.write("unflushed,"); sys.exit("message")', 'unflushed,message')
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'latin-1'
        check_exit_message('import sys; sys.exit(u"h\\xe9")', 'h\xe9', env=env)
        return

    def test_getdefaultencoding(self):
        if test.test_support.have_unicode:
            self.assertRaises(TypeError, sys.getdefaultencoding, 42)
            self.assertIsInstance(sys.getdefaultencoding(), str)

    def test_setcheckinterval(self):
        self.assertRaises(TypeError, sys.setcheckinterval)
        orig = sys.getcheckinterval()
        for n in (0,
         100,
         120,
         orig):
            sys.setcheckinterval(n)
            self.assertEqual(sys.getcheckinterval(), n)

    def test_recursionlimit(self):
        self.assertRaises(TypeError, sys.getrecursionlimit, 42)
        oldlimit = sys.getrecursionlimit()
        self.assertRaises(TypeError, sys.setrecursionlimit)
        self.assertRaises(ValueError, sys.setrecursionlimit, -42)
        sys.setrecursionlimit(10000)
        self.assertEqual(sys.getrecursionlimit(), 10000)
        sys.setrecursionlimit(oldlimit)
        self.assertRaises(OverflowError, sys.setrecursionlimit, 2147483648L)
        try:
            sys.setrecursionlimit(2147483643L)
            try:
                raise ValueError()
            except ValueError as e:
                pass

        finally:
            sys.setrecursionlimit(oldlimit)

    def test_getwindowsversion(self):
        test.test_support.get_attribute(sys, 'getwindowsversion')
        v = sys.getwindowsversion()
        self.assertEqual(len(v), 5)
        self.assertIsInstance(v[0], int)
        self.assertIsInstance(v[1], int)
        self.assertIsInstance(v[2], int)
        self.assertIsInstance(v[3], int)
        self.assertIsInstance(v[4], str)
        self.assertRaises(IndexError, operator.getitem, v, 5)
        self.assertIsInstance(v.major, int)
        self.assertIsInstance(v.minor, int)
        self.assertIsInstance(v.build, int)
        self.assertIsInstance(v.platform, int)
        self.assertIsInstance(v.service_pack, str)
        self.assertIsInstance(v.service_pack_minor, int)
        self.assertIsInstance(v.service_pack_major, int)
        self.assertIsInstance(v.suite_mask, int)
        self.assertIsInstance(v.product_type, int)
        self.assertEqual(v[0], v.major)
        self.assertEqual(v[1], v.minor)
        self.assertEqual(v[2], v.build)
        self.assertEqual(v[3], v.platform)
        self.assertEqual(v[4], v.service_pack)
        maj, min, buildno, plat, csd = sys.getwindowsversion()

    def test_dlopenflags(self):
        if hasattr(sys, 'setdlopenflags'):
            self.assertTrue(hasattr(sys, 'getdlopenflags'))
            self.assertRaises(TypeError, sys.getdlopenflags, 42)
            oldflags = sys.getdlopenflags()
            self.assertRaises(TypeError, sys.setdlopenflags)
            sys.setdlopenflags(oldflags + 1)
            self.assertEqual(sys.getdlopenflags(), oldflags + 1)
            sys.setdlopenflags(oldflags)

    def test_refcount(self):
        global n
        self.assertRaises(TypeError, sys.getrefcount)
        c = sys.getrefcount(None)
        n = None
        self.assertEqual(sys.getrefcount(None), c + 1)
        del n
        self.assertEqual(sys.getrefcount(None), c)
        if hasattr(sys, 'gettotalrefcount'):
            self.assertIsInstance(sys.gettotalrefcount(), int)
        return

    def test_getframe(self):
        self.assertRaises(TypeError, sys._getframe, 42, 42)
        self.assertRaises(ValueError, sys._getframe, 2000000000)
        self.assertTrue(SysModuleTest.test_getframe.im_func.func_code is sys._getframe().f_code)

    def test_current_frames(self):
        have_threads = True
        try:
            import thread
        except ImportError:
            have_threads = False

        if have_threads:
            self.current_frames_with_threads()
        else:
            self.current_frames_without_threads()

    @test.test_support.reap_threads
    def current_frames_with_threads(self):
        import threading, thread
        import traceback
        entered_g = threading.Event()
        leave_g = threading.Event()
        thread_info = []

        def f123():
            g456()

        def g456():
            thread_info.append(thread.get_ident())
            entered_g.set()
            leave_g.wait()

        t = threading.Thread(target=f123)
        t.start()
        entered_g.wait()
        self.assertEqual(len(thread_info), 1)
        thread_id = thread_info[0]
        d = sys._current_frames()
        main_id = thread.get_ident()
        self.assertIn(main_id, d)
        self.assertIn(thread_id, d)
        frame = d.pop(main_id)
        self.assertTrue(frame is sys._getframe())
        frame = d.pop(thread_id)
        stack = traceback.extract_stack(frame)
        for i, (filename, lineno, funcname, sourceline) in enumerate(stack):
            if funcname == 'f123':
                break
        else:
            self.fail("didn't find f123() on thread's call stack")

        self.assertEqual(sourceline, 'g456()')
        filename, lineno, funcname, sourceline = stack[i + 1]
        self.assertEqual(funcname, 'g456')
        self.assertIn(sourceline, ['leave_g.wait()', 'entered_g.set()'])
        leave_g.set()
        t.join()

    def current_frames_without_threads(self):
        d = sys._current_frames()
        self.assertEqual(len(d), 1)
        self.assertIn(0, d)
        self.assertTrue(d[0] is sys._getframe())

    def test_attributes(self):
        self.assertIsInstance(sys.api_version, int)
        self.assertIsInstance(sys.argv, list)
        self.assertIn(sys.byteorder, ('little', 'big'))
        self.assertIsInstance(sys.builtin_module_names, tuple)
        self.assertIsInstance(sys.copyright, basestring)
        self.assertIsInstance(sys.exec_prefix, basestring)
        self.assertIsInstance(sys.executable, basestring)
        self.assertEqual(len(sys.float_info), 11)
        self.assertEqual(sys.float_info.radix, 2)
        self.assertEqual(len(sys.long_info), 2)
        self.assertTrue(sys.long_info.bits_per_digit % 5 == 0)
        self.assertTrue(sys.long_info.sizeof_digit >= 1)
        self.assertEqual(type(sys.long_info.bits_per_digit), int)
        self.assertEqual(type(sys.long_info.sizeof_digit), int)
        self.assertIsInstance(sys.hexversion, int)
        self.assertIsInstance(sys.maxint, int)
        if test.test_support.have_unicode:
            self.assertIsInstance(sys.maxunicode, int)
        self.assertIsInstance(sys.platform, basestring)
        self.assertIsInstance(sys.prefix, basestring)
        self.assertIsInstance(sys.version, basestring)
        vi = sys.version_info
        self.assertIsInstance(vi[:], tuple)
        self.assertEqual(len(vi), 5)
        self.assertIsInstance(vi[0], int)
        self.assertIsInstance(vi[1], int)
        self.assertIsInstance(vi[2], int)
        self.assertIn(vi[3], ('alpha', 'beta', 'candidate', 'final'))
        self.assertIsInstance(vi[4], int)
        self.assertIsInstance(vi.major, int)
        self.assertIsInstance(vi.minor, int)
        self.assertIsInstance(vi.micro, int)
        self.assertIn(vi.releaselevel, ('alpha', 'beta', 'candidate', 'final'))
        self.assertIsInstance(vi.serial, int)
        self.assertEqual(vi[0], vi.major)
        self.assertEqual(vi[1], vi.minor)
        self.assertEqual(vi[2], vi.micro)
        self.assertEqual(vi[3], vi.releaselevel)
        self.assertEqual(vi[4], vi.serial)
        self.assertTrue(vi > (1, 0, 0))
        self.assertIsInstance(sys.float_repr_style, str)
        self.assertIn(sys.float_repr_style, ('short', 'legacy'))

    def test_43581(self):
        self.assertTrue(sys.__stdout__.encoding == sys.__stderr__.encoding)

    def test_sys_flags(self):
        self.assertTrue(sys.flags)
        attrs = ('debug', 'py3k_warning', 'division_warning', 'division_new', 'inspect', 'interactive', 'optimize', 'dont_write_bytecode', 'no_site', 'ignore_environment', 'tabcheck', 'verbose', 'unicode', 'bytes_warning', 'hash_randomization')
        for attr in attrs:
            self.assertTrue(hasattr(sys.flags, attr), attr)
            self.assertEqual(type(getattr(sys.flags, attr)), int, attr)

        self.assertTrue(repr(sys.flags))

    def test_clear_type_cache(self):
        sys._clear_type_cache()

    def test_ioencoding(self):
        import subprocess
        env = dict(os.environ)
        env['PYTHONIOENCODING'] = 'cp424'
        p = subprocess.Popen([sys.executable, '-c', 'print unichr(0xa2)'], stdout=subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        self.assertEqual(out, unichr(162).encode('cp424'))
        env['PYTHONIOENCODING'] = 'ascii:replace'
        p = subprocess.Popen([sys.executable, '-c', 'print unichr(0xa2)'], stdout=subprocess.PIPE, env=env)
        out = p.communicate()[0].strip()
        self.assertEqual(out, '?')

    def test_call_tracing(self):
        self.assertEqual(sys.call_tracing(str, (2,)), '2')
        self.assertRaises(TypeError, sys.call_tracing, str, 2)

    def test_executable(self):
        self.assertEqual(os.path.abspath(sys.executable), sys.executable)
        import subprocess
        python_dir = os.path.dirname(os.path.realpath(sys.executable))
        p = subprocess.Popen(['nonexistent', '-c', 'import sys; print repr(sys.executable)'], executable=sys.executable, stdout=subprocess.PIPE, cwd=python_dir)
        executable = p.communicate()[0].strip()
        p.wait()
        self.assertIn(executable, ["''", repr(sys.executable)])


class SizeofTest(unittest.TestCase):
    TPFLAGS_HAVE_GC = 16384
    TPFLAGS_HEAPTYPE = 512L

    def setUp(self):
        self.c = len(struct.pack('c', ' '))
        self.H = len(struct.pack('H', 0))
        self.i = len(struct.pack('i', 0))
        self.l = len(struct.pack('l', 0))
        self.P = len(struct.pack('P', 0))
        self.header = 'PP'
        self.vheader = self.header + 'P'
        if hasattr(sys, 'gettotalrefcount'):
            self.header += '2P'
            self.vheader += '2P'
        self.longdigit = sys.long_info.sizeof_digit
        import _testcapi
        self.gc_headsize = _testcapi.SIZEOF_PYGC_HEAD
        self.file = open(test.test_support.TESTFN, 'wb')

    def tearDown(self):
        self.file.close()
        test.test_support.unlink(test.test_support.TESTFN)

    def check_sizeof(self, o, size):
        result = sys.getsizeof(o)
        if type(o) == type and o.__flags__ & self.TPFLAGS_HEAPTYPE or type(o) != type and type(o).__flags__ & self.TPFLAGS_HAVE_GC:
            size += self.gc_headsize
        msg = 'wrong size for %s: got %d, expected %d' % (type(o), result, size)
        self.assertEqual(result, size, msg)

    def calcsize(self, fmt):
        """Wrapper around struct.calcsize which enforces the alignment of the
        end of a structure to the alignment requirement of pointer.
        
        Note: This wrapper should only be used if a pointer member is included
        and no member with a size larger than a pointer exists.
        """
        return struct.calcsize(fmt + '0P')

    def test_gc_head_size(self):
        h = self.header
        size = self.calcsize
        gc_header_size = self.gc_headsize
        self.assertEqual(sys.getsizeof(True), size(h + 'l'))
        self.assertEqual(sys.getsizeof([]), size(h + 'P PP') + gc_header_size)

    def test_default(self):
        h = self.header
        size = self.calcsize
        self.assertEqual(sys.getsizeof(True, -1), size(h + 'l'))

    def test_objecttypes(self):
        h = self.header
        vh = self.vheader
        size = self.calcsize
        check = self.check_sizeof
        check(True, size(h + 'l'))
        with test.test_support.check_py3k_warnings():
            check(buffer(''), size(h + '2P2Pil'))
        check(len, size(h + '3P'))
        samples = ['', 'u' * 100000]
        for sample in samples:
            x = bytearray(sample)
            check(x, size(vh + 'iPP') + x.__alloc__() * self.c)

        check(iter(bytearray()), size(h + 'PP'))

        def get_cell():
            x = 42

            def inner():
                return x

            return inner

        check(get_cell().func_closure[0], size(h + 'P'))

        class class_oldstyle:

            def method():
                pass

        check(class_oldstyle, size(h + '7P'))
        check(class_oldstyle(), size(h + '3P'))
        check(class_oldstyle().method, size(h + '4P'))
        check(complex(0, 1), size(h + '2d'))
        check(get_cell().func_code, size(h + '4i8Pi3P'))
        check(BaseException(), size(h + '3P'))
        check(UnicodeEncodeError('', u'', 0, 0, ''), size(h + '5P2PP'))
        check(UnicodeDecodeError('', '', 0, 0, ''), size(h + '5P2PP'))
        check(UnicodeTranslateError(u'', 0, 1, ''), size(h + '5P2PP'))
        check(str.lower, size(h + '2PP'))
        import datetime
        check(datetime.timedelta.days, size(h + '2PP'))
        import __builtin__
        check(__builtin__.file.closed, size(h + '2PP'))
        check(int.__add__, size(h + '2P2P'))

        class C(object):
            pass

        check(C.__dict__, size(h + 'P'))
        check({}.__iter__, size(h + '2P'))
        check({}, size(h + '3P2P' + 8 * 'P2P'))
        x = {1: 1,
         2: 2,
         3: 3,
         4: 4,
         5: 5,
         6: 6,
         7: 7,
         8: 8}
        check(x, size(h + '3P2P' + 8 * 'P2P') + 16 * size('P2P'))
        check({}.iterkeys(), size(h + 'P2PPP'))
        check({}.itervalues(), size(h + 'P2PPP'))
        check({}.iteritems(), size(h + 'P2PPP'))
        check(Ellipsis, size(h + ''))
        import codecs, encodings.iso8859_3
        x = codecs.charmap_build(encodings.iso8859_3.decoding_table)
        check(x, size(h + '32B2iB'))
        check(enumerate([]), size(h + 'l3P'))
        check(self.file, size(h + '4P2i4P3i3P3i'))
        check(float(0), size(h + 'd'))
        check(sys.float_info, size(vh) + self.P * len(sys.float_info))
        import inspect
        CO_MAXBLOCKS = 20
        x = inspect.currentframe()
        ncells = len(x.f_code.co_cellvars)
        nfrees = len(x.f_code.co_freevars)
        extras = x.f_code.co_stacksize + x.f_code.co_nlocals + ncells + nfrees - 1
        check(x, size(vh + '12P3i' + CO_MAXBLOCKS * '3i' + 'P' + extras * 'P'))

        def func():
            pass

        check(func, size(h + '9P'))

        class c:

            @staticmethod
            def foo():
                pass

            @classmethod
            def bar(cls):
                pass

            check(foo, size(h + 'P'))
            check(bar, size(h + 'P'))

        def get_gen():
            yield 1

        check(get_gen(), size(h + 'Pi2P'))
        check(1, size(h + 'l'))
        check(100, size(h + 'l'))
        check(iter('abc'), size(h + 'lP'))
        import re
        check(re.finditer('', ''), size(h + '2P'))
        samples = [[], [1, 2, 3], ['1', '2', '3']]
        for sample in samples:
            check(sample, size(vh + 'PP') + len(sample) * self.P)

        check(iter([]), size(h + 'lP'))
        check(reversed([]), size(h + 'lP'))
        check(0L, size(vh))
        check(1L, size(vh) + self.longdigit)
        check(-1L, size(vh) + self.longdigit)
        PyLong_BASE = 2 ** sys.long_info.bits_per_digit
        check(long(PyLong_BASE), size(vh) + 2 * self.longdigit)
        check(long(PyLong_BASE ** 2 - 1), size(vh) + 2 * self.longdigit)
        check(long(PyLong_BASE ** 2), size(vh) + 3 * self.longdigit)
        check(unittest, size(h + 'P'))
        check(None, size(h + ''))
        check(object(), size(h + ''))

        class C(object):

            def getx(self):
                return self.__x

            def setx(self, value):
                self.__x = value

            def delx(self):
                del self.__x

            x = property(getx, setx, delx, '')
            check(x, size(h + '4Pi'))

        check(iter(xrange(1)), size(h + '4l'))
        check(reversed(''), size(h + 'PP'))
        PySet_MINSIZE = 8
        samples = [[], range(10), range(50)]
        s = size(h + '3P2P' + PySet_MINSIZE * 'lP' + 'lP')
        for sample in samples:
            minused = len(sample)
            if minused == 0:
                tmp = 1
            minused = minused * 2
            newsize = PySet_MINSIZE
            while newsize <= minused:
                newsize = newsize << 1

            if newsize <= 8:
                check(set(sample), s)
                check(frozenset(sample), s)
            else:
                check(set(sample), s + newsize * struct.calcsize('lP'))
                check(frozenset(sample), s + newsize * struct.calcsize('lP'))

        check(iter(set()), size(h + 'P3P'))
        check(slice(1), size(h + '3P'))
        check('', struct.calcsize(vh + 'li') + 1)
        check('abc', struct.calcsize(vh + 'li') + 1 + 3 * self.c)
        check(super(int), size(h + '3P'))
        check((), size(vh))
        check((1, 2, 3), size(vh) + 3 * self.P)
        check(iter(()), size(h + 'lP'))
        s = size(vh + 'P2P15Pl4PP9PP11PI') + size('41P 10P 3P 6P')

        class newstyleclass(object):
            pass

        check(newstyleclass, s)
        check(int, s)
        import types
        check(types.NotImplementedType, s)
        usize = len(u'\x00'.encode('unicode-internal'))
        samples = [u'', u'1' * 100]
        for s in samples:
            check(s, size(h + 'PPlP') + usize * (len(s) + 1))

        import weakref
        check(weakref.ref(int), size(h + '2Pl2P'))
        check(weakref.proxy(int), size(h + '2Pl2P'))
        check(xrange(1), size(h + '3l'))
        check(xrange(66000), size(h + '3l'))
        return

    def test_pythontypes(self):
        h = self.header
        vh = self.vheader
        size = self.calcsize
        check = self.check_sizeof
        import _ast
        check(_ast.AST(), size(h + ''))
        import imp
        check(imp.NullImporter(self.file.name), size(h + ''))
        try:
            raise TypeError
        except TypeError:
            tb = sys.exc_info()[2]
            if tb != None:
                check(tb, size(h + '2P2i'))

        check(sys.flags, size(vh) + self.P * len(sys.flags))
        return


def test_main():
    test_classes = (SysModuleTest, SizeofTest)
    test.test_support.run_unittest(*test_classes)


if __name__ == '__main__':
    test_main()