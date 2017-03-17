# Embedded file name: scripts/common/Lib/test/test_cmd_line_script.py
import unittest
import os
import os.path
import test.test_support
from test.script_helper import run_python, temp_dir, make_script, compile_script, make_pkg, make_zip_script, make_zip_pkg
verbose = test.test_support.verbose
test_source = "# Script may be run with optimisation enabled, so don't rely on assert\n# statements being executed\ndef assertEqual(lhs, rhs):\n    if lhs != rhs:\n        raise AssertionError('%r != %r' % (lhs, rhs))\ndef assertIdentical(lhs, rhs):\n    if lhs is not rhs:\n        raise AssertionError('%r is not %r' % (lhs, rhs))\n# Check basic code execution\nresult = ['Top level assignment']\ndef f():\n    result.append('Lower level reference')\nf()\nassertEqual(result, ['Top level assignment', 'Lower level reference'])\n# Check population of magic variables\nassertEqual(__name__, '__main__')\nprint '__file__==%r' % __file__\nprint '__package__==%r' % __package__\n# Check the sys module\nimport sys\nassertIdentical(globals(), sys.modules[__name__].__dict__)\nprint 'sys.argv[0]==%r' % sys.argv[0]\n"

def _make_test_script(script_dir, script_basename, source = test_source):
    return make_script(script_dir, script_basename, source)


def _make_test_zip_pkg(zip_dir, zip_basename, pkg_name, script_basename, source = test_source, depth = 1):
    return make_zip_pkg(zip_dir, zip_basename, pkg_name, script_basename, source, depth)


launch_source = 'import sys, os.path, runpy\nsys.path.insert(0, %s)\nrunpy._run_module_as_main(%r)\n'

def _make_launch_script(script_dir, script_basename, module_name, path = None):
    if path is None:
        path = 'os.path.dirname(__file__)'
    else:
        path = repr(path)
    source = launch_source % (path, module_name)
    return make_script(script_dir, script_basename, source)


class CmdLineTest(unittest.TestCase):

    def _check_script(self, script_name, expected_file, expected_argv0, expected_package, *cmd_line_switches):
        run_args = cmd_line_switches + (script_name,)
        exit_code, data = run_python(*run_args)
        if verbose:
            print 'Output from test script %r:' % script_name
            print data
        self.assertEqual(exit_code, 0)
        printed_file = '__file__==%r' % expected_file
        printed_argv0 = 'sys.argv[0]==%r' % expected_argv0
        printed_package = '__package__==%r' % expected_package
        if verbose:
            print 'Expected output:'
            print printed_file
            print printed_package
            print printed_argv0
        self.assertIn(printed_file, data)
        self.assertIn(printed_package, data)
        self.assertIn(printed_argv0, data)

    def _check_import_error(self, script_name, expected_msg, *cmd_line_switches):
        run_args = cmd_line_switches + (script_name,)
        exit_code, data = run_python(*run_args)
        if verbose:
            print 'Output from test script %r:' % script_name
            print data
            print 'Expected output: %r' % expected_msg
        self.assertIn(expected_msg, data)

    def test_basic_script(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, 'script')
            self._check_script(script_name, script_name, script_name, None)
        return

    def test_script_compiled(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, 'script')
            compiled_name = compile_script(script_name)
            os.remove(script_name)
            self._check_script(compiled_name, compiled_name, compiled_name, None)
        return

    def test_directory(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, '__main__')
            self._check_script(script_dir, script_name, script_dir, '')

    def test_directory_compiled(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, '__main__')
            compiled_name = compile_script(script_name)
            os.remove(script_name)
            self._check_script(script_dir, compiled_name, script_dir, '')

    def test_directory_error(self):
        with temp_dir() as script_dir:
            msg = "can't find '__main__' module in %r" % script_dir
            self._check_import_error(script_dir, msg)

    def test_zipfile(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, '__main__')
            zip_name, run_name = make_zip_script(script_dir, 'test_zip', script_name)
            self._check_script(zip_name, run_name, zip_name, '')

    def test_zipfile_compiled(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, '__main__')
            compiled_name = compile_script(script_name)
            zip_name, run_name = make_zip_script(script_dir, 'test_zip', compiled_name)
            self._check_script(zip_name, run_name, zip_name, '')

    def test_zipfile_error(self):
        with temp_dir() as script_dir:
            script_name = _make_test_script(script_dir, 'not_main')
            zip_name, run_name = make_zip_script(script_dir, 'test_zip', script_name)
            msg = "can't find '__main__' module in %r" % zip_name
            self._check_import_error(zip_name, msg)

    def test_module_in_package(self):
        with temp_dir() as script_dir:
            pkg_dir = os.path.join(script_dir, 'test_pkg')
            make_pkg(pkg_dir)
            script_name = _make_test_script(pkg_dir, 'script')
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg.script')
            self._check_script(launch_name, script_name, script_name, 'test_pkg')

    def test_module_in_package_in_zipfile(self):
        with temp_dir() as script_dir:
            zip_name, run_name = _make_test_zip_pkg(script_dir, 'test_zip', 'test_pkg', 'script')
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg.script', zip_name)
            self._check_script(launch_name, run_name, run_name, 'test_pkg')

    def test_module_in_subpackage_in_zipfile(self):
        with temp_dir() as script_dir:
            zip_name, run_name = _make_test_zip_pkg(script_dir, 'test_zip', 'test_pkg', 'script', depth=2)
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg.test_pkg.script', zip_name)
            self._check_script(launch_name, run_name, run_name, 'test_pkg.test_pkg')

    def test_package(self):
        with temp_dir() as script_dir:
            pkg_dir = os.path.join(script_dir, 'test_pkg')
            make_pkg(pkg_dir)
            script_name = _make_test_script(pkg_dir, '__main__')
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg')
            self._check_script(launch_name, script_name, script_name, 'test_pkg')

    def test_package_compiled(self):
        with temp_dir() as script_dir:
            pkg_dir = os.path.join(script_dir, 'test_pkg')
            make_pkg(pkg_dir)
            script_name = _make_test_script(pkg_dir, '__main__')
            compiled_name = compile_script(script_name)
            os.remove(script_name)
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg')
            self._check_script(launch_name, compiled_name, compiled_name, 'test_pkg')

    def test_package_error(self):
        with temp_dir() as script_dir:
            pkg_dir = os.path.join(script_dir, 'test_pkg')
            make_pkg(pkg_dir)
            msg = "'test_pkg' is a package and cannot be directly executed"
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg')
            self._check_import_error(launch_name, msg)

    def test_package_recursion(self):
        with temp_dir() as script_dir:
            pkg_dir = os.path.join(script_dir, 'test_pkg')
            make_pkg(pkg_dir)
            main_dir = os.path.join(pkg_dir, '__main__')
            make_pkg(main_dir)
            msg = "Cannot use package as __main__ module; 'test_pkg' is a package and cannot be directly executed"
            launch_name = _make_launch_script(script_dir, 'launch', 'test_pkg')
            self._check_import_error(launch_name, msg)


def test_main():
    test.test_support.run_unittest(CmdLineTest)
    test.test_support.reap_children()


if __name__ == '__main__':
    test_main()