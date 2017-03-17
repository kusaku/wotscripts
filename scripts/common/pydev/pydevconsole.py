# Embedded file name: scripts/common/pydev/pydevconsole.py
"""
Entry point module to start the interactive console.
"""
from _pydev_imps._pydev_thread import start_new_thread
try:
    from code import InteractiveConsole
except ImportError:
    from _pydevd_bundle.pydevconsole_code_for_ironpython import InteractiveConsole

from code import compile_command
from code import InteractiveInterpreter
import os
import sys
from _pydev_imps import _pydev_threading as threading
import traceback
from _pydev_bundle import fix_getpass
fix_getpass.fix_getpass()
from _pydevd_bundle import pydevd_vars
from _pydev_bundle.pydev_imports import Exec, _queue
try:
    import __builtin__
except:
    import builtins as __builtin__

try:
    False
    True
except NameError:
    import __builtin__
    setattr(__builtin__, 'True', 1)
    setattr(__builtin__, 'False', 0)

from _pydev_bundle.pydev_console_utils import BaseInterpreterInterface, BaseStdIn
from _pydev_bundle.pydev_console_utils import CodeFragment
IS_PYTHON_3K = False
IS_PY24 = False
try:
    if sys.version_info[0] == 3:
        IS_PYTHON_3K = True
    elif sys.version_info[0] == 2 and sys.version_info[1] == 4:
        IS_PY24 = True
except:
    pass

class Command:

    def __init__(self, interpreter, code_fragment):
        """
        :type code_fragment: CodeFragment
        :type interpreter: InteractiveConsole
        """
        self.interpreter = interpreter
        self.code_fragment = code_fragment
        self.more = None
        return

    def symbol_for_fragment(code_fragment):
        if code_fragment.is_single_line:
            symbol = 'single'
        else:
            symbol = 'exec'
        return symbol

    symbol_for_fragment = staticmethod(symbol_for_fragment)

    def run(self):
        text = self.code_fragment.text
        symbol = self.symbol_for_fragment(self.code_fragment)
        self.more = self.interpreter.runsource(text, '<input>', symbol)


try:
    try:
        execfile
    except NameError:
        from _pydev_bundle.pydev_imports import execfile
        __builtin__.execfile = execfile

except:
    pass

from _pydev_bundle.pydev_umd import runfile, _set_globals_function
try:
    import builtins
    builtins.runfile = runfile
except:
    import __builtin__
    __builtin__.runfile = runfile

class InterpreterInterface(BaseInterpreterInterface):
    """
        The methods in this class should be registered in the xml-rpc server.
    """

    def __init__(self, host, client_port, mainThread, show_banner = True):
        BaseInterpreterInterface.__init__(self, mainThread)
        self.client_port = client_port
        self.host = host
        self.namespace = {}
        self.interpreter = InteractiveConsole(self.namespace)
        self._input_error_printed = False

    def do_add_exec(self, codeFragment):
        command = Command(self.interpreter, codeFragment)
        command.run()
        return command.more

    def get_namespace(self):
        return self.namespace

    def getCompletions(self, text, act_tok):
        try:
            from _pydev_bundle._pydev_completer import Completer
            completer = Completer(self.namespace, None)
            return completer.complete(act_tok)
        except:
            import traceback
            traceback.print_exc()
            return []

        return

    def close(self):
        sys.exit(0)

    def get_greeting_msg(self):
        return 'PyDev console: starting.\n'


class _ProcessExecQueueHelper:
    _debug_hook = None
    _return_control_osc = False


def set_debug_hook(debug_hook):
    _ProcessExecQueueHelper._debug_hook = debug_hook


def process_exec_queue--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        ('get_inputhook', 'set_return_control_callback')
6	IMPORT_NAME       'pydev_ipython.inputhook'
9	IMPORT_FROM       'get_inputhook'
12	STORE_FAST        'get_inputhook'
15	IMPORT_FROM       'set_return_control_callback'
18	STORE_FAST        'set_return_control_callback'
21	POP_TOP           None

22	LOAD_CLOSURE      'interpreter'
28	LOAD_CONST        '<code_object return_control>'
31	MAKE_CLOSURE_0    None
34	STORE_FAST        'return_control'

37	LOAD_FAST         'set_return_control_callback'
40	LOAD_FAST         'return_control'
43	CALL_FUNCTION_1   None
46	POP_TOP           None

47	LOAD_CONST        -1
50	LOAD_CONST        ('import_hook_manager',)
53	IMPORT_NAME       '_pydev_bundle.pydev_import_hook'
56	IMPORT_FROM       'import_hook_manager'
59	STORE_FAST        'import_hook_manager'
62	POP_TOP           None

63	LOAD_CONST        -1
66	LOAD_CONST        ('activate_matplotlib', 'activate_pylab', 'activate_pyplot')
69	IMPORT_NAME       'pydev_ipython.matplotlibtools'
72	IMPORT_FROM       'activate_matplotlib'
75	STORE_DEREF       'activate_matplotlib'
78	IMPORT_FROM       'activate_pylab'
81	STORE_FAST        'activate_pylab'
84	IMPORT_FROM       'activate_pyplot'
87	STORE_FAST        'activate_pyplot'
90	POP_TOP           None

91	LOAD_FAST         'import_hook_manager'
94	LOAD_ATTR         'add_module_name'
97	LOAD_CONST        'matplotlib'
100	LOAD_CLOSURE      'activate_matplotlib'
103	LOAD_CLOSURE      'interpreter'
109	LOAD_LAMBDA       '<code_object <lambda>>'
112	MAKE_CLOSURE_0    None
115	CALL_FUNCTION_2   None
118	POP_TOP           None

119	LOAD_FAST         'import_hook_manager'
122	LOAD_ATTR         'add_module_name'
125	LOAD_CONST        'pylab'
128	LOAD_FAST         'activate_pylab'
131	CALL_FUNCTION_2   None
134	POP_TOP           None

135	LOAD_FAST         'import_hook_manager'
138	LOAD_ATTR         'add_module_name'
141	LOAD_CONST        'pyplot'
144	LOAD_FAST         'activate_pyplot'
147	CALL_FUNCTION_2   None
150	POP_TOP           None

151	SETUP_LOOP        '456'

154	LOAD_FAST         'get_inputhook'
157	CALL_FUNCTION_0   None
160	STORE_FAST        'inputhook'

163	LOAD_GLOBAL       '_ProcessExecQueueHelper'
166	LOAD_ATTR         '_debug_hook'
169	POP_JUMP_IF_FALSE '185'

172	LOAD_GLOBAL       '_ProcessExecQueueHelper'
175	LOAD_ATTR         '_debug_hook'
178	CALL_FUNCTION_0   None
181	POP_TOP           None
182	JUMP_FORWARD      '185'
185_0	COME_FROM         '182'

185	LOAD_FAST         'inputhook'
188	POP_JUMP_IF_FALSE '237'

191	SETUP_EXCEPT      '205'

194	LOAD_FAST         'inputhook'
197	CALL_FUNCTION_0   None
200	POP_TOP           None
201	POP_BLOCK         None
202	JUMP_ABSOLUTE     '237'
205_0	COME_FROM         '191'

205	POP_TOP           None
206	POP_TOP           None
207	POP_TOP           None

208	LOAD_CONST        -1
211	LOAD_CONST        None
214	IMPORT_NAME       'traceback'
217	STORE_FAST        'traceback'
220	LOAD_FAST         'traceback'
223	LOAD_ATTR         'print_exc'
226	CALL_FUNCTION_0   None
229	POP_TOP           None
230	JUMP_ABSOLUTE     '237'
233	END_FINALLY       None
234_0	COME_FROM         '233'
234	JUMP_FORWARD      '237'
237_0	COME_FROM         '234'

237	SETUP_EXCEPT      '342'

240	SETUP_EXCEPT      '278'

243	LOAD_DEREF        'interpreter'
246	LOAD_ATTR         'exec_queue'
249	LOAD_ATTR         'get'
252	LOAD_CONST        'block'
255	LOAD_GLOBAL       'True'
258	LOAD_CONST        'timeout'
261	LOAD_CONST        1
264	LOAD_CONST        20.0
267	BINARY_DIVIDE     None
268	CALL_FUNCTION_512 None
271	STORE_FAST        'code_fragment'
274	POP_BLOCK         None
275	JUMP_FORWARD      '301'
278_0	COME_FROM         '240'

278	DUP_TOP           None
279	LOAD_GLOBAL       '_queue'
282	LOAD_ATTR         'Empty'
285	COMPARE_OP        'exception match'
288	POP_JUMP_IF_FALSE '300'
291	POP_TOP           None
292	POP_TOP           None
293	POP_TOP           None

294	CONTINUE_LOOP     '154'
297	JUMP_FORWARD      '301'
300	END_FINALLY       None
301_0	COME_FROM         '275'
301_1	COME_FROM         '300'

301	LOAD_GLOBAL       'callable'
304	LOAD_FAST         'code_fragment'
307	CALL_FUNCTION_1   None
310	POP_JUMP_IF_FALSE '323'

313	LOAD_FAST         'code_fragment'
316	CALL_FUNCTION_0   None
319	POP_TOP           None
320	JUMP_FORWARD      '338'

323	LOAD_DEREF        'interpreter'
326	LOAD_ATTR         'add_exec'
329	LOAD_FAST         'code_fragment'
332	CALL_FUNCTION_1   None
335	STORE_FAST        'more'
338_0	COME_FROM         '320'
338	POP_BLOCK         None
339	JUMP_BACK         '154'
342_0	COME_FROM         '237'

342	DUP_TOP           None
343	LOAD_GLOBAL       'KeyboardInterrupt'
346	COMPARE_OP        'exception match'
349	POP_JUMP_IF_FALSE '370'
352	POP_TOP           None
353	POP_TOP           None
354	POP_TOP           None

355	LOAD_CONST        None
358	LOAD_DEREF        'interpreter'
361	STORE_ATTR        'buffer'

364	CONTINUE          '154'
367	JUMP_BACK         '154'

370	DUP_TOP           None
371	LOAD_GLOBAL       'SystemExit'
374	COMPARE_OP        'exception match'
377	POP_JUMP_IF_FALSE '389'
380	POP_TOP           None
381	POP_TOP           None
382	POP_TOP           None

383	RAISE_VARARGS_0   None
386	JUMP_BACK         '154'

389	POP_TOP           None
390	POP_TOP           None
391	POP_TOP           None

392	LOAD_GLOBAL       'sys'
395	LOAD_ATTR         'exc_info'
398	CALL_FUNCTION_0   None
401	UNPACK_SEQUENCE_3 None
404	STORE_FAST        'type'
407	STORE_FAST        'value'
410	STORE_FAST        'tb'

413	LOAD_FAST         'traceback'
416	LOAD_ATTR         'print_exception'
419	LOAD_FAST         'type'
422	LOAD_FAST         'value'
425	LOAD_FAST         'tb'
428	LOAD_CONST        'file'
431	LOAD_GLOBAL       'sys'
434	LOAD_ATTR         '__stderr__'
437	CALL_FUNCTION_259 None
440	POP_TOP           None

441	LOAD_GLOBAL       'exit'
444	CALL_FUNCTION_0   None
447	POP_TOP           None
448	JUMP_BACK         '154'
451	END_FINALLY       None
452_0	COME_FROM         '451'
452	JUMP_BACK         '154'
455	POP_BLOCK         None
456_0	COME_FROM         '151'
456	LOAD_CONST        None
459	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 455


if 'IPYTHONENABLE' in os.environ:
    IPYTHON = os.environ['IPYTHONENABLE'] == 'True'
else:
    IPYTHON = True
try:
    try:
        exitfunc = sys.exitfunc
    except AttributeError:
        exitfunc = None

    if IPYTHON:
        from _pydev_bundle.pydev_ipython_console import InterpreterInterface
        if exitfunc is not None:
            sys.exitfunc = exitfunc
        else:
            try:
                delattr(sys, 'exitfunc')
            except:
                pass

except:
    IPYTHON = False

def do_exit(*args):
    """
        We have to override the exit because calling sys.exit will only actually exit the main thread,
        and as we're in a Xml-rpc server, that won't work.
    """
    try:
        import java.lang.System
        java.lang.System.exit(1)
    except ImportError:
        if len(args) == 1:
            os._exit(args[0])
        else:
            os._exit(0)


def handshake():
    return 'PyCharm'


def start_console_server(host, port, interpreter):
    if port == 0:
        host = ''
    from _pydev_bundle.pydev_imports import SimpleXMLRPCServer as XMLRPCServer
    try:
        if IS_PY24:
            server = XMLRPCServer((host, port), logRequests=False)
        else:
            server = XMLRPCServer((host, port), logRequests=False, allow_none=True)
    except:
        sys.stderr.write('Error starting server with host: %s, port: %s, client_port: %s\n' % (host, port, interpreter.client_port))
        raise

    _set_globals_function(interpreter.get_namespace)
    server.register_function(interpreter.execLine)
    server.register_function(interpreter.execMultipleLines)
    server.register_function(interpreter.getCompletions)
    server.register_function(interpreter.getFrame)
    server.register_function(interpreter.getVariable)
    server.register_function(interpreter.changeVariable)
    server.register_function(interpreter.getDescription)
    server.register_function(interpreter.close)
    server.register_function(interpreter.interrupt)
    server.register_function(handshake)
    server.register_function(interpreter.connectToDebugger)
    server.register_function(interpreter.hello)
    server.register_function(interpreter.getArray)
    server.register_function(interpreter.evaluate)
    server.register_function(interpreter.enableGui)
    if port == 0:
        h, port = server.socket.getsockname()
        print port
        print interpreter.client_port
    sys.stderr.write(interpreter.get_greeting_msg())
    sys.stderr.flush()
    while True:
        try:
            server.serve_forever()
        except:
            e = sys.exc_info()[1]
            retry = False
            try:
                retry = e.args[0] == 4
            except:
                pass

            if not retry:
                raise

    return server


def start_server(host, port, client_port):
    sys.exit = do_exit
    interpreter = InterpreterInterface(host, client_port, threading.currentThread())
    start_new_thread(start_console_server, (host, port, interpreter))
    process_exec_queue(interpreter)


def get_interpreter():
    try:
        interpreterInterface = getattr(__builtin__, 'interpreter')
    except AttributeError:
        interpreterInterface = InterpreterInterface(None, None, threading.currentThread())
        setattr(__builtin__, 'interpreter', interpreterInterface)

    return interpreterInterface


def get_completions(text, token, globals, locals):
    interpreterInterface = get_interpreter()
    interpreterInterface.interpreter.update(globals, locals)
    return interpreterInterface.getCompletions(text, token)


def exec_code(code, globals, locals):
    interpreterInterface = get_interpreter()
    interpreterInterface.interpreter.update(globals, locals)
    res = interpreterInterface.need_more(code)
    if res:
        return True
    interpreterInterface.add_exec(code)
    return False


class ConsoleWriter(InteractiveInterpreter):
    skip = 0

    def __init__(self, locals = None):
        InteractiveInterpreter.__init__(self, locals)

    def write(self, data):
        if self.skip > 0:
            self.skip -= 1
        else:
            if data == 'Traceback (most recent call last):\n':
                self.skip = 1
            sys.stderr.write(data)

    def showsyntaxerror(self, filename = None):
        """Display the syntax error that just occurred."""
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        if filename and type is SyntaxError:
            try:
                msg, (dummy_filename, lineno, offset, line) = value.args
            except ValueError:
                pass
            else:
                value = SyntaxError(msg, (filename,
                 lineno,
                 offset,
                 line))
                sys.last_value = value

        list = traceback.format_exception_only(type, value)
        sys.stderr.write(''.join(list))

    def showtraceback(self):
        """Display the exception that just occurred."""
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            lines = traceback.format_list(tblist)
            if lines:
                lines.insert(0, 'Traceback (most recent call last):\n')
            lines.extend(traceback.format_exception_only(type, value))
        finally:
            tblist = tb = None

        sys.stderr.write(''.join(lines))
        return


def console_exec(thread_id, frame_id, expression):
    """returns 'False' in case expression is partially correct
    """
    frame = pydevd_vars.find_frame(thread_id, frame_id)
    expression = str(expression.replace('@LINE@', '\n'))
    updated_globals = {}
    updated_globals.update(frame.f_globals)
    updated_globals.update(frame.f_locals)
    if IPYTHON:
        return exec_code(CodeFragment(expression), updated_globals, frame.f_locals)
    else:
        interpreter = ConsoleWriter()
        try:
            code = compile_command(expression)
        except (OverflowError, SyntaxError, ValueError):
            interpreter.showsyntaxerror()
            return False

        if code is None:
            return True
        try:
            Exec(code, updated_globals, frame.f_locals)
        except SystemExit:
            raise
        except:
            interpreter.showtraceback()

        return False


if __name__ == '__main__':
    import pydevconsole
    sys.stdin = pydevconsole.BaseStdIn()
    port, client_port = sys.argv[1:3]
    from _pydev_bundle import pydev_localhost
    if int(port) == 0 and int(client_port) == 0:
        h, p = pydev_localhost.get_socket_name()
        client_port = p
    pydevconsole.start_server(pydev_localhost.get_localhost(), int(port), int(client_port))