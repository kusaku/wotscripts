# Embedded file name: scripts/common/Lib/test/test_unicode_file.py
import os, glob, time, shutil
import unicodedata
import unittest
from test.test_support import run_unittest, TESTFN_UNICODE
from test.test_support import TESTFN_ENCODING, TESTFN_UNENCODABLE
try:
    TESTFN_ENCODED = TESTFN_UNICODE.encode(TESTFN_ENCODING)
except (UnicodeError, TypeError):
    raise unittest.SkipTest('No Unicode filesystem semantics on this platform.')

if TESTFN_ENCODED.decode(TESTFN_ENCODING) != TESTFN_UNICODE:
    import sys
    try:
        TESTFN_UNICODE = unicode('@test-\xe0\xf2', sys.getfilesystemencoding())
        TESTFN_ENCODED = TESTFN_UNICODE.encode(TESTFN_ENCODING)
        if '?' in TESTFN_ENCODED:
            raise UnicodeError, 'mbcs encoding problem'
    except (UnicodeError, TypeError):
        raise unittest.SkipTest('Cannot find a suiteable filename.')

if TESTFN_ENCODED.decode(TESTFN_ENCODING) != TESTFN_UNICODE:
    raise unittest.SkipTest('Cannot find a suitable filename.')

def remove_if_exists(filename):
    if os.path.exists(filename):
        os.unlink(filename)


class TestUnicodeFiles(unittest.TestCase):

    def _do_single(self, filename):
        self.assertTrue(os.path.exists(filename))
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.access(filename, os.R_OK))
        self.assertTrue(os.path.exists(os.path.abspath(filename)))
        self.assertTrue(os.path.isfile(os.path.abspath(filename)))
        self.assertTrue(os.access(os.path.abspath(filename), os.R_OK))
        os.chmod(filename, 511)
        os.utime(filename, None)
        os.utime(filename, (time.time(), time.time()))
        self._do_copyish(filename, filename)
        self.assertTrue(os.path.abspath(filename) == os.path.abspath(glob.glob(filename)[0]))
        path, base = os.path.split(os.path.abspath(filename))
        if isinstance(base, str):
            base = base.decode(TESTFN_ENCODING)
        file_list = os.listdir(path)
        if file_list and isinstance(file_list[0], str):
            file_list = [ f.decode(TESTFN_ENCODING) for f in file_list ]
        base = unicodedata.normalize('NFD', base)
        file_list = [ unicodedata.normalize('NFD', f) for f in file_list ]
        self.assertIn(base, file_list)
        return

    def _do_equivalent(self, filename1, filename2):
        self.assertTrue(type(filename1) != type(filename2), 'No point checking equivalent filenames of the same type')
        self.assertEqual(os.stat(filename1), os.stat(filename2))
        self.assertEqual(os.lstat(filename1), os.lstat(filename2))
        self._do_copyish(filename1, filename2)

    def _do_copyish(self, filename1, filename2):
        self.assertTrue(os.path.isfile(filename1))
        os.rename(filename1, filename2 + '.new')
        self.assertTrue(os.path.isfile(filename1 + '.new'))
        os.rename(filename1 + '.new', filename2)
        self.assertTrue(os.path.isfile(filename2))
        shutil.copy(filename1, filename2 + '.new')
        os.unlink(filename1 + '.new')
        shutil.move(filename1, filename2 + '.new')
        self.assertTrue(not os.path.exists(filename2))
        shutil.move(filename1 + '.new', filename2)
        self.assertTrue(os.path.exists(filename1))
        shutil.copy2(filename1, filename2 + '.new')
        os.unlink(filename1 + '.new')

    def _do_directory(self, make_name, chdir_name, encoded):
        cwd = os.getcwd()
        if os.path.isdir(make_name):
            os.rmdir(make_name)
        os.mkdir(make_name)
        try:
            os.chdir(chdir_name)
            try:
                if not encoded:
                    cwd_result = os.getcwdu()
                    name_result = make_name
                else:
                    cwd_result = os.getcwd().decode(TESTFN_ENCODING)
                    name_result = make_name.decode(TESTFN_ENCODING)
                cwd_result = unicodedata.normalize('NFD', cwd_result)
                name_result = unicodedata.normalize('NFD', name_result)
                self.assertEqual(os.path.basename(cwd_result), name_result)
            finally:
                os.chdir(cwd)

        finally:
            os.rmdir(make_name)

    def _test_single(self, filename):
        remove_if_exists(filename)
        f = file(filename, 'w')
        f.close()
        try:
            self._do_single(filename)
        finally:
            os.unlink(filename)

        self.assertTrue(not os.path.exists(filename))
        f = os.open(filename, os.O_CREAT)
        os.close(f)
        try:
            self._do_single(filename)
        finally:
            os.unlink(filename)

    def _test_equivalent(self, filename1, filename2):
        remove_if_exists(filename1)
        self.assertTrue(not os.path.exists(filename2))
        f = file(filename1, 'w')
        f.close()
        try:
            self._do_equivalent(filename1, filename2)
        finally:
            os.unlink(filename1)

    def test_single_files(self):
        self._test_single(TESTFN_ENCODED)
        self._test_single(TESTFN_UNICODE)
        if TESTFN_UNENCODABLE is not None:
            self._test_single(TESTFN_UNENCODABLE)
        return

    def test_equivalent_files(self):
        self._test_equivalent(TESTFN_ENCODED, TESTFN_UNICODE)
        self._test_equivalent(TESTFN_UNICODE, TESTFN_ENCODED)

    def test_directories(self):
        ext = '.dir'
        self._do_directory(TESTFN_ENCODED + ext, TESTFN_ENCODED + ext, True)
        self._do_directory(TESTFN_ENCODED + ext, TESTFN_UNICODE + ext, True)
        self._do_directory(TESTFN_UNICODE + ext, TESTFN_ENCODED + ext, False)
        self._do_directory(TESTFN_UNICODE + ext, TESTFN_UNICODE + ext, False)
        if TESTFN_UNENCODABLE is not None:
            self._do_directory(TESTFN_UNENCODABLE + ext, TESTFN_UNENCODABLE + ext, False)
        return


def test_main():
    run_unittest(__name__)


if __name__ == '__main__':
    test_main()