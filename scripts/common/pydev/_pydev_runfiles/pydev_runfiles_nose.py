# Embedded file name: scripts/common/pydev/_pydev_runfiles/pydev_runfiles_nose.py
from nose.plugins.multiprocess import MultiProcessTestRunner
from nose.plugins.base import Plugin
import sys
from _pydev_runfiles import pydev_runfiles_xml_rpc
import time
from _pydev_runfiles.pydev_runfiles_coverage import start_coverage_support

class PydevPlugin(Plugin):

    def __init__(self, configuration):
        self.configuration = configuration
        Plugin.__init__(self)

    def begin(self):
        self.start_time = time.time()
        self.coverage_files, self.coverage = start_coverage_support(self.configuration)

    def finalize(self, result):
        self.coverage.stop()
        self.coverage.save()
        pydev_runfiles_xml_rpc.notifyTestRunFinished('Finished in: %.2f secs.' % (time.time() - self.start_time,))

    def report_cond(self, cond, test, captured_output, error = ''):
        """
        @param cond: fail, error, ok
        """
        try:
            if hasattr(test, 'address'):
                address = test.address()
                address = (address[0], address[2])
            else:
                try:
                    address = (test[0], test[1])
                except TypeError:
                    f = test.context.__file__
                    if f.endswith('.pyc'):
                        f = f[:-1]
                    address = (f, '?')

        except:
            sys.stderr.write('PyDev: Internal pydev error getting test address. Please report at the pydev bug tracker\n')
            import traceback
            traceback.print_exc()
            sys.stderr.write('\n\n\n')
            address = ('?', '?')

        error_contents = self.get_io_from_error(error)
        try:
            time_str = '%.2f' % (time.time() - test._pydev_start_time)
        except:
            time_str = '?'

        pydev_runfiles_xml_rpc.notifyTest(cond, captured_output, error_contents, address[0], address[1], time_str)

    def startTest(self, test):
        test._pydev_start_time = time.time()
        if hasattr(test, 'address'):
            address = test.address()
            file, test = address[0], address[2]
        else:
            file, test = test
        pydev_runfiles_xml_rpc.notifyStartTest(file, test)

    def get_io_from_error(self, err):
        if type(err) == type(()):
            if len(err) != 3:
                if len(err) == 2:
                    return err[1]
            try:
                from StringIO import StringIO
            except:
                from io import StringIO

            s = StringIO()
            etype, value, tb = err
            import traceback
            traceback.print_exception(etype, value, tb, file=s)
            return s.getvalue()
        return err

    def get_captured_output(self, test):
        if hasattr(test, 'capturedOutput') and test.capturedOutput:
            return test.capturedOutput
        return ''

    def addError(self, test, err):
        self.report_cond('error', test, self.get_captured_output(test), err)

    def addFailure(self, test, err):
        self.report_cond('fail', test, self.get_captured_output(test), err)

    def addSuccess(self, test):
        self.report_cond('ok', test, self.get_captured_output(test), '')


PYDEV_NOSE_PLUGIN_SINGLETON = None

def start_pydev_nose_plugin_singleton(configuration):
    global PYDEV_NOSE_PLUGIN_SINGLETON
    PYDEV_NOSE_PLUGIN_SINGLETON = PydevPlugin(configuration)
    return PYDEV_NOSE_PLUGIN_SINGLETON


original = MultiProcessTestRunner.consolidate

def new_consolidate(self, result, batch_result):
    """
    Used so that it can work with the multiprocess plugin.
    Monkeypatched because nose seems a bit unsupported at this time (ideally
    the plugin would have this support by default).
    """
    ret = original(self, result, batch_result)
    parent_frame = sys._getframe().f_back
    addr = parent_frame.f_locals['addr']
    i = addr.rindex(':')
    addr = [addr[:i], addr[i + 1:]]
    output, testsRun, failures, errors, errorClasses = batch_result
    if failures or errors:
        for failure in failures:
            PYDEV_NOSE_PLUGIN_SINGLETON.report_cond('fail', addr, output, failure)

        for error in errors:
            PYDEV_NOSE_PLUGIN_SINGLETON.report_cond('error', addr, output, error)

    else:
        PYDEV_NOSE_PLUGIN_SINGLETON.report_cond('ok', addr, output)
    return ret


MultiProcessTestRunner.consolidate = new_consolidate