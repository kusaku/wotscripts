# Embedded file name: scripts/common/Lib/multiprocessing/reduction.py
__all__ = []
import os
import sys
import socket
import threading
import _multiprocessing
from multiprocessing import current_process
from multiprocessing.forking import Popen, duplicate, close, ForkingPickler
from multiprocessing.util import register_after_fork, debug, sub_debug
from multiprocessing.connection import Client, Listener
if not (sys.platform == 'win32' or hasattr(_multiprocessing, 'recvfd')):
    raise ImportError('pickling of connections not supported')
if sys.platform == 'win32':
    import _subprocess
    from _multiprocessing import win32

    def send_handle(conn, handle, destination_pid):
        process_handle = win32.OpenProcess(win32.PROCESS_ALL_ACCESS, False, destination_pid)
        try:
            new_handle = duplicate(handle, process_handle)
            conn.send(new_handle)
        finally:
            close(process_handle)


    def recv_handle(conn):
        return conn.recv()


else:

    def send_handle(conn, handle, destination_pid):
        _multiprocessing.sendfd(conn.fileno(), handle)


    def recv_handle(conn):
        return _multiprocessing.recvfd(conn.fileno())


_cache = set()

def _reset(obj):
    global _cache
    global _listener
    global _lock
    for h in _cache:
        close(h)

    _cache.clear()
    _lock = threading.Lock()
    _listener = None
    return


_reset(None)
register_after_fork(_reset, _reset)

def _get_listener():
    global _listener
    if _listener is None:
        _lock.acquire()
        try:
            if _listener is None:
                debug('starting listener and thread for sending handles')
                _listener = Listener(authkey=current_process().authkey)
                t = threading.Thread(target=_serve)
                t.daemon = True
                t.start()
        finally:
            _lock.release()

    return _listener


def _serve--- This code section failed: ---

0	LOAD_CONST        1
3	LOAD_CONST        ('is_exiting', 'sub_warning')
6	IMPORT_NAME       'util'
9	IMPORT_FROM       'is_exiting'
12	STORE_FAST        'is_exiting'
15	IMPORT_FROM       'sub_warning'
18	STORE_FAST        'sub_warning'
21	POP_TOP           None

22	SETUP_LOOP        '186'

25	SETUP_EXCEPT      '111'

28	LOAD_GLOBAL       '_listener'
31	LOAD_ATTR         'accept'
34	CALL_FUNCTION_0   None
37	STORE_FAST        'conn'

40	LOAD_FAST         'conn'
43	LOAD_ATTR         'recv'
46	CALL_FUNCTION_0   None
49	UNPACK_SEQUENCE_2 None
52	STORE_FAST        'handle_wanted'
55	STORE_FAST        'destination_pid'

58	LOAD_GLOBAL       '_cache'
61	LOAD_ATTR         'remove'
64	LOAD_FAST         'handle_wanted'
67	CALL_FUNCTION_1   None
70	POP_TOP           None

71	LOAD_GLOBAL       'send_handle'
74	LOAD_FAST         'conn'
77	LOAD_FAST         'handle_wanted'
80	LOAD_FAST         'destination_pid'
83	CALL_FUNCTION_3   None
86	POP_TOP           None

87	LOAD_GLOBAL       'close'
90	LOAD_FAST         'handle_wanted'
93	CALL_FUNCTION_1   None
96	POP_TOP           None

97	LOAD_FAST         'conn'
100	LOAD_ATTR         'close'
103	CALL_FUNCTION_0   None
106	POP_TOP           None
107	POP_BLOCK         None
108	JUMP_BACK         '25'
111_0	COME_FROM         '25'

111	POP_TOP           None
112	POP_TOP           None
113	POP_TOP           None

114	LOAD_FAST         'is_exiting'
117	CALL_FUNCTION_0   None
120	POP_JUMP_IF_TRUE  '182'

123	LOAD_CONST        -1
126	LOAD_CONST        None
129	IMPORT_NAME       'traceback'
132	STORE_FAST        'traceback'

135	LOAD_FAST         'sub_warning'

138	LOAD_CONST        'thread for sharing handles raised exception :\n'
141	LOAD_CONST        '-'
144	LOAD_CONST        79
147	BINARY_MULTIPLY   None
148	BINARY_ADD        None
149	LOAD_CONST        '\n'
152	BINARY_ADD        None
153	LOAD_FAST         'traceback'
156	LOAD_ATTR         'format_exc'
159	CALL_FUNCTION_0   None
162	BINARY_ADD        None
163	LOAD_CONST        '-'
166	LOAD_CONST        79
169	BINARY_MULTIPLY   None
170	BINARY_ADD        None
171	CALL_FUNCTION_1   None
174	POP_TOP           None
175	JUMP_ABSOLUTE     '182'
178	JUMP_BACK         '25'
181	END_FINALLY       None
182_0	COME_FROM         '181'
182	JUMP_BACK         '25'
185	POP_BLOCK         None
186_0	COME_FROM         '22'

Syntax error at or near `POP_BLOCK' token at offset 185


def reduce_handle(handle):
    if Popen.thread_is_spawning():
        return (None, Popen.duplicate_for_child(handle), True)
    else:
        dup_handle = duplicate(handle)
        _cache.add(dup_handle)
        sub_debug('reducing handle %d', handle)
        return (_get_listener().address, dup_handle, False)


def rebuild_handle(pickled_data):
    address, handle, inherited = pickled_data
    if inherited:
        return handle
    sub_debug('rebuilding handle %d', handle)
    conn = Client(address, authkey=current_process().authkey)
    conn.send((handle, os.getpid()))
    new_handle = recv_handle(conn)
    conn.close()
    return new_handle


def reduce_connection(conn):
    rh = reduce_handle(conn.fileno())
    return (rebuild_connection, (rh, conn.readable, conn.writable))


def rebuild_connection(reduced_handle, readable, writable):
    handle = rebuild_handle(reduced_handle)
    return _multiprocessing.Connection(handle, readable=readable, writable=writable)


ForkingPickler.register(_multiprocessing.Connection, reduce_connection)

def fromfd(fd, family, type_, proto = 0):
    s = socket.fromfd(fd, family, type_, proto)
    if s.__class__ is not socket.socket:
        s = socket.socket(_sock=s)
    return s


def reduce_socket(s):
    reduced_handle = reduce_handle(s.fileno())
    return (rebuild_socket, (reduced_handle,
      s.family,
      s.type,
      s.proto))


def rebuild_socket(reduced_handle, family, type_, proto):
    fd = rebuild_handle(reduced_handle)
    _sock = fromfd(fd, family, type_, proto)
    close(fd)
    return _sock


ForkingPickler.register(socket.socket, reduce_socket)
if sys.platform == 'win32':

    def reduce_pipe_connection(conn):
        rh = reduce_handle(conn.fileno())
        return (rebuild_pipe_connection, (rh, conn.readable, conn.writable))


    def rebuild_pipe_connection(reduced_handle, readable, writable):
        handle = rebuild_handle(reduced_handle)
        return _multiprocessing.PipeConnection(handle, readable=readable, writable=writable)


    ForkingPickler.register(_multiprocessing.PipeConnection, reduce_pipe_connection)