# Embedded file name: scripts/common/Lib/idlelib/rpc.py
"""RPC Implemention, originally written for the Python Idle IDE

For security reasons, GvR requested that Idle's Python execution server process
connect to the Idle process, which listens for the connection.  Since Idle has
has only one client per server, this was not a limitation.

   +---------------------------------+ +-------------+
   | SocketServer.BaseRequestHandler | | SocketIO    |
   +---------------------------------+ +-------------+
                   ^                   | register()  |
                   |                   | unregister()|
                   |                   +-------------+
                   |                      ^  ^
                   |                      |  |
                   | + -------------------+  |
                   | |                       |
   +-------------------------+        +-----------------+
   | RPCHandler              |        | RPCClient       |
   | [attribute of RPCServer]|        |                 |
   +-------------------------+        +-----------------+

The RPCServer handler class is expected to provide register/unregister methods.
RPCHandler inherits the mix-in class SocketIO, which provides these methods.

See the Idle run.main() docstring for further information on how this was
accomplished in Idle.

"""
import sys
import os
import socket
import select
import SocketServer
import struct
import cPickle as pickle
import threading
import Queue
import traceback
import copy_reg
import types
import marshal

def unpickle_code(ms):
    co = marshal.loads(ms)
    raise isinstance(co, types.CodeType) or AssertionError
    return co


def pickle_code(co):
    raise isinstance(co, types.CodeType) or AssertionError
    ms = marshal.dumps(co)
    return (unpickle_code, (ms,))


copy_reg.pickle(types.CodeType, pickle_code, unpickle_code)
BUFSIZE = 8 * 1024
LOCALHOST = '127.0.0.1'

class RPCServer(SocketServer.TCPServer):

    def __init__(self, addr, handlerclass = None):
        if handlerclass is None:
            handlerclass = RPCHandler
        SocketServer.TCPServer.__init__(self, addr, handlerclass)
        return

    def server_bind(self):
        """Override TCPServer method, no bind() phase for connecting entity"""
        pass

    def server_activate(self):
        """Override TCPServer method, connect() instead of listen()
        
        Due to the reversed connection, self.server_address is actually the
        address of the Idle Client to which we are connecting.
        
        """
        self.socket.connect(self.server_address)

    def get_request(self):
        """Override TCPServer method, return already connected socket"""
        return (self.socket, self.server_address)

    def handle_error(self, request, client_address):
        """Override TCPServer method
        
        Error message goes to __stderr__.  No error message if exiting
        normally or socket raised EOF.  Other exceptions not handled in
        server code will cause os._exit.
        
        """
        try:
            raise
        except SystemExit:
            raise
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
            os._exit(0)


objecttable = {}
request_queue = Queue.Queue(0)
response_queue = Queue.Queue(0)

class SocketIO(object):
    nextseq = 0

    def __init__(self, sock, objtable = None, debugging = None):
        self.sockthread = threading.currentThread()
        if debugging is not None:
            self.debugging = debugging
        self.sock = sock
        if objtable is None:
            objtable = objecttable
        self.objtable = objtable
        self.responses = {}
        self.cvars = {}
        return

    def close(self):
        sock = self.sock
        self.sock = None
        if sock is not None:
            sock.close()
        return

    def exithook(self):
        """override for specific exit action"""
        os._exit()

    def debug(self, *args):
        if not self.debugging:
            return
        s = self.location + ' ' + str(threading.currentThread().getName())
        for a in args:
            s = s + ' ' + str(a)

        print >> sys.__stderr__, s

    def register(self, oid, object):
        self.objtable[oid] = object

    def unregister(self, oid):
        try:
            del self.objtable[oid]
        except KeyError:
            pass

    def localcall(self, seq, request):
        self.debug('localcall:', request)
        try:
            how, (oid, methodname, args, kwargs) = request
        except TypeError:
            return ('ERROR', 'Bad request format')

        if oid not in self.objtable:
            return ('ERROR', 'Unknown object id: %r' % (oid,))
        else:
            obj = self.objtable[oid]
            if methodname == '__methods__':
                methods = {}
                _getmethods(obj, methods)
                return ('OK', methods)
            if methodname == '__attributes__':
                attributes = {}
                _getattributes(obj, attributes)
                return ('OK', attributes)
            if not hasattr(obj, methodname):
                return ('ERROR', 'Unsupported method name: %r' % (methodname,))
            method = getattr(obj, methodname)
            try:
                if how == 'CALL':
                    ret = method(*args, **kwargs)
                    if isinstance(ret, RemoteObject):
                        ret = remoteref(ret)
                    return ('OK', ret)
                if how == 'QUEUE':
                    request_queue.put((seq, (method, args, kwargs)))
                    return ('QUEUED', None)
                return ('ERROR', 'Unsupported message type: %s' % how)
            except SystemExit:
                raise
            except socket.error:
                raise
            except:
                msg = '*** Internal Error: rpc.py:SocketIO.localcall()\n\n Object: %s \n Method: %s \n Args: %s\n'
                print >> sys.__stderr__, msg % (oid, method, args)
                traceback.print_exc(file=sys.__stderr__)
                return ('EXCEPTION', None)

            return None

    def remotecall(self, oid, methodname, args, kwargs):
        self.debug('remotecall:asynccall: ', oid, methodname)
        seq = self.asynccall(oid, methodname, args, kwargs)
        return self.asyncreturn(seq)

    def remotequeue(self, oid, methodname, args, kwargs):
        self.debug('remotequeue:asyncqueue: ', oid, methodname)
        seq = self.asyncqueue(oid, methodname, args, kwargs)
        return self.asyncreturn(seq)

    def asynccall(self, oid, methodname, args, kwargs):
        request = ('CALL', (oid,
          methodname,
          args,
          kwargs))
        seq = self.newseq()
        if threading.currentThread() != self.sockthread:
            cvar = threading.Condition()
            self.cvars[seq] = cvar
        self.debug('asynccall:%d:' % seq, oid, methodname, args, kwargs)
        self.putmessage((seq, request))
        return seq

    def asyncqueue(self, oid, methodname, args, kwargs):
        request = ('QUEUE', (oid,
          methodname,
          args,
          kwargs))
        seq = self.newseq()
        if threading.currentThread() != self.sockthread:
            cvar = threading.Condition()
            self.cvars[seq] = cvar
        self.debug('asyncqueue:%d:' % seq, oid, methodname, args, kwargs)
        self.putmessage((seq, request))
        return seq

    def asyncreturn(self, seq):
        self.debug('asyncreturn:%d:call getresponse(): ' % seq)
        response = self.getresponse(seq, wait=0.05)
        self.debug('asyncreturn:%d:response: ' % seq, response)
        return self.decoderesponse(response)

    def decoderesponse(self, response):
        how, what = response
        if how == 'OK':
            return what
        elif how == 'QUEUED':
            return None
        elif how == 'EXCEPTION':
            self.debug('decoderesponse: EXCEPTION')
            return None
        elif how == 'EOF':
            self.debug('decoderesponse: EOF')
            self.decode_interrupthook()
            return None
        else:
            if how == 'ERROR':
                self.debug('decoderesponse: Internal ERROR:', what)
                raise RuntimeError, what
            raise SystemError, (how, what)
            return None

    def decode_interrupthook(self):
        """"""
        raise EOFError

    def mainloop(self):
        """Listen on socket until I/O not ready or EOF
        
        pollresponse() will loop looking for seq number None, which
        never comes, and exit on EOFError.
        
        """
        try:
            self.getresponse(myseq=None, wait=0.05)
        except EOFError:
            self.debug('mainloop:return')
            return

        return

    def getresponse(self, myseq, wait):
        response = self._getresponse(myseq, wait)
        if response is not None:
            how, what = response
            if how == 'OK':
                response = (how, self._proxify(what))
        return response

    def _proxify(self, obj):
        if isinstance(obj, RemoteProxy):
            return RPCProxy(self, obj.oid)
        if isinstance(obj, types.ListType):
            return map(self._proxify, obj)
        return obj

    def _getresponse--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'debug'
6	LOAD_CONST        '_getresponse:myseq:'
9	LOAD_FAST         'myseq'
12	CALL_FUNCTION_2   None
15	POP_TOP           None

16	LOAD_GLOBAL       'threading'
19	LOAD_ATTR         'currentThread'
22	CALL_FUNCTION_0   None
25	LOAD_FAST         'self'
28	LOAD_ATTR         'sockthread'
31	COMPARE_OP        'is'
34	POP_JUMP_IF_FALSE '81'

37	SETUP_LOOP        '206'

40	LOAD_FAST         'self'
43	LOAD_ATTR         'pollresponse'
46	LOAD_FAST         'myseq'
49	LOAD_FAST         'wait'
52	CALL_FUNCTION_2   None
55	STORE_FAST        'response'

58	LOAD_FAST         'response'
61	LOAD_CONST        None
64	COMPARE_OP        'is not'
67	POP_JUMP_IF_FALSE '40'

70	LOAD_FAST         'response'
73	RETURN_END_IF     None
74	JUMP_BACK         '40'
77	POP_BLOCK         None
78_0	COME_FROM         '37'
78	JUMP_FORWARD      '206'

81	LOAD_FAST         'self'
84	LOAD_ATTR         'cvars'
87	LOAD_FAST         'myseq'
90	BINARY_SUBSCR     None
91	STORE_FAST        'cvar'

94	LOAD_FAST         'cvar'
97	LOAD_ATTR         'acquire'
100	CALL_FUNCTION_0   None
103	POP_TOP           None

104	SETUP_LOOP        '136'
107	LOAD_FAST         'myseq'
110	LOAD_FAST         'self'
113	LOAD_ATTR         'responses'
116	COMPARE_OP        'not in'
119	POP_JUMP_IF_FALSE '135'

122	LOAD_FAST         'cvar'
125	LOAD_ATTR         'wait'
128	CALL_FUNCTION_0   None
131	POP_TOP           None
132	JUMP_BACK         '107'
135	POP_BLOCK         None
136_0	COME_FROM         '104'

136	LOAD_FAST         'self'
139	LOAD_ATTR         'responses'
142	LOAD_FAST         'myseq'
145	BINARY_SUBSCR     None
146	STORE_FAST        'response'

149	LOAD_FAST         'self'
152	LOAD_ATTR         'debug'
155	LOAD_CONST        '_getresponse:%s: thread woke up: response: %s'

158	LOAD_FAST         'myseq'
161	LOAD_FAST         'response'
164	BUILD_TUPLE_2     None
167	BINARY_MODULO     None
168	CALL_FUNCTION_1   None
171	POP_TOP           None

172	LOAD_FAST         'self'
175	LOAD_ATTR         'responses'
178	LOAD_FAST         'myseq'
181	DELETE_SUBSCR     None

182	LOAD_FAST         'self'
185	LOAD_ATTR         'cvars'
188	LOAD_FAST         'myseq'
191	DELETE_SUBSCR     None

192	LOAD_FAST         'cvar'
195	LOAD_ATTR         'release'
198	CALL_FUNCTION_0   None
201	POP_TOP           None

202	LOAD_FAST         'response'
205	RETURN_VALUE      None
206_0	COME_FROM         '78'
206	LOAD_CONST        None
209	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 77

    def newseq(self):
        self.nextseq = seq = self.nextseq + 2
        return seq

    def putmessage(self, message):
        self.debug('putmessage:%d:' % message[0])
        try:
            s = pickle.dumps(message)
        except pickle.PicklingError:
            print >> sys.__stderr__, 'Cannot pickle:', repr(message)
            raise

        s = struct.pack('<i', len(s)) + s
        while len(s) > 0:
            try:
                r, w, x = select.select([], [self.sock], [])
                n = self.sock.send(s[:BUFSIZE])
            except (AttributeError, TypeError):
                raise IOError, 'socket no longer exists'
            except socket.error:
                raise
            else:
                s = s[n:]

    buffer = ''
    bufneed = 4
    bufstate = 0

    def pollpacket(self, wait):
        self._stage0()
        if len(self.buffer) < self.bufneed:
            r, w, x = select.select([self.sock.fileno()], [], [], wait)
            if len(r) == 0:
                return None
            try:
                s = self.sock.recv(BUFSIZE)
            except socket.error:
                raise EOFError

            if len(s) == 0:
                raise EOFError
            self.buffer += s
            self._stage0()
        return self._stage1()

    def _stage0(self):
        if self.bufstate == 0 and len(self.buffer) >= 4:
            s = self.buffer[:4]
            self.buffer = self.buffer[4:]
            self.bufneed = struct.unpack('<i', s)[0]
            self.bufstate = 1

    def _stage1(self):
        if self.bufstate == 1 and len(self.buffer) >= self.bufneed:
            packet = self.buffer[:self.bufneed]
            self.buffer = self.buffer[self.bufneed:]
            self.bufneed = 4
            self.bufstate = 0
            return packet

    def pollmessage(self, wait):
        packet = self.pollpacket(wait)
        if packet is None:
            return
        else:
            try:
                message = pickle.loads(packet)
            except pickle.UnpicklingError:
                print >> sys.__stderr__, '-----------------------'
                print >> sys.__stderr__, 'cannot unpickle packet:', repr(packet)
                traceback.print_stack(file=sys.__stderr__)
                print >> sys.__stderr__, '-----------------------'
                raise

            return message

    def pollresponse--- This code section failed: ---

0	SETUP_LOOP        '443'

3	SETUP_EXCEPT      '25'

6	LOAD_GLOBAL       'response_queue'
9	LOAD_ATTR         'get'
12	LOAD_CONST        0
15	CALL_FUNCTION_1   None
18	STORE_FAST        'qmsg'
21	POP_BLOCK         None
22	JUMP_FORWARD      '45'
25_0	COME_FROM         '3'

25	DUP_TOP           None
26	LOAD_GLOBAL       'Queue'
29	LOAD_ATTR         'Empty'
32	COMPARE_OP        'exception match'
35	POP_JUMP_IF_FALSE '44'
38	POP_TOP           None
39	POP_TOP           None
40	POP_TOP           None

41	JUMP_FORWARD      '88'
44	END_FINALLY       None
45_0	COME_FROM         '22'

45	LOAD_FAST         'qmsg'
48	UNPACK_SEQUENCE_2 None
51	STORE_FAST        'seq'
54	STORE_FAST        'response'

57	LOAD_FAST         'seq'
60	LOAD_CONST        'OK'
63	LOAD_FAST         'response'
66	BUILD_TUPLE_2     None
69	BUILD_TUPLE_2     None
72	STORE_FAST        'message'

75	LOAD_FAST         'self'
78	LOAD_ATTR         'putmessage'
81	LOAD_FAST         'message'
84	CALL_FUNCTION_1   None
87	POP_TOP           None
88_0	COME_FROM         '44'

88	SETUP_EXCEPT      '126'

91	LOAD_FAST         'self'
94	LOAD_ATTR         'pollmessage'
97	LOAD_FAST         'wait'
100	CALL_FUNCTION_1   None
103	STORE_FAST        'message'

106	LOAD_FAST         'message'
109	LOAD_CONST        None
112	COMPARE_OP        'is'
115	POP_JUMP_IF_FALSE '122'

118	LOAD_CONST        None
121	RETURN_END_IF     None
122	POP_BLOCK         None
123	JUMP_FORWARD      '171'
126_0	COME_FROM         '88'

126	DUP_TOP           None
127	LOAD_GLOBAL       'EOFError'
130	COMPARE_OP        'exception match'
133	POP_JUMP_IF_FALSE '153'
136	POP_TOP           None
137	POP_TOP           None
138	POP_TOP           None

139	LOAD_FAST         'self'
142	LOAD_ATTR         'handle_EOF'
145	CALL_FUNCTION_0   None
148	POP_TOP           None

149	LOAD_CONST        None
152	RETURN_VALUE      None

153	DUP_TOP           None
154	LOAD_GLOBAL       'AttributeError'
157	COMPARE_OP        'exception match'
160	POP_JUMP_IF_FALSE '170'
163	POP_TOP           None
164	POP_TOP           None
165	POP_TOP           None

166	LOAD_CONST        None
169	RETURN_VALUE      None
170	END_FINALLY       None
171_0	COME_FROM         '123'
171_1	COME_FROM         '170'

171	LOAD_FAST         'message'
174	UNPACK_SEQUENCE_2 None
177	STORE_FAST        'seq'
180	STORE_FAST        'resq'

183	LOAD_FAST         'resq'
186	LOAD_CONST        0
189	BINARY_SUBSCR     None
190	STORE_FAST        'how'

193	LOAD_FAST         'self'
196	LOAD_ATTR         'debug'
199	LOAD_CONST        'pollresponse:%d:myseq:%s'
202	LOAD_FAST         'seq'
205	LOAD_FAST         'myseq'
208	BUILD_TUPLE_2     None
211	BINARY_MODULO     None
212	CALL_FUNCTION_1   None
215	POP_TOP           None

216	LOAD_FAST         'how'
219	LOAD_CONST        ('CALL', 'QUEUE')
222	COMPARE_OP        'in'
225	POP_JUMP_IF_FALSE '341'

228	LOAD_FAST         'self'
231	LOAD_ATTR         'debug'
234	LOAD_CONST        'pollresponse:%d:localcall:call:'
237	LOAD_FAST         'seq'
240	BINARY_MODULO     None
241	CALL_FUNCTION_1   None
244	POP_TOP           None

245	LOAD_FAST         'self'
248	LOAD_ATTR         'localcall'
251	LOAD_FAST         'seq'
254	LOAD_FAST         'resq'
257	CALL_FUNCTION_2   None
260	STORE_FAST        'response'

263	LOAD_FAST         'self'
266	LOAD_ATTR         'debug'
269	LOAD_CONST        'pollresponse:%d:localcall:response:%s'

272	LOAD_FAST         'seq'
275	LOAD_FAST         'response'
278	BUILD_TUPLE_2     None
281	BINARY_MODULO     None
282	CALL_FUNCTION_1   None
285	POP_TOP           None

286	LOAD_FAST         'how'
289	LOAD_CONST        'CALL'
292	COMPARE_OP        '=='
295	POP_JUMP_IF_FALSE '320'

298	LOAD_FAST         'self'
301	LOAD_ATTR         'putmessage'
304	LOAD_FAST         'seq'
307	LOAD_FAST         'response'
310	BUILD_TUPLE_2     None
313	CALL_FUNCTION_1   None
316	POP_TOP           None
317	JUMP_BACK         '3'

320	LOAD_FAST         'how'
323	LOAD_CONST        'QUEUE'
326	COMPARE_OP        '=='
329	POP_JUMP_IF_FALSE '3'

332	JUMP_BACK         '3'

335	CONTINUE          '3'
338	JUMP_BACK         '3'

341	LOAD_FAST         'seq'
344	LOAD_FAST         'myseq'
347	COMPARE_OP        '=='
350	POP_JUMP_IF_FALSE '357'

353	LOAD_FAST         'resq'
356	RETURN_END_IF     None

357	LOAD_FAST         'self'
360	LOAD_ATTR         'cvars'
363	LOAD_ATTR         'get'
366	LOAD_FAST         'seq'
369	LOAD_CONST        None
372	CALL_FUNCTION_2   None
375	STORE_FAST        'cv'

378	LOAD_FAST         'cv'
381	LOAD_CONST        None
384	COMPARE_OP        'is not'
387	POP_JUMP_IF_FALSE '3'

390	LOAD_FAST         'cv'
393	LOAD_ATTR         'acquire'
396	CALL_FUNCTION_0   None
399	POP_TOP           None

400	LOAD_FAST         'resq'
403	LOAD_FAST         'self'
406	LOAD_ATTR         'responses'
409	LOAD_FAST         'seq'
412	STORE_SUBSCR      None

413	LOAD_FAST         'cv'
416	LOAD_ATTR         'notify'
419	CALL_FUNCTION_0   None
422	POP_TOP           None

423	LOAD_FAST         'cv'
426	LOAD_ATTR         'release'
429	CALL_FUNCTION_0   None
432	POP_TOP           None
433	JUMP_BACK         '3'

436	CONTINUE          '3'
439	JUMP_BACK         '3'
442	POP_BLOCK         None
443_0	COME_FROM         '0'
443	LOAD_CONST        None
446	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 442

    def handle_EOF(self):
        """action taken upon link being closed by peer"""
        self.EOFhook()
        self.debug('handle_EOF')
        for key in self.cvars:
            cv = self.cvars[key]
            cv.acquire()
            self.responses[key] = ('EOF', None)
            cv.notify()
            cv.release()

        self.exithook()
        return None

    def EOFhook(self):
        """Classes using rpc client/server can override to augment EOF action"""
        pass


class RemoteObject(object):
    pass


def remoteref(obj):
    oid = id(obj)
    objecttable[oid] = obj
    return RemoteProxy(oid)


class RemoteProxy(object):

    def __init__(self, oid):
        self.oid = oid


class RPCHandler(SocketServer.BaseRequestHandler, SocketIO):
    debugging = False
    location = '#S'

    def __init__(self, sock, addr, svr):
        svr.current_handler = self
        SocketIO.__init__(self, sock)
        SocketServer.BaseRequestHandler.__init__(self, sock, addr, svr)

    def handle(self):
        """handle() method required by SocketServer"""
        self.mainloop()

    def get_remote_proxy(self, oid):
        return RPCProxy(self, oid)


class RPCClient(SocketIO):
    debugging = False
    location = '#C'
    nextseq = 1

    def __init__(self, address, family = socket.AF_INET, type = socket.SOCK_STREAM):
        self.listening_sock = socket.socket(family, type)
        self.listening_sock.bind(address)
        self.listening_sock.listen(1)

    def accept(self):
        working_sock, address = self.listening_sock.accept()
        if self.debugging:
            print >> sys.__stderr__, '****** Connection request from ', address
        if address[0] == LOCALHOST:
            SocketIO.__init__(self, working_sock)
        else:
            print >> sys.__stderr__, '** Invalid host: ', address
            raise socket.error

    def get_remote_proxy(self, oid):
        return RPCProxy(self, oid)


class RPCProxy(object):
    __methods = None
    __attributes = None

    def __init__(self, sockio, oid):
        self.sockio = sockio
        self.oid = oid

    def __getattr__(self, name):
        if self.__methods is None:
            self.__getmethods()
        if self.__methods.get(name):
            return MethodProxy(self.sockio, self.oid, name)
        else:
            if self.__attributes is None:
                self.__getattributes()
            if name in self.__attributes:
                value = self.sockio.remotecall(self.oid, '__getattribute__', (name,), {})
                return value
            raise AttributeError, name
            return

    def __getattributes(self):
        self.__attributes = self.sockio.remotecall(self.oid, '__attributes__', (), {})

    def __getmethods(self):
        self.__methods = self.sockio.remotecall(self.oid, '__methods__', (), {})


def _getmethods(obj, methods):
    for name in dir(obj):
        attr = getattr(obj, name)
        if hasattr(attr, '__call__'):
            methods[name] = 1

    if type(obj) == types.InstanceType:
        _getmethods(obj.__class__, methods)
    if type(obj) == types.ClassType:
        for super in obj.__bases__:
            _getmethods(super, methods)


def _getattributes(obj, attributes):
    for name in dir(obj):
        attr = getattr(obj, name)
        if not hasattr(attr, '__call__'):
            attributes[name] = 1


class MethodProxy(object):

    def __init__(self, sockio, oid, name):
        self.sockio = sockio
        self.oid = oid
        self.name = name

    def __call__(self, *args, **kwargs):
        value = self.sockio.remotecall(self.oid, self.name, args, kwargs)
        return value