# Embedded file name: scripts/common/Lib/rfc822.py
r"""RFC 2822 message manipulation.

Note: This is only a very rough sketch of a full RFC-822 parser; in particular
the tokenizing of addresses does not adhere to all the quoting rules.

Note: RFC 2822 is a long awaited update to RFC 822.  This module should
conform to RFC 2822, and is thus mis-named (it's not worth renaming it).  Some
effort at RFC 2822 updates have been made, but a thorough audit has not been
performed.  Consider any RFC 2822 non-conformance to be a bug.

    RFC 2822: http://www.faqs.org/rfcs/rfc2822.html
    RFC 822 : http://www.faqs.org/rfcs/rfc822.html (obsolete)

Directions for use:

To create a Message object: first open a file, e.g.:

  fp = open(file, 'r')

You can use any other legal way of getting an open file object, e.g. use
sys.stdin or call os.popen().  Then pass the open file object to the Message()
constructor:

  m = Message(fp)

This class can work with any input object that supports a readline method.  If
the input object has seek and tell capability, the rewindbody method will
work; also illegal lines will be pushed back onto the input stream.  If the
input object lacks seek but has an `unread' method that can push back a line
of input, Message will use that to push back illegal lines.  Thus this class
can be used to parse messages coming from a buffered stream.

The optional `seekable' argument is provided as a workaround for certain stdio
libraries in which tell() discards buffered data before discovering that the
lseek() system call doesn't work.  For maximum portability, you should set the
seekable argument to zero to prevent that initial \code{tell} when passing in
an unseekable object such as a file object created from a socket object.  If
it is 1 on entry -- which it is by default -- the tell() method of the open
file object is called once; if this raises an exception, seekable is reset to
0.  For other nonzero values of seekable, this test is not made.

To get the text of a particular header there are several methods:

  str = m.getheader(name)
  str = m.getrawheader(name)

where name is the name of the header, e.g. 'Subject'.  The difference is that
getheader() strips the leading and trailing whitespace, while getrawheader()
doesn't.  Both functions retain embedded whitespace (including newlines)
exactly as they are specified in the header, and leave the case of the text
unchanged.

For addresses and address lists there are functions

  realname, mailaddress = m.getaddr(name)
  list = m.getaddrlist(name)

where the latter returns a list of (realname, mailaddr) tuples.

There is also a method

  time = m.getdate(name)

which parses a Date-like field and returns a time-compatible tuple,
i.e. a tuple such as returned by time.localtime() or accepted by
time.mktime().

See the class definition for lower level access methods.

There are also some utility functions here.
"""
import time
from warnings import warnpy3k
warnpy3k('in 3.x, rfc822 has been removed in favor of the email package', stacklevel=2)
__all__ = ['Message',
 'AddressList',
 'parsedate',
 'parsedate_tz',
 'mktime_tz']
_blanklines = ('\r\n', '\n')

class Message():
    """Represents a single RFC 2822-compliant message."""

    def __init__(self, fp, seekable = 1):
        """Initialize the class instance and read the headers."""
        if seekable == 1:
            try:
                fp.tell()
            except (AttributeError, IOError):
                seekable = 0

        self.fp = fp
        self.seekable = seekable
        self.startofheaders = None
        self.startofbody = None
        if self.seekable:
            try:
                self.startofheaders = self.fp.tell()
            except IOError:
                self.seekable = 0

        self.readheaders()
        if self.seekable:
            try:
                self.startofbody = self.fp.tell()
            except IOError:
                self.seekable = 0

        return

    def rewindbody(self):
        """Rewind the file to the start of the body (if seekable)."""
        if not self.seekable:
            raise IOError, 'unseekable file'
        self.fp.seek(self.startofbody)

    def readheaders--- This code section failed: ---

0	BUILD_MAP         None
3	LOAD_FAST         'self'
6	STORE_ATTR        'dict'

9	LOAD_CONST        ''
12	LOAD_FAST         'self'
15	STORE_ATTR        'unixfrom'

18	BUILD_LIST_0      None
21	DUP_TOP           None
22	LOAD_FAST         'self'
25	STORE_ATTR        'headers'
28	STORE_FAST        'lst'

31	LOAD_CONST        ''
34	LOAD_FAST         'self'
37	STORE_ATTR        'status'

40	LOAD_CONST        ''
43	STORE_FAST        'headerseen'

46	LOAD_CONST        1
49	STORE_FAST        'firstline'

52	LOAD_CONST        None
55	DUP_TOP           None
56	STORE_FAST        'startofline'
59	DUP_TOP           None
60	STORE_FAST        'unread'
63	STORE_FAST        'tell'

66	LOAD_GLOBAL       'hasattr'
69	LOAD_FAST         'self'
72	LOAD_ATTR         'fp'
75	LOAD_CONST        'unread'
78	CALL_FUNCTION_2   None
81	POP_JUMP_IF_FALSE '99'

84	LOAD_FAST         'self'
87	LOAD_ATTR         'fp'
90	LOAD_ATTR         'unread'
93	STORE_FAST        'unread'
96	JUMP_FORWARD      '123'

99	LOAD_FAST         'self'
102	LOAD_ATTR         'seekable'
105	POP_JUMP_IF_FALSE '123'

108	LOAD_FAST         'self'
111	LOAD_ATTR         'fp'
114	LOAD_ATTR         'tell'
117	STORE_FAST        'tell'
120	JUMP_FORWARD      '123'
123_0	COME_FROM         '96'
123_1	COME_FROM         '120'

123	SETUP_LOOP        '565'

126	LOAD_FAST         'tell'
129	POP_JUMP_IF_FALSE '187'

132	SETUP_EXCEPT      '148'

135	LOAD_FAST         'tell'
138	CALL_FUNCTION_0   None
141	STORE_FAST        'startofline'
144	POP_BLOCK         None
145	JUMP_ABSOLUTE     '187'
148_0	COME_FROM         '132'

148	DUP_TOP           None
149	LOAD_GLOBAL       'IOError'
152	COMPARE_OP        'exception match'
155	POP_JUMP_IF_FALSE '183'
158	POP_TOP           None
159	POP_TOP           None
160	POP_TOP           None

161	LOAD_CONST        None
164	DUP_TOP           None
165	STORE_FAST        'startofline'
168	STORE_FAST        'tell'

171	LOAD_CONST        0
174	LOAD_FAST         'self'
177	STORE_ATTR        'seekable'
180	JUMP_ABSOLUTE     '187'
183	END_FINALLY       None
184_0	COME_FROM         '183'
184	JUMP_FORWARD      '187'
187_0	COME_FROM         '184'

187	LOAD_FAST         'self'
190	LOAD_ATTR         'fp'
193	LOAD_ATTR         'readline'
196	CALL_FUNCTION_0   None
199	STORE_FAST        'line'

202	LOAD_FAST         'line'
205	POP_JUMP_IF_TRUE  '221'

208	LOAD_CONST        'EOF in headers'
211	LOAD_FAST         'self'
214	STORE_ATTR        'status'

217	BREAK_LOOP        None
218	JUMP_FORWARD      '221'
221_0	COME_FROM         '218'

221	LOAD_FAST         'firstline'
224	POP_JUMP_IF_FALSE '264'
227	LOAD_FAST         'line'
230	LOAD_ATTR         'startswith'
233	LOAD_CONST        'From '
236	CALL_FUNCTION_1   None
239_0	COME_FROM         '224'
239	POP_JUMP_IF_FALSE '264'

242	LOAD_FAST         'self'
245	LOAD_ATTR         'unixfrom'
248	LOAD_FAST         'line'
251	BINARY_ADD        None
252	LOAD_FAST         'self'
255	STORE_ATTR        'unixfrom'

258	CONTINUE          '126'
261	JUMP_FORWARD      '264'
264_0	COME_FROM         '261'

264	LOAD_CONST        0
267	STORE_FAST        'firstline'

270	LOAD_FAST         'headerseen'
273	POP_JUMP_IF_FALSE '357'
276	LOAD_FAST         'line'
279	LOAD_CONST        0
282	BINARY_SUBSCR     None
283	LOAD_CONST        ' \t'
286	COMPARE_OP        'in'
289_0	COME_FROM         '273'
289	POP_JUMP_IF_FALSE '357'

292	LOAD_FAST         'lst'
295	LOAD_ATTR         'append'
298	LOAD_FAST         'line'
301	CALL_FUNCTION_1   None
304	POP_TOP           None

305	LOAD_FAST         'self'
308	LOAD_ATTR         'dict'
311	LOAD_FAST         'headerseen'
314	BINARY_SUBSCR     None
315	LOAD_CONST        '\n '
318	BINARY_ADD        None
319	LOAD_FAST         'line'
322	LOAD_ATTR         'strip'
325	CALL_FUNCTION_0   None
328	BINARY_ADD        None
329	STORE_FAST        'x'

332	LOAD_FAST         'x'
335	LOAD_ATTR         'strip'
338	CALL_FUNCTION_0   None
341	LOAD_FAST         'self'
344	LOAD_ATTR         'dict'
347	LOAD_FAST         'headerseen'
350	STORE_SUBSCR      None

351	CONTINUE          '126'
354	JUMP_FORWARD      '397'

357	LOAD_FAST         'self'
360	LOAD_ATTR         'iscomment'
363	LOAD_FAST         'line'
366	CALL_FUNCTION_1   None
369	POP_JUMP_IF_FALSE '378'

372	CONTINUE          '126'
375	JUMP_FORWARD      '397'

378	LOAD_FAST         'self'
381	LOAD_ATTR         'islast'
384	LOAD_FAST         'line'
387	CALL_FUNCTION_1   None
390	POP_JUMP_IF_FALSE '397'

393	BREAK_LOOP        None
394	JUMP_FORWARD      '397'
397_0	COME_FROM         '354'
397_1	COME_FROM         '375'
397_2	COME_FROM         '394'

397	LOAD_FAST         'self'
400	LOAD_ATTR         'isheader'
403	LOAD_FAST         'line'
406	CALL_FUNCTION_1   None
409	STORE_FAST        'headerseen'

412	LOAD_FAST         'headerseen'
415	POP_JUMP_IF_FALSE '470'

418	LOAD_FAST         'lst'
421	LOAD_ATTR         'append'
424	LOAD_FAST         'line'
427	CALL_FUNCTION_1   None
430	POP_TOP           None

431	LOAD_FAST         'line'
434	LOAD_GLOBAL       'len'
437	LOAD_FAST         'headerseen'
440	CALL_FUNCTION_1   None
443	LOAD_CONST        1
446	BINARY_ADD        None
447	SLICE+1           None
448	LOAD_ATTR         'strip'
451	CALL_FUNCTION_0   None
454	LOAD_FAST         'self'
457	LOAD_ATTR         'dict'
460	LOAD_FAST         'headerseen'
463	STORE_SUBSCR      None

464	CONTINUE          '126'
467	JUMP_BACK         '126'

470	LOAD_FAST         'self'
473	LOAD_ATTR         'dict'
476	POP_JUMP_IF_TRUE  '491'

479	LOAD_CONST        'No headers'
482	LOAD_FAST         'self'
485	STORE_ATTR        'status'
488	JUMP_FORWARD      '500'

491	LOAD_CONST        'Non-header line where header expected'
494	LOAD_FAST         'self'
497	STORE_ATTR        'status'
500_0	COME_FROM         '488'

500	LOAD_FAST         'unread'
503	POP_JUMP_IF_FALSE '519'

506	LOAD_FAST         'unread'
509	LOAD_FAST         'line'
512	CALL_FUNCTION_1   None
515	POP_TOP           None
516	JUMP_FORWARD      '560'

519	LOAD_FAST         'tell'
522	POP_JUMP_IF_FALSE '544'

525	LOAD_FAST         'self'
528	LOAD_ATTR         'fp'
531	LOAD_ATTR         'seek'
534	LOAD_FAST         'startofline'
537	CALL_FUNCTION_1   None
540	POP_TOP           None
541	JUMP_FORWARD      '560'

544	LOAD_FAST         'self'
547	LOAD_ATTR         'status'
550	LOAD_CONST        '; bad seek'
553	BINARY_ADD        None
554	LOAD_FAST         'self'
557	STORE_ATTR        'status'
560_0	COME_FROM         '516'
560_1	COME_FROM         '541'

560	BREAK_LOOP        None
561	JUMP_BACK         '126'
564	POP_BLOCK         None
565_0	COME_FROM         '123'
565	LOAD_CONST        None
568	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 564

    def isheader(self, line):
        """Determine whether a given line is a legal header.
        
        This method should return the header name, suitably canonicalized.
        You may override this method in order to use Message parsing on tagged
        data in RFC 2822-like formats with special header formats.
        """
        i = line.find(':')
        if i > 0:
            return line[:i].lower()
        else:
            return None

    def islast(self, line):
        """Determine whether a line is a legal end of RFC 2822 headers.
        
               You may override this method if your application wants to bend the
               rules, e.g. to strip trailing whitespace, or to recognize MH template
               separators ('--------').  For convenience (e.g. for code reading from
               sockets) a line consisting of 
        also matches.
               """
        return line in _blanklines

    def iscomment(self, line):
        """Determine whether a line should be skipped entirely.
        
        You may override this method in order to use Message parsing on tagged
        data in RFC 2822-like formats that support embedded comments or
        free-text data.
        """
        return False

    def getallmatchingheaders(self, name):
        """Find all header lines matching a given header name.
        
        Look through the list of headers and find all lines matching a given
        header name (and their continuation lines).  A list of the lines is
        returned, without interpretation.  If the header does not occur, an
        empty list is returned.  If the header occurs multiple times, all
        occurrences are returned.  Case is not important in the header name.
        """
        name = name.lower() + ':'
        n = len(name)
        lst = []
        hit = 0
        for line in self.headers:
            if line[:n].lower() == name:
                hit = 1
            elif not line[:1].isspace():
                hit = 0
            if hit:
                lst.append(line)

        return lst

    def getfirstmatchingheader(self, name):
        """Get the first header line matching name.
        
        This is similar to getallmatchingheaders, but it returns only the
        first matching header (and its continuation lines).
        """
        name = name.lower() + ':'
        n = len(name)
        lst = []
        hit = 0
        for line in self.headers:
            if hit:
                if not line[:1].isspace():
                    break
            elif line[:n].lower() == name:
                hit = 1
            if hit:
                lst.append(line)

        return lst

    def getrawheader(self, name):
        """A higher-level interface to getfirstmatchingheader().
        
        Return a string containing the literal text of the header but with the
        keyword stripped.  All leading, trailing and embedded whitespace is
        kept in the string, however.  Return None if the header does not
        occur.
        """
        lst = self.getfirstmatchingheader(name)
        if not lst:
            return None
        else:
            lst[0] = lst[0][len(name) + 1:]
            return ''.join(lst)

    def getheader(self, name, default = None):
        """Get the header value for a name.
        
        This is the normal interface: it returns a stripped version of the
        header value for a given header name, or None if it doesn't exist.
        This uses the dictionary version which finds the *last* such header.
        """
        return self.dict.get(name.lower(), default)

    get = getheader

    def getheaders(self, name):
        """Get all values for a header.
        
        This returns a list of values for headers given more than once; each
        value in the result list is stripped in the same way as the result of
        getheader().  If the header is not given, return an empty list.
        """
        result = []
        current = ''
        have_header = 0
        for s in self.getallmatchingheaders(name):
            if s[0].isspace():
                if current:
                    current = '%s\n %s' % (current, s.strip())
                else:
                    current = s.strip()
            else:
                if have_header:
                    result.append(current)
                current = s[s.find(':') + 1:].strip()
                have_header = 1

        if have_header:
            result.append(current)
        return result

    def getaddr(self, name):
        """Get a single address from a header, as a tuple.
        
        An example return value:
        ('Guido van Rossum', 'guido@cwi.nl')
        """
        alist = self.getaddrlist(name)
        if alist:
            return alist[0]
        else:
            return (None, None)
            return None

    def getaddrlist(self, name):
        """Get a list of addresses from a header.
        
        Retrieves a list of addresses from a header, where each address is a
        tuple as returned by getaddr().  Scans all named headers, so it works
        properly with multiple To: or Cc: headers for example.
        """
        raw = []
        for h in self.getallmatchingheaders(name):
            if h[0] in ' \t':
                raw.append(h)
            else:
                if raw:
                    raw.append(', ')
                i = h.find(':')
                if i > 0:
                    addr = h[i + 1:]
                raw.append(addr)

        alladdrs = ''.join(raw)
        a = AddressList(alladdrs)
        return a.addresslist

    def getdate(self, name):
        """Retrieve a date field from a header.
        
        Retrieves a date field from the named header, returning a tuple
        compatible with time.mktime().
        """
        try:
            data = self[name]
        except KeyError:
            return None

        return parsedate(data)

    def getdate_tz(self, name):
        """Retrieve a date field from a header as a 10-tuple.
        
        The first 9 elements make up a tuple compatible with time.mktime(),
        and the 10th is the offset of the poster's time zone from GMT/UTC.
        """
        try:
            data = self[name]
        except KeyError:
            return None

        return parsedate_tz(data)

    def __len__(self):
        """Get the number of headers in a message."""
        return len(self.dict)

    def __getitem__(self, name):
        """Get a specific header, as from a dictionary."""
        return self.dict[name.lower()]

    def __setitem__(self, name, value):
        """Set the value of a header.
        
        Note: This is not a perfect inversion of __getitem__, because any
        changed headers get stuck at the end of the raw-headers list rather
        than where the altered header was.
        """
        del self[name]
        self.dict[name.lower()] = value
        text = name + ': ' + value
        for line in text.split('\n'):
            self.headers.append(line + '\n')

    def __delitem__(self, name):
        """Delete all occurrences of a specific header, if it is present."""
        name = name.lower()
        if name not in self.dict:
            return
        del self.dict[name]
        name = name + ':'
        n = len(name)
        lst = []
        hit = 0
        for i in range(len(self.headers)):
            line = self.headers[i]
            if line[:n].lower() == name:
                hit = 1
            elif not line[:1].isspace():
                hit = 0
            if hit:
                lst.append(i)

        for i in reversed(lst):
            del self.headers[i]

    def setdefault(self, name, default = ''):
        lowername = name.lower()
        if lowername in self.dict:
            return self.dict[lowername]
        else:
            text = name + ': ' + default
            for line in text.split('\n'):
                self.headers.append(line + '\n')

            self.dict[lowername] = default
            return default

    def has_key(self, name):
        """Determine whether a message contains the named header."""
        return name.lower() in self.dict

    def __contains__(self, name):
        """Determine whether a message contains the named header."""
        return name.lower() in self.dict

    def __iter__(self):
        return iter(self.dict)

    def keys(self):
        """Get all of a message's header field names."""
        return self.dict.keys()

    def values(self):
        """Get all of a message's header field values."""
        return self.dict.values()

    def items(self):
        """Get all of a message's headers.
        
        Returns a list of name, value tuples.
        """
        return self.dict.items()

    def __str__(self):
        return ''.join(self.headers)


def unquote(s):
    """Remove quotes from a string."""
    if len(s) > 1:
        if s.startswith('"') and s.endswith('"'):
            return s[1:-1].replace('\\\\', '\\').replace('\\"', '"')
        if s.startswith('<') and s.endswith('>'):
            return s[1:-1]
    return s


def quote(s):
    """Add quotes around a string."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def parseaddr(address):
    """Parse an address into a (realname, mailaddr) tuple."""
    a = AddressList(address)
    lst = a.addresslist
    if not lst:
        return (None, None)
    else:
        return lst[0]


class AddrlistClass():
    """Address parser class by Ben Escoto.
    
    To understand what this class does, it helps to have a copy of
    RFC 2822 in front of you.
    
    http://www.faqs.org/rfcs/rfc2822.html
    
    Note: this class interface is deprecated and may be removed in the future.
    Use rfc822.AddressList instead.
    """

    def __init__(self, field):
        """Initialize a new instance.
        
        `field' is an unparsed address header field, containing one or more
        addresses.
        """
        self.specials = '()<>@,:;."[]'
        self.pos = 0
        self.LWS = ' \t'
        self.CR = '\r\n'
        self.atomends = self.specials + self.LWS + self.CR
        self.phraseends = self.atomends.replace('.', '')
        self.field = field
        self.commentlist = []

    def gotonext(self):
        """Parse up to the start of the next address."""
        while self.pos < len(self.field):
            if self.field[self.pos] in self.LWS + '\n\r':
                self.pos = self.pos + 1
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            else:
                break

    def getaddrlist(self):
        """Parse all addresses.
        
        Returns a list containing all of the addresses.
        """
        result = []
        ad = self.getaddress()
        while ad:
            result += ad
            ad = self.getaddress()

        return result

    def getaddress(self):
        """Parse the next address."""
        self.commentlist = []
        self.gotonext()
        oldpos = self.pos
        oldcl = self.commentlist
        plist = self.getphraselist()
        self.gotonext()
        returnlist = []
        if self.pos >= len(self.field):
            if plist:
                returnlist = [(' '.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in '.@':
            self.pos = oldpos
            self.commentlist = oldcl
            addrspec = self.getaddrspec()
            returnlist = [(' '.join(self.commentlist), addrspec)]
        elif self.field[self.pos] == ':':
            returnlist = []
            fieldlen = len(self.field)
            self.pos += 1
            while self.pos < len(self.field):
                self.gotonext()
                if self.pos < fieldlen and self.field[self.pos] == ';':
                    self.pos += 1
                    break
                returnlist = returnlist + self.getaddress()

        elif self.field[self.pos] == '<':
            routeaddr = self.getrouteaddr()
            if self.commentlist:
                returnlist = [(' '.join(plist) + ' (' + ' '.join(self.commentlist) + ')', routeaddr)]
            else:
                returnlist = [(' '.join(plist), routeaddr)]
        elif plist:
            returnlist = [(' '.join(self.commentlist), plist[0])]
        elif self.field[self.pos] in self.specials:
            self.pos += 1
        self.gotonext()
        if self.pos < len(self.field) and self.field[self.pos] == ',':
            self.pos += 1
        return returnlist

    def getrouteaddr(self):
        """Parse a route address (Return-path value).
        
        This method just skips all the route stuff and returns the addrspec.
        """
        if self.field[self.pos] != '<':
            return
        expectroute = 0
        self.pos += 1
        self.gotonext()
        adlist = ''
        while self.pos < len(self.field):
            if expectroute:
                self.getdomain()
                expectroute = 0
            elif self.field[self.pos] == '>':
                self.pos += 1
                break
            elif self.field[self.pos] == '@':
                self.pos += 1
                expectroute = 1
            elif self.field[self.pos] == ':':
                self.pos += 1
            else:
                adlist = self.getaddrspec()
                self.pos += 1
                break
            self.gotonext()

        return adlist

    def getaddrspec(self):
        """Parse an RFC 2822 addr-spec."""
        aslist = []
        self.gotonext()
        while self.pos < len(self.field):
            if self.field[self.pos] == '.':
                aslist.append('.')
                self.pos += 1
            elif self.field[self.pos] == '"':
                aslist.append('"%s"' % self.getquote())
            elif self.field[self.pos] in self.atomends:
                break
            else:
                aslist.append(self.getatom())
            self.gotonext()

        if self.pos >= len(self.field) or self.field[self.pos] != '@':
            return ''.join(aslist)
        aslist.append('@')
        self.pos += 1
        self.gotonext()
        return ''.join(aslist) + self.getdomain()

    def getdomain(self):
        """Get the complete domain name from an address."""
        sdlist = []
        while self.pos < len(self.field):
            if self.field[self.pos] in self.LWS:
                self.pos += 1
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            elif self.field[self.pos] == '[':
                sdlist.append(self.getdomainliteral())
            elif self.field[self.pos] == '.':
                self.pos += 1
                sdlist.append('.')
            elif self.field[self.pos] in self.atomends:
                break
            else:
                sdlist.append(self.getatom())

        return ''.join(sdlist)

    def getdelimited(self, beginchar, endchars, allowcomments = 1):
        """Parse a header fragment delimited by special characters.
        
        `beginchar' is the start character for the fragment.  If self is not
        looking at an instance of `beginchar' then getdelimited returns the
        empty string.
        
        `endchars' is a sequence of allowable end-delimiting characters.
        Parsing stops when one of these is encountered.
        
        If `allowcomments' is non-zero, embedded RFC 2822 comments are allowed
        within the parsed fragment.
        """
        if self.field[self.pos] != beginchar:
            return ''
        slist = ['']
        quote = 0
        self.pos += 1
        while self.pos < len(self.field):
            if quote == 1:
                slist.append(self.field[self.pos])
                quote = 0
            elif self.field[self.pos] in endchars:
                self.pos += 1
                break
            elif allowcomments and self.field[self.pos] == '(':
                slist.append(self.getcomment())
                continue
            elif self.field[self.pos] == '\\':
                quote = 1
            else:
                slist.append(self.field[self.pos])
            self.pos += 1

        return ''.join(slist)

    def getquote(self):
        """Get a quote-delimited fragment from self's field."""
        return self.getdelimited('"', '"\r', 0)

    def getcomment(self):
        """Get a parenthesis-delimited fragment from self's field."""
        return self.getdelimited('(', ')\r', 1)

    def getdomainliteral(self):
        """Parse an RFC 2822 domain-literal."""
        return '[%s]' % self.getdelimited('[', ']\r', 0)

    def getatom(self, atomends = None):
        """Parse an RFC 2822 atom.
        
        Optional atomends specifies a different set of end token delimiters
        (the default is to use self.atomends).  This is used e.g. in
        getphraselist() since phrase endings must not include the `.' (which
        is legal in phrases)."""
        atomlist = ['']
        if atomends is None:
            atomends = self.atomends
        while self.pos < len(self.field):
            if self.field[self.pos] in atomends:
                break
            else:
                atomlist.append(self.field[self.pos])
            self.pos += 1

        return ''.join(atomlist)

    def getphraselist(self):
        """Parse a sequence of RFC 2822 phrases.
        
        A phrase is a sequence of words, which are in turn either RFC 2822
        atoms or quoted-strings.  Phrases are canonicalized by squeezing all
        runs of continuous whitespace into one space.
        """
        plist = []
        while self.pos < len(self.field):
            if self.field[self.pos] in self.LWS:
                self.pos += 1
            elif self.field[self.pos] == '"':
                plist.append(self.getquote())
            elif self.field[self.pos] == '(':
                self.commentlist.append(self.getcomment())
            elif self.field[self.pos] in self.phraseends:
                break
            else:
                plist.append(self.getatom(self.phraseends))

        return plist


class AddressList(AddrlistClass):
    """An AddressList encapsulates a list of parsed RFC 2822 addresses."""

    def __init__(self, field):
        AddrlistClass.__init__(self, field)
        if field:
            self.addresslist = self.getaddrlist()
        else:
            self.addresslist = []

    def __len__(self):
        return len(self.addresslist)

    def __str__(self):
        return ', '.join(map(dump_address_pair, self.addresslist))

    def __add__(self, other):
        newaddr = AddressList(None)
        newaddr.addresslist = self.addresslist[:]
        for x in other.addresslist:
            if x not in self.addresslist:
                newaddr.addresslist.append(x)

        return newaddr

    def __iadd__(self, other):
        for x in other.addresslist:
            if x not in self.addresslist:
                self.addresslist.append(x)

        return self

    def __sub__(self, other):
        newaddr = AddressList(None)
        for x in self.addresslist:
            if x not in other.addresslist:
                newaddr.addresslist.append(x)

        return newaddr

    def __isub__(self, other):
        for x in other.addresslist:
            if x in self.addresslist:
                self.addresslist.remove(x)

        return self

    def __getitem__(self, index):
        return self.addresslist[index]


def dump_address_pair(pair):
    """Dump a (name, address) pair in a canonicalized form."""
    if pair[0]:
        return '"' + pair[0] + '" <' + pair[1] + '>'
    else:
        return pair[1]


_monthnames = ['jan',
 'feb',
 'mar',
 'apr',
 'may',
 'jun',
 'jul',
 'aug',
 'sep',
 'oct',
 'nov',
 'dec',
 'january',
 'february',
 'march',
 'april',
 'may',
 'june',
 'july',
 'august',
 'september',
 'october',
 'november',
 'december']
_daynames = ['mon',
 'tue',
 'wed',
 'thu',
 'fri',
 'sat',
 'sun']
_timezones = {'UT': 0,
 'UTC': 0,
 'GMT': 0,
 'Z': 0,
 'AST': -400,
 'ADT': -300,
 'EST': -500,
 'EDT': -400,
 'CST': -600,
 'CDT': -500,
 'MST': -700,
 'MDT': -600,
 'PST': -800,
 'PDT': -700}

def parsedate_tz(data):
    """Convert a date string to a time tuple.
    
    Accounts for military timezones.
    """
    if not data:
        return
    else:
        data = data.split()
        if data[0][-1] in (',', '.') or data[0].lower() in _daynames:
            del data[0]
        else:
            i = data[0].rfind(',')
            if i >= 0:
                data[0] = data[0][i + 1:]
        if len(data) == 3:
            stuff = data[0].split('-')
            if len(stuff) == 3:
                data = stuff + data[1:]
        if len(data) == 4:
            s = data[3]
            i = s.find('+')
            if i > 0:
                data[3:] = [s[:i], s[i + 1:]]
            else:
                data.append('')
        if len(data) < 5:
            return
        data = data[:5]
        dd, mm, yy, tm, tz = data
        mm = mm.lower()
        if mm not in _monthnames:
            dd, mm = mm, dd.lower()
            if mm not in _monthnames:
                return
        mm = _monthnames.index(mm) + 1
        if mm > 12:
            mm = mm - 12
        if dd[-1] == ',':
            dd = dd[:-1]
        i = yy.find(':')
        if i > 0:
            yy, tm = tm, yy
        if yy[-1] == ',':
            yy = yy[:-1]
        if not yy[0].isdigit():
            yy, tz = tz, yy
        if tm[-1] == ',':
            tm = tm[:-1]
        tm = tm.split(':')
        if len(tm) == 2:
            thh, tmm = tm
            tss = '0'
        elif len(tm) == 3:
            thh, tmm, tss = tm
        else:
            return
        try:
            yy = int(yy)
            dd = int(dd)
            thh = int(thh)
            tmm = int(tmm)
            tss = int(tss)
        except ValueError:
            return

        tzoffset = None
        tz = tz.upper()
        if tz in _timezones:
            tzoffset = _timezones[tz]
        else:
            try:
                tzoffset = int(tz)
            except ValueError:
                pass

        if tzoffset:
            if tzoffset < 0:
                tzsign = -1
                tzoffset = -tzoffset
            else:
                tzsign = 1
            tzoffset = tzsign * (tzoffset // 100 * 3600 + tzoffset % 100 * 60)
        return (yy,
         mm,
         dd,
         thh,
         tmm,
         tss,
         0,
         1,
         0,
         tzoffset)


def parsedate(data):
    """Convert a time string to a time tuple."""
    t = parsedate_tz(data)
    if t is None:
        return t
    else:
        return t[:9]


def mktime_tz(data):
    """Turn a 10-tuple as returned by parsedate_tz() into a UTC timestamp."""
    if data[9] is None:
        return time.mktime(data[:8] + (-1,))
    else:
        t = time.mktime(data[:8] + (0,))
        return t - data[9] - time.timezone
        return


def formatdate(timeval = None):
    """Returns time format preferred for Internet standards.
    
    Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
    
    According to RFC 1123, day and month names must always be in
    English.  If not for that, this code could use strftime().  It
    can't because strftime() honors the locale and could generated
    non-English names.
    """
    if timeval is None:
        timeval = time.time()
    timeval = time.gmtime(timeval)
    return '%s, %02d %s %04d %02d:%02d:%02d GMT' % (('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')[timeval[6]],
     timeval[2],
     ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[timeval[1] - 1],
     timeval[0],
     timeval[3],
     timeval[4],
     timeval[5])


if __name__ == '__main__':
    import sys, os
    file = os.path.join(os.environ['HOME'], 'Mail/inbox/1')
    if sys.argv[1:]:
        file = sys.argv[1]
    f = open(file, 'r')
    m = Message(f)
    print 'From:', m.getaddr('from')
    print 'To:', m.getaddrlist('to')
    print 'Subject:', m.getheader('subject')
    print 'Date:', m.getheader('date')
    date = m.getdate_tz('date')
    tz = date[-1]
    date = time.localtime(mktime_tz(date))
    if date:
        print 'ParsedDate:', time.asctime(date),
        hhmmss = tz
        hhmm, ss = divmod(hhmmss, 60)
        hh, mm = divmod(hhmm, 60)
        print '%+03d%02d' % (hh, mm),
        if ss:
            print '.%02d' % ss,
        print
    else:
        print 'ParsedDate:', None
    m.rewindbody()
    n = 0
    while f.readline():
        n += 1

    print 'Lines:', n
    print '-' * 70
    print 'len =', len(m)
    if 'Date' in m:
        print 'Date =', m['Date']
    if 'X-Nonsense' in m:
        pass
    print 'keys =', m.keys()
    print 'values =', m.values()
    print 'items =', m.items()