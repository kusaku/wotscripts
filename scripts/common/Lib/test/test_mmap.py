# Embedded file name: scripts/common/Lib/test/test_mmap.py
from test.test_support import TESTFN, run_unittest, import_module, unlink, requires, _2G, _4G
import unittest
import os, re, itertools, socket, sys
mmap = import_module('mmap')
PAGESIZE = mmap.PAGESIZE

class MmapTests(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TESTFN):
            os.unlink(TESTFN)

    def tearDown(self):
        try:
            os.unlink(TESTFN)
        except OSError:
            pass

    def test_basic(self):
        f = open(TESTFN, 'w+')
        try:
            f.write('\x00' * PAGESIZE)
            f.write('foo')
            f.write('\x00' * (PAGESIZE - 3))
            f.flush()
            m = mmap.mmap(f.fileno(), 2 * PAGESIZE)
            f.close()
            tp = str(type(m))
            self.assertEqual(m.find('foo'), PAGESIZE)
            self.assertEqual(len(m), 2 * PAGESIZE)
            self.assertEqual(m[0], '\x00')
            self.assertEqual(m[0:3], '\x00\x00\x00')
            self.assertRaises(IndexError, m.__getitem__, len(m))
            self.assertRaises(IndexError, m.__setitem__, len(m), '\x00')
            m[0] = '3'
            m[PAGESIZE + 3:PAGESIZE + 3 + 3] = 'bar'
            self.assertEqual(m[0], '3')
            self.assertEqual(m[0:3], '3\x00\x00')
            self.assertEqual(m[PAGESIZE - 1:PAGESIZE + 7], '\x00foobar\x00')
            m.flush()
            match = re.search('[A-Za-z]+', m)
            if match is None:
                self.fail('regex match on mmap failed!')
            else:
                start, end = match.span(0)
                length = end - start
                self.assertEqual(start, PAGESIZE)
                self.assertEqual(end, PAGESIZE + 6)
            m.seek(0, 0)
            self.assertEqual(m.tell(), 0)
            m.seek(42, 1)
            self.assertEqual(m.tell(), 42)
            m.seek(0, 2)
            self.assertEqual(m.tell(), len(m))
            self.assertRaises(ValueError, m.seek, -1)
            self.assertRaises(ValueError, m.seek, 1, 2)
            self.assertRaises(ValueError, m.seek, -len(m) - 1, 2)
            try:
                m.resize(512)
            except SystemError:
                pass
            else:
                self.assertEqual(len(m), 512)
                self.assertRaises(ValueError, m.seek, 513, 0)
                f = open(TESTFN)
                f.seek(0, 2)
                self.assertEqual(f.tell(), 512)
                f.close()
                self.assertEqual(m.size(), 512)

            m.close()
        finally:
            try:
                f.close()
            except OSError:
                pass

        return

    def test_access_parameter(self):
        mapsize = 10
        open(TESTFN, 'wb').write('a' * mapsize)
        f = open(TESTFN, 'rb')
        m = mmap.mmap(f.fileno(), mapsize, access=mmap.ACCESS_READ)
        self.assertEqual(m[:], 'a' * mapsize, 'Readonly memory map data incorrect.')
        try:
            m[:] = 'b' * mapsize
        except TypeError:
            pass
        else:
            self.fail('Able to write to readonly memory map')

        try:
            m[0] = 'b'
        except TypeError:
            pass
        else:
            self.fail('Able to write to readonly memory map')

        try:
            m.seek(0, 0)
            m.write('abc')
        except TypeError:
            pass
        else:
            self.fail('Able to write to readonly memory map')

        try:
            m.seek(0, 0)
            m.write_byte('d')
        except TypeError:
            pass
        else:
            self.fail('Able to write to readonly memory map')

        try:
            m.resize(2 * mapsize)
        except SystemError:
            pass
        except TypeError:
            pass
        else:
            self.fail('Able to resize readonly memory map')

        f.close()
        del m
        del f
        self.assertEqual(open(TESTFN, 'rb').read(), 'a' * mapsize, 'Readonly memory map data file was modified')
        import sys
        f = open(TESTFN, 'r+b')
        try:
            m = mmap.mmap(f.fileno(), mapsize + 1)
        except ValueError:
            if sys.platform.startswith('win'):
                self.fail('Opening mmap with size+1 should work on Windows.')
        else:
            if not sys.platform.startswith('win'):
                self.fail('Opening mmap with size+1 should raise ValueError.')
            m.close()

        f.close()
        if sys.platform.startswith('win'):
            f = open(TESTFN, 'r+b')
            f.truncate(mapsize)
            f.close()
        f = open(TESTFN, 'r+b')
        m = mmap.mmap(f.fileno(), mapsize, access=mmap.ACCESS_WRITE)
        m[:] = 'c' * mapsize
        self.assertEqual(m[:], 'c' * mapsize, 'Write-through memory map memory not updated properly.')
        m.flush()
        m.close()
        f.close()
        f = open(TESTFN, 'rb')
        stuff = f.read()
        f.close()
        self.assertEqual(stuff, 'c' * mapsize, 'Write-through memory map data file not updated properly.')
        f = open(TESTFN, 'r+b')
        m = mmap.mmap(f.fileno(), mapsize, access=mmap.ACCESS_COPY)
        m[:] = 'd' * mapsize
        self.assertEqual(m[:], 'd' * mapsize, 'Copy-on-write memory map data not written correctly.')
        m.flush()
        self.assertEqual(open(TESTFN, 'rb').read(), 'c' * mapsize, 'Copy-on-write test data file should not be modified.')
        self.assertRaises(TypeError, m.resize, 2 * mapsize)
        f.close()
        del m
        del f
        f = open(TESTFN, 'r+b')
        self.assertRaises(ValueError, mmap.mmap, f.fileno(), mapsize, access=4)
        f.close()
        if os.name == 'posix':
            f = open(TESTFN, 'r+b')
            self.assertRaises(ValueError, mmap.mmap, f.fileno(), mapsize, flags=mmap.MAP_PRIVATE, prot=mmap.PROT_READ, access=mmap.ACCESS_WRITE)
            f.close()
            prot = mmap.PROT_READ | getattr(mmap, 'PROT_EXEC', 0)
            with open(TESTFN, 'r+b') as f:
                m = mmap.mmap(f.fileno(), mapsize, prot=prot)
                self.assertRaises(TypeError, m.write, 'abcdef')
                self.assertRaises(TypeError, m.write_byte, 0)
                m.close()

    def test_bad_file_desc(self):
        self.assertRaises(mmap.error, mmap.mmap, -2, 4096)

    def test_tougher_find(self):
        f = open(TESTFN, 'w+')
        data = 'aabaac\x00deef\x00\x00aa\x00'
        n = len(data)
        f.write(data)
        f.flush()
        m = mmap.mmap(f.fileno(), n)
        f.close()
        for start in range(n + 1):
            for finish in range(start, n + 1):
                slice = data[start:finish]
                self.assertEqual(m.find(slice), data.find(slice))
                self.assertEqual(m.find(slice + 'x'), -1)

        m.close()

    def test_find_end(self):
        f = open(TESTFN, 'w+')
        data = 'one two ones'
        n = len(data)
        f.write(data)
        f.flush()
        m = mmap.mmap(f.fileno(), n)
        f.close()
        self.assertEqual(m.find('one'), 0)
        self.assertEqual(m.find('ones'), 8)
        self.assertEqual(m.find('one', 0, -1), 0)
        self.assertEqual(m.find('one', 1), 8)
        self.assertEqual(m.find('one', 1, -1), 8)
        self.assertEqual(m.find('one', 1, -2), -1)

    def test_rfind(self):
        f = open(TESTFN, 'w+')
        data = 'one two ones'
        n = len(data)
        f.write(data)
        f.flush()
        m = mmap.mmap(f.fileno(), n)
        f.close()
        self.assertEqual(m.rfind('one'), 8)
        self.assertEqual(m.rfind('one '), 0)
        self.assertEqual(m.rfind('one', 0, -1), 8)
        self.assertEqual(m.rfind('one', 0, -2), 0)
        self.assertEqual(m.rfind('one', 1, -1), 8)
        self.assertEqual(m.rfind('one', 1, -2), -1)

    def test_double_close(self):
        f = open(TESTFN, 'w+')
        f.write(65536 * 'a')
        f.close()
        f = open(TESTFN)
        mf = mmap.mmap(f.fileno(), 65536, access=mmap.ACCESS_READ)
        mf.close()
        mf.close()
        f.close()

    def test_entire_file(self):
        if hasattr(os, 'stat'):
            f = open(TESTFN, 'w+')
            f.write(65536 * 'm')
            f.close()
            f = open(TESTFN, 'rb+')
            mf = mmap.mmap(f.fileno(), 0)
            self.assertEqual(len(mf), 65536, 'Map size should equal file size.')
            self.assertEqual(mf.read(65536), 65536 * 'm')
            mf.close()
            f.close()

    def test_length_0_offset(self):
        if not hasattr(os, 'stat'):
            self.skipTest('needs os.stat')
        with open(TESTFN, 'wb') as f:
            f.write(131072 * 'm')
        with open(TESTFN, 'rb') as f:
            mf = mmap.mmap(f.fileno(), 0, offset=65536, access=mmap.ACCESS_READ)
            try:
                self.assertRaises(IndexError, mf.__getitem__, 80000)
            finally:
                mf.close()

    def test_length_0_large_offset(self):
        if not hasattr(os, 'stat'):
            self.skipTest('needs os.stat')
        with open(TESTFN, 'wb') as f:
            f.write(115699 * 'm')
        with open(TESTFN, 'w+b') as f:
            self.assertRaises(ValueError, mmap.mmap, f.fileno(), 0, offset=2147418112)

    def test_move(self):
        f = open(TESTFN, 'w+')
        f.write('ABCDEabcde')
        f.flush()
        mf = mmap.mmap(f.fileno(), 10)
        mf.move(5, 0, 5)
        self.assertEqual(mf[:], 'ABCDEABCDE', 'Map move should have duplicated front 5')
        mf.close()
        f.close()
        data = '0123456789'
        for dest in range(len(data)):
            for src in range(len(data)):
                for count in range(len(data) - max(dest, src)):
                    expected = data[:dest] + data[src:src + count] + data[dest + count:]
                    m = mmap.mmap(-1, len(data))
                    m[:] = data
                    m.move(dest, src, count)
                    self.assertEqual(m[:], expected)
                    m.close()

        m = mmap.mmap(-1, 100)
        offsets = [-100,
         -1,
         0,
         1,
         100]
        for source, dest, size in itertools.product(offsets, offsets, offsets):
            try:
                m.move(source, dest, size)
            except ValueError:
                pass

        offsets = [(-1, -1, -1),
         (-1, -1, 0),
         (-1, 0, -1),
         (0, -1, -1),
         (-1, 0, 0),
         (0, -1, 0),
         (0, 0, -1)]
        for source, dest, size in offsets:
            self.assertRaises(ValueError, m.move, source, dest, size)

        m.close()
        m = mmap.mmap(-1, 1)
        self.assertRaises(ValueError, m.move, 0, 0, 2)
        self.assertRaises(ValueError, m.move, 1, 0, 1)
        self.assertRaises(ValueError, m.move, 0, 1, 1)
        m.move(0, 0, 1)
        m.move(0, 0, 0)

    def test_anonymous(self):
        m = mmap.mmap(-1, PAGESIZE)
        for x in xrange(PAGESIZE):
            self.assertEqual(m[x], '\x00', "anonymously mmap'ed contents should be zero")

        for x in xrange(PAGESIZE):
            m[x] = ch = chr(x & 255)
            self.assertEqual(m[x], ch)

    def test_extended_getslice(self):
        s = ''.join((chr(c) for c in reversed(range(256))))
        m = mmap.mmap(-1, len(s))
        m[:] = s
        self.assertEqual(m[:], s)
        indices = (0, None, 1, 3, 19, 300, -1, -2, -31, -300)
        for start in indices:
            for stop in indices:
                for step in indices[1:]:
                    self.assertEqual(m[start:stop:step], s[start:stop:step])

        return None

    def test_extended_set_del_slice(self):
        s = ''.join((chr(c) for c in reversed(range(256))))
        m = mmap.mmap(-1, len(s))
        indices = (0, None, 1, 3, 19, 300, -1, -2, -31, -300)
        for start in indices:
            for stop in indices:
                for step in indices[1:]:
                    m[:] = s
                    self.assertEqual(m[:], s)
                    L = list(s)
                    data = L[start:stop:step]
                    data = ''.join(reversed(data))
                    L[start:stop:step] = data
                    m[start:stop:step] = data
                    self.assertEqual(m[:], ''.join(L))

        return None

    def make_mmap_file(self, f, halfsize):
        f.write('\x00' * halfsize)
        f.write('foo')
        f.write('\x00' * (halfsize - 3))
        f.flush()
        return mmap.mmap(f.fileno(), 0)

    def test_offset(self):
        f = open(TESTFN, 'w+b')
        try:
            halfsize = mmap.ALLOCATIONGRANULARITY
            m = self.make_mmap_file(f, halfsize)
            m.close()
            f.close()
            mapsize = halfsize * 2
            f = open(TESTFN, 'r+b')
            for offset in [-2, -1, None]:
                try:
                    m = mmap.mmap(f.fileno(), mapsize, offset=offset)
                    self.assertEqual(0, 1)
                except (ValueError, TypeError, OverflowError):
                    pass
                else:
                    self.assertEqual(0, 0)

            f.close()
            f = open(TESTFN, 'r+b')
            m = mmap.mmap(f.fileno(), mapsize - halfsize, offset=halfsize)
            self.assertEqual(m[0:3], 'foo')
            f.close()
            try:
                m.resize(512)
            except SystemError:
                pass
            else:
                self.assertEqual(len(m), 512)
                self.assertRaises(ValueError, m.seek, 513, 0)
                self.assertEqual(m[0:3], 'foo')
                f = open(TESTFN)
                f.seek(0, 2)
                self.assertEqual(f.tell(), halfsize + 512)
                f.close()
                self.assertEqual(m.size(), halfsize + 512)

            m.close()
        finally:
            f.close()
            try:
                os.unlink(TESTFN)
            except OSError:
                pass

        return

    def test_subclass(self):

        class anon_mmap(mmap.mmap):

            def __new__(klass, *args, **kwargs):
                return mmap.mmap.__new__(klass, (-1), *args, **kwargs)

        anon_mmap(PAGESIZE)

    def test_prot_readonly(self):
        if not hasattr(mmap, 'PROT_READ'):
            return
        mapsize = 10
        open(TESTFN, 'wb').write('a' * mapsize)
        f = open(TESTFN, 'rb')
        m = mmap.mmap(f.fileno(), mapsize, prot=mmap.PROT_READ)
        self.assertRaises(TypeError, m.write, 'foo')
        f.close()

    def test_error(self):
        self.assertTrue(issubclass(mmap.error, EnvironmentError))
        self.assertIn('mmap.error', str(mmap.error))

    def test_io_methods(self):
        data = '0123456789'
        open(TESTFN, 'wb').write('x' * len(data))
        f = open(TESTFN, 'r+b')
        m = mmap.mmap(f.fileno(), len(data))
        f.close()
        for i in xrange(len(data)):
            self.assertEqual(m.tell(), i)
            m.write_byte(data[i])
            self.assertEqual(m.tell(), i + 1)

        self.assertRaises(ValueError, m.write_byte, 'x')
        self.assertEqual(m[:], data)
        m.seek(0)
        for i in xrange(len(data)):
            self.assertEqual(m.tell(), i)
            self.assertEqual(m.read_byte(), data[i])
            self.assertEqual(m.tell(), i + 1)

        self.assertRaises(ValueError, m.read_byte)
        m.seek(3)
        self.assertEqual(m.read(3), '345')
        self.assertEqual(m.tell(), 6)
        m.seek(3)
        m.write('bar')
        self.assertEqual(m.tell(), 6)
        self.assertEqual(m[:], '012bar6789')
        m.seek(8)
        self.assertRaises(ValueError, m.write, 'bar')

    if os.name == 'nt':

        def test_tagname(self):
            data1 = '0123456789'
            data2 = 'abcdefghij'
            raise len(data1) == len(data2) or AssertionError
            m1 = mmap.mmap(-1, len(data1), tagname='foo')
            m1[:] = data1
            m2 = mmap.mmap(-1, len(data2), tagname='foo')
            m2[:] = data2
            self.assertEqual(m1[:], data2)
            self.assertEqual(m2[:], data2)
            m2.close()
            m1.close()
            m1 = mmap.mmap(-1, len(data1), tagname='foo')
            m1[:] = data1
            m2 = mmap.mmap(-1, len(data2), tagname='boo')
            m2[:] = data2
            self.assertEqual(m1[:], data1)
            self.assertEqual(m2[:], data2)
            m2.close()
            m1.close()

        def test_crasher_on_windows(self):
            m = mmap.mmap(-1, 1000, tagname='foo')
            try:
                mmap.mmap(-1, 5000, tagname='foo')[:]
            except:
                pass

            m.close()
            open(TESTFN, 'wb').write('xxxxxxxxxx')
            f = open(TESTFN, 'r+b')
            m = mmap.mmap(f.fileno(), 0)
            f.close()
            try:
                m.resize(0)
            except:
                pass

            try:
                m[:]
            except:
                pass

            m.close()

        def test_invalid_descriptor(self):
            s = socket.socket()
            try:
                with self.assertRaises(mmap.error):
                    m = mmap.mmap(s.fileno(), 10)
            finally:
                s.close()


class LargeMmapTests(unittest.TestCase):

    def setUp(self):
        unlink(TESTFN)

    def tearDown(self):
        unlink(TESTFN)

    def _make_test_file(self, num_zeroes, tail):
        if sys.platform[:3] == 'win' or sys.platform == 'darwin':
            requires('largefile', 'test requires %s bytes and a long time to run' % str(6442450944L))
        f = open(TESTFN, 'w+b')
        try:
            f.seek(num_zeroes)
            f.write(tail)
            f.flush()
        except (IOError, OverflowError):
            f.close()
            raise unittest.SkipTest('filesystem does not have largefile support')

        return f

    def test_large_offset(self):
        with self._make_test_file(5637144575L, ' ') as f:
            m = mmap.mmap(f.fileno(), 0, offset=5368709120L, access=mmap.ACCESS_READ)
            try:
                self.assertEqual(m[268435455], ' ')
            finally:
                m.close()

    def test_large_filesize(self):
        with self._make_test_file(6442450943L, ' ') as f:
            m = mmap.mmap(f.fileno(), 65536, access=mmap.ACCESS_READ)
            try:
                self.assertEqual(m.size(), 6442450944L)
            finally:
                m.close()

    def _test_around_boundary(self, boundary):
        tail = '  DEARdear  '
        start = boundary - len(tail) // 2
        end = start + len(tail)
        with self._make_test_file(start, tail) as f:
            m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            try:
                self.assertEqual(m[start:end], tail)
            finally:
                m.close()

    @unittest.skipUnless(sys.maxsize > _4G, 'test cannot run on 32-bit systems')
    def test_around_2GB(self):
        self._test_around_boundary(_2G)

    @unittest.skipUnless(sys.maxsize > _4G, 'test cannot run on 32-bit systems')
    def test_around_4GB(self):
        self._test_around_boundary(_4G)


def test_main():
    run_unittest(MmapTests, LargeMmapTests)


if __name__ == '__main__':
    test_main()