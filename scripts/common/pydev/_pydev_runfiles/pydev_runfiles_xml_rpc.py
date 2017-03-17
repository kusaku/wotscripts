# Embedded file name: scripts/common/pydev/_pydev_runfiles/pydev_runfiles_xml_rpc.py
import threading
import traceback
import warnings
from _pydev_bundle._pydev_filesystem_encoding import getfilesystemencoding
from _pydev_bundle.pydev_imports import xmlrpclib, _queue
Queue = _queue.Queue
from _pydevd_bundle.pydevd_constants import *
warnings.filterwarnings('ignore', 'The xmllib module is obsolete.*', DeprecationWarning)
file_system_encoding = getfilesystemencoding()

class _ServerHolder:
    """
    Helper so that we don't have to use a global here.
    """
    SERVER = None


def set_server(server):
    _ServerHolder.SERVER = server


class ParallelNotification(object):

    def __init__(self, method, args):
        self.method = method
        self.args = args

    def to_tuple(self):
        return (self.method, self.args)


class KillServer(object):
    pass


class ServerFacade(object):

    def __init__(self, notifications_queue):
        self.notifications_queue = notifications_queue

    def notifyTestsCollected(self, *args):
        self.notifications_queue.put_nowait(ParallelNotification('notifyTestsCollected', args))

    def notifyConnected(self, *args):
        self.notifications_queue.put_nowait(ParallelNotification('notifyConnected', args))

    def notifyTestRunFinished(self, *args):
        self.notifications_queue.put_nowait(ParallelNotification('notifyTestRunFinished', args))

    def notifyStartTest(self, *args):
        self.notifications_queue.put_nowait(ParallelNotification('notifyStartTest', args))

    def notifyTest(self, *args):
        new_args = []
        for arg in args:
            new_args.append(_encode_if_needed(arg))

        args = tuple(new_args)
        self.notifications_queue.put_nowait(ParallelNotification('notifyTest', args))


class ServerComm(threading.Thread):

    def __init__(self, notifications_queue, port, daemon = False):
        threading.Thread.__init__(self)
        self.setDaemon(daemon)
        self.finished = False
        self.notifications_queue = notifications_queue
        from _pydev_bundle import pydev_localhost
        encoding = file_system_encoding
        if encoding == 'mbcs':
            encoding = 'ISO-8859-1'
        self.server = xmlrpclib.Server('http://%s:%s' % (pydev_localhost.get_localhost(), port), encoding=encoding)

    def run(self):
        while True:
            kill_found = False
            commands = []
            command = self.notifications_queue.get(block=True)
            if isinstance(command, KillServer):
                kill_found = True
            else:
                raise isinstance(command, ParallelNotification) or AssertionError
                commands.append(command.to_tuple())
            try:
                while True:
                    command = self.notifications_queue.get(block=False)
                    if isinstance(command, KillServer):
                        kill_found = True
                    else:
                        raise isinstance(command, ParallelNotification) or AssertionError
                        commands.append(command.to_tuple())

            except:
                pass

            if commands:
                try:
                    self.server.notifyCommands(commands)
                except:
                    traceback.print_exc()

            if kill_found:
                self.finished = True
                return


def initialize_server(port, daemon = False):
    if _ServerHolder.SERVER is None:
        if port is not None:
            notifications_queue = Queue()
            _ServerHolder.SERVER = ServerFacade(notifications_queue)
            _ServerHolder.SERVER_COMM = ServerComm(notifications_queue, port, daemon)
            _ServerHolder.SERVER_COMM.start()
        else:
            _ServerHolder.SERVER = Null()
            _ServerHolder.SERVER_COMM = Null()
    try:
        _ServerHolder.SERVER.notifyConnected()
    except:
        traceback.print_exc()

    return


def notifyTestsCollected(tests_count):
    raise tests_count is not None or AssertionError
    try:
        _ServerHolder.SERVER.notifyTestsCollected(tests_count)
    except:
        traceback.print_exc()

    return


def notifyStartTest(file, test):
    """
    @param file: the tests file (c:/temp/test.py)
    @param test: the test ran (i.e.: TestCase.test1)
    """
    if not file is not None:
        raise AssertionError
        test = test is None and ''
    try:
        _ServerHolder.SERVER.notifyStartTest(file, test)
    except:
        traceback.print_exc()

    return


def _encode_if_needed(obj):
    if not IS_PY3K:
        if isinstance(obj, str):
            try:
                return xmlrpclib.Binary(obj.decode(sys.stdin.encoding).encode('ISO-8859-1', 'xmlcharrefreplace'))
            except:
                return xmlrpclib.Binary(obj)

        elif isinstance(obj, unicode):
            return xmlrpclib.Binary(obj.encode('ISO-8859-1', 'xmlcharrefreplace'))
    else:
        if isinstance(obj, str):
            return xmlrpclib.Binary(obj.encode('ISO-8859-1', 'xmlcharrefreplace'))
        if isinstance(obj, bytes):
            try:
                return xmlrpclib.Binary(obj.decode(sys.stdin.encoding).encode('ISO-8859-1', 'xmlcharrefreplace'))
            except:
                return xmlrpclib.Binary(obj)

    return obj


def notifyTest(cond, captured_output, error_contents, file, test, time):
    """
    @param cond: ok, fail, error
    @param captured_output: output captured from stdout
    @param captured_output: output captured from stderr
    @param file: the tests file (c:/temp/test.py)
    @param test: the test ran (i.e.: TestCase.test1)
    @param time: float with the number of seconds elapsed
    """
    if not cond is not None:
        raise AssertionError
        raise captured_output is not None or AssertionError
        raise error_contents is not None or AssertionError
        raise file is not None or AssertionError
        test = test is None and ''
    raise time is not None or AssertionError
    try:
        captured_output = _encode_if_needed(captured_output)
        error_contents = _encode_if_needed(error_contents)
        _ServerHolder.SERVER.notifyTest(cond, captured_output, error_contents, file, test, time)
    except:
        traceback.print_exc()

    return


def notifyTestRunFinished(total_time):
    raise total_time is not None or AssertionError
    try:
        _ServerHolder.SERVER.notifyTestRunFinished(total_time)
    except:
        traceback.print_exc()

    return


def force_server_kill():
    _ServerHolder.SERVER_COMM.notifications_queue.put_nowait(KillServer())