# Embedded file name: scripts/common/Lib/test/test___all__.py
from __future__ import print_function
import unittest
from test import test_support as support
import os
import sys
try:
    bsddb = support.import_module('bsddb', deprecated=True)
except unittest.SkipTest:
    pass

class NoAll(RuntimeError):
    pass


class FailedImport(RuntimeError):
    pass


class AllTest(unittest.TestCase):

    def check_all(self, modname):
        names = {}
        with support.check_warnings(('.* (module|package)', DeprecationWarning), quiet=True):
            try:
                exec 'import %s' % modname in names
            except:
                raise FailedImport(modname)

        if not hasattr(sys.modules[modname], '__all__'):
            raise NoAll(modname)
        names = {}
        try:
            exec 'from %s import *' % modname in names
        except Exception as e:
            self.fail('__all__ failure in {}: {}: {}'.format(modname, e.__class__.__name__, e))

        if '__builtins__' in names:
            del names['__builtins__']
        keys = set(names)
        all = set(sys.modules[modname].__all__)
        self.assertEqual(keys, all)

    def walk_modules(self, basedir, modpath):
        for fn in sorted(os.listdir(basedir)):
            path = os.path.join(basedir, fn)
            if os.path.isdir(path):
                pkg_init = os.path.join(path, '__init__.py')
                if os.path.exists(pkg_init):
                    yield (pkg_init, modpath + fn)
                    for p, m in self.walk_modules(path, modpath + fn + '.'):
                        yield (p, m)

                continue
            if not fn.endswith('.py') or fn == '__init__.py':
                continue
            yield (path, modpath + fn[:-3])

    def test_all(self):
        blacklist = set(['__future__'])
        if not sys.platform.startswith('java'):
            import _socket
        try:
            import rlcompleter
            import locale
        except ImportError:
            pass
        else:
            locale.setlocale(locale.LC_CTYPE, 'C')

        ignored = []
        failed_imports = []
        lib_dir = os.path.dirname(os.path.dirname(__file__))
        for path, modname in self.walk_modules(lib_dir, ''):
            m = modname
            blacklisted = False
            while m:
                if m in blacklist:
                    blacklisted = True
                    break
                m = m.rpartition('.')[0]

            if blacklisted:
                continue
            if support.verbose:
                print(modname)
            try:
                with open(path, 'rb') as f:
                    if '__all__' not in f.read():
                        raise NoAll(modname)
                    self.check_all(modname)
            except NoAll:
                ignored.append(modname)
            except FailedImport:
                failed_imports.append(modname)

        if support.verbose:
            print('Following modules have no __all__ and have been ignored:', ignored)
            print('Following modules failed to be imported:', failed_imports)


def test_main():
    support.run_unittest(AllTest)


if __name__ == '__main__':
    test_main()