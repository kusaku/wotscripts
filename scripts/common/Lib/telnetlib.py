# Embedded file name: scripts/common/Lib/telnetlib.py
r"""TELNET client class.

Based on RFC 854: TELNET Protocol Specification, by J. Postel and
J. Reynolds

Example:

>>> from telnetlib import Telnet
>>> tn = Telnet('www.python.org', 79)   # connect to finger port
>>> tn.write('guido\r\n')
>>> print tn.read_all()
Login       Name               TTY         Idle    When    Where
guido    Guido van Rossum      pts/2        <Dec  2 11:10> snag.cnri.reston..

>>>

Note that read_all() won't read until eof -- it just reads some data
-- but it guarantees to read at least one byte unless EOF is hit.

It is possible to pass a Telnet object to select.select() in order to
wait until more data is available.  Note that in this case,
read_eager() may return '' even if there was data on the socket,
because the protocol negotiation may have eaten the data.  This is why
EOFError is needed in some cases to distinguish between "no data" and
"connection closed" (since the socket also appears ready for reading
when it is closed).

To do:
- option negotiation
- timeout should be intrinsic to the connection object instead of an
  option on one of the read calls only

"""
import sys
import socket
import select
__all__ = ['Telnet']
DEBUGLEVEL = 0
TELNET_PORT = 23
IAC = chr(255)
DONT = chr(254)
DO = chr(253)
WONT = chr(252)
WILL = chr(251)
theNULL = chr(0)
SE = chr(240)
NOP = chr(241)
DM = chr(242)
BRK = chr(243)
IP = chr(244)
AO = chr(245)
AYT = chr(246)
EC = chr(247)
EL = chr(248)
GA = chr(249)
SB = chr(250)
BINARY = chr(0)
ECHO = chr(1)
RCP = chr(2)
SGA = chr(3)
NAMS = chr(4)
STATUS = chr(5)
TM = chr(6)
RCTE = chr(7)
NAOL = chr(8)
NAOP = chr(9)
NAOCRD = chr(10)
NAOHTS = chr(11)
NAOHTD = chr(12)
NAOFFD = chr(13)
NAOVTS = chr(14)
NAOVTD = chr(15)
NAOLFD = chr(16)
XASCII = chr(17)
LOGOUT = chr(18)
BM = chr(19)
DET = chr(20)
SUPDUP = chr(21)
SUPDUPOUTPUT = chr(22)
SNDLOC = chr(23)
TTYPE = chr(24)
EOR = chr(25)
TUID = chr(26)
OUTMRK = chr(27)
TTYLOC = chr(28)
VT3270REGIME = chr(29)
X3PAD = chr(30)
NAWS = chr(31)
TSPEED = chr(32)
LFLOW = chr(33)
LINEMODE = chr(34)
XDISPLOC = chr(35)
OLD_ENVIRON = chr(36)
AUTHENTICATION = chr(37)
ENCRYPT = chr(38)
NEW_ENVIRON = chr(39)
TN3270E = chr(40)
XAUTH = chr(41)
CHARSET = chr(42)
RSP = chr(43)
COM_PORT_OPTION = chr(44)
SUPPRESS_LOCAL_ECHO = chr(45)
TLS = chr(46)
KERMIT = chr(47)
SEND_URL = chr(48)
FORWARD_X = chr(49)
PRAGMA_LOGON = chr(138)
SSPI_LOGON = chr(139)
PRAGMA_HEARTBEAT = chr(140)
EXOPL = chr(255)
NOOPT = chr(0)

class Telnet():
    """Telnet interface class.
    
    An instance of this class represents a connection to a telnet
    server.  The instance is initially not connected; the open()
    method must be used to establish a connection.  Alternatively, the
    host name and optional port number can be passed to the
    constructor, too.
    
    Don't try to reopen an already connected instance.
    
    This class has many read_*() methods.  Note that some of them
    raise EOFError when the end of the connection is read, because
    they can return an empty string for other reasons.  See the
    individual doc strings.
    
    read_until(expected, [timeout])
        Read until the expected string has been seen, or a timeout is
        hit (default is no timeout); may block.
    
    read_all()
        Read all data until EOF; may block.
    
    read_some()
        Read at least one byte or EOF; may block.
    
    read_very_eager()
        Read all data available already queued or on the socket,
        without blocking.
    
    read_eager()
        Read either data already queued or some data available on the
        socket, without blocking.
    
    read_lazy()
        Read all data in the raw queue (processing it first), without
        doing any socket I/O.
    
    read_very_lazy()
        Reads all data in the cooked queue, without doing any socket
        I/O.
    
    read_sb_data()
        Reads available data between SB ... SE sequence. Don't block.
    
    set_option_negotiation_callback(callback)
        Each time a telnet option is read on the input flow, this callback
        (if set) is called with the following parameters :
        callback(telnet socket, command, option)
            option will be chr(0) when there is no option.
        No other action is done afterwards by telnetlib.
    
    """

    def __init__(self, host = None, port = 0, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
        """Constructor.
        
        When called without arguments, create an unconnected instance.
        With a hostname argument, it connects the instance; port number
        and timeout are optional.
        """
        self.debuglevel = DEBUGLEVEL
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.rawq = ''
        self.irawq = 0
        self.cookedq = ''
        self.eof = 0
        self.iacseq = ''
        self.sb = 0
        self.sbdataq = ''
        self.option_callback = None
        if host is not None:
            self.open(host, port, timeout)
        return

    def open(self, host, port = 0, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
        """Connect to a host.
        
        The optional second argument is the port number, which
        defaults to the standard telnet port (23).
        
        Don't try to reopen an already connected instance.
        """
        self.eof = 0
        if not port:
            port = TELNET_PORT
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((host, port), timeout)

    def __del__(self):
        """Destructor -- close the connection."""
        self.close()

    def msg(self, msg, *args):
        """Print a debug message, when the debug level is > 0.
        
        If extra arguments are present, they are substituted in the
        message using the standard string formatting operator.
        
        """
        if self.debuglevel > 0:
            print 'Telnet(%s,%s):' % (self.host, self.port),
            if args:
                print msg % args
            else:
                print msg

    def set_debuglevel(self, debuglevel):
        """Set the debug level.
        
        The higher it is, the more debug output you get (on sys.stdout).
        
        """
        self.debuglevel = debuglevel

    def close(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()
        self.sock = 0
        self.eof = 1
        self.iacseq = ''
        self.sb = 0

    def get_socket(self):
        """Return the socket object used internally."""
        return self.sock

    def fileno(self):
        """Return the fileno() of the socket object used internally."""
        return self.sock.fileno()

    def write(self, buffer):
        """Write a string to the socket, doubling any IAC characters.
        
        Can block if the connection is blocked.  May raise
        socket.error if the connection is closed.
        
        """
        if IAC in buffer:
            buffer = buffer.replace(IAC, IAC + IAC)
        self.msg('send %r', buffer)
        self.sock.sendall(buffer)

    def read_until(self, match, timeout = None):
        """Read until a given string is encountered or until timeout.
        
        When no match is found, return whatever is available instead,
        possibly the empty string.  Raise EOFError if the connection
        is closed and no cooked data is available.
        
        """
        n = len(match)
        self.process_rawq()
        i = self.cookedq.find(match)
        if i >= 0:
            i = i + n
            buf = self.cookedq[:i]
            self.cookedq = self.cookedq[i:]
            return buf
        else:
            s_reply = ([self], [], [])
            s_args = s_reply
            if timeout is not None:
                s_args = s_args + (timeout,)
                from time import time
                time_start = time()
            while not self.eof and select.select(*s_args) == s_reply:
                i = max(0, len(self.cookedq) - n)
                self.fill_rawq()
                self.process_rawq()
                i = self.cookedq.find(match, i)
                if i >= 0:
                    i = i + n
                    buf = self.cookedq[:i]
                    self.cookedq = self.cookedq[i:]
                    return buf
                if timeout is not None:
                    elapsed = time() - time_start
                    if elapsed >= timeout:
                        break
                    s_args = s_reply + (timeout - elapsed,)

            return self.read_very_lazy()

    def read_all(self):
        """Read all data until EOF; block until connection closed."""
        self.process_rawq()
        while not self.eof:
            self.fill_rawq()
            self.process_rawq()

        buf = self.cookedq
        self.cookedq = ''
        return buf

    def read_some(self):
        """Read at least one byte of cooked data unless EOF is hit.
        
        Return '' if EOF is hit.  Block if no data is immediately
        available.
        
        """
        self.process_rawq()
        while not self.cookedq and not self.eof:
            self.fill_rawq()
            self.process_rawq()

        buf = self.cookedq
        self.cookedq = ''
        return buf

    def read_very_eager(self):
        """Read everything that's possible without blocking in I/O (eager).
        
        Raise EOFError if connection closed and no cooked data
        available.  Return '' if no cooked data available otherwise.
        Don't block unless in the midst of an IAC sequence.
        
        """
        self.process_rawq()
        while not self.eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()

        return self.read_very_lazy()

    def read_eager(self):
        """Read readily available data.
        
        Raise EOFError if connection closed and no cooked data
        available.  Return '' if no cooked data available otherwise.
        Don't block unless in the midst of an IAC sequence.
        
        """
        self.process_rawq()
        while not self.cookedq and not self.eof and self.sock_avail():
            self.fill_rawq()
            self.process_rawq()

        return self.read_very_lazy()

    def read_lazy(self):
        """Process and return data that's already in the queues (lazy).
        
        Raise EOFError if connection closed and no data available.
        Return '' if no cooked data available otherwise.  Don't block
        unless in the midst of an IAC sequence.
        
        """
        self.process_rawq()
        return self.read_very_lazy()

    def read_very_lazy(self):
        """Return any data available in the cooked queue (very lazy).
        
        Raise EOFError if connection closed and no data available.
        Return '' if no cooked data available otherwise.  Don't block.
        
        """
        buf = self.cookedq
        self.cookedq = ''
        if not buf and self.eof and not self.rawq:
            raise EOFError, 'telnet connection closed'
        return buf

    def read_sb_data(self):
        """Return any data available in the SB ... SE queue.
        
        Return '' if no SB ... SE available. Should only be called
        after seeing a SB or SE command. When a new SB command is
        found, old unread SB data will be discarded. Don't block.
        
        """
        buf = self.sbdataq
        self.sbdataq = ''
        return buf

    def set_option_negotiation_callback(self, callback):
        """Provide a callback function called after each receipt of a telnet option."""
        self.option_callback = callback

    def process_rawq(self):
        """Transfer from raw queue to cooked queue.
        
        Set self.eof when connection is closed.  Don't block unless in
        the midst of an IAC sequence.
        
        """
        buf = ['', '']
        try:
            while self.rawq:
                c = self.rawq_getchar()
                if not self.iacseq:
                    if c == theNULL:
                        continue
                    if c == '\x11':
                        continue
                    if c != IAC:
                        buf[self.sb] = buf[self.sb] + c
                        continue
                    else:
                        self.iacseq += c
                elif len(self.iacseq) == 1:
                    if c in (DO,
                     DONT,
                     WILL,
                     WONT):
                        self.iacseq += c
                        continue
                    self.iacseq = ''
                    if c == IAC:
                        buf[self.sb] = buf[self.sb] + c
                    else:
                        if c == SB:
                            self.sb = 1
                            self.sbdataq = ''
                        elif c == SE:
                            self.sb = 0
                            self.sbdataq = self.sbdataq + buf[1]
                            buf[1] = ''
                        if self.option_callback:
                            self.option_callback(self.sock, c, NOOPT)
                        else:
                            self.msg('IAC %d not recognized' % ord(c))
                elif len(self.iacseq) == 2:
                    cmd = self.iacseq[1]
                    self.iacseq = ''
                    opt = c
                    if cmd in (DO, DONT):
                        self.msg('IAC %s %d', cmd == DO and 'DO' or 'DONT', ord(opt))
                        if self.option_callback:
                            self.option_callback(self.sock, cmd, opt)
                        else:
                            self.sock.sendall(IAC + WONT + opt)
                    elif cmd in (WILL, WONT):
                        self.msg('IAC %s %d', cmd == WILL and 'WILL' or 'WONT', ord(opt))
                        if self.option_callback:
                            self.option_callback(self.sock, cmd, opt)
                        else:
                            self.sock.sendall(IAC + DONT + opt)

        except EOFError:
            self.iacseq = ''
            self.sb = 0

        self.cookedq = self.cookedq + buf[0]
        self.sbdataq = self.sbdataq + buf[1]

    def rawq_getchar(self):
        """Get next char from raw queue.
        
        Block if no data is immediately available.  Raise EOFError
        when connection is closed.
        
        """
        if not self.rawq:
            self.fill_rawq()
            if self.eof:
                raise EOFError
        c = self.rawq[self.irawq]
        self.irawq = self.irawq + 1
        if self.irawq >= len(self.rawq):
            self.rawq = ''
            self.irawq = 0
        return c

    def fill_rawq(self):
        """Fill raw queue from exactly one recv() system call.
        
        Block if no data is immediately available.  Set self.eof when
        connection is closed.
        
        """
        if self.irawq >= len(self.rawq):
            self.rawq = ''
            self.irawq = 0
        buf = self.sock.recv(50)
        self.msg('recv %r', buf)
        self.eof = not buf
        self.rawq = self.rawq + buf

    def sock_avail(self):
        """Test whether data is available on the socket."""
        return select.select([self], [], [], 0) == ([self], [], [])

    def interact--- This code section failed: ---

0	LOAD_GLOBAL       'sys'
3	LOAD_ATTR         'platform'
6	LOAD_CONST        'win32'
9	COMPARE_OP        '=='
12	POP_JUMP_IF_FALSE '29'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'mt_interact'
21	CALL_FUNCTION_0   None
24	POP_TOP           None

25	LOAD_CONST        None
28	RETURN_END_IF     None

29	SETUP_LOOP        '226'

32	LOAD_GLOBAL       'select'
35	LOAD_ATTR         'select'
38	LOAD_FAST         'self'
41	LOAD_GLOBAL       'sys'
44	LOAD_ATTR         'stdin'
47	BUILD_LIST_2      None
50	BUILD_LIST_0      None
53	BUILD_LIST_0      None
56	CALL_FUNCTION_3   None
59	UNPACK_SEQUENCE_3 None
62	STORE_FAST        'rfd'
65	STORE_FAST        'wfd'
68	STORE_FAST        'xfd'

71	LOAD_FAST         'self'
74	LOAD_FAST         'rfd'
77	COMPARE_OP        'in'
80	POP_JUMP_IF_FALSE '166'

83	SETUP_EXCEPT      '102'

86	LOAD_FAST         'self'
89	LOAD_ATTR         'read_eager'
92	CALL_FUNCTION_0   None
95	STORE_FAST        'text'
98	POP_BLOCK         None
99	JUMP_FORWARD      '125'
102_0	COME_FROM         '83'

102	DUP_TOP           None
103	LOAD_GLOBAL       'EOFError'
106	COMPARE_OP        'exception match'
109	POP_JUMP_IF_FALSE '124'
112	POP_TOP           None
113	POP_TOP           None
114	POP_TOP           None

115	LOAD_CONST        '*** Connection closed by remote host ***'
118	PRINT_ITEM        None
119	PRINT_NEWLINE_CONT None

120	BREAK_LOOP        None
121	JUMP_FORWARD      '125'
124	END_FINALLY       None
125_0	COME_FROM         '99'
125_1	COME_FROM         '124'

125	LOAD_FAST         'text'
128	POP_JUMP_IF_FALSE '166'

131	LOAD_GLOBAL       'sys'
134	LOAD_ATTR         'stdout'
137	LOAD_ATTR         'write'
140	LOAD_FAST         'text'
143	CALL_FUNCTION_1   None
146	POP_TOP           None

147	LOAD_GLOBAL       'sys'
150	LOAD_ATTR         'stdout'
153	LOAD_ATTR         'flush'
156	CALL_FUNCTION_0   None
159	POP_TOP           None
160	JUMP_ABSOLUTE     '166'
163	JUMP_FORWARD      '166'
166_0	COME_FROM         '163'

166	LOAD_GLOBAL       'sys'
169	LOAD_ATTR         'stdin'
172	LOAD_FAST         'rfd'
175	COMPARE_OP        'in'
178	POP_JUMP_IF_FALSE '32'

181	LOAD_GLOBAL       'sys'
184	LOAD_ATTR         'stdin'
187	LOAD_ATTR         'readline'
190	CALL_FUNCTION_0   None
193	STORE_FAST        'line'

196	LOAD_FAST         'line'
199	POP_JUMP_IF_TRUE  '206'

202	BREAK_LOOP        None
203	JUMP_FORWARD      '206'
206_0	COME_FROM         '203'

206	LOAD_FAST         'self'
209	LOAD_ATTR         'write'
212	LOAD_FAST         'line'
215	CALL_FUNCTION_1   None
218	POP_TOP           None
219	JUMP_BACK         '32'
222	JUMP_BACK         '32'
225	POP_BLOCK         None
226_0	COME_FROM         '29'

Syntax error at or near `POP_BLOCK' token at offset 225

    def mt_interact--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        None
6	IMPORT_NAME       'thread'
9	STORE_FAST        'thread'

12	LOAD_FAST         'thread'
15	LOAD_ATTR         'start_new_thread'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'listener'
24	LOAD_CONST        ()
27	CALL_FUNCTION_2   None
30	POP_TOP           None

31	SETUP_LOOP        '76'

34	LOAD_GLOBAL       'sys'
37	LOAD_ATTR         'stdin'
40	LOAD_ATTR         'readline'
43	CALL_FUNCTION_0   None
46	STORE_FAST        'line'

49	LOAD_FAST         'line'
52	POP_JUMP_IF_TRUE  '59'

55	BREAK_LOOP        None
56	JUMP_FORWARD      '59'
59_0	COME_FROM         '56'

59	LOAD_FAST         'self'
62	LOAD_ATTR         'write'
65	LOAD_FAST         'line'
68	CALL_FUNCTION_1   None
71	POP_TOP           None
72	JUMP_BACK         '34'
75	POP_BLOCK         None
76_0	COME_FROM         '31'

Syntax error at or near `POP_BLOCK' token at offset 75

    def listener--- This code section failed: ---

0	SETUP_LOOP        '87'

3	SETUP_EXCEPT      '22'

6	LOAD_FAST         'self'
9	LOAD_ATTR         'read_eager'
12	CALL_FUNCTION_0   None
15	STORE_FAST        'data'
18	POP_BLOCK         None
19	JUMP_FORWARD      '45'
22_0	COME_FROM         '3'

22	DUP_TOP           None
23	LOAD_GLOBAL       'EOFError'
26	COMPARE_OP        'exception match'
29	POP_JUMP_IF_FALSE '44'
32	POP_TOP           None
33	POP_TOP           None
34	POP_TOP           None

35	LOAD_CONST        '*** Connection closed by remote host ***'
38	PRINT_ITEM        None
39	PRINT_NEWLINE_CONT None

40	LOAD_CONST        None
43	RETURN_VALUE      None
44	END_FINALLY       None
45_0	COME_FROM         '19'
45_1	COME_FROM         '44'

45	LOAD_FAST         'data'
48	POP_JUMP_IF_FALSE '70'

51	LOAD_GLOBAL       'sys'
54	LOAD_ATTR         'stdout'
57	LOAD_ATTR         'write'
60	LOAD_FAST         'data'
63	CALL_FUNCTION_1   None
66	POP_TOP           None
67	JUMP_BACK         '3'

70	LOAD_GLOBAL       'sys'
73	LOAD_ATTR         'stdout'
76	LOAD_ATTR         'flush'
79	CALL_FUNCTION_0   None
82	POP_TOP           None
83	JUMP_BACK         '3'
86	POP_BLOCK         None
87_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 86

    def expect--- This code section failed: ---

0	LOAD_CONST        None
3	STORE_FAST        're'

6	LOAD_FAST         'list'
9	SLICE+0           None
10	STORE_FAST        'list'

13	LOAD_GLOBAL       'range'
16	LOAD_GLOBAL       'len'
19	LOAD_FAST         'list'
22	CALL_FUNCTION_1   None
25	CALL_FUNCTION_1   None
28	STORE_FAST        'indices'

31	SETUP_LOOP        '114'
34	LOAD_FAST         'indices'
37	GET_ITER          None
38	FOR_ITER          '113'
41	STORE_FAST        'i'

44	LOAD_GLOBAL       'hasattr'
47	LOAD_FAST         'list'
50	LOAD_FAST         'i'
53	BINARY_SUBSCR     None
54	LOAD_CONST        'search'
57	CALL_FUNCTION_2   None
60	POP_JUMP_IF_TRUE  '38'

63	LOAD_FAST         're'
66	POP_JUMP_IF_TRUE  '84'
69	LOAD_CONST        -1
72	LOAD_CONST        None
75	IMPORT_NAME       're'
78	STORE_FAST        're'
81	JUMP_FORWARD      '84'
84_0	COME_FROM         '81'

84	LOAD_FAST         're'
87	LOAD_ATTR         'compile'
90	LOAD_FAST         'list'
93	LOAD_FAST         'i'
96	BINARY_SUBSCR     None
97	CALL_FUNCTION_1   None
100	LOAD_FAST         'list'
103	LOAD_FAST         'i'
106	STORE_SUBSCR      None
107	JUMP_BACK         '38'
110	JUMP_BACK         '38'
113	POP_BLOCK         None
114_0	COME_FROM         '31'

114	LOAD_FAST         'timeout'
117	LOAD_CONST        None
120	COMPARE_OP        'is not'
123	POP_JUMP_IF_FALSE '154'

126	LOAD_CONST        -1
129	LOAD_CONST        ('time',)
132	IMPORT_NAME       'time'
135	IMPORT_FROM       'time'
138	STORE_FAST        'time'
141	POP_TOP           None

142	LOAD_FAST         'time'
145	CALL_FUNCTION_0   None
148	STORE_FAST        'time_start'
151	JUMP_FORWARD      '154'
154_0	COME_FROM         '151'

154	SETUP_LOOP        '402'

157	LOAD_FAST         'self'
160	LOAD_ATTR         'process_rawq'
163	CALL_FUNCTION_0   None
166	POP_TOP           None

167	SETUP_LOOP        '266'
170	LOAD_FAST         'indices'
173	GET_ITER          None
174	FOR_ITER          '265'
177	STORE_FAST        'i'

180	LOAD_FAST         'list'
183	LOAD_FAST         'i'
186	BINARY_SUBSCR     None
187	LOAD_ATTR         'search'
190	LOAD_FAST         'self'
193	LOAD_ATTR         'cookedq'
196	CALL_FUNCTION_1   None
199	STORE_FAST        'm'

202	LOAD_FAST         'm'
205	POP_JUMP_IF_FALSE '174'

208	LOAD_FAST         'm'
211	LOAD_ATTR         'end'
214	CALL_FUNCTION_0   None
217	STORE_FAST        'e'

220	LOAD_FAST         'self'
223	LOAD_ATTR         'cookedq'
226	LOAD_FAST         'e'
229	SLICE+2           None
230	STORE_FAST        'text'

233	LOAD_FAST         'self'
236	LOAD_ATTR         'cookedq'
239	LOAD_FAST         'e'
242	SLICE+1           None
243	LOAD_FAST         'self'
246	STORE_ATTR        'cookedq'

249	LOAD_FAST         'i'
252	LOAD_FAST         'm'
255	LOAD_FAST         'text'
258	BUILD_TUPLE_3     None
261	RETURN_END_IF     None
262	JUMP_BACK         '174'
265	POP_BLOCK         None
266_0	COME_FROM         '167'

266	LOAD_FAST         'self'
269	LOAD_ATTR         'eof'
272	POP_JUMP_IF_FALSE '279'

275	BREAK_LOOP        None
276	JUMP_FORWARD      '279'
279_0	COME_FROM         '276'

279	LOAD_FAST         'timeout'
282	LOAD_CONST        None
285	COMPARE_OP        'is not'
288	POP_JUMP_IF_FALSE '388'

291	LOAD_FAST         'time'
294	CALL_FUNCTION_0   None
297	LOAD_FAST         'time_start'
300	BINARY_SUBTRACT   None
301	STORE_FAST        'elapsed'

304	LOAD_FAST         'elapsed'
307	LOAD_FAST         'timeout'
310	COMPARE_OP        '>='
313	POP_JUMP_IF_FALSE '320'

316	BREAK_LOOP        None
317	JUMP_FORWARD      '320'
320_0	COME_FROM         '317'

320	LOAD_FAST         'self'
323	LOAD_ATTR         'fileno'
326	CALL_FUNCTION_0   None
329	BUILD_LIST_1      None
332	BUILD_LIST_0      None
335	BUILD_LIST_0      None
338	LOAD_FAST         'timeout'
341	LOAD_FAST         'elapsed'
344	BINARY_SUBTRACT   None
345	BUILD_TUPLE_4     None
348	STORE_FAST        's_args'

351	LOAD_GLOBAL       'select'
354	LOAD_ATTR         'select'
357	LOAD_FAST         's_args'
360	CALL_FUNCTION_VAR_0 None
363	UNPACK_SEQUENCE_3 None
366	STORE_FAST        'r'
369	STORE_FAST        'w'
372	STORE_FAST        'x'

375	LOAD_FAST         'r'
378	POP_JUMP_IF_TRUE  '388'

381	BREAK_LOOP        None
382	JUMP_ABSOLUTE     '388'
385	JUMP_FORWARD      '388'
388_0	COME_FROM         '385'

388	LOAD_FAST         'self'
391	LOAD_ATTR         'fill_rawq'
394	CALL_FUNCTION_0   None
397	POP_TOP           None
398	JUMP_BACK         '157'
401	POP_BLOCK         None
402_0	COME_FROM         '154'

402	LOAD_FAST         'self'
405	LOAD_ATTR         'read_very_lazy'
408	CALL_FUNCTION_0   None
411	STORE_FAST        'text'

414	LOAD_FAST         'text'
417	UNARY_NOT         None
418	POP_JUMP_IF_FALSE '439'
421	LOAD_FAST         'self'
424	LOAD_ATTR         'eof'
427_0	COME_FROM         '418'
427	POP_JUMP_IF_FALSE '439'

430	LOAD_GLOBAL       'EOFError'
433	RAISE_VARARGS_1   None
436	JUMP_FORWARD      '439'
439_0	COME_FROM         '436'

439	LOAD_CONST        -1
442	LOAD_CONST        None
445	LOAD_FAST         'text'
448	BUILD_TUPLE_3     None
451	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 401


def test():
    """Test program for telnetlib.
    
    Usage: python telnetlib.py [-d] ... [host [port]]
    
    Default host is localhost; default port is 23.
    
    """
    debuglevel = 0
    while sys.argv[1:] and sys.argv[1] == '-d':
        debuglevel = debuglevel + 1
        del sys.argv[1]

    host = 'localhost'
    if sys.argv[1:]:
        host = sys.argv[1]
    port = 0
    if sys.argv[2:]:
        portstr = sys.argv[2]
        try:
            port = int(portstr)
        except ValueError:
            port = socket.getservbyname(portstr, 'tcp')

    tn = Telnet()
    tn.set_debuglevel(debuglevel)
    tn.open(host, port, timeout=0.5)
    tn.interact()
    tn.close()


if __name__ == '__main__':
    test()