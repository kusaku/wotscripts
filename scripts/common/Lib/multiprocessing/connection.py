# Embedded file name: scripts/common/Lib/multiprocessing/connection.py
__all__ = ['Client', 'Listener', 'Pipe']
import os
import sys
import socket
import errno
import time
import tempfile
import itertools
import _multiprocessing
from multiprocessing import current_process, AuthenticationError
from multiprocessing.util import get_temp_dir, Finalize, sub_debug, debug
from multiprocessing.forking import duplicate, close
BUFSIZE = 8192
CONNECTION_TIMEOUT = 20.0
_mmap_counter = itertools.count()
default_family = 'AF_INET'
families = ['AF_INET']
if hasattr(socket, 'AF_UNIX'):
    default_family = 'AF_UNIX'
    families += ['AF_UNIX']
if sys.platform == 'win32':
    default_family = 'AF_PIPE'
    families += ['AF_PIPE']

def _init_timeout(timeout = CONNECTION_TIMEOUT):
    return time.time() + timeout


def _check_timeout(t):
    return time.time() > t


def arbitrary_address(family):
    """
    Return an arbitrary free address for the given family
    """
    if family == 'AF_INET':
        return ('localhost', 0)
    if family == 'AF_UNIX':
        return tempfile.mktemp(prefix='listener-', dir=get_temp_dir())
    if family == 'AF_PIPE':
        return tempfile.mktemp(prefix='\\\\.\\pipe\\pyc-%d-%d-' % (os.getpid(), _mmap_counter.next()))
    raise ValueError('unrecognized family')


def address_type(address):
    """
    Return the types of the address
    
    This can be 'AF_INET', 'AF_UNIX', or 'AF_PIPE'
    """
    if type(address) == tuple:
        return 'AF_INET'
    if type(address) is str and address.startswith('\\\\'):
        return 'AF_PIPE'
    if type(address) is str:
        return 'AF_UNIX'
    raise ValueError('address type of %r unrecognized' % address)


class Listener(object):
    """
    Returns a listener object.
    
    This is a wrapper for a bound socket which is 'listening' for
    connections, or for a Windows named pipe.
    """

    def __init__(self, address = None, family = None, backlog = 1, authkey = None):
        family = family or address and address_type(address) or default_family
        address = address or arbitrary_address(family)
        if family == 'AF_PIPE':
            self._listener = PipeListener(address, backlog)
        else:
            self._listener = SocketListener(address, family, backlog)
        if authkey is not None and not isinstance(authkey, bytes):
            raise TypeError, 'authkey should be a byte string'
        self._authkey = authkey
        return

    def accept(self):
        """
        Accept a connection on the bound socket or named pipe of `self`.
        
        Returns a `Connection` object.
        """
        c = self._listener.accept()
        if self._authkey:
            deliver_challenge(c, self._authkey)
            answer_challenge(c, self._authkey)
        return c

    def close(self):
        """
        Close the bound socket or named pipe of `self`.
        """
        return self._listener.close()

    address = property(lambda self: self._listener._address)
    last_accepted = property(lambda self: self._listener._last_accepted)


def Client(address, family = None, authkey = None):
    """
    Returns a connection to the address of a `Listener`
    """
    family = family or address_type(address)
    if family == 'AF_PIPE':
        c = PipeClient(address)
    else:
        c = SocketClient(address)
    if authkey is not None and not isinstance(authkey, bytes):
        raise TypeError, 'authkey should be a byte string'
    if authkey is not None:
        answer_challenge(c, authkey)
        deliver_challenge(c, authkey)
    return c


if sys.platform != 'win32':

    def Pipe(duplex = True):
        """
        Returns pair of connection objects at either end of a pipe
        """
        if duplex:
            s1, s2 = socket.socketpair()
            c1 = _multiprocessing.Connection(os.dup(s1.fileno()))
            c2 = _multiprocessing.Connection(os.dup(s2.fileno()))
            s1.close()
            s2.close()
        else:
            fd1, fd2 = os.pipe()
            c1 = _multiprocessing.Connection(fd1, writable=False)
            c2 = _multiprocessing.Connection(fd2, readable=False)
        return (c1, c2)


else:
    from _multiprocessing import win32

    def Pipe(duplex = True):
        """
        Returns pair of connection objects at either end of a pipe
        """
        address = arbitrary_address('AF_PIPE')
        if duplex:
            openmode = win32.PIPE_ACCESS_DUPLEX
            access = win32.GENERIC_READ | win32.GENERIC_WRITE
            obsize, ibsize = BUFSIZE, BUFSIZE
        else:
            openmode = win32.PIPE_ACCESS_INBOUND
            access = win32.GENERIC_WRITE
            obsize, ibsize = 0, BUFSIZE
        h1 = win32.CreateNamedPipe(address, openmode, win32.PIPE_TYPE_MESSAGE | win32.PIPE_READMODE_MESSAGE | win32.PIPE_WAIT, 1, obsize, ibsize, win32.NMPWAIT_WAIT_FOREVER, win32.NULL)
        h2 = win32.CreateFile(address, access, 0, win32.NULL, win32.OPEN_EXISTING, 0, win32.NULL)
        win32.SetNamedPipeHandleState(h2, win32.PIPE_READMODE_MESSAGE, None, None)
        try:
            win32.ConnectNamedPipe(h1, win32.NULL)
        except WindowsError as e:
            if e.args[0] != win32.ERROR_PIPE_CONNECTED:
                raise

        c1 = _multiprocessing.PipeConnection(h1, writable=duplex)
        c2 = _multiprocessing.PipeConnection(h2, readable=duplex)
        return (c1, c2)


class SocketListener(object):
    """
    Representation of a socket which is bound to an address and listening
    """

    def __init__(self, address, family, backlog = 1):
        self._socket = socket.socket(getattr(socket, family))
        try:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(address)
            self._socket.listen(backlog)
            self._address = self._socket.getsockname()
        except socket.error:
            self._socket.close()
            raise

        self._family = family
        self._last_accepted = None
        if family == 'AF_UNIX':
            self._unlink = Finalize(self, os.unlink, args=(address,), exitpriority=0)
        else:
            self._unlink = None
        return

    def accept(self):
        s, self._last_accepted = self._socket.accept()
        fd = duplicate(s.fileno())
        conn = _multiprocessing.Connection(fd)
        s.close()
        return conn

    def close(self):
        self._socket.close()
        if self._unlink is not None:
            self._unlink()
        return


def SocketClient--- This code section failed: ---

0	LOAD_GLOBAL       'address_type'
3	LOAD_FAST         'address'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'family'

12	LOAD_GLOBAL       'socket'
15	LOAD_ATTR         'socket'
18	LOAD_GLOBAL       'getattr'
21	LOAD_GLOBAL       'socket'
24	LOAD_FAST         'family'
27	CALL_FUNCTION_2   None
30	CALL_FUNCTION_1   None
33	STORE_FAST        's'

36	LOAD_GLOBAL       '_init_timeout'
39	CALL_FUNCTION_0   None
42	STORE_FAST        't'

45	SETUP_LOOP        '164'

48	SETUP_EXCEPT      '68'

51	LOAD_FAST         's'
54	LOAD_ATTR         'connect'
57	LOAD_FAST         'address'
60	CALL_FUNCTION_1   None
63	POP_TOP           None
64	POP_BLOCK         None
65	JUMP_FORWARD      '156'
68_0	COME_FROM         '48'

68	DUP_TOP           None
69	LOAD_GLOBAL       'socket'
72	LOAD_ATTR         'error'
75	COMPARE_OP        'exception match'
78	POP_JUMP_IF_FALSE '155'
81	POP_TOP           None
82	STORE_FAST        'e'
85	POP_TOP           None

86	LOAD_FAST         'e'
89	LOAD_ATTR         'args'
92	LOAD_CONST        0
95	BINARY_SUBSCR     None
96	LOAD_GLOBAL       'errno'
99	LOAD_ATTR         'ECONNREFUSED'
102	COMPARE_OP        '!='
105	POP_JUMP_IF_TRUE  '120'
108	LOAD_GLOBAL       '_check_timeout'
111	LOAD_FAST         't'
114	CALL_FUNCTION_1   None
117_0	COME_FROM         '105'
117	POP_JUMP_IF_FALSE '139'

120	LOAD_GLOBAL       'debug'
123	LOAD_CONST        'failed to connect to address %s'
126	LOAD_FAST         'address'
129	CALL_FUNCTION_2   None
132	POP_TOP           None

133	RAISE_VARARGS_0   None
136	JUMP_FORWARD      '139'
139_0	COME_FROM         '136'

139	LOAD_GLOBAL       'time'
142	LOAD_ATTR         'sleep'
145	LOAD_CONST        0.01
148	CALL_FUNCTION_1   None
151	POP_TOP           None
152	JUMP_BACK         '48'
155	END_FINALLY       None
156_0	COME_FROM         '65'

156	BREAK_LOOP        None
157_0	COME_FROM         '155'
157	JUMP_BACK         '48'
160	POP_BLOCK         None

161	RAISE_VARARGS_0   None
164_0	COME_FROM         '45'

164	LOAD_GLOBAL       'duplicate'
167	LOAD_FAST         's'
170	LOAD_ATTR         'fileno'
173	CALL_FUNCTION_0   None
176	CALL_FUNCTION_1   None
179	STORE_FAST        'fd'

182	LOAD_GLOBAL       '_multiprocessing'
185	LOAD_ATTR         'Connection'
188	LOAD_FAST         'fd'
191	CALL_FUNCTION_1   None
194	STORE_FAST        'conn'

197	LOAD_FAST         's'
200	LOAD_ATTR         'close'
203	CALL_FUNCTION_0   None
206	POP_TOP           None

207	LOAD_FAST         'conn'
210	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 160


if sys.platform == 'win32':

    class PipeListener(object):
        """
        Representation of a named pipe
        """

        def __init__(self, address, backlog = None):
            self._address = address
            handle = win32.CreateNamedPipe(address, win32.PIPE_ACCESS_DUPLEX, win32.PIPE_TYPE_MESSAGE | win32.PIPE_READMODE_MESSAGE | win32.PIPE_WAIT, win32.PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, win32.NMPWAIT_WAIT_FOREVER, win32.NULL)
            self._handle_queue = [handle]
            self._last_accepted = None
            sub_debug('listener created with address=%r', self._address)
            self.close = Finalize(self, PipeListener._finalize_pipe_listener, args=(self._handle_queue, self._address), exitpriority=0)
            return

        def accept(self):
            newhandle = win32.CreateNamedPipe(self._address, win32.PIPE_ACCESS_DUPLEX, win32.PIPE_TYPE_MESSAGE | win32.PIPE_READMODE_MESSAGE | win32.PIPE_WAIT, win32.PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, win32.NMPWAIT_WAIT_FOREVER, win32.NULL)
            self._handle_queue.append(newhandle)
            handle = self._handle_queue.pop(0)
            try:
                win32.ConnectNamedPipe(handle, win32.NULL)
            except WindowsError as e:
                if e.args[0] != win32.ERROR_PIPE_CONNECTED:
                    raise

            return _multiprocessing.PipeConnection(handle)

        @staticmethod
        def _finalize_pipe_listener(queue, address):
            sub_debug('closing listener with address=%r', address)
            for handle in queue:
                close(handle)


    def PipeClient--- This code section failed: ---

0	LOAD_GLOBAL       '_init_timeout'
3	CALL_FUNCTION_0   None
6	STORE_FAST        't'

9	SETUP_LOOP        '163'

12	SETUP_EXCEPT      '87'

15	LOAD_GLOBAL       'win32'
18	LOAD_ATTR         'WaitNamedPipe'
21	LOAD_FAST         'address'
24	LOAD_CONST        1000
27	CALL_FUNCTION_2   None
30	POP_TOP           None

31	LOAD_GLOBAL       'win32'
34	LOAD_ATTR         'CreateFile'

37	LOAD_FAST         'address'
40	LOAD_GLOBAL       'win32'
43	LOAD_ATTR         'GENERIC_READ'
46	LOAD_GLOBAL       'win32'
49	LOAD_ATTR         'GENERIC_WRITE'
52	BINARY_OR         None

53	LOAD_CONST        0
56	LOAD_GLOBAL       'win32'
59	LOAD_ATTR         'NULL'
62	LOAD_GLOBAL       'win32'
65	LOAD_ATTR         'OPEN_EXISTING'
68	LOAD_CONST        0
71	LOAD_GLOBAL       'win32'
74	LOAD_ATTR         'NULL'
77	CALL_FUNCTION_7   None
80	STORE_FAST        'h'
83	POP_BLOCK         None
84	JUMP_FORWARD      '155'
87_0	COME_FROM         '12'

87	DUP_TOP           None
88	LOAD_GLOBAL       'WindowsError'
91	COMPARE_OP        'exception match'
94	POP_JUMP_IF_FALSE '154'
97	POP_TOP           None
98	STORE_FAST        'e'
101	POP_TOP           None

102	LOAD_FAST         'e'
105	LOAD_ATTR         'args'
108	LOAD_CONST        0
111	BINARY_SUBSCR     None
112	LOAD_GLOBAL       'win32'
115	LOAD_ATTR         'ERROR_SEM_TIMEOUT'

118	LOAD_GLOBAL       'win32'
121	LOAD_ATTR         'ERROR_PIPE_BUSY'
124	BUILD_TUPLE_2     None
127	COMPARE_OP        'not in'
130	POP_JUMP_IF_TRUE  '145'
133	LOAD_GLOBAL       '_check_timeout'
136	LOAD_FAST         't'
139	CALL_FUNCTION_1   None
142_0	COME_FROM         '130'
142	POP_JUMP_IF_FALSE '156'

145	RAISE_VARARGS_0   None
148	JUMP_ABSOLUTE     '156'
151	JUMP_BACK         '12'
154	END_FINALLY       None
155_0	COME_FROM         '84'

155	BREAK_LOOP        None
156_0	COME_FROM         '154'
156	JUMP_BACK         '12'
159	POP_BLOCK         None

160	RAISE_VARARGS_0   None
163_0	COME_FROM         '9'

163	LOAD_GLOBAL       'win32'
166	LOAD_ATTR         'SetNamedPipeHandleState'

169	LOAD_FAST         'h'
172	LOAD_GLOBAL       'win32'
175	LOAD_ATTR         'PIPE_READMODE_MESSAGE'
178	LOAD_CONST        None
181	LOAD_CONST        None
184	CALL_FUNCTION_4   None
187	POP_TOP           None

188	LOAD_GLOBAL       '_multiprocessing'
191	LOAD_ATTR         'PipeConnection'
194	LOAD_FAST         'h'
197	CALL_FUNCTION_1   None
200	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 159


MESSAGE_LENGTH = 20
CHALLENGE = '#CHALLENGE#'
WELCOME = '#WELCOME#'
FAILURE = '#FAILURE#'

def deliver_challenge(connection, authkey):
    import hmac
    if not isinstance(authkey, bytes):
        raise AssertionError
        message = os.urandom(MESSAGE_LENGTH)
        connection.send_bytes(CHALLENGE + message)
        digest = hmac.new(authkey, message).digest()
        response = connection.recv_bytes(256)
        response == digest and connection.send_bytes(WELCOME)
    else:
        connection.send_bytes(FAILURE)
        raise AuthenticationError('digest received was wrong')


def answer_challenge(connection, authkey):
    import hmac
    raise isinstance(authkey, bytes) or AssertionError
    message = connection.recv_bytes(256)
    if not message[:len(CHALLENGE)] == CHALLENGE:
        raise AssertionError('message = %r' % message)
        message = message[len(CHALLENGE):]
        digest = hmac.new(authkey, message).digest()
        connection.send_bytes(digest)
        response = connection.recv_bytes(256)
        raise response != WELCOME and AuthenticationError('digest sent was rejected')


class ConnectionWrapper(object):

    def __init__(self, conn, dumps, loads):
        self._conn = conn
        self._dumps = dumps
        self._loads = loads
        for attr in ('fileno', 'close', 'poll', 'recv_bytes', 'send_bytes'):
            obj = getattr(conn, attr)
            setattr(self, attr, obj)

    def send(self, obj):
        s = self._dumps(obj)
        self._conn.send_bytes(s)

    def recv(self):
        s = self._conn.recv_bytes()
        return self._loads(s)


def _xml_dumps(obj):
    return xmlrpclib.dumps((obj,), None, None, None, 1).encode('utf8')


def _xml_loads(s):
    (obj,), method = xmlrpclib.loads(s.decode('utf8'))
    return obj


class XmlListener(Listener):

    def accept(self):
        global xmlrpclib
        import xmlrpclib
        obj = Listener.accept(self)
        return ConnectionWrapper(obj, _xml_dumps, _xml_loads)


def XmlClient(*args, **kwds):
    global xmlrpclib
    import xmlrpclib
    return ConnectionWrapper(Client(*args, **kwds), _xml_dumps, _xml_loads)