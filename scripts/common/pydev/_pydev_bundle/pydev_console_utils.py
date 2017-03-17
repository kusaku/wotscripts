# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_console_utils.py
from _pydev_bundle.pydev_imports import xmlrpclib, _queue, Exec
import sys
from _pydevd_bundle.pydevd_constants import IS_JYTHON
from _pydev_imps import _pydev_thread as thread
from _pydevd_bundle import pydevd_xml
from _pydevd_bundle import pydevd_vars
from _pydevd_bundle.pydevd_utils import *
import traceback

class Null():
    """
    Gotten from: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/68205
    """

    def __init__(self, *args, **kwargs):
        return None

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, mname):
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self

    def __repr__(self):
        return '<Null>'

    def __str__(self):
        return 'Null'

    def __len__(self):
        return 0

    def __getitem__(self):
        return self

    def __setitem__(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def __nonzero__(self):
        return 0


class BaseStdIn():

    def __init__(self, *args, **kwargs):
        try:
            self.encoding = sys.stdin.encoding
        except:
            pass

    def readline(self, *args, **kwargs):
        return '\n'

    def isatty(self):
        return False

    def write(self, *args, **kwargs):
        pass

    def flush(self, *args, **kwargs):
        pass

    def read(self, *args, **kwargs):
        return self.readline()

    def close(self, *args, **kwargs):
        pass


class StdIn(BaseStdIn):
    """
        Object to be added to stdin (to emulate it as non-blocking while the next line arrives)
    """

    def __init__(self, interpreter, host, client_port):
        BaseStdIn.__init__(self)
        self.interpreter = interpreter
        self.client_port = client_port
        self.host = host

    def readline(self, *args, **kwargs):
        try:
            server = xmlrpclib.Server('http://%s:%s' % (self.host, self.client_port))
            requested_input = server.RequestInput()
            if not requested_input:
                return '\n'
            return requested_input
        except:
            return '\n'


class CodeFragment():

    def __init__(self, text, is_single_line = True):
        self.text = text
        self.is_single_line = is_single_line

    def append(self, code_fragment):
        self.text = self.text + '\n' + code_fragment.text
        if not code_fragment.is_single_line:
            self.is_single_line = False


class BaseInterpreterInterface():

    def __init__(self, mainThread):
        self.mainThread = mainThread
        self.interruptable = False
        self.exec_queue = _queue.Queue(0)
        self.buffer = None
        return

    def need_more_for_code(self, source):
        if source.endswith('\\'):
            return True
        elif hasattr(self.interpreter, 'is_complete'):
            return not self.interpreter.is_complete(source)
        try:
            code = self.interpreter.compile(source, '<input>', 'exec')
        except (OverflowError, SyntaxError, ValueError):
            return False

        if code is None:
            return True
        else:
            return False

    def need_more(self, code_fragment):
        if self.buffer is None:
            self.buffer = code_fragment
        else:
            self.buffer.append(code_fragment)
        return self.need_more_for_code(self.buffer.text)

    def create_std_in(self):
        return StdIn(self, self.host, self.client_port)

    def add_exec(self, code_fragment):
        original_in = sys.stdin
        try:
            help = None
            if 'pydoc' in sys.modules:
                pydoc = sys.modules['pydoc']
                if hasattr(pydoc, 'help'):
                    help = pydoc.help
                    if not hasattr(help, 'input'):
                        help = None
        except:
            pass

        more = False
        try:
            sys.stdin = self.create_std_in()
            try:
                if help is not None:
                    try:
                        try:
                            help.input = sys.stdin
                        except AttributeError:
                            help._input = sys.stdin

                    except:
                        help = None
                        if not self._input_error_printed:
                            self._input_error_printed = True
                            sys.stderr.write('\nError when trying to update pydoc.help.input\n')
                            sys.stderr.write('(help() may not work -- please report this as a bug in the pydev bugtracker).\n\n')
                            traceback.print_exc()

                try:
                    self.start_exec()
                    if hasattr(self, 'debugger'):
                        from _pydevd_bundle import pydevd_tracing
                        pydevd_tracing.SetTrace(self.debugger.trace_dispatch)
                    more = self.do_add_exec(code_fragment)
                    if hasattr(self, 'debugger'):
                        from _pydevd_bundle import pydevd_tracing
                        pydevd_tracing.SetTrace(None)
                    self.finish_exec(more)
                finally:
                    if help is not None:
                        try:
                            try:
                                help.input = original_in
                            except AttributeError:
                                help._input = original_in

                        except:
                            pass

            finally:
                sys.stdin = original_in

        except SystemExit:
            raise
        except:
            traceback.print_exc()

        return more

    def do_add_exec(self, codeFragment):
        """
        Subclasses should override.
        
        @return: more (True if more input is needed to complete the statement and False if the statement is complete).
        """
        raise NotImplementedError()

    def get_namespace(self):
        """
        Subclasses should override.
        
        @return: dict with namespace.
        """
        raise NotImplementedError()

    def getDescription(self, text):
        try:
            obj = None
            if '.' not in text:
                try:
                    obj = self.get_namespace()[text]
                except KeyError:
                    return ''

            else:
                try:
                    splitted = text.split('.')
                    obj = self.get_namespace()[splitted[0]]
                    for t in splitted[1:]:
                        obj = getattr(obj, t)

                except:
                    return ''

            if obj is not None:
                try:
                    if sys.platform.startswith('java'):
                        doc = obj.__doc__
                        if doc is not None:
                            return doc
                        from _pydev_bundle import _pydev_jy_imports_tipper
                        is_method, infos = _pydev_jy_imports_tipper.ismethod(obj)
                        ret = ''
                        if is_method:
                            for info in infos:
                                ret += info.get_as_doc()

                            return ret
                    else:
                        import inspect
                        doc = inspect.getdoc(obj)
                        if doc is not None:
                            return doc
                except:
                    pass

            try:
                return repr(obj)
            except:
                try:
                    return str(obj.__class__)
                except:
                    return ''

        except:
            traceback.print_exc()
            return ''

        return

    def do_exec_code(self, code, is_single_line):
        try:
            code_fragment = CodeFragment(code, is_single_line)
            more = self.need_more(code_fragment)
            if not more:
                code_fragment = self.buffer
                self.buffer = None
                self.exec_queue.put(code_fragment)
            return more
        except:
            traceback.print_exc()
            return False

        return

    def execLine(self, line):
        return self.do_exec_code(line, True)

    def execMultipleLines(self, lines):
        if IS_JYTHON:
            for line in lines.split('\n'):
                self.do_exec_code(line, True)

        else:
            return self.do_exec_code(lines, False)

    def interrupt(self):
        self.buffer = None
        try:
            if self.interruptable:
                called = False
                try:
                    import os
                    import signal
                    if os.name == 'posix':
                        os.kill(os.getpid(), signal.SIGINT)
                        called = True
                    elif os.name == 'nt':
                        os.kill(0, signal.CTRL_C_EVENT)
                        called = True
                except:
                    pass

                if not called:
                    if hasattr(thread, 'interrupt_main'):
                        thread.interrupt_main()
                    else:
                        self.mainThread._thread.interrupt()
            return True
        except:
            traceback.print_exc()
            return False

        return

    def close(self):
        sys.exit(0)

    def start_exec(self):
        self.interruptable = True

    def get_server(self):
        if getattr(self, 'host', None) is not None:
            return xmlrpclib.Server('http://%s:%s' % (self.host, self.client_port))
        else:
            return
            return

    server = property(get_server)

    def finish_exec(self, more):
        self.interruptable = False
        server = self.get_server()
        if server is not None:
            return server.NotifyFinished(more)
        else:
            return True
            return

    def getFrame(self):
        xml = '<xml>'
        xml += pydevd_xml.frame_vars_to_xml(self.get_namespace())
        xml += '</xml>'
        return xml

    def getVariable(self, attributes):
        xml = '<xml>'
        valDict = pydevd_vars.resolve_var(self.get_namespace(), attributes)
        if valDict is None:
            valDict = {}
        keys = valDict.keys()
        for k in keys:
            xml += pydevd_vars.var_to_xml(valDict[k], to_string(k))

        xml += '</xml>'
        return xml

    def getArray(self, attr, roffset, coffset, rows, cols, format):
        xml = '<xml>'
        name = attr.split('\t')[-1]
        array = pydevd_vars.eval_in_context(name, self.get_namespace(), self.get_namespace())
        array, metaxml, r, c, f = pydevd_vars.array_to_meta_xml(array, name, format)
        xml += metaxml
        format = '%' + f
        if rows == -1 and cols == -1:
            rows = r
            cols = c
        xml += pydevd_vars.array_to_xml(array, roffset, coffset, rows, cols, format)
        xml += '</xml>'
        return xml

    def evaluate(self, expression):
        xml = '<xml>'
        result = pydevd_vars.eval_in_context(expression, self.get_namespace(), self.get_namespace())
        xml += pydevd_vars.var_to_xml(result, expression)
        xml += '</xml>'
        return xml

    def changeVariable(self, attr, value):

        def do_change_variable():
            Exec('%s=%s' % (attr, value), self.get_namespace(), self.get_namespace())

        self.exec_queue.put(do_change_variable)

    def _findFrame(self, thread_id, frame_id):
        """
        Used to show console with variables connection.
        Always return a frame where the locals map to our internal namespace.
        """
        VIRTUAL_FRAME_ID = '1'
        VIRTUAL_CONSOLE_ID = 'console_main'
        if thread_id == VIRTUAL_CONSOLE_ID and frame_id == VIRTUAL_FRAME_ID:
            f = FakeFrame()
            f.f_globals = {}
            f.f_locals = self.get_namespace()
            return f
        else:
            return self.orig_find_frame(thread_id, frame_id)

    def connectToDebugger(self, debuggerPort):
        """
        Used to show console with variables connection.
        Mainly, monkey-patches things in the debugger structure so that the debugger protocol works.
        """

        def do_connect_to_debugger():
            try:
                import pydevd
                from _pydev_imps import _pydev_threading as threading
            except:
                traceback.print_exc()
                sys.stderr.write('pydevd is not available, cannot connect\n')

            from _pydev_bundle import pydev_localhost
            threading.currentThread().__pydevd_id__ = 'console_main'
            self.orig_find_frame = pydevd_vars.find_frame
            pydevd_vars.find_frame = self._findFrame
            self.debugger = pydevd.PyDB()
            try:
                self.debugger.connect(pydev_localhost.get_localhost(), debuggerPort)
                self.debugger.prepare_to_run()
                from _pydevd_bundle import pydevd_tracing
                pydevd_tracing.SetTrace(None)
            except:
                traceback.print_exc()
                sys.stderr.write('Failed to connect to target debugger.\n')

            self.debugrunning = False
            try:
                import pydevconsole
                pydevconsole.set_debug_hook(self.debugger.process_internal_commands)
            except:
                traceback.print_exc()
                sys.stderr.write('Version of Python does not support debuggable Interactive Console.\n')

            return

        self.exec_queue.put(do_connect_to_debugger)
        return ('connect complete',)

    def hello(self, input_str):
        return ('Hello eclipse',)

    def enableGui(self, guiname):
        """ Enable the GUI specified in guiname (see inputhook for list).
            As with IPython, enabling multiple GUIs isn't an error, but
            only the last one's main loop runs and it may not work
        """

        def do_enable_gui():
            from _pydev_bundle.pydev_versioncheck import versionok_for_gui
            if versionok_for_gui():
                try:
                    from pydev_ipython.inputhook import enable_gui
                    enable_gui(guiname)
                except:
                    sys.stderr.write("Failed to enable GUI event loop integration for '%s'\n" % guiname)
                    traceback.print_exc()

            elif guiname not in ('none', '', None):
                sys.stderr.write("PyDev console: Python version does not support GUI event loop integration for '%s'\n" % guiname)
            return guiname

        self.exec_queue.put(do_enable_gui)


class FakeFrame():
    """
    Used to show console with variables connection.
    A class to be used as a mock of a frame.
    """
    pass