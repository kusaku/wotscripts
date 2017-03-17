# Embedded file name: scripts/common/Lib/test/test_os.py
import os
import errno
import unittest
import warnings
import sys
import signal
import subprocess
import time
from test import test_support
import mmap
import uuid
warnings.filterwarnings('ignore', 'tempnam', RuntimeWarning, __name__)
warnings.filterwarnings('ignore', 'tmpnam', RuntimeWarning, __name__)

class FileTests(unittest.TestCase):

    def setUp(self):
        if os.path.exists(test_support.TESTFN):
            os.unlink(test_support.TESTFN)

    tearDown = setUp

    def test_access(self):
        f = os.open(test_support.TESTFN, os.O_CREAT | os.O_RDWR)
        os.close(f)
        self.assertTrue(os.access(test_support.TESTFN, os.W_OK))

    def test_closerange(self):
        first = os.open(test_support.TESTFN, os.O_CREAT | os.O_RDWR)
        second = os.dup(first)
        try:
            retries = 0
            while second != first + 1:
                os.close(first)
                retries += 1
                if retries > 10:
                    self.skipTest("couldn't allocate two consecutive fds")
                first, second = second, os.dup(second)

        finally:
            os.close(second)

        os.closerange(first, first + 2)
        self.assertRaises(OSError, os.write, first, 'a')

    @test_support.cpython_only
    def test_rename(self):
        path = unicode(test_support.TESTFN)
        old = sys.getrefcount(path)
        self.assertRaises(TypeError, os.rename, path, 0)
        new = sys.getrefcount(path)
        self.assertEqual(old, new)


class TemporaryFileTests(unittest.TestCase):

    def setUp(self):
        self.files = []
        os.mkdir(test_support.TESTFN)

    def tearDown(self):
        for name in self.files:
            os.unlink(name)

        os.rmdir(test_support.TESTFN)

    def check_tempfile(self, name):
        self.assertFalse(os.path.exists(name), 'file already exists for temporary file')
        open(name, 'w')
        self.files.append(name)

    def test_tempnam(self):
        if not hasattr(os, 'tempnam'):
            return
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'tempnam', RuntimeWarning, 'test_os$')
            warnings.filterwarnings('ignore', 'tempnam', DeprecationWarning)
            self.check_tempfile(os.tempnam())
            name = os.tempnam(test_support.TESTFN)
            self.check_tempfile(name)
            name = os.tempnam(test_support.TESTFN, 'pfx')
            self.assertTrue(os.path.basename(name)[:3] == 'pfx')
            self.check_tempfile(name)

    def test_tmpfile(self):
        if not hasattr(os, 'tmpfile'):
            return
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'tmpfile', DeprecationWarning)
            if sys.platform == 'win32':
                name = '\\python_test_os_test_tmpfile.txt'
                if os.path.exists(name):
                    os.remove(name)
                try:
                    fp = open(name, 'w')
                except IOError as first:
                    try:
                        fp = os.tmpfile()
                    except OSError as second:
                        self.assertEqual(first.args, second.args)
                    else:
                        self.fail('expected os.tmpfile() to raise OSError')

                    return

                fp.close()
                os.remove(name)
            fp = os.tmpfile()
            fp.write('foobar')
            fp.seek(0, 0)
            s = fp.read()
            fp.close()
            self.assertTrue(s == 'foobar')

    def test_tmpnam(self):
        if not hasattr(os, 'tmpnam'):
            return
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', 'tmpnam', RuntimeWarning, 'test_os$')
            warnings.filterwarnings('ignore', 'tmpnam', DeprecationWarning)
            name = os.tmpnam()
            if sys.platform in ('win32',):
                self.assertFalse(os.path.exists(name), 'file already exists for temporary file')
            else:
                self.check_tempfile(name)


class StatAttributeTests(unittest.TestCase):

    def setUp(self):
        os.mkdir(test_support.TESTFN)
        self.fname = os.path.join(test_support.TESTFN, 'f1')
        f = open(self.fname, 'wb')
        f.write('ABC')
        f.close()

    def tearDown(self):
        os.unlink(self.fname)
        os.rmdir(test_support.TESTFN)

    def test_stat_attributes(self):
        if not hasattr(os, 'stat'):
            return
        import stat
        result = os.stat(self.fname)
        self.assertEqual(result[stat.ST_SIZE], 3)
        self.assertEqual(result.st_size, 3)
        members = dir(result)
        for name in dir(stat):
            if name[:3] == 'ST_':
                attr = name.lower()
                if name.endswith('TIME'):

                    def trunc(x):
                        return int(x)

                else:

                    def trunc(x):
                        return x

                self.assertEqual(trunc(getattr(result, attr)), result[getattr(stat, name)])
                self.assertIn(attr, members)

        try:
            result[200]
            self.fail('No exception thrown')
        except IndexError:
            pass

        try:
            result.st_mode = 1
            self.fail('No exception thrown')
        except (AttributeError, TypeError):
            pass

        try:
            result.st_rdev = 1
            self.fail('No exception thrown')
        except (AttributeError, TypeError):
            pass

        try:
            result.parrot = 1
            self.fail('No exception thrown')
        except AttributeError:
            pass

        try:
            result2 = os.stat_result((10,))
            self.fail('No exception thrown')
        except TypeError:
            pass

        try:
            result2 = os.stat_result((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
        except TypeError:
            pass

    def test_statvfs_attributes(self):
        if not hasattr(os, 'statvfs'):
            return
        try:
            result = os.statvfs(self.fname)
        except OSError as e:
            if e.errno == errno.ENOSYS:
                return

        self.assertEqual(result.f_bfree, result[3])
        members = ('bsize', 'frsize', 'blocks', 'bfree', 'bavail', 'files', 'ffree', 'favail', 'flag', 'namemax')
        for value, member in enumerate(members):
            self.assertEqual(getattr(result, 'f_' + member), result[value])

        try:
            result.f_bfree = 1
            self.fail('No exception thrown')
        except TypeError:
            pass

        try:
            result.parrot = 1
            self.fail('No exception thrown')
        except AttributeError:
            pass

        try:
            result2 = os.statvfs_result((10,))
            self.fail('No exception thrown')
        except TypeError:
            pass

        try:
            result2 = os.statvfs_result((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))
        except TypeError:
            pass

    def test_utime_dir(self):
        delta = 1000000
        st = os.stat(test_support.TESTFN)
        os.utime(test_support.TESTFN, (st.st_atime, int(st.st_mtime - delta)))
        st2 = os.stat(test_support.TESTFN)
        self.assertEqual(st2.st_mtime, int(st.st_mtime - delta))

    if sys.platform == 'win32':

        def get_file_system(path):
            root = os.path.splitdrive(os.path.abspath(path))[0] + '\\'
            import ctypes
            kernel32 = ctypes.windll.kernel32
            buf = ctypes.create_string_buffer('', 100)
            if kernel32.GetVolumeInformationA(root, None, 0, None, None, None, buf, len(buf)):
                return buf.value
            else:
                return

        if get_file_system(test_support.TESTFN) == 'NTFS':

            def test_1565150(self):
                t1 = 1159195039.25
                os.utime(self.fname, (t1, t1))
                self.assertEqual(os.stat(self.fname).st_mtime, t1)

            def test_large_time(self):
                t1 = 5000000000L
                os.utime(self.fname, (t1, t1))
                self.assertEqual(os.stat(self.fname).st_mtime, t1)

        def test_1686475(self):
            try:
                os.stat('c:\\pagefile.sys')
            except WindowsError as e:
                if e.errno == 2:
                    return
                self.fail('Could not stat pagefile.sys')


from test import mapping_tests

class EnvironTests(mapping_tests.BasicTestMappingProtocol):
    """check that os.environ object conform to mapping protocol"""
    type2test = None

    def _reference(self):
        return {'KEY1': 'VALUE1',
         'KEY2': 'VALUE2',
         'KEY3': 'VALUE3'}

    def _empty_mapping(self):
        os.environ.clear()
        return os.environ

    def setUp(self):
        self.__save = dict(os.environ)
        os.environ.clear()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.__save)

    def test_update2(self):
        if os.path.exists('/bin/sh'):
            os.environ.update(HELLO='World')
            with os.popen("/bin/sh -c 'echo $HELLO'") as popen:
                value = popen.read().strip()
                self.assertEqual(value, 'World')

    @unittest.skipIf(sys.platform.startswith(('freebsd', 'darwin')), 'due to known OS bug: see issue #13415')
    def test_unset_error(self):
        if sys.platform == 'win32':
            key = 'x' * 50000
            self.assertRaises(ValueError, os.environ.__delitem__, key)
        else:
            key = 'key='
            self.assertRaises(OSError, os.environ.__delitem__, key)


class WalkTests(unittest.TestCase):
    """Tests for os.walk()."""

    def test_traversal(self):
        import os
        from os.path import join
        walk_path = join(test_support.TESTFN, 'TEST1')
        sub1_path = join(walk_path, 'SUB1')
        sub11_path = join(sub1_path, 'SUB11')
        sub2_path = join(walk_path, 'SUB2')
        tmp1_path = join(walk_path, 'tmp1')
        tmp2_path = join(sub1_path, 'tmp2')
        tmp3_path = join(sub2_path, 'tmp3')
        link_path = join(sub2_path, 'link')
        t2_path = join(test_support.TESTFN, 'TEST2')
        tmp4_path = join(test_support.TESTFN, 'TEST2', 'tmp4')
        os.makedirs(sub11_path)
        os.makedirs(sub2_path)
        os.makedirs(t2_path)
        for path in (tmp1_path,
         tmp2_path,
         tmp3_path,
         tmp4_path):
            f = file(path, 'w')
            f.write("I'm " + path + ' and proud of it.  Blame test_os.\n')
            f.close()

        if hasattr(os, 'symlink'):
            os.symlink(os.path.abspath(t2_path), link_path)
            sub2_tree = (sub2_path, ['link'], ['tmp3'])
        else:
            sub2_tree = (sub2_path, [], ['tmp3'])
        all = list(os.walk(walk_path))
        self.assertEqual(len(all), 4)
        flipped = all[0][1][0] != 'SUB1'
        all[0][1].sort()
        self.assertEqual(all[0], (walk_path, ['SUB1', 'SUB2'], ['tmp1']))
        self.assertEqual(all[1 + flipped], (sub1_path, ['SUB11'], ['tmp2']))
        self.assertEqual(all[2 + flipped], (sub11_path, [], []))
        self.assertEqual(all[3 - 2 * flipped], sub2_tree)
        all = []
        for root, dirs, files in os.walk(walk_path):
            all.append((root, dirs, files))
            if 'SUB1' in dirs:
                dirs.remove('SUB1')

        self.assertEqual(len(all), 2)
        self.assertEqual(all[0], (walk_path, ['SUB2'], ['tmp1']))
        self.assertEqual(all[1], sub2_tree)
        all = list(os.walk(walk_path, topdown=False))
        self.assertEqual(len(all), 4)
        flipped = all[3][1][0] != 'SUB1'
        all[3][1].sort()
        self.assertEqual(all[3], (walk_path, ['SUB1', 'SUB2'], ['tmp1']))
        self.assertEqual(all[flipped], (sub11_path, [], []))
        self.assertEqual(all[flipped + 1], (sub1_path, ['SUB11'], ['tmp2']))
        self.assertEqual(all[2 - 2 * flipped], sub2_tree)
        if hasattr(os, 'symlink'):
            for root, dirs, files in os.walk(walk_path, followlinks=True):
                if root == link_path:
                    self.assertEqual(dirs, [])
                    self.assertEqual(files, ['tmp4'])
                    break
            else:
                self.fail("Didn't follow symlink with followlinks=True")

    def tearDown(self):
        for root, dirs, files in os.walk(test_support.TESTFN, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

            for name in dirs:
                dirname = os.path.join(root, name)
                if not os.path.islink(dirname):
                    os.rmdir(dirname)
                else:
                    os.remove(dirname)

        os.rmdir(test_support.TESTFN)


class MakedirTests(unittest.TestCase):

    def setUp(self):
        os.mkdir(test_support.TESTFN)

    def test_makedir(self):
        base = test_support.TESTFN
        path = os.path.join(base, 'dir1', 'dir2', 'dir3')
        os.makedirs(path)
        path = os.path.join(base, 'dir1', 'dir2', 'dir3', 'dir4')
        os.makedirs(path)
        self.assertRaises(OSError, os.makedirs, os.curdir)
        path = os.path.join(base, 'dir1', 'dir2', 'dir3', 'dir4', 'dir5', os.curdir)
        os.makedirs(path)
        path = os.path.join(base, 'dir1', os.curdir, 'dir2', 'dir3', 'dir4', 'dir5', 'dir6')
        os.makedirs(path)

    def tearDown(self):
        path = os.path.join(test_support.TESTFN, 'dir1', 'dir2', 'dir3', 'dir4', 'dir5', 'dir6')
        while not os.path.exists(path) and path != test_support.TESTFN:
            path = os.path.dirname(path)

        os.removedirs(path)


class DevNullTests(unittest.TestCase):

    def test_devnull(self):
        f = file(os.devnull, 'w')
        f.write('hello')
        f.close()
        f = file(os.devnull, 'r')
        self.assertEqual(f.read(), '')
        f.close()


class URandomTests(unittest.TestCase):

    def test_urandom_length(self):
        self.assertEqual(len(os.urandom(0)), 0)
        self.assertEqual(len(os.urandom(1)), 1)
        self.assertEqual(len(os.urandom(10)), 10)
        self.assertEqual(len(os.urandom(100)), 100)
        self.assertEqual(len(os.urandom(1000)), 1000)

    def test_urandom_value(self):
        data1 = os.urandom(16)
        data2 = os.urandom(16)
        self.assertNotEqual(data1, data2)

    def get_urandom_subprocess(self, count):
        code = '\n'.join(('import os, sys',
         'data = os.urandom(%s)' % count,
         'sys.stdout.write(repr(data))',
         'sys.stdout.flush()',
         'print >> sys.stderr, (len(data), data)'))
        cmd_line = [sys.executable, '-c', code]
        p = subprocess.Popen(cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        self.assertEqual(p.wait(), 0, (p.wait(), err))
        out = eval(out)
        self.assertEqual(len(out), count, err)
        return out

    def test_urandom_subprocess(self):
        data1 = self.get_urandom_subprocess(16)
        data2 = self.get_urandom_subprocess(16)
        self.assertNotEqual(data1, data2)

    def test_execvpe_with_bad_arglist(self):
        self.assertRaises(ValueError, os.execvpe, 'notepad', [], None)
        return


class Win32ErrorTests(unittest.TestCase):

    def test_rename(self):
        self.assertRaises(WindowsError, os.rename, test_support.TESTFN, test_support.TESTFN + '.bak')

    def test_remove(self):
        self.assertRaises(WindowsError, os.remove, test_support.TESTFN)

    def test_chdir(self):
        self.assertRaises(WindowsError, os.chdir, test_support.TESTFN)

    def test_mkdir(self):
        f = open(test_support.TESTFN, 'w')
        try:
            self.assertRaises(WindowsError, os.mkdir, test_support.TESTFN)
        finally:
            f.close()
            os.unlink(test_support.TESTFN)

    def test_utime(self):
        self.assertRaises(WindowsError, os.utime, test_support.TESTFN, None)
        return

    def test_chmod(self):
        self.assertRaises(WindowsError, os.chmod, test_support.TESTFN, 0)


class TestInvalidFD(unittest.TestCase):
    singles = ['fchdir',
     'fdopen',
     'dup',
     'fdatasync',
     'fstat',
     'fstatvfs',
     'fsync',
     'tcgetpgrp',
     'ttyname']

    def get_single(f):

        def helper(self):
            if hasattr(os, f):
                self.check(getattr(os, f))

        return helper

    for f in singles:
        locals()['test_' + f] = get_single(f)

    def check(self, f, *args):
        try:
            f(test_support.make_bad_fd(), *args)
        except OSError as e:
            self.assertEqual(e.errno, errno.EBADF)
        else:
            self.fail("%r didn't raise a OSError with a bad file descriptor" % f)

    def test_isatty(self):
        if hasattr(os, 'isatty'):
            self.assertEqual(os.isatty(test_support.make_bad_fd()), False)

    def test_closerange(self):
        if hasattr(os, 'closerange'):
            fd = test_support.make_bad_fd()
            for i in range(10):
                try:
                    os.fstat(fd + i)
                except OSError:
                    pass
                else:
                    break

            if i < 2:
                raise unittest.SkipTest('Unable to acquire a range of invalid file descriptors')
            self.assertEqual(os.closerange(fd, fd + i - 1), None)
        return

    def test_dup2(self):
        if hasattr(os, 'dup2'):
            self.check(os.dup2, 20)

    def test_fchmod(self):
        if hasattr(os, 'fchmod'):
            self.check(os.fchmod, 0)

    def test_fchown(self):
        if hasattr(os, 'fchown'):
            self.check(os.fchown, -1, -1)

    def test_fpathconf(self):
        if hasattr(os, 'fpathconf'):
            self.check(os.fpathconf, 'PC_NAME_MAX')

    def test_ftruncate(self):
        if hasattr(os, 'ftruncate'):
            self.check(os.ftruncate, 0)

    def test_lseek(self):
        if hasattr(os, 'lseek'):
            self.check(os.lseek, 0, 0)

    def test_read(self):
        if hasattr(os, 'read'):
            self.check(os.read, 1)

    def test_tcsetpgrpt(self):
        if hasattr(os, 'tcsetpgrp'):
            self.check(os.tcsetpgrp, 0)

    def test_write(self):
        if hasattr(os, 'write'):
            self.check(os.write, ' ')


if sys.platform != 'win32':

    class Win32ErrorTests(unittest.TestCase):
        pass


    class PosixUidGidTests(unittest.TestCase):
        if hasattr(os, 'setuid'):

            def test_setuid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.setuid, 0)
                self.assertRaises(OverflowError, os.setuid, 4294967296L)

        if hasattr(os, 'setgid'):

            def test_setgid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.setgid, 0)
                self.assertRaises(OverflowError, os.setgid, 4294967296L)

        if hasattr(os, 'seteuid'):

            def test_seteuid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.seteuid, 0)
                self.assertRaises(OverflowError, os.seteuid, 4294967296L)

        if hasattr(os, 'setegid'):

            def test_setegid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.setegid, 0)
                self.assertRaises(OverflowError, os.setegid, 4294967296L)

        if hasattr(os, 'setreuid'):

            def test_setreuid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.setreuid, 0, 0)
                self.assertRaises(OverflowError, os.setreuid, 4294967296L, 0)
                self.assertRaises(OverflowError, os.setreuid, 0, 4294967296L)

            def test_setreuid_neg1(self):
                subprocess.check_call([sys.executable, '-c', 'import os,sys;os.setreuid(-1,-1);sys.exit(0)'])

        if hasattr(os, 'setregid'):

            def test_setregid(self):
                if os.getuid() != 0:
                    self.assertRaises(os.error, os.setregid, 0, 0)
                self.assertRaises(OverflowError, os.setregid, 4294967296L, 0)
                self.assertRaises(OverflowError, os.setregid, 0, 4294967296L)

            def test_setregid_neg1(self):
                subprocess.check_call([sys.executable, '-c', 'import os,sys;os.setregid(-1,-1);sys.exit(0)'])


else:

    class PosixUidGidTests(unittest.TestCase):
        pass


@unittest.skipUnless(sys.platform == 'win32', 'Win32 specific tests')

class Win32KillTests(unittest.TestCase):

    def _kill(self, sig):
        import ctypes
        from ctypes import wintypes
        import msvcrt
        PeekNamedPipe = ctypes.windll.kernel32.PeekNamedPipe
        PeekNamedPipe.restype = wintypes.BOOL
        PeekNamedPipe.argtypes = (wintypes.HANDLE,
         ctypes.POINTER(ctypes.c_char),
         wintypes.DWORD,
         ctypes.POINTER(wintypes.DWORD),
         ctypes.POINTER(wintypes.DWORD),
         ctypes.POINTER(wintypes.DWORD))
        msg = 'running'
        proc = subprocess.Popen([sys.executable, '-c', "import sys;sys.stdout.write('{}');sys.stdout.flush();input()".format(msg)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        self.addCleanup(proc.stdout.close)
        self.addCleanup(proc.stderr.close)
        self.addCleanup(proc.stdin.close)
        count, max = (0, 100)
        while count < max and proc.poll() is None:
            buf = ctypes.create_string_buffer(len(msg))
            rslt = PeekNamedPipe(msvcrt.get_osfhandle(proc.stdout.fileno()), buf, ctypes.sizeof(buf), None, None, None)
            self.assertNotEqual(rslt, 0, 'PeekNamedPipe failed')
            if buf.value:
                self.assertEqual(msg, buf.value)
                break
            time.sleep(0.1)
            count += 1
        else:
            self.fail('Did not receive communication from the subprocess')

        os.kill(proc.pid, sig)
        self.assertEqual(proc.wait(), sig)
        return

    def test_kill_sigterm(self):
        self._kill(signal.SIGTERM)

    def test_kill_int(self):
        self._kill(100)

    def _kill_with_event(self, event, name):
        tagname = 'test_os_%s' % uuid.uuid1()
        m = mmap.mmap(-1, 1, tagname)
        m[0] = '0'
        proc = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), 'win_console_handler.py'), tagname], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        count, max = (0, 20)
        while count < max and proc.poll() is None:
            if m[0] == '1':
                break
            time.sleep(0.5)
            count += 1
        else:
            self.fail("Subprocess didn't finish initialization")

        os.kill(proc.pid, event)
        time.sleep(0.5)
        if not proc.poll():
            os.kill(proc.pid, signal.SIGINT)
            self.fail('subprocess did not stop on {}'.format(name))
        return

    @unittest.skip("subprocesses aren't inheriting CTRL+C property")
    def test_CTRL_C_EVENT(self):
        from ctypes import wintypes
        import ctypes
        NULL = ctypes.POINTER(ctypes.c_int)()
        SetConsoleCtrlHandler = ctypes.windll.kernel32.SetConsoleCtrlHandler
        SetConsoleCtrlHandler.argtypes = (ctypes.POINTER(ctypes.c_int), wintypes.BOOL)
        SetConsoleCtrlHandler.restype = wintypes.BOOL
        SetConsoleCtrlHandler(NULL, 0)
        self._kill_with_event(signal.CTRL_C_EVENT, 'CTRL_C_EVENT')

    def test_CTRL_BREAK_EVENT(self):
        self._kill_with_event(signal.CTRL_BREAK_EVENT, 'CTRL_BREAK_EVENT')


def test_main():
    test_support.run_unittest(FileTests, TemporaryFileTests, StatAttributeTests, EnvironTests, WalkTests, MakedirTests, DevNullTests, URandomTests, Win32ErrorTests, TestInvalidFD, PosixUidGidTests, Win32KillTests)


if __name__ == '__main__':
    test_main()