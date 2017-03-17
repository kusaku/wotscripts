# Embedded file name: scripts/common/Lib/idlelib/run.py
import sys
import linecache
import time
import socket
import traceback
import thread
import threading
import Queue
from idlelib import CallTips
from idlelib import AutoComplete
from idlelib import RemoteDebugger
from idlelib import RemoteObjectBrowser
from idlelib import StackViewer
from idlelib import rpc
import __main__
LOCALHOST = '127.0.0.1'
try:
    import warnings
except ImportError:
    pass
else:

    def idle_formatwarning_subproc(message, category, filename, lineno, line = None):
        """Format warnings the IDLE way"""
        s = '\nWarning (from warnings module):\n'
        s += '  File "%s", line %s\n' % (filename, lineno)
        if line is None:
            line = linecache.getline(filename, lineno)
        line = line.strip()
        if line:
            s += '    %s\n' % line
        s += '%s: %s\n' % (category.__name__, message)
        return s


    warnings.formatwarning = idle_formatwarning_subproc

exit_now = False
quitting = False
interruptable = False

def main--- This code section failed: ---

0	LOAD_FAST         'del_exitfunc'
3	STORE_GLOBAL      'no_exitfunc'

6	SETUP_EXCEPT      '59'

9	LOAD_GLOBAL       'len'
12	LOAD_GLOBAL       'sys'
15	LOAD_ATTR         'argv'
18	CALL_FUNCTION_1   None
21	LOAD_CONST        1
24	COMPARE_OP        '>'
27	POP_JUMP_IF_TRUE  '36'
30	LOAD_ASSERT       'AssertionError'
33	RAISE_VARARGS_1   None

36	LOAD_GLOBAL       'int'
39	LOAD_GLOBAL       'sys'
42	LOAD_ATTR         'argv'
45	LOAD_CONST        -1
48	BINARY_SUBSCR     None
49	CALL_FUNCTION_1   None
52	STORE_FAST        'port'
55	POP_BLOCK         None
56	JUMP_FORWARD      '80'
59_0	COME_FROM         '6'

59	POP_TOP           None
60	POP_TOP           None
61	POP_TOP           None

62	LOAD_GLOBAL       'sys'
65	LOAD_ATTR         'stderr'
68	DUP_TOP           None
69	LOAD_CONST        'IDLE Subprocess: no IP port passed in sys.argv.'
72	ROT_TWO           None
73	PRINT_ITEM_TO     None
74	PRINT_NEWLINE_TO  None

75	LOAD_CONST        None
78	RETURN_VALUE      None
79	END_FINALLY       None
80_0	COME_FROM         '56'
80_1	COME_FROM         '79'

80	LOAD_CONST        ''
83	BUILD_LIST_1      None
86	LOAD_GLOBAL       'sys'
89	LOAD_ATTR         'argv'
92	STORE_SLICE+0     None

93	LOAD_GLOBAL       'threading'
96	LOAD_ATTR         'Thread'
99	LOAD_CONST        'target'
102	LOAD_GLOBAL       'manage_socket'
105	LOAD_CONST        'name'

108	LOAD_CONST        'SockThread'
111	LOAD_CONST        'args'

114	LOAD_GLOBAL       'LOCALHOST'
117	LOAD_FAST         'port'
120	BUILD_TUPLE_2     None
123	BUILD_TUPLE_1     None
126	CALL_FUNCTION_768 None
129	STORE_FAST        'sockthread'

132	LOAD_FAST         'sockthread'
135	LOAD_ATTR         'setDaemon'
138	LOAD_GLOBAL       'True'
141	CALL_FUNCTION_1   None
144	POP_TOP           None

145	LOAD_FAST         'sockthread'
148	LOAD_ATTR         'start'
151	CALL_FUNCTION_0   None
154	POP_TOP           None

155	SETUP_LOOP        '489'

158	SETUP_EXCEPT      '323'

161	LOAD_GLOBAL       'exit_now'
164	POP_JUMP_IF_FALSE '204'

167	SETUP_EXCEPT      '181'

170	LOAD_GLOBAL       'exit'
173	CALL_FUNCTION_0   None
176	POP_TOP           None
177	POP_BLOCK         None
178	JUMP_ABSOLUTE     '204'
181_0	COME_FROM         '167'

181	DUP_TOP           None
182	LOAD_GLOBAL       'KeyboardInterrupt'
185	COMPARE_OP        'exception match'
188	POP_JUMP_IF_FALSE '200'
191	POP_TOP           None
192	POP_TOP           None
193	POP_TOP           None

194	CONTINUE_LOOP     '158'
197	JUMP_ABSOLUTE     '204'
200	END_FINALLY       None
201_0	COME_FROM         '200'
201	JUMP_FORWARD      '204'
204_0	COME_FROM         '201'

204	SETUP_EXCEPT      '244'

207	LOAD_GLOBAL       'rpc'
210	LOAD_ATTR         'request_queue'
213	LOAD_ATTR         'get'
216	LOAD_CONST        'block'
219	LOAD_GLOBAL       'True'
222	LOAD_CONST        'timeout'
225	LOAD_CONST        0.05
228	CALL_FUNCTION_512 None
231	UNPACK_SEQUENCE_2 None
234	STORE_FAST        'seq'
237	STORE_FAST        'request'
240	POP_BLOCK         None
241	JUMP_FORWARD      '267'
244_0	COME_FROM         '204'

244	DUP_TOP           None
245	LOAD_GLOBAL       'Queue'
248	LOAD_ATTR         'Empty'
251	COMPARE_OP        'exception match'
254	POP_JUMP_IF_FALSE '266'
257	POP_TOP           None
258	POP_TOP           None
259	POP_TOP           None

260	CONTINUE_LOOP     '158'
263	JUMP_FORWARD      '267'
266	END_FINALLY       None
267_0	COME_FROM         '241'
267_1	COME_FROM         '266'

267	LOAD_FAST         'request'
270	UNPACK_SEQUENCE_3 None
273	STORE_FAST        'method'
276	STORE_FAST        'args'
279	STORE_FAST        'kwargs'

282	LOAD_FAST         'method'
285	LOAD_FAST         'args'
288	LOAD_FAST         'kwargs'
291	CALL_FUNCTION_VAR_KW_0 None
294	STORE_FAST        'ret'

297	LOAD_GLOBAL       'rpc'
300	LOAD_ATTR         'response_queue'
303	LOAD_ATTR         'put'
306	LOAD_FAST         'seq'
309	LOAD_FAST         'ret'
312	BUILD_TUPLE_2     None
315	CALL_FUNCTION_1   None
318	POP_TOP           None
319	POP_BLOCK         None
320	JUMP_BACK         '158'
323_0	COME_FROM         '158'

323	DUP_TOP           None
324	LOAD_GLOBAL       'KeyboardInterrupt'
327	COMPARE_OP        'exception match'
330	POP_JUMP_IF_FALSE '357'
333	POP_TOP           None
334	POP_TOP           None
335	POP_TOP           None

336	LOAD_GLOBAL       'quitting'
339	POP_JUMP_IF_FALSE '158'

342	LOAD_GLOBAL       'True'
345	STORE_GLOBAL      'exit_now'
348	JUMP_BACK         '158'

351	CONTINUE          '158'
354	JUMP_BACK         '158'

357	DUP_TOP           None
358	LOAD_GLOBAL       'SystemExit'
361	COMPARE_OP        'exception match'
364	POP_JUMP_IF_FALSE '376'
367	POP_TOP           None
368	POP_TOP           None
369	POP_TOP           None

370	RAISE_VARARGS_0   None
373	JUMP_BACK         '158'

376	POP_TOP           None
377	POP_TOP           None
378	POP_TOP           None

379	LOAD_GLOBAL       'sys'
382	LOAD_ATTR         'exc_info'
385	CALL_FUNCTION_0   None
388	UNPACK_SEQUENCE_3 None
391	STORE_FAST        'type'
394	STORE_FAST        'value'
397	STORE_FAST        'tb'

400	SETUP_EXCEPT      '436'

403	LOAD_GLOBAL       'print_exception'
406	CALL_FUNCTION_0   None
409	POP_TOP           None

410	LOAD_GLOBAL       'rpc'
413	LOAD_ATTR         'response_queue'
416	LOAD_ATTR         'put'
419	LOAD_FAST         'seq'
422	LOAD_CONST        None
425	BUILD_TUPLE_2     None
428	CALL_FUNCTION_1   None
431	POP_TOP           None
432	POP_BLOCK         None
433	JUMP_BACK         '158'
436_0	COME_FROM         '400'

436	POP_TOP           None
437	POP_TOP           None
438	POP_TOP           None

439	LOAD_GLOBAL       'traceback'
442	LOAD_ATTR         'print_exception'
445	LOAD_FAST         'type'
448	LOAD_FAST         'value'
451	LOAD_FAST         'tb'
454	LOAD_CONST        'file'
457	LOAD_GLOBAL       'sys'
460	LOAD_ATTR         '__stderr__'
463	CALL_FUNCTION_259 None
466	POP_TOP           None

467	LOAD_GLOBAL       'exit'
470	CALL_FUNCTION_0   None
473	POP_TOP           None
474	JUMP_ABSOLUTE     '485'
477	END_FINALLY       None

478	CONTINUE          '158'
481_0	COME_FROM         '477'
481	JUMP_BACK         '158'
484	END_FINALLY       None
485_0	COME_FROM         '484'
485	JUMP_BACK         '158'
488	POP_BLOCK         None
489_0	COME_FROM         '155'
489	LOAD_CONST        None
492	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 488


def manage_socket(address):
    global exit_now
    for i in range(3):
        time.sleep(i)
        try:
            server = MyRPCServer(address, MyHandler)
            break
        except socket.error as err:
            print >> sys.__stderr__, 'IDLE Subprocess: socket error: ' + err.args[1] + ', retrying....'

    else:
        print >> sys.__stderr__, 'IDLE Subprocess: Connection to IDLE GUI failed, exiting.'
        show_socket_error(err, address)
        exit_now = True
        return

    server.handle_request()


def show_socket_error(err, address):
    import Tkinter
    import tkMessageBox
    root = Tkinter.Tk()
    root.withdraw()
    if err.args[0] == 61:
        msg = "IDLE's subprocess can't connect to %s:%d.  This may be due to your personal firewall configuration.  It is safe to allow this internal connection because no data is visible on external ports." % address
        tkMessageBox.showerror('IDLE Subprocess Error', msg, parent=root)
    else:
        tkMessageBox.showerror('IDLE Subprocess Error', 'Socket Error: %s' % err.args[1])
    root.destroy()


def print_exception():
    import linecache
    linecache.checkcache()
    flush_stdout()
    efile = sys.stderr
    typ, val, tb = excinfo = sys.exc_info()
    sys.last_type, sys.last_value, sys.last_traceback = excinfo
    tbe = traceback.extract_tb(tb)
    print >> efile, '\nTraceback (most recent call last):'
    exclude = ('run.py', 'rpc.py', 'threading.py', 'Queue.py', 'RemoteDebugger.py', 'bdb.py')
    cleanup_traceback(tbe, exclude)
    traceback.print_list(tbe, file=efile)
    lines = traceback.format_exception_only(typ, val)
    for line in lines:
        print >> efile, line,


def cleanup_traceback(tb, exclude):
    """Remove excluded traces from beginning/end of tb; get cached lines"""
    orig_tb = tb[:]
    while tb:
        for rpcfile in exclude:
            if tb[0][0].count(rpcfile):
                break
        else:
            break

        del tb[0]

    while tb:
        for rpcfile in exclude:
            if tb[-1][0].count(rpcfile):
                break
        else:
            break

        del tb[-1]

    if len(tb) == 0:
        tb[:] = orig_tb[:]
        print >> sys.stderr, '** IDLE Internal Exception: '
    rpchandler = rpc.objecttable['exec'].rpchandler
    for i in range(len(tb)):
        fn, ln, nm, line = tb[i]
        if nm == '?':
            nm = '-toplevel-'
        if not line and fn.startswith('<pyshell#'):
            line = rpchandler.remotecall('linecache', 'getline', (fn, ln), {})
        tb[i] = (fn,
         ln,
         nm,
         line)


def flush_stdout():
    try:
        if sys.stdout.softspace:
            sys.stdout.softspace = 0
            sys.stdout.write('\n')
    except (AttributeError, EOFError):
        pass


def exit():
    """Exit subprocess, possibly after first deleting sys.exitfunc
    
    If config-main.cfg/.def 'General' 'delete-exitfunc' is True, then any
    sys.exitfunc will be removed before exiting.  (VPython support)
    
    """
    if no_exitfunc:
        try:
            del sys.exitfunc
        except AttributeError:
            pass

    sys.exit(0)


class MyRPCServer(rpc.RPCServer):

    def handle_error(self, request, client_address):
        """Override RPCServer method for IDLE
        
        Interrupt the MainThread and exit server if link is dropped.
        
        """
        global quitting
        global exit_now
        try:
            raise
        except SystemExit:
            raise
        except EOFError:
            exit_now = True
            thread.interrupt_main()
        except:
            erf = sys.__stderr__
            print >> erf, '\n' + '-' * 40
            print >> erf, 'Unhandled server exception!'
            print >> erf, 'Thread: %s' % threading.currentThread().getName()
            print >> erf, 'Client Address: ', client_address
            print >> erf, 'Request: ', repr(request)
            traceback.print_exc(file=erf)
            print >> erf, '\n*** Unrecoverable, server exiting!'
            print >> erf, '-' * 40
            quitting = True
            thread.interrupt_main()


class MyHandler(rpc.RPCHandler):

    def handle(self):
        """Override base method"""
        executive = Executive(self)
        self.register('exec', executive)
        sys.stdin = self.console = self.get_remote_proxy('stdin')
        sys.stdout = self.get_remote_proxy('stdout')
        sys.stderr = self.get_remote_proxy('stderr')
        from idlelib import IOBinding
        sys.stdin.encoding = sys.stdout.encoding = sys.stderr.encoding = IOBinding.encoding
        self.interp = self.get_remote_proxy('interp')
        rpc.RPCHandler.getresponse(self, myseq=None, wait=0.05)
        return

    def exithook(self):
        """override SocketIO method - wait for MainThread to shut us down"""
        time.sleep(10)

    def EOFhook(self):
        """Override SocketIO method - terminate wait on callback and exit thread"""
        global quitting
        quitting = True
        thread.interrupt_main()

    def decode_interrupthook(self):
        """interrupt awakened thread"""
        global quitting
        quitting = True
        thread.interrupt_main()


class Executive(object):

    def __init__(self, rpchandler):
        self.rpchandler = rpchandler
        self.locals = __main__.__dict__
        self.calltip = CallTips.CallTips()
        self.autocomplete = AutoComplete.AutoComplete()

    def runcode(self, code):
        global interruptable
        try:
            self.usr_exc_info = None
            interruptable = True
            try:
                exec code in self.locals
            finally:
                interruptable = False

        except:
            self.usr_exc_info = sys.exc_info()
            if quitting:
                exit()
            print_exception()
            jit = self.rpchandler.console.getvar('<<toggle-jit-stack-viewer>>')
            if jit:
                self.rpchandler.interp.open_remote_stack_viewer()
        else:
            flush_stdout()

        return

    def interrupt_the_server(self):
        if interruptable:
            thread.interrupt_main()

    def start_the_debugger(self, gui_adap_oid):
        return RemoteDebugger.start_debugger(self.rpchandler, gui_adap_oid)

    def stop_the_debugger(self, idb_adap_oid):
        """Unregister the Idb Adapter.  Link objects and Idb then subject to GC"""
        self.rpchandler.unregister(idb_adap_oid)

    def get_the_calltip(self, name):
        return self.calltip.fetch_tip(name)

    def get_the_completion_list(self, what, mode):
        return self.autocomplete.fetch_completions(what, mode)

    def stackviewer(self, flist_oid = None):
        if self.usr_exc_info:
            typ, val, tb = self.usr_exc_info
        else:
            return
        flist = None
        if flist_oid is not None:
            flist = self.rpchandler.get_remote_proxy(flist_oid)
        while tb and tb.tb_frame.f_globals['__name__'] in ('rpc', 'run'):
            tb = tb.tb_next

        sys.last_type = typ
        sys.last_value = val
        item = StackViewer.StackTreeItem(flist, tb)
        return RemoteObjectBrowser.remote_object_tree_item(item)