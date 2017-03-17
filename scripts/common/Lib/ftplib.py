# Embedded file name: scripts/common/Lib/ftplib.py
"""An FTP client class and some helper functions.

Based on RFC 959: File Transfer Protocol (FTP), by J. Postel and J. Reynolds

Example:

>>> from ftplib import FTP
>>> ftp = FTP('ftp.python.org') # connect to host, default port
>>> ftp.login() # default, i.e.: user anonymous, passwd anonymous@
'230 Guest login ok, access restrictions apply.'
>>> ftp.retrlines('LIST') # list directory contents
total 9
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 .
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 ..
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 bin
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 etc
d-wxrwxr-x   2 ftp      wheel        1024 Sep  5 13:43 incoming
drwxr-xr-x   2 root     wheel        1024 Nov 17  1993 lib
drwxr-xr-x   6 1094     wheel        1024 Sep 13 19:07 pub
drwxr-xr-x   3 root     wheel        1024 Jan  3  1994 usr
-rw-r--r--   1 root     root          312 Aug  1  1994 welcome.msg
'226 Transfer complete.'
>>> ftp.quit()
'221 Goodbye.'
>>>

A nice test that reveals some of the network dialogue would be:
python ftplib.py -d localhost -l -p -l
"""
import os
import sys
try:
    import SOCKS
    socket = SOCKS
    del SOCKS
    from socket import getfqdn
    socket.getfqdn = getfqdn
    del getfqdn
except ImportError:
    import socket

from socket import _GLOBAL_DEFAULT_TIMEOUT
__all__ = ['FTP', 'Netrc']
MSG_OOB = 1
FTP_PORT = 21

class Error(Exception):
    pass


class error_reply(Error):
    pass


class error_temp(Error):
    pass


class error_perm(Error):
    pass


class error_proto(Error):
    pass


all_errors = (Error, IOError, EOFError)
CRLF = '\r\n'

class FTP():
    """An FTP client class.
    
        To create a connection, call the class using these arguments:
                host, user, passwd, acct, timeout
    
        The first four arguments are all strings, and have default value ''.
        timeout must be numeric and defaults to None if not passed,
        meaning that no timeout will be set on any ftp socket(s)
        If a timeout is passed, then this is now the default timeout for all ftp
        socket operations for this instance.
    
        Then use self.connect() with optional host and port argument.
    
        To download a file, use ftp.retrlines('RETR ' + filename),
        or ftp.retrbinary() with slightly different arguments.
        To upload a file, use ftp.storlines() or ftp.storbinary(),
        which have an open file as argument (see their definitions
        below for details).
        The download/upload functions first issue appropriate TYPE
        and PORT or PASV commands.
    """
    debugging = 0
    host = ''
    port = FTP_PORT
    sock = None
    file = None
    welcome = None
    passiveserver = 1

    def __init__(self, host = '', user = '', passwd = '', acct = '', timeout = _GLOBAL_DEFAULT_TIMEOUT):
        self.timeout = timeout
        if host:
            self.connect(host)
            if user:
                self.login(user, passwd, acct)

    def connect(self, host = '', port = 0, timeout = -999):
        """Connect to host.  Arguments are:
         - host: hostname to connect to (string, default previous host)
         - port: port to connect to (integer, default previous port)
        """
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), self.timeout)
        self.af = self.sock.family
        self.file = self.sock.makefile('rb')
        self.welcome = self.getresp()
        return self.welcome

    def getwelcome(self):
        """Get the welcome message from the server.
        (this is read and squirreled away by connect())"""
        if self.debugging:
            print '*welcome*', self.sanitize(self.welcome)
        return self.welcome

    def set_debuglevel(self, level):
        """Set the debugging level.
        The required argument level means:
        0: no debugging output (default)
        1: print commands and responses but not body text etc.
        2: also print raw lines read and sent before stripping CR/LF"""
        self.debugging = level

    debug = set_debuglevel

    def set_pasv(self, val):
        """Use passive or active mode for data transfers.
        With a false argument, use the normal PORT mode,
        With a true argument, use the PASV command."""
        self.passiveserver = val

    def sanitize(self, s):
        if s[:5] == 'pass ' or s[:5] == 'PASS ':
            i = len(s)
            while i > 5 and s[i - 1] in '\r\n':
                i = i - 1

            s = s[:5] + '*' * (i - 5) + s[i:]
        return repr(s)

    def putline(self, line):
        line = line + CRLF
        if self.debugging > 1:
            print '*put*', self.sanitize(line)
        self.sock.sendall(line)

    def putcmd(self, line):
        if self.debugging:
            print '*cmd*', self.sanitize(line)
        self.putline(line)

    def getline(self):
        line = self.file.readline()
        if self.debugging > 1:
            print '*get*', self.sanitize(line)
        if not line:
            raise EOFError
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        return line

    def getmultiline--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'getline'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'line'

12	LOAD_FAST         'line'
15	LOAD_CONST        3
18	LOAD_CONST        4
21	SLICE+3           None
22	LOAD_CONST        '-'
25	COMPARE_OP        '=='
28	POP_JUMP_IF_FALSE '116'

31	LOAD_FAST         'line'
34	LOAD_CONST        3
37	SLICE+2           None
38	STORE_FAST        'code'

41	SETUP_LOOP        '116'

44	LOAD_FAST         'self'
47	LOAD_ATTR         'getline'
50	CALL_FUNCTION_0   None
53	STORE_FAST        'nextline'

56	LOAD_FAST         'line'
59	LOAD_CONST        '\n'
62	LOAD_FAST         'nextline'
65	BINARY_ADD        None
66	BINARY_ADD        None
67	STORE_FAST        'line'

70	LOAD_FAST         'nextline'
73	LOAD_CONST        3
76	SLICE+2           None
77	LOAD_FAST         'code'
80	COMPARE_OP        '=='
83	POP_JUMP_IF_FALSE '44'

86	LOAD_FAST         'nextline'
89	LOAD_CONST        3
92	LOAD_CONST        4
95	SLICE+3           None
96	LOAD_CONST        '-'
99	COMPARE_OP        '!='
102_0	COME_FROM         '83'
102	POP_JUMP_IF_FALSE '44'

105	BREAK_LOOP        None
106	JUMP_BACK         '44'
109	JUMP_BACK         '44'
112	POP_BLOCK         None
113_0	COME_FROM         '41'
113	JUMP_FORWARD      '116'
116_0	COME_FROM         '113'

116	LOAD_FAST         'line'
119	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 112

    def getresp(self):
        resp = self.getmultiline()
        if self.debugging:
            print '*resp*', self.sanitize(resp)
        self.lastresp = resp[:3]
        c = resp[:1]
        if c in ('1', '2', '3'):
            return resp
        if c == '4':
            raise error_temp, resp
        if c == '5':
            raise error_perm, resp
        raise error_proto, resp

    def voidresp(self):
        """Expect a response beginning with '2'."""
        resp = self.getresp()
        if resp[:1] != '2':
            raise error_reply, resp
        return resp

    def abort(self):
        """Abort a file transfer.  Uses out-of-band data.
        This does not follow the procedure from the RFC to send Telnet
        IP and Synch; that doesn't seem to work with the servers I've
        tried.  Instead, just send the ABOR command as OOB data."""
        line = 'ABOR' + CRLF
        if self.debugging > 1:
            print '*put urgent*', self.sanitize(line)
        self.sock.sendall(line, MSG_OOB)
        resp = self.getmultiline()
        if resp[:3] not in ('426', '225', '226'):
            raise error_proto, resp

    def sendcmd(self, cmd):
        """Send a command and return the response."""
        self.putcmd(cmd)
        return self.getresp()

    def voidcmd(self, cmd):
        """Send a command and expect a response beginning with '2'."""
        self.putcmd(cmd)
        return self.voidresp()

    def sendport(self, host, port):
        """Send a PORT command with the current host and the given
        port number.
        """
        hbytes = host.split('.')
        pbytes = [repr(port // 256), repr(port % 256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.voidcmd(cmd)

    def sendeprt(self, host, port):
        """Send a EPRT command with the current host and the given port number."""
        af = 0
        if self.af == socket.AF_INET:
            af = 1
        if self.af == socket.AF_INET6:
            af = 2
        if af == 0:
            raise error_proto, 'unsupported address family'
        fields = ['',
         repr(af),
         host,
         repr(port),
         '']
        cmd = 'EPRT ' + '|'.join(fields)
        return self.voidcmd(cmd)

    def makeport(self):
        """Create a new socket and send a PORT command for it."""
        msg = 'getaddrinfo returns an empty list'
        sock = None
        for res in socket.getaddrinfo(None, 0, self.af, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
                sock.bind(sa)
            except socket.error as msg:
                if sock:
                    sock.close()
                sock = None
                continue

            break

        if not sock:
            raise socket.error, msg
        sock.listen(1)
        port = sock.getsockname()[1]
        host = self.sock.getsockname()[0]
        if self.af == socket.AF_INET:
            resp = self.sendport(host, port)
        else:
            resp = self.sendeprt(host, port)
        if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(self.timeout)
        return sock

    def makepasv(self):
        if self.af == socket.AF_INET:
            host, port = parse227(self.sendcmd('PASV'))
        else:
            host, port = parse229(self.sendcmd('EPSV'), self.sock.getpeername())
        return (host, port)

    def ntransfercmd(self, cmd, rest = None):
        """Initiate a transfer over the data connection.
        
        If the transfer is active, send a port command and the
        transfer command, and accept the connection.  If the server is
        passive, send a pasv command, connect to it, and start the
        transfer command.  Either way, return the socket for the
        connection and the expected size of the transfer.  The
        expected size may be None if it could not be determined.
        
        Optional `rest' argument can be a string that is sent as the
        argument to a REST command.  This is essentially a server
        marker used to tell the server to skip over any data up to the
        given marker.
        """
        size = None
        if self.passiveserver:
            host, port = self.makepasv()
            conn = socket.create_connection((host, port), self.timeout)
            try:
                if rest is not None:
                    self.sendcmd('REST %s' % rest)
                resp = self.sendcmd(cmd)
                if resp[0] == '2':
                    resp = self.getresp()
                if resp[0] != '1':
                    raise error_reply, resp
            except:
                conn.close()
                raise

        else:
            sock = self.makeport()
            try:
                if rest is not None:
                    self.sendcmd('REST %s' % rest)
                resp = self.sendcmd(cmd)
                if resp[0] == '2':
                    resp = self.getresp()
                if resp[0] != '1':
                    raise error_reply, resp
                conn, sockaddr = sock.accept()
                if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                    conn.settimeout(self.timeout)
            finally:
                sock.close()

        if resp[:3] == '150':
            size = parse150(resp)
        return (conn, size)

    def transfercmd(self, cmd, rest = None):
        """Like ntransfercmd() but returns only the socket."""
        return self.ntransfercmd(cmd, rest)[0]

    def login(self, user = '', passwd = '', acct = ''):
        """Login, default anonymous."""
        if not user:
            user = 'anonymous'
        if not passwd:
            passwd = ''
        if not acct:
            acct = ''
        if user == 'anonymous' and passwd in ('', '-'):
            passwd = passwd + 'anonymous@'
        resp = self.sendcmd('USER ' + user)
        if resp[0] == '3':
            resp = self.sendcmd('PASS ' + passwd)
        if resp[0] == '3':
            resp = self.sendcmd('ACCT ' + acct)
        if resp[0] != '2':
            raise error_reply, resp
        return resp

    def retrbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	LOAD_FAST         'rest'
25	CALL_FUNCTION_2   None
28	STORE_FAST        'conn'

31	SETUP_LOOP        '73'

34	LOAD_FAST         'conn'
37	LOAD_ATTR         'recv'
40	LOAD_FAST         'blocksize'
43	CALL_FUNCTION_1   None
46	STORE_FAST        'data'

49	LOAD_FAST         'data'
52	POP_JUMP_IF_TRUE  '59'

55	BREAK_LOOP        None
56	JUMP_FORWARD      '59'
59_0	COME_FROM         '56'

59	LOAD_FAST         'callback'
62	LOAD_FAST         'data'
65	CALL_FUNCTION_1   None
68	POP_TOP           None
69	JUMP_BACK         '34'
72	POP_BLOCK         None
73_0	COME_FROM         '31'

73	LOAD_FAST         'conn'
76	LOAD_ATTR         'close'
79	CALL_FUNCTION_0   None
82	POP_TOP           None

83	LOAD_FAST         'self'
86	LOAD_ATTR         'voidresp'
89	CALL_FUNCTION_0   None
92	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 72

    def retrlines--- This code section failed: ---

0	LOAD_FAST         'callback'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	POP_JUMP_IF_FALSE '21'
12	LOAD_GLOBAL       'print_line'
15	STORE_FAST        'callback'
18	JUMP_FORWARD      '21'
21_0	COME_FROM         '18'

21	LOAD_FAST         'self'
24	LOAD_ATTR         'sendcmd'
27	LOAD_CONST        'TYPE A'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'resp'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'transfercmd'
42	LOAD_FAST         'cmd'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'conn'

51	LOAD_FAST         'conn'
54	LOAD_ATTR         'makefile'
57	LOAD_CONST        'rb'
60	CALL_FUNCTION_1   None
63	STORE_FAST        'fp'

66	SETUP_LOOP        '196'

69	LOAD_FAST         'fp'
72	LOAD_ATTR         'readline'
75	CALL_FUNCTION_0   None
78	STORE_FAST        'line'

81	LOAD_FAST         'self'
84	LOAD_ATTR         'debugging'
87	LOAD_CONST        2
90	COMPARE_OP        '>'
93	POP_JUMP_IF_FALSE '114'
96	LOAD_CONST        '*retr*'
99	PRINT_ITEM        None
100	LOAD_GLOBAL       'repr'
103	LOAD_FAST         'line'
106	CALL_FUNCTION_1   None
109	PRINT_ITEM_CONT   None
110	PRINT_NEWLINE_CONT None
111	JUMP_FORWARD      '114'
114_0	COME_FROM         '111'

114	LOAD_FAST         'line'
117	POP_JUMP_IF_TRUE  '124'

120	BREAK_LOOP        None
121	JUMP_FORWARD      '124'
124_0	COME_FROM         '121'

124	LOAD_FAST         'line'
127	LOAD_CONST        -2
130	SLICE+1           None
131	LOAD_GLOBAL       'CRLF'
134	COMPARE_OP        '=='
137	POP_JUMP_IF_FALSE '153'

140	LOAD_FAST         'line'
143	LOAD_CONST        -2
146	SLICE+2           None
147	STORE_FAST        'line'
150	JUMP_FORWARD      '182'

153	LOAD_FAST         'line'
156	LOAD_CONST        -1
159	SLICE+1           None
160	LOAD_CONST        '\n'
163	COMPARE_OP        '=='
166	POP_JUMP_IF_FALSE '182'

169	LOAD_FAST         'line'
172	LOAD_CONST        -1
175	SLICE+2           None
176	STORE_FAST        'line'
179	JUMP_FORWARD      '182'
182_0	COME_FROM         '150'
182_1	COME_FROM         '179'

182	LOAD_FAST         'callback'
185	LOAD_FAST         'line'
188	CALL_FUNCTION_1   None
191	POP_TOP           None
192	JUMP_BACK         '69'
195	POP_BLOCK         None
196_0	COME_FROM         '66'

196	LOAD_FAST         'fp'
199	LOAD_ATTR         'close'
202	CALL_FUNCTION_0   None
205	POP_TOP           None

206	LOAD_FAST         'conn'
209	LOAD_ATTR         'close'
212	CALL_FUNCTION_0   None
215	POP_TOP           None

216	LOAD_FAST         'self'
219	LOAD_ATTR         'voidresp'
222	CALL_FUNCTION_0   None
225	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 195

    def storbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	LOAD_FAST         'rest'
25	CALL_FUNCTION_2   None
28	STORE_FAST        'conn'

31	SETUP_LOOP        '95'

34	LOAD_FAST         'fp'
37	LOAD_ATTR         'read'
40	LOAD_FAST         'blocksize'
43	CALL_FUNCTION_1   None
46	STORE_FAST        'buf'

49	LOAD_FAST         'buf'
52	POP_JUMP_IF_TRUE  '59'
55	BREAK_LOOP        None
56	JUMP_FORWARD      '59'
59_0	COME_FROM         '56'

59	LOAD_FAST         'conn'
62	LOAD_ATTR         'sendall'
65	LOAD_FAST         'buf'
68	CALL_FUNCTION_1   None
71	POP_TOP           None

72	LOAD_FAST         'callback'
75	POP_JUMP_IF_FALSE '34'
78	LOAD_FAST         'callback'
81	LOAD_FAST         'buf'
84	CALL_FUNCTION_1   None
87	POP_TOP           None
88	JUMP_BACK         '34'
91	JUMP_BACK         '34'
94	POP_BLOCK         None
95_0	COME_FROM         '31'

95	LOAD_FAST         'conn'
98	LOAD_ATTR         'close'
101	CALL_FUNCTION_0   None
104	POP_TOP           None

105	LOAD_FAST         'self'
108	LOAD_ATTR         'voidresp'
111	CALL_FUNCTION_0   None
114	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 94

    def storlines--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE A'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	CALL_FUNCTION_1   None
25	STORE_FAST        'conn'

28	SETUP_LOOP        '147'

31	LOAD_FAST         'fp'
34	LOAD_ATTR         'readline'
37	CALL_FUNCTION_0   None
40	STORE_FAST        'buf'

43	LOAD_FAST         'buf'
46	POP_JUMP_IF_TRUE  '53'
49	BREAK_LOOP        None
50	JUMP_FORWARD      '53'
53_0	COME_FROM         '50'

53	LOAD_FAST         'buf'
56	LOAD_CONST        -2
59	SLICE+1           None
60	LOAD_GLOBAL       'CRLF'
63	COMPARE_OP        '!='
66	POP_JUMP_IF_FALSE '111'

69	LOAD_FAST         'buf'
72	LOAD_CONST        -1
75	BINARY_SUBSCR     None
76	LOAD_GLOBAL       'CRLF'
79	COMPARE_OP        'in'
82	POP_JUMP_IF_FALSE '98'
85	LOAD_FAST         'buf'
88	LOAD_CONST        -1
91	SLICE+2           None
92	STORE_FAST        'buf'
95	JUMP_FORWARD      '98'
98_0	COME_FROM         '95'

98	LOAD_FAST         'buf'
101	LOAD_GLOBAL       'CRLF'
104	BINARY_ADD        None
105	STORE_FAST        'buf'
108	JUMP_FORWARD      '111'
111_0	COME_FROM         '108'

111	LOAD_FAST         'conn'
114	LOAD_ATTR         'sendall'
117	LOAD_FAST         'buf'
120	CALL_FUNCTION_1   None
123	POP_TOP           None

124	LOAD_FAST         'callback'
127	POP_JUMP_IF_FALSE '31'
130	LOAD_FAST         'callback'
133	LOAD_FAST         'buf'
136	CALL_FUNCTION_1   None
139	POP_TOP           None
140	JUMP_BACK         '31'
143	JUMP_BACK         '31'
146	POP_BLOCK         None
147_0	COME_FROM         '28'

147	LOAD_FAST         'conn'
150	LOAD_ATTR         'close'
153	CALL_FUNCTION_0   None
156	POP_TOP           None

157	LOAD_FAST         'self'
160	LOAD_ATTR         'voidresp'
163	CALL_FUNCTION_0   None
166	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 146

    def acct(self, password):
        """Send new account name."""
        cmd = 'ACCT ' + password
        return self.voidcmd(cmd)

    def nlst(self, *args):
        """Return a list of files in a given directory (default the current)."""
        cmd = 'NLST'
        for arg in args:
            cmd = cmd + (' ' + arg)

        files = []
        self.retrlines(cmd, files.append)
        return files

    def dir(self, *args):
        """List a directory in long form.
        By default list current directory to stdout.
        Optional last argument is callback function; all
        non-empty arguments before it are concatenated to the
        LIST command.  (This *should* only be used for a pathname.)"""
        cmd = 'LIST'
        func = None
        if args[-1:] and type(args[-1]) != type(''):
            args, func = args[:-1], args[-1]
        for arg in args:
            if arg:
                cmd = cmd + (' ' + arg)

        self.retrlines(cmd, func)
        return

    def rename(self, fromname, toname):
        """Rename a file."""
        resp = self.sendcmd('RNFR ' + fromname)
        if resp[0] != '3':
            raise error_reply, resp
        return self.voidcmd('RNTO ' + toname)

    def delete(self, filename):
        """Delete a file."""
        resp = self.sendcmd('DELE ' + filename)
        if resp[:3] in ('250', '200'):
            return resp
        raise error_reply, resp

    def cwd(self, dirname):
        """Change to a directory."""
        if dirname == '..':
            try:
                return self.voidcmd('CDUP')
            except error_perm as msg:
                if msg.args[0][:3] != '500':
                    raise

        elif dirname == '':
            dirname = '.'
        cmd = 'CWD ' + dirname
        return self.voidcmd(cmd)

    def size(self, filename):
        """Retrieve the size of a file."""
        resp = self.sendcmd('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            try:
                return int(s)
            except (OverflowError, ValueError):
                return long(s)

    def mkd(self, dirname):
        """Make a directory, return its full pathname."""
        resp = self.sendcmd('MKD ' + dirname)
        return parse257(resp)

    def rmd(self, dirname):
        """Remove a directory."""
        return self.voidcmd('RMD ' + dirname)

    def pwd(self):
        """Return current working directory."""
        resp = self.sendcmd('PWD')
        return parse257(resp)

    def quit(self):
        """Quit, and close the connection."""
        resp = self.voidcmd('QUIT')
        self.close()
        return resp

    def close(self):
        """Close the connection without assuming anything about it."""
        if self.file is not None:
            self.file.close()
        if self.sock is not None:
            self.sock.close()
        self.file = self.sock = None
        return


try:
    import ssl
except ImportError:
    pass
else:

    class FTP_TLS(FTP):
        """A FTP subclass which adds TLS support to FTP as described
        in RFC-4217.
        
        Connect as usual to port 21 implicitly securing the FTP control
        connection before authenticating.
        
        Securing the data connection requires user to explicitly ask
        for it by calling prot_p() method.
        
        Usage example:
        >>> from ftplib import FTP_TLS
        >>> ftps = FTP_TLS('ftp.python.org')
        >>> ftps.login()  # login anonymously previously securing control channel
        '230 Guest login ok, access restrictions apply.'
        >>> ftps.prot_p()  # switch to secure data connection
        '200 Protection level set to P'
        >>> ftps.retrlines('LIST')  # list directory content securely
        total 9
        drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 .
        drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 ..
        drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 bin
        drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 etc
        d-wxrwxr-x   2 ftp      wheel        1024 Sep  5 13:43 incoming
        drwxr-xr-x   2 root     wheel        1024 Nov 17  1993 lib
        drwxr-xr-x   6 1094     wheel        1024 Sep 13 19:07 pub
        drwxr-xr-x   3 root     wheel        1024 Jan  3  1994 usr
        -rw-r--r--   1 root     root          312 Aug  1  1994 welcome.msg
        '226 Transfer complete.'
        >>> ftps.quit()
        '221 Goodbye.'
        >>>
        """
        ssl_version = ssl.PROTOCOL_TLSv1

        def __init__(self, host = '', user = '', passwd = '', acct = '', keyfile = None, certfile = None, timeout = _GLOBAL_DEFAULT_TIMEOUT):
            self.keyfile = keyfile
            self.certfile = certfile
            self._prot_p = False
            FTP.__init__(self, host, user, passwd, acct, timeout)

        def login(self, user = '', passwd = '', acct = '', secure = True):
            if secure and not isinstance(self.sock, ssl.SSLSocket):
                self.auth()
            return FTP.login(self, user, passwd, acct)

        def auth(self):
            """Set up secure control connection by using TLS/SSL."""
            if isinstance(self.sock, ssl.SSLSocket):
                raise ValueError('Already using TLS')
            if self.ssl_version == ssl.PROTOCOL_TLSv1:
                resp = self.voidcmd('AUTH TLS')
            else:
                resp = self.voidcmd('AUTH SSL')
            self.sock = ssl.wrap_socket(self.sock, self.keyfile, self.certfile, ssl_version=self.ssl_version)
            self.file = self.sock.makefile(mode='rb')
            return resp

        def prot_p(self):
            """Set up secure data connection."""
            self.voidcmd('PBSZ 0')
            resp = self.voidcmd('PROT P')
            self._prot_p = True
            return resp

        def prot_c(self):
            """Set up clear text data connection."""
            resp = self.voidcmd('PROT C')
            self._prot_p = False
            return resp

        def ntransfercmd(self, cmd, rest = None):
            conn, size = FTP.ntransfercmd(self, cmd, rest)
            if self._prot_p:
                conn = ssl.wrap_socket(conn, self.keyfile, self.certfile, ssl_version=self.ssl_version)
            return (conn, size)

        def retrbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	LOAD_FAST         'rest'
25	CALL_FUNCTION_2   None
28	STORE_FAST        'conn'

31	SETUP_FINALLY     '111'

34	SETUP_LOOP        '76'

37	LOAD_FAST         'conn'
40	LOAD_ATTR         'recv'
43	LOAD_FAST         'blocksize'
46	CALL_FUNCTION_1   None
49	STORE_FAST        'data'

52	LOAD_FAST         'data'
55	POP_JUMP_IF_TRUE  '62'

58	BREAK_LOOP        None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'callback'
65	LOAD_FAST         'data'
68	CALL_FUNCTION_1   None
71	POP_TOP           None
72	JUMP_BACK         '37'
75	POP_BLOCK         None
76_0	COME_FROM         '34'

76	LOAD_GLOBAL       'isinstance'
79	LOAD_FAST         'conn'
82	LOAD_GLOBAL       'ssl'
85	LOAD_ATTR         'SSLSocket'
88	CALL_FUNCTION_2   None
91	POP_JUMP_IF_FALSE '107'

94	LOAD_FAST         'conn'
97	LOAD_ATTR         'unwrap'
100	CALL_FUNCTION_0   None
103	POP_TOP           None
104	JUMP_FORWARD      '107'
107_0	COME_FROM         '104'
107	POP_BLOCK         None
108	LOAD_CONST        None
111_0	COME_FROM         '31'

111	LOAD_FAST         'conn'
114	LOAD_ATTR         'close'
117	CALL_FUNCTION_0   None
120	POP_TOP           None
121	END_FINALLY       None

122	LOAD_FAST         'self'
125	LOAD_ATTR         'voidresp'
128	CALL_FUNCTION_0   None
131	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 75

        def retrlines--- This code section failed: ---

0	LOAD_FAST         'callback'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	POP_JUMP_IF_FALSE '21'
12	LOAD_GLOBAL       'print_line'
15	STORE_FAST        'callback'
18	JUMP_FORWARD      '21'
21_0	COME_FROM         '18'

21	LOAD_FAST         'self'
24	LOAD_ATTR         'sendcmd'
27	LOAD_CONST        'TYPE A'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'resp'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'transfercmd'
42	LOAD_FAST         'cmd'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'conn'

51	LOAD_FAST         'conn'
54	LOAD_ATTR         'makefile'
57	LOAD_CONST        'rb'
60	CALL_FUNCTION_1   None
63	STORE_FAST        'fp'

66	SETUP_FINALLY     '234'

69	SETUP_LOOP        '199'

72	LOAD_FAST         'fp'
75	LOAD_ATTR         'readline'
78	CALL_FUNCTION_0   None
81	STORE_FAST        'line'

84	LOAD_FAST         'self'
87	LOAD_ATTR         'debugging'
90	LOAD_CONST        2
93	COMPARE_OP        '>'
96	POP_JUMP_IF_FALSE '117'
99	LOAD_CONST        '*retr*'
102	PRINT_ITEM        None
103	LOAD_GLOBAL       'repr'
106	LOAD_FAST         'line'
109	CALL_FUNCTION_1   None
112	PRINT_ITEM_CONT   None
113	PRINT_NEWLINE_CONT None
114	JUMP_FORWARD      '117'
117_0	COME_FROM         '114'

117	LOAD_FAST         'line'
120	POP_JUMP_IF_TRUE  '127'

123	BREAK_LOOP        None
124	JUMP_FORWARD      '127'
127_0	COME_FROM         '124'

127	LOAD_FAST         'line'
130	LOAD_CONST        -2
133	SLICE+1           None
134	LOAD_GLOBAL       'CRLF'
137	COMPARE_OP        '=='
140	POP_JUMP_IF_FALSE '156'

143	LOAD_FAST         'line'
146	LOAD_CONST        -2
149	SLICE+2           None
150	STORE_FAST        'line'
153	JUMP_FORWARD      '185'

156	LOAD_FAST         'line'
159	LOAD_CONST        -1
162	SLICE+1           None
163	LOAD_CONST        '\n'
166	COMPARE_OP        '=='
169	POP_JUMP_IF_FALSE '185'

172	LOAD_FAST         'line'
175	LOAD_CONST        -1
178	SLICE+2           None
179	STORE_FAST        'line'
182	JUMP_FORWARD      '185'
185_0	COME_FROM         '153'
185_1	COME_FROM         '182'

185	LOAD_FAST         'callback'
188	LOAD_FAST         'line'
191	CALL_FUNCTION_1   None
194	POP_TOP           None
195	JUMP_BACK         '72'
198	POP_BLOCK         None
199_0	COME_FROM         '69'

199	LOAD_GLOBAL       'isinstance'
202	LOAD_FAST         'conn'
205	LOAD_GLOBAL       'ssl'
208	LOAD_ATTR         'SSLSocket'
211	CALL_FUNCTION_2   None
214	POP_JUMP_IF_FALSE '230'

217	LOAD_FAST         'conn'
220	LOAD_ATTR         'unwrap'
223	CALL_FUNCTION_0   None
226	POP_TOP           None
227	JUMP_FORWARD      '230'
230_0	COME_FROM         '227'
230	POP_BLOCK         None
231	LOAD_CONST        None
234_0	COME_FROM         '66'

234	LOAD_FAST         'fp'
237	LOAD_ATTR         'close'
240	CALL_FUNCTION_0   None
243	POP_TOP           None

244	LOAD_FAST         'conn'
247	LOAD_ATTR         'close'
250	CALL_FUNCTION_0   None
253	POP_TOP           None
254	END_FINALLY       None

255	LOAD_FAST         'self'
258	LOAD_ATTR         'voidresp'
261	CALL_FUNCTION_0   None
264	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 198

        def storbinary--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE I'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	LOAD_FAST         'rest'
25	CALL_FUNCTION_2   None
28	STORE_FAST        'conn'

31	SETUP_FINALLY     '133'

34	SETUP_LOOP        '98'

37	LOAD_FAST         'fp'
40	LOAD_ATTR         'read'
43	LOAD_FAST         'blocksize'
46	CALL_FUNCTION_1   None
49	STORE_FAST        'buf'

52	LOAD_FAST         'buf'
55	POP_JUMP_IF_TRUE  '62'
58	BREAK_LOOP        None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'conn'
65	LOAD_ATTR         'sendall'
68	LOAD_FAST         'buf'
71	CALL_FUNCTION_1   None
74	POP_TOP           None

75	LOAD_FAST         'callback'
78	POP_JUMP_IF_FALSE '37'
81	LOAD_FAST         'callback'
84	LOAD_FAST         'buf'
87	CALL_FUNCTION_1   None
90	POP_TOP           None
91	JUMP_BACK         '37'
94	JUMP_BACK         '37'
97	POP_BLOCK         None
98_0	COME_FROM         '34'

98	LOAD_GLOBAL       'isinstance'
101	LOAD_FAST         'conn'
104	LOAD_GLOBAL       'ssl'
107	LOAD_ATTR         'SSLSocket'
110	CALL_FUNCTION_2   None
113	POP_JUMP_IF_FALSE '129'

116	LOAD_FAST         'conn'
119	LOAD_ATTR         'unwrap'
122	CALL_FUNCTION_0   None
125	POP_TOP           None
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'
129	POP_BLOCK         None
130	LOAD_CONST        None
133_0	COME_FROM         '31'

133	LOAD_FAST         'conn'
136	LOAD_ATTR         'close'
139	CALL_FUNCTION_0   None
142	POP_TOP           None
143	END_FINALLY       None

144	LOAD_FAST         'self'
147	LOAD_ATTR         'voidresp'
150	CALL_FUNCTION_0   None
153	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 97

        def storlines--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'voidcmd'
6	LOAD_CONST        'TYPE A'
9	CALL_FUNCTION_1   None
12	POP_TOP           None

13	LOAD_FAST         'self'
16	LOAD_ATTR         'transfercmd'
19	LOAD_FAST         'cmd'
22	CALL_FUNCTION_1   None
25	STORE_FAST        'conn'

28	SETUP_FINALLY     '185'

31	SETUP_LOOP        '150'

34	LOAD_FAST         'fp'
37	LOAD_ATTR         'readline'
40	CALL_FUNCTION_0   None
43	STORE_FAST        'buf'

46	LOAD_FAST         'buf'
49	POP_JUMP_IF_TRUE  '56'
52	BREAK_LOOP        None
53	JUMP_FORWARD      '56'
56_0	COME_FROM         '53'

56	LOAD_FAST         'buf'
59	LOAD_CONST        -2
62	SLICE+1           None
63	LOAD_GLOBAL       'CRLF'
66	COMPARE_OP        '!='
69	POP_JUMP_IF_FALSE '114'

72	LOAD_FAST         'buf'
75	LOAD_CONST        -1
78	BINARY_SUBSCR     None
79	LOAD_GLOBAL       'CRLF'
82	COMPARE_OP        'in'
85	POP_JUMP_IF_FALSE '101'
88	LOAD_FAST         'buf'
91	LOAD_CONST        -1
94	SLICE+2           None
95	STORE_FAST        'buf'
98	JUMP_FORWARD      '101'
101_0	COME_FROM         '98'

101	LOAD_FAST         'buf'
104	LOAD_GLOBAL       'CRLF'
107	BINARY_ADD        None
108	STORE_FAST        'buf'
111	JUMP_FORWARD      '114'
114_0	COME_FROM         '111'

114	LOAD_FAST         'conn'
117	LOAD_ATTR         'sendall'
120	LOAD_FAST         'buf'
123	CALL_FUNCTION_1   None
126	POP_TOP           None

127	LOAD_FAST         'callback'
130	POP_JUMP_IF_FALSE '34'
133	LOAD_FAST         'callback'
136	LOAD_FAST         'buf'
139	CALL_FUNCTION_1   None
142	POP_TOP           None
143	JUMP_BACK         '34'
146	JUMP_BACK         '34'
149	POP_BLOCK         None
150_0	COME_FROM         '31'

150	LOAD_GLOBAL       'isinstance'
153	LOAD_FAST         'conn'
156	LOAD_GLOBAL       'ssl'
159	LOAD_ATTR         'SSLSocket'
162	CALL_FUNCTION_2   None
165	POP_JUMP_IF_FALSE '181'

168	LOAD_FAST         'conn'
171	LOAD_ATTR         'unwrap'
174	CALL_FUNCTION_0   None
177	POP_TOP           None
178	JUMP_FORWARD      '181'
181_0	COME_FROM         '178'
181	POP_BLOCK         None
182	LOAD_CONST        None
185_0	COME_FROM         '28'

185	LOAD_FAST         'conn'
188	LOAD_ATTR         'close'
191	CALL_FUNCTION_0   None
194	POP_TOP           None
195	END_FINALLY       None

196	LOAD_FAST         'self'
199	LOAD_ATTR         'voidresp'
202	CALL_FUNCTION_0   None
205	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 149


    __all__.append('FTP_TLS')
    all_errors = (Error,
     IOError,
     EOFError,
     ssl.SSLError)

_150_re = None

def parse150(resp):
    """Parse the '150' response for a RETR request.
    Returns the expected transfer size or None; size is not guaranteed to
    be present in the 150 message.
    """
    global _150_re
    if resp[:3] != '150':
        raise error_reply, resp
    if _150_re is None:
        import re
        _150_re = re.compile('150 .* \\((\\d+) bytes\\)', re.IGNORECASE)
    m = _150_re.match(resp)
    if not m:
        return
    else:
        s = m.group(1)
        try:
            return int(s)
        except (OverflowError, ValueError):
            return long(s)

        return


_227_re = None

def parse227(resp):
    """Parse the '227' response for a PASV request.
    Raises error_proto if it does not contain '(h1,h2,h3,h4,p1,p2)'
    Return ('host.addr.as.numbers', port#) tuple."""
    global _227_re
    if resp[:3] != '227':
        raise error_reply, resp
    if _227_re is None:
        import re
        _227_re = re.compile('(\\d+),(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)')
    m = _227_re.search(resp)
    if not m:
        raise error_proto, resp
    numbers = m.groups()
    host = '.'.join(numbers[:4])
    port = (int(numbers[4]) << 8) + int(numbers[5])
    return (host, port)


def parse229(resp, peer):
    """Parse the '229' response for a EPSV request.
    Raises error_proto if it does not contain '(|||port|)'
    Return ('host.addr.as.numbers', port#) tuple."""
    if resp[:3] != '229':
        raise error_reply, resp
    left = resp.find('(')
    if left < 0:
        raise error_proto, resp
    right = resp.find(')', left + 1)
    if right < 0:
        raise error_proto, resp
    if resp[left + 1] != resp[right - 1]:
        raise error_proto, resp
    parts = resp[left + 1:right].split(resp[left + 1])
    if len(parts) != 5:
        raise error_proto, resp
    host = peer[0]
    port = int(parts[3])
    return (host, port)


def parse257(resp):
    """Parse the '257' response for a MKD or PWD request.
    This is a response to a MKD or PWD request: a directory name.
    Returns the directoryname in the 257 reply."""
    if resp[:3] != '257':
        raise error_reply, resp
    if resp[3:5] != ' "':
        return ''
    dirname = ''
    i = 5
    n = len(resp)
    while i < n:
        c = resp[i]
        i = i + 1
        if c == '"':
            if i >= n or resp[i] != '"':
                break
            i = i + 1
        dirname = dirname + c

    return dirname


def print_line(line):
    """Default retrlines callback to print a line."""
    print line


def ftpcp(source, sourcename, target, targetname = '', type = 'I'):
    """Copy file from one FTP-instance to another."""
    if not targetname:
        targetname = sourcename
    type = 'TYPE ' + type
    source.voidcmd(type)
    target.voidcmd(type)
    sourcehost, sourceport = parse227(source.sendcmd('PASV'))
    target.sendport(sourcehost, sourceport)
    treply = target.sendcmd('STOR ' + targetname)
    if treply[:3] not in ('125', '150'):
        raise error_proto
    sreply = source.sendcmd('RETR ' + sourcename)
    if sreply[:3] not in ('125', '150'):
        raise error_proto
    source.voidresp()
    target.voidresp()


class Netrc():
    """Class to parse & provide access to 'netrc' format files.
    
    See the netrc(4) man page for information on the file format.
    
    WARNING: This class is obsolete -- use module netrc instead.
    
    """
    __defuser = None
    __defpasswd = None
    __defacct = None

    def __init__--- This code section failed: ---

0	LOAD_FAST         'filename'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	POP_JUMP_IF_FALSE '70'

12	LOAD_CONST        'HOME'
15	LOAD_GLOBAL       'os'
18	LOAD_ATTR         'environ'
21	COMPARE_OP        'in'
24	POP_JUMP_IF_FALSE '58'

27	LOAD_GLOBAL       'os'
30	LOAD_ATTR         'path'
33	LOAD_ATTR         'join'
36	LOAD_GLOBAL       'os'
39	LOAD_ATTR         'environ'
42	LOAD_CONST        'HOME'
45	BINARY_SUBSCR     None

46	LOAD_CONST        '.netrc'
49	CALL_FUNCTION_2   None
52	STORE_FAST        'filename'
55	JUMP_ABSOLUTE     '70'

58	LOAD_GLOBAL       'IOError'

61	LOAD_CONST        'specify file to load or set $HOME'
64	RAISE_VARARGS_2   None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	BUILD_MAP         None
73	LOAD_FAST         'self'
76	STORE_ATTR        '__hosts'

79	BUILD_MAP         None
82	LOAD_FAST         'self'
85	STORE_ATTR        '__macros'

88	LOAD_GLOBAL       'open'
91	LOAD_FAST         'filename'
94	LOAD_CONST        'r'
97	CALL_FUNCTION_2   None
100	STORE_FAST        'fp'

103	LOAD_CONST        0
106	STORE_FAST        'in_macro'

109	SETUP_LOOP        '726'

112	LOAD_FAST         'fp'
115	LOAD_ATTR         'readline'
118	CALL_FUNCTION_0   None
121	STORE_FAST        'line'

124	LOAD_FAST         'line'
127	POP_JUMP_IF_TRUE  '134'
130	BREAK_LOOP        None
131	JUMP_FORWARD      '134'
134_0	COME_FROM         '131'

134	LOAD_FAST         'in_macro'
137	POP_JUMP_IF_FALSE '171'
140	LOAD_FAST         'line'
143	LOAD_ATTR         'strip'
146	CALL_FUNCTION_0   None
149_0	COME_FROM         '137'
149	POP_JUMP_IF_FALSE '171'

152	LOAD_FAST         'macro_lines'
155	LOAD_ATTR         'append'
158	LOAD_FAST         'line'
161	CALL_FUNCTION_1   None
164	POP_TOP           None

165	CONTINUE          '112'
168	JUMP_FORWARD      '205'

171	LOAD_FAST         'in_macro'
174	POP_JUMP_IF_FALSE '205'

177	LOAD_GLOBAL       'tuple'
180	LOAD_FAST         'macro_lines'
183	CALL_FUNCTION_1   None
186	LOAD_FAST         'self'
189	LOAD_ATTR         '__macros'
192	LOAD_FAST         'macro_name'
195	STORE_SUBSCR      None

196	LOAD_CONST        0
199	STORE_FAST        'in_macro'
202	JUMP_FORWARD      '205'
205_0	COME_FROM         '168'
205_1	COME_FROM         '202'

205	LOAD_FAST         'line'
208	LOAD_ATTR         'split'
211	CALL_FUNCTION_0   None
214	STORE_FAST        'words'

217	LOAD_CONST        None
220	DUP_TOP           None
221	STORE_FAST        'host'
224	DUP_TOP           None
225	STORE_FAST        'user'
228	DUP_TOP           None
229	STORE_FAST        'passwd'
232	STORE_FAST        'acct'

235	LOAD_CONST        0
238	STORE_FAST        'default'

241	LOAD_CONST        0
244	STORE_FAST        'i'

247	SETUP_LOOP        '552'
250	LOAD_FAST         'i'
253	LOAD_GLOBAL       'len'
256	LOAD_FAST         'words'
259	CALL_FUNCTION_1   None
262	COMPARE_OP        '<'
265	POP_JUMP_IF_FALSE '551'

268	LOAD_FAST         'words'
271	LOAD_FAST         'i'
274	BINARY_SUBSCR     None
275	STORE_FAST        'w1'

278	LOAD_FAST         'i'
281	LOAD_CONST        1
284	BINARY_ADD        None
285	LOAD_GLOBAL       'len'
288	LOAD_FAST         'words'
291	CALL_FUNCTION_1   None
294	COMPARE_OP        '<'
297	POP_JUMP_IF_FALSE '317'

300	LOAD_FAST         'words'
303	LOAD_FAST         'i'
306	LOAD_CONST        1
309	BINARY_ADD        None
310	BINARY_SUBSCR     None
311	STORE_FAST        'w2'
314	JUMP_FORWARD      '323'

317	LOAD_CONST        None
320	STORE_FAST        'w2'
323_0	COME_FROM         '314'

323	LOAD_FAST         'w1'
326	LOAD_CONST        'default'
329	COMPARE_OP        '=='
332	POP_JUMP_IF_FALSE '344'

335	LOAD_CONST        1
338	STORE_FAST        'default'
341	JUMP_FORWARD      '538'

344	LOAD_FAST         'w1'
347	LOAD_CONST        'machine'
350	COMPARE_OP        '=='
353	POP_JUMP_IF_FALSE '387'
356	LOAD_FAST         'w2'
359_0	COME_FROM         '353'
359	POP_JUMP_IF_FALSE '387'

362	LOAD_FAST         'w2'
365	LOAD_ATTR         'lower'
368	CALL_FUNCTION_0   None
371	STORE_FAST        'host'

374	LOAD_FAST         'i'
377	LOAD_CONST        1
380	BINARY_ADD        None
381	STORE_FAST        'i'
384	JUMP_FORWARD      '538'

387	LOAD_FAST         'w1'
390	LOAD_CONST        'login'
393	COMPARE_OP        '=='
396	POP_JUMP_IF_FALSE '424'
399	LOAD_FAST         'w2'
402_0	COME_FROM         '396'
402	POP_JUMP_IF_FALSE '424'

405	LOAD_FAST         'w2'
408	STORE_FAST        'user'

411	LOAD_FAST         'i'
414	LOAD_CONST        1
417	BINARY_ADD        None
418	STORE_FAST        'i'
421	JUMP_FORWARD      '538'

424	LOAD_FAST         'w1'
427	LOAD_CONST        'password'
430	COMPARE_OP        '=='
433	POP_JUMP_IF_FALSE '461'
436	LOAD_FAST         'w2'
439_0	COME_FROM         '433'
439	POP_JUMP_IF_FALSE '461'

442	LOAD_FAST         'w2'
445	STORE_FAST        'passwd'

448	LOAD_FAST         'i'
451	LOAD_CONST        1
454	BINARY_ADD        None
455	STORE_FAST        'i'
458	JUMP_FORWARD      '538'

461	LOAD_FAST         'w1'
464	LOAD_CONST        'account'
467	COMPARE_OP        '=='
470	POP_JUMP_IF_FALSE '498'
473	LOAD_FAST         'w2'
476_0	COME_FROM         '470'
476	POP_JUMP_IF_FALSE '498'

479	LOAD_FAST         'w2'
482	STORE_FAST        'acct'

485	LOAD_FAST         'i'
488	LOAD_CONST        1
491	BINARY_ADD        None
492	STORE_FAST        'i'
495	JUMP_FORWARD      '538'

498	LOAD_FAST         'w1'
501	LOAD_CONST        'macdef'
504	COMPARE_OP        '=='
507	POP_JUMP_IF_FALSE '538'
510	LOAD_FAST         'w2'
513_0	COME_FROM         '507'
513	POP_JUMP_IF_FALSE '538'

516	LOAD_FAST         'w2'
519	STORE_FAST        'macro_name'

522	BUILD_LIST_0      None
525	STORE_FAST        'macro_lines'

528	LOAD_CONST        1
531	STORE_FAST        'in_macro'

534	BREAK_LOOP        None
535	JUMP_FORWARD      '538'
538_0	COME_FROM         '341'
538_1	COME_FROM         '384'
538_2	COME_FROM         '421'
538_3	COME_FROM         '458'
538_4	COME_FROM         '495'
538_5	COME_FROM         '535'

538	LOAD_FAST         'i'
541	LOAD_CONST        1
544	BINARY_ADD        None
545	STORE_FAST        'i'
548	JUMP_BACK         '250'
551	POP_BLOCK         None
552_0	COME_FROM         '247'

552	LOAD_FAST         'default'
555	POP_JUMP_IF_FALSE '615'

558	LOAD_FAST         'user'
561	JUMP_IF_TRUE_OR_POP '570'
564	LOAD_FAST         'self'
567	LOAD_ATTR         '__defuser'
570_0	COME_FROM         '561'
570	LOAD_FAST         'self'
573	STORE_ATTR        '__defuser'

576	LOAD_FAST         'passwd'
579	JUMP_IF_TRUE_OR_POP '588'
582	LOAD_FAST         'self'
585	LOAD_ATTR         '__defpasswd'
588_0	COME_FROM         '579'
588	LOAD_FAST         'self'
591	STORE_ATTR        '__defpasswd'

594	LOAD_FAST         'acct'
597	JUMP_IF_TRUE_OR_POP '606'
600	LOAD_FAST         'self'
603	LOAD_ATTR         '__defacct'
606_0	COME_FROM         '597'
606	LOAD_FAST         'self'
609	STORE_ATTR        '__defacct'
612	JUMP_FORWARD      '615'
615_0	COME_FROM         '612'

615	LOAD_FAST         'host'
618	POP_JUMP_IF_FALSE '112'

621	LOAD_FAST         'host'
624	LOAD_FAST         'self'
627	LOAD_ATTR         '__hosts'
630	COMPARE_OP        'in'
633	POP_JUMP_IF_FALSE '697'

636	LOAD_FAST         'self'
639	LOAD_ATTR         '__hosts'
642	LOAD_FAST         'host'
645	BINARY_SUBSCR     None
646	UNPACK_SEQUENCE_3 None
649	STORE_FAST        'ouser'
652	STORE_FAST        'opasswd'
655	STORE_FAST        'oacct'

658	LOAD_FAST         'user'
661	JUMP_IF_TRUE_OR_POP '667'
664	LOAD_FAST         'ouser'
667_0	COME_FROM         '661'
667	STORE_FAST        'user'

670	LOAD_FAST         'passwd'
673	JUMP_IF_TRUE_OR_POP '679'
676	LOAD_FAST         'opasswd'
679_0	COME_FROM         '673'
679	STORE_FAST        'passwd'

682	LOAD_FAST         'acct'
685	JUMP_IF_TRUE_OR_POP '691'
688	LOAD_FAST         'oacct'
691_0	COME_FROM         '685'
691	STORE_FAST        'acct'
694	JUMP_FORWARD      '697'
697_0	COME_FROM         '694'

697	LOAD_FAST         'user'
700	LOAD_FAST         'passwd'
703	LOAD_FAST         'acct'
706	BUILD_TUPLE_3     None
709	LOAD_FAST         'self'
712	LOAD_ATTR         '__hosts'
715	LOAD_FAST         'host'
718	STORE_SUBSCR      None
719	JUMP_BACK         '112'
722	JUMP_BACK         '112'
725	POP_BLOCK         None
726_0	COME_FROM         '109'

726	LOAD_FAST         'fp'
729	LOAD_ATTR         'close'
732	CALL_FUNCTION_0   None
735	POP_TOP           None
736	LOAD_CONST        None
739	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 725

    def get_hosts(self):
        """Return a list of hosts mentioned in the .netrc file."""
        return self.__hosts.keys()

    def get_account(self, host):
        """Returns login information for the named host.
        
        The return value is a triple containing userid,
        password, and the accounting field.
        
        """
        host = host.lower()
        user = passwd = acct = None
        if host in self.__hosts:
            user, passwd, acct = self.__hosts[host]
        user = user or self.__defuser
        passwd = passwd or self.__defpasswd
        acct = acct or self.__defacct
        return (user, passwd, acct)

    def get_macros(self):
        """Return a list of all defined macro names."""
        return self.__macros.keys()

    def get_macro(self, macro):
        """Return a sequence of lines which define a named macro."""
        return self.__macros[macro]


def test():
    """Test program.
    Usage: ftp [-d] [-r[file]] host [-l[dir]] [-d[dir]] [-p] [file] ...
    
    -d dir
    -l list
    -p password
    """
    if len(sys.argv) < 2:
        print test.__doc__
        sys.exit(0)
    debugging = 0
    rcfile = None
    while sys.argv[1] == '-d':
        debugging = debugging + 1
        del sys.argv[1]

    if sys.argv[1][:2] == '-r':
        rcfile = sys.argv[1][2:]
        del sys.argv[1]
    host = sys.argv[1]
    ftp = FTP(host)
    ftp.set_debuglevel(debugging)
    userid = passwd = acct = ''
    try:
        netrc = Netrc(rcfile)
    except IOError:
        if rcfile is not None:
            sys.stderr.write('Could not open account file -- using anonymous login.')
    else:
        try:
            userid, passwd, acct = netrc.get_account(host)
        except KeyError:
            sys.stderr.write('No account -- using anonymous login.')

    ftp.login(userid, passwd, acct)
    for file in sys.argv[2:]:
        if file[:2] == '-l':
            ftp.dir(file[2:])
        elif file[:2] == '-d':
            cmd = 'CWD'
            if file[2:]:
                cmd = cmd + ' ' + file[2:]
            resp = ftp.sendcmd(cmd)
        elif file == '-p':
            ftp.set_pasv(not ftp.passiveserver)
        else:
            ftp.retrbinary('RETR ' + file, sys.stdout.write, 1024)

    ftp.quit()
    return


if __name__ == '__main__':
    test()