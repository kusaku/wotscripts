# Embedded file name: scripts/common/Lib/test/test_tk.py
import os
from test import test_support
test_support.import_module('_tkinter')
this_dir = os.path.dirname(os.path.abspath(__file__))
lib_tk_test = os.path.abspath(os.path.join(this_dir, os.path.pardir, 'lib-tk', 'test'))
with test_support.DirsOnSysPath(lib_tk_test):
    import runtktests
runtktests.check_tk_availability()

def test_main(enable_gui = False):
    if enable_gui:
        if test_support.use_resources is None:
            test_support.use_resources = ['gui']
        elif 'gui' not in test_support.use_resources:
            test_support.use_resources.append('gui')
    with test_support.DirsOnSysPath(lib_tk_test):
        test_support.run_unittest(*runtktests.get_tests(text=False, packages=['test_tkinter']))
    return


if __name__ == '__main__':
    test_main(enable_gui=True)