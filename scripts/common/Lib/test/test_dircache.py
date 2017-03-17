# Embedded file name: scripts/common/Lib/test/test_dircache.py
"""
  Test cases for the dircache module
  Nick Mathewson
"""
import unittest
from test.test_support import run_unittest, import_module
dircache = import_module('dircache', deprecated=True)
import os, time, sys, tempfile

class DircacheTests(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        for fname in os.listdir(self.tempdir):
            self.delTemp(fname)

        os.rmdir(self.tempdir)

    def writeTemp(self, fname):
        f = open(os.path.join(self.tempdir, fname), 'w')
        f.close()

    def mkdirTemp(self, fname):
        os.mkdir(os.path.join(self.tempdir, fname))

    def delTemp(self, fname):
        fname = os.path.join(self.tempdir, fname)
        if os.path.isdir(fname):
            os.rmdir(fname)
        else:
            os.unlink(fname)

    def test_listdir(self):
        entries = dircache.listdir(self.tempdir)
        self.assertEqual(entries, [])
        self.assertTrue(dircache.listdir(self.tempdir) is entries)
        if sys.platform[:3] not in ('win', 'os2'):
            time.sleep(1)
            self.writeTemp('test1')
            entries = dircache.listdir(self.tempdir)
            self.assertEqual(entries, ['test1'])
            self.assertTrue(dircache.listdir(self.tempdir) is entries)
        self.assertRaises(OSError, dircache.listdir, self.tempdir + '_nonexistent')

    def test_annotate(self):
        self.writeTemp('test2')
        self.mkdirTemp('A')
        lst = ['A', 'test2', 'test_nonexistent']
        dircache.annotate(self.tempdir, lst)
        self.assertEqual(lst, ['A/', 'test2', 'test_nonexistent'])


def test_main():
    try:
        run_unittest(DircacheTests)
    finally:
        dircache.reset()


if __name__ == '__main__':
    test_main()