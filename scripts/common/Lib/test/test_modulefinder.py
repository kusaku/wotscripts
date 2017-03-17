# Embedded file name: scripts/common/Lib/test/test_modulefinder.py
import __future__
import os
import unittest
import distutils.dir_util
import tempfile
from test import test_support
try:
    set
except NameError:
    from sets import Set as set

import modulefinder
TEST_DIR = tempfile.mkdtemp()
TEST_PATH = [TEST_DIR, os.path.dirname(__future__.__file__)]
maybe_test = ['a.module',
 ['a',
  'a.module',
  'sys',
  'b'],
 ['c'],
 ['b.something'],
 'a/__init__.py\na/module.py\n                                from b import something\n                                from c import something\nb/__init__.py\n                                from sys import *\n']
maybe_test_new = ['a.module',
 ['a',
  'a.module',
  'sys',
  'b',
  '__future__'],
 ['c'],
 ['b.something'],
 'a/__init__.py\na/module.py\n                                from b import something\n                                from c import something\nb/__init__.py\n                                from __future__ import absolute_import\n                                from sys import *\n']
package_test = ['a.module',
 ['a',
  'a.b',
  'a.c',
  'a.module',
  'mymodule',
  'sys'],
 ['blahblah'],
 [],
 'mymodule.py\na/__init__.py\n                                import blahblah\n                                from a import b\n                                import c\na/module.py\n                                import sys\n                                from a import b as x\n                                from a.c import sillyname\na/b.py\na/c.py\n                                from a.module import x\n                                import mymodule as sillyname\n                                from sys import version_info\n']
absolute_import_test = ['a.module',
 ['a',
  'a.module',
  'b',
  'b.x',
  'b.y',
  'b.z',
  '__future__',
  'sys',
  'exceptions'],
 ['blahblah'],
 [],
 'mymodule.py\na/__init__.py\na/module.py\n                                from __future__ import absolute_import\n                                import sys # sys\n                                import blahblah # fails\n                                import exceptions # exceptions\n                                import b.x # b.x\n                                from b import y # b.y\n                                from b.z import * # b.z.*\na/exceptions.py\na/sys.py\n                                import mymodule\na/b/__init__.py\na/b/x.py\na/b/y.py\na/b/z.py\nb/__init__.py\n                                import z\nb/unused.py\nb/x.py\nb/y.py\nb/z.py\n']
relative_import_test = ['a.module',
 ['__future__',
  'a',
  'a.module',
  'a.b',
  'a.b.y',
  'a.b.z',
  'a.b.c',
  'a.b.c.moduleC',
  'a.b.c.d',
  'a.b.c.e',
  'a.b.x',
  'exceptions'],
 [],
 [],
 'mymodule.py\na/__init__.py\n                                from .b import y, z # a.b.y, a.b.z\na/module.py\n                                from __future__ import absolute_import # __future__\n                                import exceptions # exceptions\na/exceptions.py\na/sys.py\na/b/__init__.py\n                                from ..b import x # a.b.x\n                                #from a.b.c import moduleC\n                                from .c import moduleC # a.b.moduleC\na/b/x.py\na/b/y.py\na/b/z.py\na/b/g.py\na/b/c/__init__.py\n                                from ..c import e # a.b.c.e\na/b/c/moduleC.py\n                                from ..c import d # a.b.c.d\na/b/c/d.py\na/b/c/e.py\na/b/c/x.py\n']
relative_import_test_2 = ['a.module',
 ['a',
  'a.module',
  'a.sys',
  'a.b',
  'a.b.y',
  'a.b.z',
  'a.b.c',
  'a.b.c.d',
  'a.b.c.e',
  'a.b.c.moduleC',
  'a.b.c.f',
  'a.b.x',
  'a.another'],
 [],
 [],
 'mymodule.py\na/__init__.py\n                                from . import sys # a.sys\na/another.py\na/module.py\n                                from .b import y, z # a.b.y, a.b.z\na/exceptions.py\na/sys.py\na/b/__init__.py\n                                from .c import moduleC # a.b.c.moduleC\n                                from .c import d # a.b.c.d\na/b/x.py\na/b/y.py\na/b/z.py\na/b/c/__init__.py\n                                from . import e # a.b.c.e\na/b/c/moduleC.py\n                                #\n                                from . import f   # a.b.c.f\n                                from .. import x  # a.b.x\n                                from ... import another # a.another\na/b/c/d.py\na/b/c/e.py\na/b/c/f.py\n']
relative_import_test_3 = ['a.module',
 ['a', 'a.module'],
 ['a.bar'],
 [],
 'a/__init__.py\n                                def foo(): pass\na/module.py\n                                from . import foo\n                                from . import bar\n']

def open_file(path):
    dirname = os.path.dirname(path)
    distutils.dir_util.mkpath(dirname)
    return open(path, 'w')


def create_package(source):
    ofi = None
    try:
        for line in source.splitlines():
            if line.startswith(' ') or line.startswith('\t'):
                ofi.write(line.strip() + '\n')
            else:
                if ofi:
                    ofi.close()
                ofi = open_file(os.path.join(TEST_DIR, line.strip()))

    finally:
        if ofi:
            ofi.close()

    return


class ModuleFinderTest(unittest.TestCase):

    def _do_test(self, info, report = False):
        import_this, modules, missing, maybe_missing, source = info
        create_package(source)
        try:
            mf = modulefinder.ModuleFinder(path=TEST_PATH)
            mf.import_hook(import_this)
            if report:
                mf.report()
            modules = set(modules)
            found = set(mf.modules.keys())
            more = list(found - modules)
            less = list(modules - found)
            self.assertEqual((more, less), ([], []))
            bad, maybe = mf.any_missing_maybe()
            self.assertEqual(bad, missing)
            self.assertEqual(maybe, maybe_missing)
        finally:
            distutils.dir_util.remove_tree(TEST_DIR)

    def test_package(self):
        self._do_test(package_test)

    def test_maybe(self):
        self._do_test(maybe_test)

    if getattr(__future__, 'absolute_import', None):

        def test_maybe_new(self):
            self._do_test(maybe_test_new)

        def test_absolute_imports(self):
            self._do_test(absolute_import_test)

        def test_relative_imports(self):
            self._do_test(relative_import_test)

        def test_relative_imports_2(self):
            self._do_test(relative_import_test_2)

        def test_relative_imports_3(self):
            self._do_test(relative_import_test_3)


def test_main():
    distutils.log.set_threshold(distutils.log.WARN)
    test_support.run_unittest(ModuleFinderTest)


if __name__ == '__main__':
    unittest.main()