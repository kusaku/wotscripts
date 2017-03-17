# Embedded file name: scripts/common/Lib/test/test_tcl.py
import unittest
import os
from test import test_support
_tkinter = test_support.import_module('_tkinter')
from Tkinter import Tcl
from _tkinter import TclError

class TkinterTest(unittest.TestCase):

    def testFlattenLen(self):
        self.assertRaises(TypeError, _tkinter._flatten, True)


class TclTest(unittest.TestCase):

    def setUp(self):
        self.interp = Tcl()

    def testEval(self):
        tcl = self.interp
        tcl.eval('set a 1')
        self.assertEqual(tcl.eval('set a'), '1')

    def testEvalException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.eval, 'set a')

    def testEvalException2(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.eval, 'this is wrong')

    def testCall(self):
        tcl = self.interp
        tcl.call('set', 'a', '1')
        self.assertEqual(tcl.call('set', 'a'), '1')

    def testCallException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.call, 'set', 'a')

    def testCallException2(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.call, 'this', 'is', 'wrong')

    def testSetVar(self):
        tcl = self.interp
        tcl.setvar('a', '1')
        self.assertEqual(tcl.eval('set a'), '1')

    def testSetVarArray(self):
        tcl = self.interp
        tcl.setvar('a(1)', '1')
        self.assertEqual(tcl.eval('set a(1)'), '1')

    def testGetVar(self):
        tcl = self.interp
        tcl.eval('set a 1')
        self.assertEqual(tcl.getvar('a'), '1')

    def testGetVarArray(self):
        tcl = self.interp
        tcl.eval('set a(1) 1')
        self.assertEqual(tcl.getvar('a(1)'), '1')

    def testGetVarException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.getvar, 'a')

    def testGetVarArrayException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.getvar, 'a(1)')

    def testUnsetVar(self):
        tcl = self.interp
        tcl.setvar('a', 1)
        self.assertEqual(tcl.eval('info exists a'), '1')
        tcl.unsetvar('a')
        self.assertEqual(tcl.eval('info exists a'), '0')

    def testUnsetVarArray(self):
        tcl = self.interp
        tcl.setvar('a(1)', 1)
        tcl.setvar('a(2)', 2)
        self.assertEqual(tcl.eval('info exists a(1)'), '1')
        self.assertEqual(tcl.eval('info exists a(2)'), '1')
        tcl.unsetvar('a(1)')
        self.assertEqual(tcl.eval('info exists a(1)'), '0')
        self.assertEqual(tcl.eval('info exists a(2)'), '1')

    def testUnsetVarException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.unsetvar, 'a')

    def testEvalFile(self):
        tcl = self.interp
        filename = 'testEvalFile.tcl'
        fd = open(filename, 'w')
        script = 'set a 1\n        set b 2\n        set c [ expr $a + $b ]\n        '
        fd.write(script)
        fd.close()
        tcl.evalfile(filename)
        os.remove(filename)
        self.assertEqual(tcl.eval('set a'), '1')
        self.assertEqual(tcl.eval('set b'), '2')
        self.assertEqual(tcl.eval('set c'), '3')

    def testEvalFileException(self):
        tcl = self.interp
        filename = 'doesnotexists'
        try:
            os.remove(filename)
        except Exception as e:
            pass

        self.assertRaises(TclError, tcl.evalfile, filename)

    def testPackageRequireException(self):
        tcl = self.interp
        self.assertRaises(TclError, tcl.eval, 'package require DNE')

    def testLoadWithUNC(self):
        import sys
        if sys.platform != 'win32':
            return
        else:
            fullname = os.path.abspath(sys.executable)
            if fullname[1] != ':':
                return
            unc_name = '\\\\%s\\%s$\\%s' % (os.environ['COMPUTERNAME'], fullname[0], fullname[3:])
            with test_support.EnvironmentVarGuard() as env:
                env.unset('TCL_LIBRARY')
                f = os.popen('%s -c "import Tkinter; print Tkinter"' % (unc_name,))
            self.assertTrue('Tkinter.py' in f.read())
            self.assertEqual(f.close(), None)
            return


def test_main():
    test_support.run_unittest(TclTest, TkinterTest)


if __name__ == '__main__':
    test_main()