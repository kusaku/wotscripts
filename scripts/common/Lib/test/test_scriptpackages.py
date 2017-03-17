# Embedded file name: scripts/common/Lib/test/test_scriptpackages.py
import unittest
from test import test_support
test_support.import_module('aetools')

class TestScriptpackages(unittest.TestCase):

    def _test_scriptpackage(self, package, testobject = 1):
        mod = __import__(package)
        klass = getattr(mod, package)
        talker = klass()
        if testobject:
            obj = mod.application(0)

    def test__builtinSuites(self):
        self._test_scriptpackage('_builtinSuites', testobject=0)

    def test_StdSuites(self):
        self._test_scriptpackage('StdSuites')

    def test_SystemEvents(self):
        self._test_scriptpackage('SystemEvents')

    def test_Finder(self):
        self._test_scriptpackage('Finder')

    def test_Terminal(self):
        self._test_scriptpackage('Terminal')

    def test_Netscape(self):
        self._test_scriptpackage('Netscape')

    def test_Explorer(self):
        self._test_scriptpackage('Explorer')

    def test_CodeWarrior(self):
        self._test_scriptpackage('CodeWarrior')


def test_main():
    test_support.run_unittest(TestScriptpackages)


if __name__ == '__main__':
    test_main()