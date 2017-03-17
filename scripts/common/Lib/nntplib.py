# Embedded file name: scripts/common/Lib/nntplib.py
"""An NNTP client class based on RFC 977: Network News Transfer Protocol.

Example:

>>> from nntplib import NNTP
>>> s = NNTP('news')
>>> resp, count, first, last, name = s.group('comp.lang.python')
>>> print 'Group', name, 'has', count, 'articles, range', first, 'to', last
Group comp.lang.python has 51 articles, range 5770 to 5821
>>> resp, subs = s.xhdr('subject', first + '-' + last)
>>> resp = s.quit()
>>>

Here 'resp' is the server response line.
Error responses are turned into exceptions.

To post an article from a file:
>>> f = open(filename, 'r') # file containing article, including header
>>> resp = s.post(f)
>>>

For descriptions of all methods, read the comments in the code below.
Note that all arguments and return values representing article numbers
are strings, not numbers, since they are rarely used for calculations.
"""
import re
import socket
__all__ = ['NNTP',
 'NNTPReplyError',
 'NNTPTemporaryError',
 'NNTPPermanentError',
 'NNTPProtocolError',
 'NNTPDataError',
 'error_reply',
 'error_temp',
 'error_perm',
 'error_proto',
 'error_data']

class NNTPError(Exception):
    """Base class for all nntplib exceptions"""

    def __init__(self, *args):
        Exception.__init__(self, *args)
        try:
            self.response = args[0]
        except IndexError:
            self.response = 'No response given'


class NNTPReplyError(NNTPError):
    """Unexpected [123]xx reply"""
    pass


class NNTPTemporaryError(NNTPError):
    """4xx errors"""
    pass


class NNTPPermanentError(NNTPError):
    """5xx errors"""
    pass


class NNTPProtocolError(NNTPError):
    """Response does not begin with [1-5]"""
    pass


class NNTPDataError(NNTPError):
    """Error in response data"""
    pass


error_reply = NNTPReplyError
error_temp = NNTPTemporaryError
error_perm = NNTPPermanentError
error_proto = NNTPProtocolError
error_data = NNTPDataError
NNTP_PORT = 119
LONGRESP = ['100',
 '215',
 '220',
 '221',
 '222',
 '224',
 '230',
 '231',
 '282']
CRLF = '\r\n'

class NNTP():

    def __init__(self, host, port = NNTP_PORT, user = None, password = None, readermode = None, usenetrc = True):
        """Initialize an instance.  Arguments:
        - host: hostname to connect to
        - port: port to connect to (default the standard NNTP port)
        - user: username to authenticate with
        - password: password to use with username
        - readermode: if true, send 'mode reader' command after
                      connecting.
        
        readermode is sometimes necessary if you are connecting to an
        NNTP server on the local machine and intend to call
        reader-specific commands, such as `group'.  If you get
        unexpected NNTPPermanentErrors, you might need to set
        readermode.
        """
        self.host = host
        self.port = port
        self.sock = socket.create_connection((host, port))
        self.file = self.sock.makefile('rb')
        self.debugging = 0
        self.welcome = self.getresp()
        readermode_afterauth = 0
        if readermode:
            try:
                self.welcome = self.shortcmd('mode reader')
            except NNTPPermanentError:
                pass
            except NNTPTemporaryError as e:
                if user and e.response[:3] == '480':
                    readermode_afterauth = 1
                else:
                    raise

        try:
            if usenetrc and not user:
                import netrc
                credentials = netrc.netrc()
                auth = credentials.authenticators(host)
                if auth:
                    user = auth[0]
                    password = auth[2]
        except IOError:
            pass

        if user:
            resp = self.shortcmd('authinfo user ' + user)
            if resp[:3] == '381':
                if not password:
                    raise NNTPReplyError(resp)
                else:
                    resp = self.shortcmd('authinfo pass ' + password)
                    if resp[:3] != '281':
                        raise NNTPPermanentError(resp)
            if readermode_afterauth:
                try:
                    self.welcome = self.shortcmd('mode reader')
                except NNTPPermanentError:
                    pass

    def getwelcome(self):
        """Get the welcome message from the server
        (this is read and squirreled away by __init__()).
        If the response code is 200, posting is allowed;
        if it 201, posting is not allowed."""
        if self.debugging:
            print '*welcome*', repr(self.welcome)
        return self.welcome

    def set_debuglevel(self, level):
        """Set the debugging level.  Argument 'level' means:
        0: no debugging output (default)
        1: print commands and responses but not body text etc.
        2: also print raw lines read and sent before stripping CR/LF"""
        self.debugging = level

    debug = set_debuglevel

    def putline(self, line):
        """Internal: send one line to the server, appending CRLF."""
        line = line + CRLF
        if self.debugging > 1:
            print '*put*', repr(line)
        self.sock.sendall(line)

    def putcmd(self, line):
        """Internal: send one command to the server (through putline())."""
        if self.debugging:
            print '*cmd*', repr(line)
        self.putline(line)

    def getline(self):
        """Internal: return one line from the server, stripping CRLF.
        Raise EOFError if the connection is closed."""
        line = self.file.readline()
        if self.debugging > 1:
            print '*get*', repr(line)
        if not line:
            raise EOFError
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        return line

    def getresp(self):
        """Internal: get a response from the server.
        Raise various errors if the response indicates an error."""
        resp = self.getline()
        if self.debugging:
            print '*resp*', repr(resp)
        c = resp[:1]
        if c == '4':
            raise NNTPTemporaryError(resp)
        if c == '5':
            raise NNTPPermanentError(resp)
        if c not in '123':
            raise NNTPProtocolError(resp)
        return resp

    def getlongresp--- This code section failed: ---

0	LOAD_CONST        None
3	STORE_FAST        'openedFile'

6	SETUP_FINALLY     '202'

9	LOAD_GLOBAL       'isinstance'
12	LOAD_FAST         'file'
15	LOAD_GLOBAL       'str'
18	CALL_FUNCTION_2   None
21	POP_JUMP_IF_FALSE '46'

24	LOAD_GLOBAL       'open'
27	LOAD_FAST         'file'
30	LOAD_CONST        'w'
33	CALL_FUNCTION_2   None
36	DUP_TOP           None
37	STORE_FAST        'openedFile'
40	STORE_FAST        'file'
43	JUMP_FORWARD      '46'
46_0	COME_FROM         '43'

46	LOAD_FAST         'self'
49	LOAD_ATTR         'getresp'
52	CALL_FUNCTION_0   None
55	STORE_FAST        'resp'

58	LOAD_FAST         'resp'
61	LOAD_CONST        3
64	SLICE+2           None
65	LOAD_GLOBAL       'LONGRESP'
68	COMPARE_OP        'not in'
71	POP_JUMP_IF_FALSE '89'

74	LOAD_GLOBAL       'NNTPReplyError'
77	LOAD_FAST         'resp'
80	CALL_FUNCTION_1   None
83	RAISE_VARARGS_1   None
86	JUMP_FORWARD      '89'
89_0	COME_FROM         '86'

89	BUILD_LIST_0      None
92	STORE_FAST        'list'

95	SETUP_LOOP        '198'

98	LOAD_FAST         'self'
101	LOAD_ATTR         'getline'
104	CALL_FUNCTION_0   None
107	STORE_FAST        'line'

110	LOAD_FAST         'line'
113	LOAD_CONST        '.'
116	COMPARE_OP        '=='
119	POP_JUMP_IF_FALSE '126'

122	BREAK_LOOP        None
123	JUMP_FORWARD      '126'
126_0	COME_FROM         '123'

126	LOAD_FAST         'line'
129	LOAD_CONST        2
132	SLICE+2           None
133	LOAD_CONST        '..'
136	COMPARE_OP        '=='
139	POP_JUMP_IF_FALSE '155'

142	LOAD_FAST         'line'
145	LOAD_CONST        1
148	SLICE+1           None
149	STORE_FAST        'line'
152	JUMP_FORWARD      '155'
155_0	COME_FROM         '152'

155	LOAD_FAST         'file'
158	POP_JUMP_IF_FALSE '181'

161	LOAD_FAST         'file'
164	LOAD_ATTR         'write'
167	LOAD_FAST         'line'
170	LOAD_CONST        '\n'
173	BINARY_ADD        None
174	CALL_FUNCTION_1   None
177	POP_TOP           None
178	JUMP_BACK         '98'

181	LOAD_FAST         'list'
184	LOAD_ATTR         'append'
187	LOAD_FAST         'line'
190	CALL_FUNCTION_1   None
193	POP_TOP           None
194	JUMP_BACK         '98'
197	POP_BLOCK         None
198_0	COME_FROM         '95'
198	POP_BLOCK         None
199	LOAD_CONST        None
202_0	COME_FROM         '6'

202	LOAD_FAST         'openedFile'
205	POP_JUMP_IF_FALSE '221'

208	LOAD_FAST         'openedFile'
211	LOAD_ATTR         'close'
214	CALL_FUNCTION_0   None
217	POP_TOP           None
218	JUMP_FORWARD      '221'
221_0	COME_FROM         '218'
221	END_FINALLY       None

222	LOAD_FAST         'resp'
225	LOAD_FAST         'list'
228	BUILD_TUPLE_2     None
231	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 197

    def shortcmd(self, line):
        """Internal: send a command and get the response."""
        self.putcmd(line)
        return self.getresp()

    def longcmd(self, line, file = None):
        """Internal: send a command and get the response plus following text."""
        self.putcmd(line)
        return self.getlongresp(file)

    def newgroups(self, date, time, file = None):
        """Process a NEWGROUPS command.  Arguments:
        - date: string 'yymmdd' indicating the date
        - time: string 'hhmmss' indicating the time
        Return:
        - resp: server response if successful
        - list: list of newsgroup names"""
        return self.longcmd('NEWGROUPS ' + date + ' ' + time, file)

    def newnews(self, group, date, time, file = None):
        """Process a NEWNEWS command.  Arguments:
        - group: group name or '*'
        - date: string 'yymmdd' indicating the date
        - time: string 'hhmmss' indicating the time
        Return:
        - resp: server response if successful
        - list: list of message ids"""
        cmd = 'NEWNEWS ' + group + ' ' + date + ' ' + time
        return self.longcmd(cmd, file)

    def list(self, file = None):
        """Process a LIST command.  Return:
        - resp: server response if successful
        - list: list of (group, last, first, flag) (strings)"""
        resp, list = self.longcmd('LIST', file)
        for i in range(len(list)):
            list[i] = tuple(list[i].split())

        return (resp, list)

    def description(self, group):
        """Get a description for a single group.  If more than one
        group matches ('group' is a pattern), return the first.  If no
        group matches, return an empty string.
        
        This elides the response code from the server, since it can
        only be '215' or '285' (for xgtitle) anyway.  If the response
        code is needed, use the 'descriptions' method.
        
        NOTE: This neither checks for a wildcard in 'group' nor does
        it check whether the group actually exists."""
        resp, lines = self.descriptions(group)
        if len(lines) == 0:
            return ''
        else:
            return lines[0][1]

    def descriptions(self, group_pattern):
        """Get descriptions for a range of groups."""
        line_pat = re.compile('^(?P<group>[^ \t]+)[ \t]+(.*)$')
        resp, raw_lines = self.longcmd('LIST NEWSGROUPS ' + group_pattern)
        if resp[:3] != '215':
            resp, raw_lines = self.longcmd('XGTITLE ' + group_pattern)
        lines = []
        for raw_line in raw_lines:
            match = line_pat.search(raw_line.strip())
            if match:
                lines.append(match.group(1, 2))

        return (resp, lines)

    def group(self, name):
        """Process a GROUP command.  Argument:
        - group: the group name
        Returns:
        - resp: server response if successful
        - count: number of articles (string)
        - first: first article number (string)
        - last: last article number (string)
        - name: the group name"""
        resp = self.shortcmd('GROUP ' + name)
        if resp[:3] != '211':
            raise NNTPReplyError(resp)
        words = resp.split()
        count = first = last = 0
        n = len(words)
        if n > 1:
            count = words[1]
            if n > 2:
                first = words[2]
                if n > 3:
                    last = words[3]
                    if n > 4:
                        name = words[4].lower()
        return (resp,
         count,
         first,
         last,
         name)

    def help(self, file = None):
        """Process a HELP command.  Returns:
        - resp: server response if successful
        - list: list of strings"""
        return self.longcmd('HELP', file)

    def statparse(self, resp):
        """Internal: parse the response of a STAT, NEXT or LAST command."""
        if resp[:2] != '22':
            raise NNTPReplyError(resp)
        words = resp.split()
        nr = 0
        id = ''
        n = len(words)
        if n > 1:
            nr = words[1]
            if n > 2:
                id = words[2]
        return (resp, nr, id)

    def statcmd(self, line):
        """Internal: process a STAT, NEXT or LAST command."""
        resp = self.shortcmd(line)
        return self.statparse(resp)

    def stat(self, id):
        """Process a STAT command.  Argument:
        - id: article number or message id
        Returns:
        - resp: server response if successful
        - nr:   the article number
        - id:   the message id"""
        return self.statcmd('STAT ' + id)

    def next(self):
        """Process a NEXT command.  No arguments.  Return as for STAT."""
        return self.statcmd('NEXT')

    def last(self):
        """Process a LAST command.  No arguments.  Return as for STAT."""
        return self.statcmd('LAST')

    def artcmd(self, line, file = None):
        """Internal: process a HEAD, BODY or ARTICLE command."""
        resp, list = self.longcmd(line, file)
        resp, nr, id = self.statparse(resp)
        return (resp,
         nr,
         id,
         list)

    def head(self, id):
        """Process a HEAD command.  Argument:
        - id: article number or message id
        Returns:
        - resp: server response if successful
        - nr: article number
        - id: message id
        - list: the lines of the article's header"""
        return self.artcmd('HEAD ' + id)

    def body(self, id, file = None):
        """Process a BODY command.  Argument:
        - id: article number or message id
        - file: Filename string or file object to store the article in
        Returns:
        - resp: server response if successful
        - nr: article number
        - id: message id
        - list: the lines of the article's body or an empty list
                if file was used"""
        return self.artcmd('BODY ' + id, file)

    def article(self, id):
        """Process an ARTICLE command.  Argument:
        - id: article number or message id
        Returns:
        - resp: server response if successful
        - nr: article number
        - id: message id
        - list: the lines of the article"""
        return self.artcmd('ARTICLE ' + id)

    def slave(self):
        """Process a SLAVE command.  Returns:
        - resp: server response if successful"""
        return self.shortcmd('SLAVE')

    def xhdr(self, hdr, str, file = None):
        """Process an XHDR command (optional server extension).  Arguments:
        - hdr: the header type (e.g. 'subject')
        - str: an article nr, a message id, or a range nr1-nr2
        Returns:
        - resp: server response if successful
        - list: list of (nr, value) strings"""
        pat = re.compile('^([0-9]+) ?(.*)\n?')
        resp, lines = self.longcmd('XHDR ' + hdr + ' ' + str, file)
        for i in range(len(lines)):
            line = lines[i]
            m = pat.match(line)
            if m:
                lines[i] = m.group(1, 2)

        return (resp, lines)

    def xover(self, start, end, file = None):
        """Process an XOVER command (optional server extension) Arguments:
        - start: start of range
        - end: end of range
        Returns:
        - resp: server response if successful
        - list: list of (art-nr, subject, poster, date,
                         id, references, size, lines)"""
        resp, lines = self.longcmd('XOVER ' + start + '-' + end, file)
        xover_lines = []
        for line in lines:
            elem = line.split('\t')
            try:
                xover_lines.append((elem[0],
                 elem[1],
                 elem[2],
                 elem[3],
                 elem[4],
                 elem[5].split(),
                 elem[6],
                 elem[7]))
            except IndexError:
                raise NNTPDataError(line)

        return (resp, xover_lines)

    def xgtitle(self, group, file = None):
        """Process an XGTITLE command (optional server extension) Arguments:
        - group: group name wildcard (i.e. news.*)
        Returns:
        - resp: server response if successful
        - list: list of (name,title) strings"""
        line_pat = re.compile('^([^ \t]+)[ \t]+(.*)$')
        resp, raw_lines = self.longcmd('XGTITLE ' + group, file)
        lines = []
        for raw_line in raw_lines:
            match = line_pat.search(raw_line.strip())
            if match:
                lines.append(match.group(1, 2))

        return (resp, lines)

    def xpath(self, id):
        """Process an XPATH command (optional server extension) Arguments:
        - id: Message id of article
        Returns:
        resp: server response if successful
        path: directory path to article"""
        resp = self.shortcmd('XPATH ' + id)
        if resp[:3] != '223':
            raise NNTPReplyError(resp)
        try:
            resp_num, path = resp.split()
        except ValueError:
            raise NNTPReplyError(resp)
        else:
            return (resp, path)

    def date(self):
        """Process the DATE command. Arguments:
        None
        Returns:
        resp: server response if successful
        date: Date suitable for newnews/newgroups commands etc.
        time: Time suitable for newnews/newgroups commands etc."""
        resp = self.shortcmd('DATE')
        if resp[:3] != '111':
            raise NNTPReplyError(resp)
        elem = resp.split()
        if len(elem) != 2:
            raise NNTPDataError(resp)
        date = elem[1][2:8]
        time = elem[1][-6:]
        if len(date) != 6 or len(time) != 6:
            raise NNTPDataError(resp)
        return (resp, date, time)

    def post--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'shortcmd'
6	LOAD_CONST        'POST'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'resp'

15	LOAD_FAST         'resp'
18	LOAD_CONST        0
21	BINARY_SUBSCR     None
22	LOAD_CONST        '3'
25	COMPARE_OP        '!='
28	POP_JUMP_IF_FALSE '46'

31	LOAD_GLOBAL       'NNTPReplyError'
34	LOAD_FAST         'resp'
37	CALL_FUNCTION_1   None
40	RAISE_VARARGS_1   None
43	JUMP_FORWARD      '46'
46_0	COME_FROM         '43'

46	SETUP_LOOP        '146'

49	LOAD_FAST         'f'
52	LOAD_ATTR         'readline'
55	CALL_FUNCTION_0   None
58	STORE_FAST        'line'

61	LOAD_FAST         'line'
64	POP_JUMP_IF_TRUE  '71'

67	BREAK_LOOP        None
68	JUMP_FORWARD      '71'
71_0	COME_FROM         '68'

71	LOAD_FAST         'line'
74	LOAD_CONST        -1
77	BINARY_SUBSCR     None
78	LOAD_CONST        '\n'
81	COMPARE_OP        '=='
84	POP_JUMP_IF_FALSE '100'

87	LOAD_FAST         'line'
90	LOAD_CONST        -1
93	SLICE+2           None
94	STORE_FAST        'line'
97	JUMP_FORWARD      '100'
100_0	COME_FROM         '97'

100	LOAD_FAST         'line'
103	LOAD_CONST        1
106	SLICE+2           None
107	LOAD_CONST        '.'
110	COMPARE_OP        '=='
113	POP_JUMP_IF_FALSE '129'

116	LOAD_CONST        '.'
119	LOAD_FAST         'line'
122	BINARY_ADD        None
123	STORE_FAST        'line'
126	JUMP_FORWARD      '129'
129_0	COME_FROM         '126'

129	LOAD_FAST         'self'
132	LOAD_ATTR         'putline'
135	LOAD_FAST         'line'
138	CALL_FUNCTION_1   None
141	POP_TOP           None
142	JUMP_BACK         '49'
145	POP_BLOCK         None
146_0	COME_FROM         '46'

146	LOAD_FAST         'self'
149	LOAD_ATTR         'putline'
152	LOAD_CONST        '.'
155	CALL_FUNCTION_1   None
158	POP_TOP           None

159	LOAD_FAST         'self'
162	LOAD_ATTR         'getresp'
165	CALL_FUNCTION_0   None
168	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 145

    def ihave--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'shortcmd'
6	LOAD_CONST        'IHAVE '
9	LOAD_FAST         'id'
12	BINARY_ADD        None
13	CALL_FUNCTION_1   None
16	STORE_FAST        'resp'

19	LOAD_FAST         'resp'
22	LOAD_CONST        0
25	BINARY_SUBSCR     None
26	LOAD_CONST        '3'
29	COMPARE_OP        '!='
32	POP_JUMP_IF_FALSE '50'

35	LOAD_GLOBAL       'NNTPReplyError'
38	LOAD_FAST         'resp'
41	CALL_FUNCTION_1   None
44	RAISE_VARARGS_1   None
47	JUMP_FORWARD      '50'
50_0	COME_FROM         '47'

50	SETUP_LOOP        '150'

53	LOAD_FAST         'f'
56	LOAD_ATTR         'readline'
59	CALL_FUNCTION_0   None
62	STORE_FAST        'line'

65	LOAD_FAST         'line'
68	POP_JUMP_IF_TRUE  '75'

71	BREAK_LOOP        None
72	JUMP_FORWARD      '75'
75_0	COME_FROM         '72'

75	LOAD_FAST         'line'
78	LOAD_CONST        -1
81	BINARY_SUBSCR     None
82	LOAD_CONST        '\n'
85	COMPARE_OP        '=='
88	POP_JUMP_IF_FALSE '104'

91	LOAD_FAST         'line'
94	LOAD_CONST        -1
97	SLICE+2           None
98	STORE_FAST        'line'
101	JUMP_FORWARD      '104'
104_0	COME_FROM         '101'

104	LOAD_FAST         'line'
107	LOAD_CONST        1
110	SLICE+2           None
111	LOAD_CONST        '.'
114	COMPARE_OP        '=='
117	POP_JUMP_IF_FALSE '133'

120	LOAD_CONST        '.'
123	LOAD_FAST         'line'
126	BINARY_ADD        None
127	STORE_FAST        'line'
130	JUMP_FORWARD      '133'
133_0	COME_FROM         '130'

133	LOAD_FAST         'self'
136	LOAD_ATTR         'putline'
139	LOAD_FAST         'line'
142	CALL_FUNCTION_1   None
145	POP_TOP           None
146	JUMP_BACK         '53'
149	POP_BLOCK         None
150_0	COME_FROM         '50'

150	LOAD_FAST         'self'
153	LOAD_ATTR         'putline'
156	LOAD_CONST        '.'
159	CALL_FUNCTION_1   None
162	POP_TOP           None

163	LOAD_FAST         'self'
166	LOAD_ATTR         'getresp'
169	CALL_FUNCTION_0   None
172	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 149

    def quit(self):
        """Process a QUIT command and close the socket.  Returns:
        - resp: server response if successful"""
        resp = self.shortcmd('QUIT')
        self.file.close()
        self.sock.close()
        del self.file
        del self.sock
        return resp


if __name__ == '__main__':
    import os
    newshost = 'news' and os.environ['NNTPSERVER']
    if newshost.find('.') == -1:
        mode = 'readermode'
    else:
        mode = None
    s = NNTP(newshost, readermode=mode)
    resp, count, first, last, name = s.group('comp.lang.python')
    print resp
    print 'Group', name, 'has', count, 'articles, range', first, 'to', last
    resp, subs = s.xhdr('subject', first + '-' + last)
    print resp
    for item in subs:
        print '%7s %s' % item

    resp = s.quit()
    print resp