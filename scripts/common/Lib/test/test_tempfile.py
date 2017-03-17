# Embedded file name: scripts/common/Lib/test/test_tempfile.py
import tempfile
import os
import signal
import sys
import re
import warnings
import unittest
from test import test_support
warnings.filterwarnings('ignore', category=RuntimeWarning, message='mktemp', module=__name__)
if hasattr(os, 'stat'):
    import stat
    has_stat = 1
else:
    has_stat = 0
has_textmode = tempfile._text_openflags != tempfile._bin_openflags
has_spawnl = hasattr(os, 'spawnl')
if sys.platform in ('openbsd3', 'openbsd4'):
    TEST_FILES = 48
else:
    TEST_FILES = 100

class TC(unittest.TestCase):
    str_check = re.compile('[a-zA-Z0-9_-]{6}$')

    def failOnException(self, what, ei = None):
        if ei is None:
            ei = sys.exc_info()
        self.fail('%s raised %s: %s' % (what, ei[0], ei[1]))
        return

    def nameCheck(self, name, dir, pre, suf):
        ndir, nbase = os.path.split(name)
        npre = nbase[:len(pre)]
        nsuf = nbase[len(nbase) - len(suf):]
        self.assertEqual(os.path.abspath(ndir), os.path.abspath(dir), "file '%s' not in directory '%s'" % (name, dir))
        self.assertEqual(npre, pre, "file '%s' does not begin with '%s'" % (nbase, pre))
        self.assertEqual(nsuf, suf, "file '%s' does not end with '%s'" % (nbase, suf))
        nbase = nbase[len(pre):len(nbase) - len(suf)]
        self.assertTrue(self.str_check.match(nbase), "random string '%s' does not match /^[a-zA-Z0-9_-]{6}$/" % nbase)


test_classes = []

class test_exports(TC):

    def test_exports(self):
        dict = tempfile.__dict__
        expected = {'NamedTemporaryFile': 1,
         'TemporaryFile': 1,
         'mkstemp': 1,
         'mkdtemp': 1,
         'mktemp': 1,
         'TMP_MAX': 1,
         'gettempprefix': 1,
         'gettempdir': 1,
         'tempdir': 1,
         'template': 1,
         'SpooledTemporaryFile': 1}
        unexp = []
        for key in dict:
            if key[0] != '_' and key not in expected:
                unexp.append(key)

        self.assertTrue(len(unexp) == 0, 'unexpected keys: %s' % unexp)


test_classes.append(test_exports)

class test__RandomNameSequence(TC):
    """Test the internal iterator object _RandomNameSequence."""

    def setUp(self):
        self.r = tempfile._RandomNameSequence()

    def test_get_six_char_str(self):
        s = self.r.next()
        self.nameCheck(s, '', '', '')

    def test_many(self):
        dict = {}
        r = self.r
        for i in xrange(TEST_FILES):
            s = r.next()
            self.nameCheck(s, '', '', '')
            self.assertNotIn(s, dict)
            dict[s] = 1

    def test_supports_iter(self):
        i = 0
        r = self.r
        try:
            for s in r:
                i += 1
                if i == 20:
                    break

        except:
            self.failOnException('iteration')

    @unittest.skipUnless(hasattr(os, 'fork'), 'os.fork is required for this test')
    def test_process_awareness(self):
        read_fd, write_fd = os.pipe()
        pid = None
        try:
            pid = os.fork()
            if not pid:
                os.close(read_fd)
                os.write(write_fd, next(self.r).encode('ascii'))
                os.close(write_fd)
                os._exit(0)
            parent_value = next(self.r)
            child_value = os.read(read_fd, len(parent_value)).decode('ascii')
        finally:
            if pid:
                try:
                    os.kill(pid, signal.SIGKILL)
                except EnvironmentError:
                    pass

            os.close(read_fd)
            os.close(write_fd)

        self.assertNotEqual(child_value, parent_value)
        return


test_classes.append(test__RandomNameSequence)

class test__candidate_tempdir_list(TC):
    """Test the internal function _candidate_tempdir_list."""

    def test_nonempty_list(self):
        cand = tempfile._candidate_tempdir_list()
        self.assertFalse(len(cand) == 0)
        for c in cand:
            self.assertIsInstance(c, basestring)

    def test_wanted_dirs(self):
        with test_support.EnvironmentVarGuard() as env:
            for envname in ('TMPDIR', 'TEMP', 'TMP'):
                dirname = os.getenv(envname)
                if not dirname:
                    env[envname] = os.path.abspath(envname)

            cand = tempfile._candidate_tempdir_list()
            for envname in ('TMPDIR', 'TEMP', 'TMP'):
                dirname = os.getenv(envname)
                if not dirname:
                    raise ValueError
                self.assertIn(dirname, cand)

            try:
                dirname = os.getcwd()
            except (AttributeError, os.error):
                dirname = os.curdir

            self.assertIn(dirname, cand)


test_classes.append(test__candidate_tempdir_list)

class test__get_candidate_names(TC):
    """Test the internal function _get_candidate_names."""

    def test_retval(self):
        obj = tempfile._get_candidate_names()
        self.assertIsInstance(obj, tempfile._RandomNameSequence)

    def test_same_thing(self):
        a = tempfile._get_candidate_names()
        b = tempfile._get_candidate_names()
        self.assertTrue(a is b)


test_classes.append(test__get_candidate_names)

class test__mkstemp_inner(TC):
    """Test the internal function _mkstemp_inner."""

    class mkstemped:
        _bflags = tempfile._bin_openflags
        _tflags = tempfile._text_openflags
        _close = os.close
        _unlink = os.unlink

        def __init__(self, dir, pre, suf, bin):
            if bin:
                flags = self._bflags
            else:
                flags = self._tflags
            self.fd, self.name = tempfile._mkstemp_inner(dir, pre, suf, flags)

        def write(self, str):
            os.write(self.fd, str)

        def __del__(self):
            self._close(self.fd)
            self._unlink(self.name)

    def do_create(self, dir = None, pre = '', suf = '', bin = 1):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            file = self.mkstemped(dir, pre, suf, bin)
        except:
            self.failOnException('_mkstemp_inner')

        self.nameCheck(file.name, dir, pre, suf)
        return file

    def test_basic(self):
        self.do_create().write('blat')
        self.do_create(pre='a').write('blat')
        self.do_create(suf='b').write('blat')
        self.do_create(pre='a', suf='b').write('blat')
        self.do_create(pre='aa', suf='.txt').write('blat')

    def test_basic_many(self):
        extant = range(TEST_FILES)
        for i in extant:
            extant[i] = self.do_create(pre='aa')

    def test_choose_directory(self):
        dir = tempfile.mkdtemp()
        try:
            self.do_create(dir=dir).write('blat')
        finally:
            os.rmdir(dir)

    def test_file_mode(self):
        if not has_stat:
            return
        file = self.do_create()
        mode = stat.S_IMODE(os.stat(file.name).st_mode)
        expected = 384
        if sys.platform in ('win32', 'os2emx'):
            user = expected >> 6
            expected = user * 73
        self.assertEqual(mode, expected)

    def test_noinherit(self):
        if not has_spawnl:
            return
        if test_support.verbose:
            v = 'v'
        else:
            v = 'q'
        file = self.do_create()
        fd = '%d' % file.fd
        try:
            me = __file__
        except NameError:
            me = sys.argv[0]

        tester = os.path.join(os.path.dirname(os.path.abspath(me)), 'tf_inherit_check.py')
        if sys.platform in ('win32',):
            decorated = '"%s"' % sys.executable
            tester = '"%s"' % tester
        else:
            decorated = sys.executable
        retval = os.spawnl(os.P_WAIT, sys.executable, decorated, tester, v, fd)
        self.assertFalse(retval < 0, 'child process caught fatal signal %d' % -retval)
        self.assertFalse(retval > 0, 'child process reports failure %d' % retval)

    def test_textmode(self):
        if not has_textmode:
            return
        self.do_create(bin=0).write('blat\n')


test_classes.append(test__mkstemp_inner)

class test_gettempprefix(TC):
    """Test gettempprefix()."""

    def test_sane_template(self):
        p = tempfile.gettempprefix()
        self.assertIsInstance(p, basestring)
        self.assertTrue(len(p) > 0)

    def test_usable_template(self):
        p = tempfile.gettempprefix() + 'xxxxxx.xxx'
        d = tempfile.mkdtemp(prefix='')
        try:
            p = os.path.join(d, p)
            try:
                fd = os.open(p, os.O_RDWR | os.O_CREAT)
            except:
                self.failOnException('os.open')

            os.close(fd)
            os.unlink(p)
        finally:
            os.rmdir(d)


test_classes.append(test_gettempprefix)

class test_gettempdir(TC):
    """Test gettempdir()."""

    def test_directory_exists(self):
        dir = tempfile.gettempdir()
        self.assertTrue(os.path.isabs(dir) or dir == os.curdir, '%s is not an absolute path' % dir)
        self.assertTrue(os.path.isdir(dir), '%s is not a directory' % dir)

    def test_directory_writable(self):
        try:
            file = tempfile.NamedTemporaryFile()
            file.write('blat')
            file.close()
        except:
            self.failOnException('create file in %s' % tempfile.gettempdir())

    def test_same_thing(self):
        a = tempfile.gettempdir()
        b = tempfile.gettempdir()
        self.assertTrue(a is b)


test_classes.append(test_gettempdir)

class test_mkstemp(TC):
    """Test mkstemp()."""

    def do_create(self, dir = None, pre = '', suf = ''):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            fd, name = tempfile.mkstemp(dir=dir, prefix=pre, suffix=suf)
            ndir, nbase = os.path.split(name)
            adir = os.path.abspath(dir)
            self.assertEqual(adir, ndir, "Directory '%s' incorrectly returned as '%s'" % (adir, ndir))
        except:
            self.failOnException('mkstemp')

        try:
            self.nameCheck(name, dir, pre, suf)
        finally:
            os.close(fd)
            os.unlink(name)

        return

    def test_basic(self):
        self.do_create()
        self.do_create(pre='a')
        self.do_create(suf='b')
        self.do_create(pre='a', suf='b')
        self.do_create(pre='aa', suf='.txt')
        self.do_create(dir='.')

    def test_choose_directory(self):
        dir = tempfile.mkdtemp()
        try:
            self.do_create(dir=dir)
        finally:
            os.rmdir(dir)


test_classes.append(test_mkstemp)

class test_mkdtemp(TC):
    """Test mkdtemp()."""

    def do_create(self, dir = None, pre = '', suf = ''):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            name = tempfile.mkdtemp(dir=dir, prefix=pre, suffix=suf)
        except:
            self.failOnException('mkdtemp')

        try:
            self.nameCheck(name, dir, pre, suf)
            return name
        except:
            os.rmdir(name)
            raise

        return

    def test_basic(self):
        os.rmdir(self.do_create())
        os.rmdir(self.do_create(pre='a'))
        os.rmdir(self.do_create(suf='b'))
        os.rmdir(self.do_create(pre='a', suf='b'))
        os.rmdir(self.do_create(pre='aa', suf='.txt'))

    def test_basic_many(self):
        extant = range(TEST_FILES)
        try:
            for i in extant:
                extant[i] = self.do_create(pre='aa')

        finally:
            for i in extant:
                if isinstance(i, basestring):
                    os.rmdir(i)

    def test_choose_directory(self):
        dir = tempfile.mkdtemp()
        try:
            os.rmdir(self.do_create(dir=dir))
        finally:
            os.rmdir(dir)

    def test_mode(self):
        if not has_stat:
            return
        dir = self.do_create()
        try:
            mode = stat.S_IMODE(os.stat(dir).st_mode)
            mode &= 511
            expected = 448
            if sys.platform in ('win32', 'os2emx'):
                user = expected >> 6
                expected = user * 73
            self.assertEqual(mode, expected)
        finally:
            os.rmdir(dir)


test_classes.append(test_mkdtemp)

class test_mktemp(TC):
    """Test mktemp()."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        if self.dir:
            os.rmdir(self.dir)
            self.dir = None
        return

    class mktemped:
        _unlink = os.unlink
        _bflags = tempfile._bin_openflags

        def __init__(self, dir, pre, suf):
            self.name = tempfile.mktemp(dir=dir, prefix=pre, suffix=suf)
            os.close(os.open(self.name, self._bflags, 384))

        def __del__(self):
            self._unlink(self.name)

    def do_create(self, pre = '', suf = ''):
        try:
            file = self.mktemped(self.dir, pre, suf)
        except:
            self.failOnException('mktemp')

        self.nameCheck(file.name, self.dir, pre, suf)
        return file

    def test_basic(self):
        self.do_create()
        self.do_create(pre='a')
        self.do_create(suf='b')
        self.do_create(pre='a', suf='b')
        self.do_create(pre='aa', suf='.txt')

    def test_many(self):
        extant = range(TEST_FILES)
        for i in extant:
            extant[i] = self.do_create(pre='aa')


test_classes.append(test_mktemp)

class test_NamedTemporaryFile(TC):
    """Test NamedTemporaryFile()."""

    def do_create(self, dir = None, pre = '', suf = '', delete = True):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            file = tempfile.NamedTemporaryFile(dir=dir, prefix=pre, suffix=suf, delete=delete)
        except:
            self.failOnException('NamedTemporaryFile')

        self.nameCheck(file.name, dir, pre, suf)
        return file

    def test_basic(self):
        self.do_create()
        self.do_create(pre='a')
        self.do_create(suf='b')
        self.do_create(pre='a', suf='b')
        self.do_create(pre='aa', suf='.txt')

    def test_creates_named(self):
        f = tempfile.NamedTemporaryFile()
        self.assertTrue(os.path.exists(f.name), 'NamedTemporaryFile %s does not exist' % f.name)

    def test_del_on_close(self):
        dir = tempfile.mkdtemp()
        try:
            f = tempfile.NamedTemporaryFile(dir=dir)
            f.write('blat')
            f.close()
            self.assertFalse(os.path.exists(f.name), 'NamedTemporaryFile %s exists after close' % f.name)
        finally:
            os.rmdir(dir)

    def test_dis_del_on_close(self):
        dir = tempfile.mkdtemp()
        tmp = None
        try:
            f = tempfile.NamedTemporaryFile(dir=dir, delete=False)
            tmp = f.name
            f.write('blat')
            f.close()
            self.assertTrue(os.path.exists(f.name), 'NamedTemporaryFile %s missing after close' % f.name)
        finally:
            if tmp is not None:
                os.unlink(tmp)
            os.rmdir(dir)

        return

    def test_multiple_close(self):
        f = tempfile.NamedTemporaryFile()
        f.write('abc\n')
        f.close()
        try:
            f.close()
            f.close()
        except:
            self.failOnException('close')

    def test_context_manager(self):
        with tempfile.NamedTemporaryFile() as f:
            self.assertTrue(os.path.exists(f.name))
        self.assertFalse(os.path.exists(f.name))

        def use_closed():
            with f:
                pass

        self.assertRaises(ValueError, use_closed)


test_classes.append(test_NamedTemporaryFile)

class test_SpooledTemporaryFile(TC):
    """Test SpooledTemporaryFile()."""

    def do_create(self, max_size = 0, dir = None, pre = '', suf = ''):
        if dir is None:
            dir = tempfile.gettempdir()
        try:
            file = tempfile.SpooledTemporaryFile(max_size=max_size, dir=dir, prefix=pre, suffix=suf)
        except:
            self.failOnException('SpooledTemporaryFile')

        return file

    def test_basic(self):
        f = self.do_create()
        self.assertFalse(f._rolled)
        f = self.do_create(max_size=100, pre='a', suf='.txt')
        self.assertFalse(f._rolled)

    def test_del_on_close(self):
        dir = tempfile.mkdtemp()
        try:
            f = tempfile.SpooledTemporaryFile(max_size=10, dir=dir)
            self.assertFalse(f._rolled)
            f.write('blat ' * 5)
            self.assertTrue(f._rolled)
            filename = f.name
            f.close()
            self.assertFalse(os.path.exists(filename), 'SpooledTemporaryFile %s exists after close' % filename)
        finally:
            os.rmdir(dir)

    def test_rewrite_small(self):
        f = self.do_create(max_size=30)
        self.assertFalse(f._rolled)
        for i in range(5):
            f.seek(0, 0)
            f.write('xxxxxxxxxxxxxxxxxxxx')

        self.assertFalse(f._rolled)

    def test_write_sequential(self):
        f = self.do_create(max_size=30)
        self.assertFalse(f._rolled)
        f.write('xxxxxxxxxxxxxxxxxxxx')
        self.assertFalse(f._rolled)
        f.write('xxxxxxxxxx')
        self.assertFalse(f._rolled)
        f.write('x')
        self.assertTrue(f._rolled)

    def test_writelines(self):
        f = self.do_create()
        f.writelines(('x', 'y', 'z'))
        f.seek(0)
        buf = f.read()
        self.assertEqual(buf, 'xyz')

    def test_writelines_sequential(self):
        f = self.do_create(max_size=35)
        f.writelines(('xxxxxxxxxxxxxxxxxxxx', 'xxxxxxxxxx', 'xxxxx'))
        self.assertFalse(f._rolled)
        f.write('x')
        self.assertTrue(f._rolled)

    def test_sparse(self):
        f = self.do_create(max_size=30)
        self.assertFalse(f._rolled)
        f.seek(100, 0)
        self.assertFalse(f._rolled)
        f.write('x')
        self.assertTrue(f._rolled)

    def test_fileno(self):
        f = self.do_create(max_size=30)
        self.assertFalse(f._rolled)
        self.assertTrue(f.fileno() > 0)
        self.assertTrue(f._rolled)

    def test_multiple_close_before_rollover(self):
        f = tempfile.SpooledTemporaryFile()
        f.write('abc\n')
        self.assertFalse(f._rolled)
        f.close()
        try:
            f.close()
            f.close()
        except:
            self.failOnException('close')

    def test_multiple_close_after_rollover(self):
        f = tempfile.SpooledTemporaryFile(max_size=1)
        f.write('abc\n')
        self.assertTrue(f._rolled)
        f.close()
        try:
            f.close()
            f.close()
        except:
            self.failOnException('close')

    def test_bound_methods(self):
        f = self.do_create(max_size=30)
        read = f.read
        write = f.write
        seek = f.seek
        write('a' * 35)
        write('b' * 35)
        seek(0, 0)
        self.assertTrue(read(70) == 'a' * 35 + 'b' * 35)

    def test_context_manager_before_rollover(self):
        with tempfile.SpooledTemporaryFile(max_size=1) as f:
            self.assertFalse(f._rolled)
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)

        def use_closed():
            with f:
                pass

        self.assertRaises(ValueError, use_closed)

    def test_context_manager_during_rollover(self):
        with tempfile.SpooledTemporaryFile(max_size=1) as f:
            self.assertFalse(f._rolled)
            f.write('abc\n')
            f.flush()
            self.assertTrue(f._rolled)
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)

        def use_closed():
            with f:
                pass

        self.assertRaises(ValueError, use_closed)

    def test_context_manager_after_rollover(self):
        f = tempfile.SpooledTemporaryFile(max_size=1)
        f.write('abc\n')
        f.flush()
        self.assertTrue(f._rolled)
        with f:
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)

        def use_closed():
            with f:
                pass

        self.assertRaises(ValueError, use_closed)


test_classes.append(test_SpooledTemporaryFile)

class test_TemporaryFile(TC):
    """Test TemporaryFile()."""

    def test_basic(self):
        try:
            tempfile.TemporaryFile()
        except:
            self.failOnException('TemporaryFile')

    def test_has_no_name(self):
        dir = tempfile.mkdtemp()
        f = tempfile.TemporaryFile(dir=dir)
        f.write('blat')
        try:
            os.rmdir(dir)
        except:
            ei = sys.exc_info()
            f.close()
            os.rmdir(dir)
            self.failOnException('rmdir', ei)

    def test_multiple_close(self):
        f = tempfile.TemporaryFile()
        f.write('abc\n')
        f.close()
        try:
            f.close()
            f.close()
        except:
            self.failOnException('close')


if tempfile.NamedTemporaryFile is not tempfile.TemporaryFile:
    test_classes.append(test_TemporaryFile)

def test_main():
    test_support.run_unittest(*test_classes)


if __name__ == '__main__':
    test_main()