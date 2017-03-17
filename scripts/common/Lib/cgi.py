# Embedded file name: scripts/common/Lib/cgi.py
"""Support module for CGI (Common Gateway Interface) scripts.

This module defines a number of utilities for use by CGI scripts
written in Python.
"""
__version__ = '2.6'
from operator import attrgetter
import sys
import os
import urllib
import UserDict
import urlparse
from warnings import filterwarnings, catch_warnings, warn
with catch_warnings():
    if sys.py3kwarning:
        filterwarnings('ignore', '.*mimetools has been removed', DeprecationWarning)
        filterwarnings('ignore', '.*rfc822 has been removed', DeprecationWarning)
    import mimetools
    import rfc822
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

__all__ = ['MiniFieldStorage',
 'FieldStorage',
 'FormContentDict',
 'SvFormContentDict',
 'InterpFormContentDict',
 'FormContent',
 'parse',
 'parse_qs',
 'parse_qsl',
 'parse_multipart',
 'parse_header',
 'print_exception',
 'print_environ',
 'print_form',
 'print_directory',
 'print_arguments',
 'print_environ_usage',
 'escape']
logfile = ''
logfp = None

def initlog(*allargs):
    """Write a log message, if there is a log file.
    
    Even though this function is called initlog(), you should always
    use log(); log is a variable that is set either to initlog
    (initially), to dolog (once the log file has been opened), or to
    nolog (when logging is disabled).
    
    The first argument is a format string; the remaining arguments (if
    any) are arguments to the % operator, so e.g.
        log("%s: %s", "a", "b")
    will write "a: b" to the log file, followed by a newline.
    
    If the global logfp is not None, it should be a file object to
    which log data is written.
    
    If the global logfp is None, the global logfile may be a string
    giving a filename to open, in append mode.  This file should be
    world writable!!!  If the file can't be opened, logging is
    silently disabled (since there is no safe place where we could
    send an error message).
    
    """
    global logfp
    global log
    if logfile and not logfp:
        try:
            logfp = open(logfile, 'a')
        except IOError:
            pass

    if not logfp:
        log = nolog
    else:
        log = dolog
    log(*allargs)


def dolog(fmt, *args):
    """Write a log message to the log file.  See initlog() for docs."""
    logfp.write(fmt % args + '\n')


def nolog(*allargs):
    """Dummy function, assigned to log when logging is disabled."""
    pass


log = initlog
maxlen = 0

def parse(fp = None, environ = os.environ, keep_blank_values = 0, strict_parsing = 0):
    """Parse a query in the environment or from a file (default stdin)
    
        Arguments, all optional:
    
        fp              : file pointer; default: sys.stdin
    
        environ         : environment dictionary; default: os.environ
    
        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.
    
        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
    """
    global maxlen
    if fp is None:
        fp = sys.stdin
    if 'REQUEST_METHOD' not in environ:
        environ['REQUEST_METHOD'] = 'GET'
    if environ['REQUEST_METHOD'] == 'POST':
        ctype, pdict = parse_header(environ['CONTENT_TYPE'])
        if ctype == 'multipart/form-data':
            return parse_multipart(fp, pdict)
        if ctype == 'application/x-www-form-urlencoded':
            clength = int(environ['CONTENT_LENGTH'])
            if maxlen and clength > maxlen:
                raise ValueError, 'Maximum content length exceeded'
            qs = fp.read(clength)
        else:
            qs = ''
        if 'QUERY_STRING' in environ:
            if qs:
                qs = qs + '&'
            qs = qs + environ['QUERY_STRING']
        elif sys.argv[1:]:
            if qs:
                qs = qs + '&'
            qs = qs + sys.argv[1]
        environ['QUERY_STRING'] = qs
    elif 'QUERY_STRING' in environ:
        qs = environ['QUERY_STRING']
    else:
        if sys.argv[1:]:
            qs = sys.argv[1]
        else:
            qs = ''
        environ['QUERY_STRING'] = qs
    return urlparse.parse_qs(qs, keep_blank_values, strict_parsing)


def parse_qs(qs, keep_blank_values = 0, strict_parsing = 0):
    """Parse a query given as a string argument."""
    warn('cgi.parse_qs is deprecated, use urlparse.parse_qs instead', PendingDeprecationWarning, 2)
    return urlparse.parse_qs(qs, keep_blank_values, strict_parsing)


def parse_qsl(qs, keep_blank_values = 0, strict_parsing = 0):
    """Parse a query given as a string argument."""
    warn('cgi.parse_qsl is deprecated, use urlparse.parse_qsl instead', PendingDeprecationWarning, 2)
    return urlparse.parse_qsl(qs, keep_blank_values, strict_parsing)


def parse_multipart--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'boundary'

6	LOAD_CONST        'boundary'
9	LOAD_FAST         'pdict'
12	COMPARE_OP        'in'
15	POP_JUMP_IF_FALSE '31'

18	LOAD_FAST         'pdict'
21	LOAD_CONST        'boundary'
24	BINARY_SUBSCR     None
25	STORE_FAST        'boundary'
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_GLOBAL       'valid_boundary'
34	LOAD_FAST         'boundary'
37	CALL_FUNCTION_1   None
40	POP_JUMP_IF_TRUE  '62'

43	LOAD_GLOBAL       'ValueError'
46	LOAD_CONST        'Invalid boundary in multipart form: %r'

49	LOAD_FAST         'boundary'
52	BUILD_TUPLE_1     None
55	BINARY_MODULO     None
56	RAISE_VARARGS_2   None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_CONST        '--'
65	LOAD_FAST         'boundary'
68	BINARY_ADD        None
69	STORE_FAST        'nextpart'

72	LOAD_CONST        '--'
75	LOAD_FAST         'boundary'
78	BINARY_ADD        None
79	LOAD_CONST        '--'
82	BINARY_ADD        None
83	STORE_FAST        'lastpart'

86	BUILD_MAP         None
89	STORE_FAST        'partdict'

92	LOAD_CONST        ''
95	STORE_FAST        'terminator'

98	SETUP_LOOP        '652'
101	LOAD_FAST         'terminator'
104	LOAD_FAST         'lastpart'
107	COMPARE_OP        '!='
110	POP_JUMP_IF_FALSE '651'

113	LOAD_CONST        -1
116	STORE_FAST        'bytes'

119	LOAD_CONST        None
122	STORE_FAST        'data'

125	LOAD_FAST         'terminator'
128	POP_JUMP_IF_FALSE '275'

131	LOAD_GLOBAL       'mimetools'
134	LOAD_ATTR         'Message'
137	LOAD_FAST         'fp'
140	CALL_FUNCTION_1   None
143	STORE_FAST        'headers'

146	LOAD_FAST         'headers'
149	LOAD_ATTR         'getheader'
152	LOAD_CONST        'content-length'
155	CALL_FUNCTION_1   None
158	STORE_FAST        'clength'

161	LOAD_FAST         'clength'
164	POP_JUMP_IF_FALSE '206'

167	SETUP_EXCEPT      '186'

170	LOAD_GLOBAL       'int'
173	LOAD_FAST         'clength'
176	CALL_FUNCTION_1   None
179	STORE_FAST        'bytes'
182	POP_BLOCK         None
183	JUMP_ABSOLUTE     '206'
186_0	COME_FROM         '167'

186	DUP_TOP           None
187	LOAD_GLOBAL       'ValueError'
190	COMPARE_OP        'exception match'
193	POP_JUMP_IF_FALSE '202'
196	POP_TOP           None
197	POP_TOP           None
198	POP_TOP           None

199	JUMP_ABSOLUTE     '206'
202	END_FINALLY       None
203_0	COME_FROM         '202'
203	JUMP_FORWARD      '206'
206_0	COME_FROM         '203'

206	LOAD_FAST         'bytes'
209	LOAD_CONST        0
212	COMPARE_OP        '>'
215	POP_JUMP_IF_FALSE '266'

218	LOAD_GLOBAL       'maxlen'
221	POP_JUMP_IF_FALSE '248'
224	LOAD_FAST         'bytes'
227	LOAD_GLOBAL       'maxlen'
230	COMPARE_OP        '>'
233_0	COME_FROM         '221'
233	POP_JUMP_IF_FALSE '248'

236	LOAD_GLOBAL       'ValueError'
239	LOAD_CONST        'Maximum content length exceeded'
242	RAISE_VARARGS_2   None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_FAST         'fp'
251	LOAD_ATTR         'read'
254	LOAD_FAST         'bytes'
257	CALL_FUNCTION_1   None
260	STORE_FAST        'data'
263	JUMP_ABSOLUTE     '275'

266	LOAD_CONST        ''
269	STORE_FAST        'data'
272	JUMP_FORWARD      '275'
275_0	COME_FROM         '272'

275	BUILD_LIST_0      None
278	STORE_FAST        'lines'

281	SETUP_LOOP        '382'

284	LOAD_FAST         'fp'
287	LOAD_ATTR         'readline'
290	CALL_FUNCTION_0   None
293	STORE_FAST        'line'

296	LOAD_FAST         'line'
299	POP_JUMP_IF_TRUE  '312'

302	LOAD_FAST         'lastpart'
305	STORE_FAST        'terminator'

308	BREAK_LOOP        None
309	JUMP_FORWARD      '312'
312_0	COME_FROM         '309'

312	LOAD_FAST         'line'
315	LOAD_CONST        2
318	SLICE+2           None
319	LOAD_CONST        '--'
322	COMPARE_OP        '=='
325	POP_JUMP_IF_FALSE '365'

328	LOAD_FAST         'line'
331	LOAD_ATTR         'strip'
334	CALL_FUNCTION_0   None
337	STORE_FAST        'terminator'

340	LOAD_FAST         'terminator'
343	LOAD_FAST         'nextpart'
346	LOAD_FAST         'lastpart'
349	BUILD_TUPLE_2     None
352	COMPARE_OP        'in'
355	POP_JUMP_IF_FALSE '365'

358	BREAK_LOOP        None
359	JUMP_ABSOLUTE     '365'
362	JUMP_FORWARD      '365'
365_0	COME_FROM         '362'

365	LOAD_FAST         'lines'
368	LOAD_ATTR         'append'
371	LOAD_FAST         'line'
374	CALL_FUNCTION_1   None
377	POP_TOP           None
378	JUMP_BACK         '284'
381	POP_BLOCK         None
382_0	COME_FROM         '281'

382	LOAD_FAST         'data'
385	LOAD_CONST        None
388	COMPARE_OP        'is'
391	POP_JUMP_IF_FALSE '400'

394	CONTINUE          '101'
397	JUMP_FORWARD      '400'
400_0	COME_FROM         '397'

400	LOAD_FAST         'bytes'
403	LOAD_CONST        0
406	COMPARE_OP        '<'
409	POP_JUMP_IF_FALSE '517'

412	LOAD_FAST         'lines'
415	POP_JUMP_IF_FALSE '517'

418	LOAD_FAST         'lines'
421	LOAD_CONST        -1
424	BINARY_SUBSCR     None
425	STORE_FAST        'line'

428	LOAD_FAST         'line'
431	LOAD_CONST        -2
434	SLICE+1           None
435	LOAD_CONST        '\r\n'
438	COMPARE_OP        '=='
441	POP_JUMP_IF_FALSE '457'

444	LOAD_FAST         'line'
447	LOAD_CONST        -2
450	SLICE+2           None
451	STORE_FAST        'line'
454	JUMP_FORWARD      '486'

457	LOAD_FAST         'line'
460	LOAD_CONST        -1
463	SLICE+1           None
464	LOAD_CONST        '\n'
467	COMPARE_OP        '=='
470	POP_JUMP_IF_FALSE '486'

473	LOAD_FAST         'line'
476	LOAD_CONST        -1
479	SLICE+2           None
480	STORE_FAST        'line'
483	JUMP_FORWARD      '486'
486_0	COME_FROM         '454'
486_1	COME_FROM         '483'

486	LOAD_FAST         'line'
489	LOAD_FAST         'lines'
492	LOAD_CONST        -1
495	STORE_SUBSCR      None

496	LOAD_CONST        ''
499	LOAD_ATTR         'join'
502	LOAD_FAST         'lines'
505	CALL_FUNCTION_1   None
508	STORE_FAST        'data'
511	JUMP_ABSOLUTE     '517'
514	JUMP_FORWARD      '517'
517_0	COME_FROM         '514'

517	LOAD_FAST         'headers'
520	LOAD_CONST        'content-disposition'
523	BINARY_SUBSCR     None
524	STORE_FAST        'line'

527	LOAD_FAST         'line'
530	POP_JUMP_IF_TRUE  '539'

533	CONTINUE          '101'
536	JUMP_FORWARD      '539'
539_0	COME_FROM         '536'

539	LOAD_GLOBAL       'parse_header'
542	LOAD_FAST         'line'
545	CALL_FUNCTION_1   None
548	UNPACK_SEQUENCE_2 None
551	STORE_FAST        'key'
554	STORE_FAST        'params'

557	LOAD_FAST         'key'
560	LOAD_CONST        'form-data'
563	COMPARE_OP        '!='
566	POP_JUMP_IF_FALSE '575'

569	CONTINUE          '101'
572	JUMP_FORWARD      '575'
575_0	COME_FROM         '572'

575	LOAD_CONST        'name'
578	LOAD_FAST         'params'
581	COMPARE_OP        'in'
584	POP_JUMP_IF_FALSE '101'

587	LOAD_FAST         'params'
590	LOAD_CONST        'name'
593	BINARY_SUBSCR     None
594	STORE_FAST        'name'
597	JUMP_FORWARD      '603'

600	CONTINUE          '101'
603_0	COME_FROM         '597'

603	LOAD_FAST         'name'
606	LOAD_FAST         'partdict'
609	COMPARE_OP        'in'
612	POP_JUMP_IF_FALSE '635'

615	LOAD_FAST         'partdict'
618	LOAD_FAST         'name'
621	BINARY_SUBSCR     None
622	LOAD_ATTR         'append'
625	LOAD_FAST         'data'
628	CALL_FUNCTION_1   None
631	POP_TOP           None
632	JUMP_BACK         '101'

635	LOAD_FAST         'data'
638	BUILD_LIST_1      None
641	LOAD_FAST         'partdict'
644	LOAD_FAST         'name'
647	STORE_SUBSCR      None
648	JUMP_BACK         '101'
651	POP_BLOCK         None
652_0	COME_FROM         '98'

652	LOAD_FAST         'partdict'
655	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 381


def _parseparam(s):
    while s[:1] == ';':
        s = s[1:]
        end = s.find(';')
        while end > 0 and (s.count('"', 0, end) - s.count('\\"', 0, end)) % 2:
            end = s.find(';', end + 1)

        if end < 0:
            end = len(s)
        f = s[:end]
        yield f.strip()
        s = s[end:]


def parse_header(line):
    """Parse a Content-type like header.
    
    Return the main content-type and a dictionary of options.
    
    """
    parts = _parseparam(';' + line)
    key = parts.next()
    pdict = {}
    for p in parts:
        i = p.find('=')
        if i >= 0:
            name = p[:i].strip().lower()
            value = p[i + 1:].strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
                value = value.replace('\\\\', '\\').replace('\\"', '"')
            pdict[name] = value

    return (key, pdict)


class MiniFieldStorage():
    """Like FieldStorage, for use when no file uploads are possible."""
    filename = None
    list = None
    type = None
    file = None
    type_options = {}
    disposition = None
    disposition_options = {}
    headers = {}

    def __init__(self, name, value):
        """Constructor from field name and value."""
        self.name = name
        self.value = value

    def __repr__(self):
        """Return printable representation."""
        return 'MiniFieldStorage(%r, %r)' % (self.name, self.value)


class FieldStorage():
    """Store a sequence of fields, reading multipart/form-data.
    
    This class provides naming, typing, files stored on disk, and
    more.  At the top level, it is accessible like a dictionary, whose
    keys are the field names.  (Note: None can occur as a field name.)
    The items are either a Python list (if there's multiple values) or
    another FieldStorage or MiniFieldStorage object.  If it's a single
    object, it has the following attributes:
    
    name: the field name, if specified; otherwise None
    
    filename: the filename, if specified; otherwise None; this is the
        client side filename, *not* the file name on which it is
        stored (that's a temporary file you don't deal with)
    
    value: the value as a *string*; for file uploads, this
        transparently reads the file every time you request the value
    
    file: the file(-like) object from which you can read the data;
        None if the data is stored a simple string
    
    type: the content-type, or None if not specified
    
    type_options: dictionary of options specified on the content-type
        line
    
    disposition: content-disposition, or None if not specified
    
    disposition_options: dictionary of corresponding options
    
    headers: a dictionary(-like) object (sometimes rfc822.Message or a
        subclass thereof) containing *all* headers
    
    The class is subclassable, mostly for the purpose of overriding
    the make_file() method, which is called internally to come up with
    a file open for reading and writing.  This makes it possible to
    override the default choice of storing all files in a temporary
    directory and unlinking them as soon as they have been opened.
    
    """

    def __init__(self, fp = None, headers = None, outerboundary = '', environ = os.environ, keep_blank_values = 0, strict_parsing = 0):
        """Constructor.  Read multipart/* until last part.
        
        Arguments, all optional:
        
        fp              : file pointer; default: sys.stdin
            (not used when the request method is GET)
        
        headers         : header dictionary-like object; default:
            taken from environ as per CGI spec
        
        outerboundary   : terminating multipart boundary
            (for internal use only)
        
        environ         : environment dictionary; default: os.environ
        
        keep_blank_values: flag indicating whether blank values in
            percent-encoded forms should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.
        
        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.
        
        """
        method = 'GET'
        self.keep_blank_values = keep_blank_values
        self.strict_parsing = strict_parsing
        if 'REQUEST_METHOD' in environ:
            method = environ['REQUEST_METHOD'].upper()
        self.qs_on_post = None
        if method == 'GET' or method == 'HEAD':
            if 'QUERY_STRING' in environ:
                qs = environ['QUERY_STRING']
            elif sys.argv[1:]:
                qs = sys.argv[1]
            else:
                qs = ''
            fp = StringIO(qs)
            if headers is None:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
        if headers is None:
            headers = {}
            if method == 'POST':
                headers['content-type'] = 'application/x-www-form-urlencoded'
            if 'CONTENT_TYPE' in environ:
                headers['content-type'] = environ['CONTENT_TYPE']
            if 'QUERY_STRING' in environ:
                self.qs_on_post = environ['QUERY_STRING']
            if 'CONTENT_LENGTH' in environ:
                headers['content-length'] = environ['CONTENT_LENGTH']
        self.fp = fp or sys.stdin
        self.headers = headers
        self.outerboundary = outerboundary
        cdisp, pdict = '', {}
        if 'content-disposition' in self.headers:
            cdisp, pdict = parse_header(self.headers['content-disposition'])
        self.disposition = cdisp
        self.disposition_options = pdict
        self.name = None
        if 'name' in pdict:
            self.name = pdict['name']
        self.filename = None
        if 'filename' in pdict:
            self.filename = pdict['filename']
        if 'content-type' in self.headers:
            ctype, pdict = parse_header(self.headers['content-type'])
        elif self.outerboundary or method != 'POST':
            ctype, pdict = 'text/plain', {}
        else:
            ctype, pdict = 'application/x-www-form-urlencoded', {}
        self.type = ctype
        self.type_options = pdict
        self.innerboundary = ''
        if 'boundary' in pdict:
            self.innerboundary = pdict['boundary']
        clen = -1
        if 'content-length' in self.headers:
            try:
                clen = int(self.headers['content-length'])
            except ValueError:
                pass

            if maxlen and clen > maxlen:
                raise ValueError, 'Maximum content length exceeded'
        self.length = clen
        self.list = self.file = None
        self.done = 0
        if ctype == 'application/x-www-form-urlencoded':
            self.read_urlencoded()
        elif ctype[:10] == 'multipart/':
            self.read_multi(environ, keep_blank_values, strict_parsing)
        else:
            self.read_single()
        return

    def __repr__(self):
        """Return a printable representation."""
        return 'FieldStorage(%r, %r, %r)' % (self.name, self.filename, self.value)

    def __iter__(self):
        return iter(self.keys())

    def __getattr__(self, name):
        if name != 'value':
            raise AttributeError, name
        if self.file:
            self.file.seek(0)
            value = self.file.read()
            self.file.seek(0)
        elif self.list is not None:
            value = self.list
        else:
            value = None
        return value

    def __getitem__(self, key):
        """Dictionary style indexing."""
        if self.list is None:
            raise TypeError, 'not indexable'
        found = []
        for item in self.list:
            if item.name == key:
                found.append(item)

        if not found:
            raise KeyError, key
        if len(found) == 1:
            return found[0]
        else:
            return found
            return

    def getvalue(self, key, default = None):
        """Dictionary style get() method, including 'value' lookup."""
        if key in self:
            value = self[key]
            if type(value) is type([]):
                return map(attrgetter('value'), value)
            else:
                return value.value
        else:
            return default

    def getfirst(self, key, default = None):
        """ Return the first value received."""
        if key in self:
            value = self[key]
            if type(value) is type([]):
                return value[0].value
            else:
                return value.value
        else:
            return default

    def getlist(self, key):
        """ Return list of received values."""
        if key in self:
            value = self[key]
            if type(value) is type([]):
                return map(attrgetter('value'), value)
            else:
                return [value.value]
        else:
            return []

    def keys(self):
        """Dictionary style keys() method."""
        if self.list is None:
            raise TypeError, 'not indexable'
        return list(set((item.name for item in self.list)))

    def has_key(self, key):
        """Dictionary style has_key() method."""
        if self.list is None:
            raise TypeError, 'not indexable'
        return any((item.name == key for item in self.list))

    def __contains__(self, key):
        """Dictionary style __contains__ method."""
        if self.list is None:
            raise TypeError, 'not indexable'
        return any((item.name == key for item in self.list))

    def __len__(self):
        """Dictionary style len(x) support."""
        return len(self.keys())

    def __nonzero__(self):
        return bool(self.list)

    def read_urlencoded(self):
        """Internal: read data in query string format."""
        qs = self.fp.read(self.length)
        if self.qs_on_post:
            qs += '&' + self.qs_on_post
        self.list = list = []
        for key, value in urlparse.parse_qsl(qs, self.keep_blank_values, self.strict_parsing):
            list.append(MiniFieldStorage(key, value))

        self.skip_lines()

    FieldStorageClass = None

    def read_multi(self, environ, keep_blank_values, strict_parsing):
        """Internal: read a part that is itself multipart."""
        ib = self.innerboundary
        if not valid_boundary(ib):
            raise ValueError, 'Invalid boundary in multipart form: %r' % (ib,)
        self.list = []
        if self.qs_on_post:
            for key, value in urlparse.parse_qsl(self.qs_on_post, self.keep_blank_values, self.strict_parsing):
                self.list.append(MiniFieldStorage(key, value))

            FieldStorageClass = None
        klass = self.FieldStorageClass or self.__class__
        part = klass(self.fp, {}, ib, environ, keep_blank_values, strict_parsing)
        while not part.done:
            headers = rfc822.Message(self.fp)
            part = klass(self.fp, headers, ib, environ, keep_blank_values, strict_parsing)
            self.list.append(part)

        self.skip_lines()
        return

    def read_single(self):
        """Internal: read an atomic part."""
        if self.length >= 0:
            self.read_binary()
            self.skip_lines()
        else:
            self.read_lines()
        self.file.seek(0)

    bufsize = 8192

    def read_binary(self):
        """Internal: read binary data."""
        self.file = self.make_file('b')
        todo = self.length
        if todo >= 0:
            while todo > 0:
                data = self.fp.read(min(todo, self.bufsize))
                if not data:
                    self.done = -1
                    break
                self.file.write(data)
                todo = todo - len(data)

    def read_lines(self):
        """Internal: read lines until EOF or outerboundary."""
        self.file = self.__file = StringIO()
        if self.outerboundary:
            self.read_lines_to_outerboundary()
        else:
            self.read_lines_to_eof()

    def __write(self, line):
        if self.__file is not None:
            if self.__file.tell() + len(line) > 1000:
                self.file = self.make_file('')
                self.file.write(self.__file.getvalue())
                self.__file = None
        self.file.write(line)
        return

    def read_lines_to_eof--- This code section failed: ---

0	SETUP_LOOP        '57'

3	LOAD_FAST         'self'
6	LOAD_ATTR         'fp'
9	LOAD_ATTR         'readline'
12	LOAD_CONST        65536
15	CALL_FUNCTION_1   None
18	STORE_FAST        'line'

21	LOAD_FAST         'line'
24	POP_JUMP_IF_TRUE  '40'

27	LOAD_CONST        -1
30	LOAD_FAST         'self'
33	STORE_ATTR        'done'

36	BREAK_LOOP        None
37	JUMP_FORWARD      '40'
40_0	COME_FROM         '37'

40	LOAD_FAST         'self'
43	LOAD_ATTR         '__write'
46	LOAD_FAST         'line'
49	CALL_FUNCTION_1   None
52	POP_TOP           None
53	JUMP_BACK         '3'
56	POP_BLOCK         None
57_0	COME_FROM         '0'

Syntax error at or near `POP_BLOCK' token at offset 56

    def read_lines_to_outerboundary--- This code section failed: ---

0	LOAD_CONST        '--'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'outerboundary'
9	BINARY_ADD        None
10	STORE_FAST        'next'

13	LOAD_FAST         'next'
16	LOAD_CONST        '--'
19	BINARY_ADD        None
20	STORE_FAST        'last'

23	LOAD_CONST        ''
26	STORE_FAST        'delim'

29	LOAD_GLOBAL       'True'
32	STORE_FAST        'last_line_lfend'

35	SETUP_LOOP        '274'

38	LOAD_FAST         'self'
41	LOAD_ATTR         'fp'
44	LOAD_ATTR         'readline'
47	LOAD_CONST        65536
50	CALL_FUNCTION_1   None
53	STORE_FAST        'line'

56	LOAD_FAST         'line'
59	POP_JUMP_IF_TRUE  '75'

62	LOAD_CONST        -1
65	LOAD_FAST         'self'
68	STORE_ATTR        'done'

71	BREAK_LOOP        None
72	JUMP_FORWARD      '75'
75_0	COME_FROM         '72'

75	LOAD_FAST         'line'
78	LOAD_CONST        2
81	SLICE+2           None
82	LOAD_CONST        '--'
85	COMPARE_OP        '=='
88	POP_JUMP_IF_FALSE '153'
91	LOAD_FAST         'last_line_lfend'
94_0	COME_FROM         '88'
94	POP_JUMP_IF_FALSE '153'

97	LOAD_FAST         'line'
100	LOAD_ATTR         'strip'
103	CALL_FUNCTION_0   None
106	STORE_FAST        'strippedline'

109	LOAD_FAST         'strippedline'
112	LOAD_FAST         'next'
115	COMPARE_OP        '=='
118	POP_JUMP_IF_FALSE '125'

121	BREAK_LOOP        None
122	JUMP_FORWARD      '125'
125_0	COME_FROM         '122'

125	LOAD_FAST         'strippedline'
128	LOAD_FAST         'last'
131	COMPARE_OP        '=='
134	POP_JUMP_IF_FALSE '153'

137	LOAD_CONST        1
140	LOAD_FAST         'self'
143	STORE_ATTR        'done'

146	BREAK_LOOP        None
147	JUMP_ABSOLUTE     '153'
150	JUMP_FORWARD      '153'
153_0	COME_FROM         '150'

153	LOAD_FAST         'delim'
156	STORE_FAST        'odelim'

159	LOAD_FAST         'line'
162	LOAD_CONST        -2
165	SLICE+1           None
166	LOAD_CONST        '\r\n'
169	COMPARE_OP        '=='
172	POP_JUMP_IF_FALSE '200'

175	LOAD_CONST        '\r\n'
178	STORE_FAST        'delim'

181	LOAD_FAST         'line'
184	LOAD_CONST        -2
187	SLICE+2           None
188	STORE_FAST        'line'

191	LOAD_GLOBAL       'True'
194	STORE_FAST        'last_line_lfend'
197	JUMP_FORWARD      '253'

200	LOAD_FAST         'line'
203	LOAD_CONST        -1
206	BINARY_SUBSCR     None
207	LOAD_CONST        '\n'
210	COMPARE_OP        '=='
213	POP_JUMP_IF_FALSE '241'

216	LOAD_CONST        '\n'
219	STORE_FAST        'delim'

222	LOAD_FAST         'line'
225	LOAD_CONST        -1
228	SLICE+2           None
229	STORE_FAST        'line'

232	LOAD_GLOBAL       'True'
235	STORE_FAST        'last_line_lfend'
238	JUMP_FORWARD      '253'

241	LOAD_CONST        ''
244	STORE_FAST        'delim'

247	LOAD_GLOBAL       'False'
250	STORE_FAST        'last_line_lfend'
253_0	COME_FROM         '197'
253_1	COME_FROM         '238'

253	LOAD_FAST         'self'
256	LOAD_ATTR         '__write'
259	LOAD_FAST         'odelim'
262	LOAD_FAST         'line'
265	BINARY_ADD        None
266	CALL_FUNCTION_1   None
269	POP_TOP           None
270	JUMP_BACK         '38'
273	POP_BLOCK         None
274_0	COME_FROM         '35'

Syntax error at or near `POP_BLOCK' token at offset 273

    def skip_lines--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'outerboundary'
6	UNARY_NOT         None
7	POP_JUMP_IF_TRUE  '19'
10	LOAD_FAST         'self'
13	LOAD_ATTR         'done'
16_0	COME_FROM         '7'
16	POP_JUMP_IF_FALSE '23'

19	LOAD_CONST        None
22	RETURN_END_IF     None

23	LOAD_CONST        '--'
26	LOAD_FAST         'self'
29	LOAD_ATTR         'outerboundary'
32	BINARY_ADD        None
33	STORE_FAST        'next'

36	LOAD_FAST         'next'
39	LOAD_CONST        '--'
42	BINARY_ADD        None
43	STORE_FAST        'last'

46	LOAD_GLOBAL       'True'
49	STORE_FAST        'last_line_lfend'

52	SETUP_LOOP        '189'

55	LOAD_FAST         'self'
58	LOAD_ATTR         'fp'
61	LOAD_ATTR         'readline'
64	LOAD_CONST        65536
67	CALL_FUNCTION_1   None
70	STORE_FAST        'line'

73	LOAD_FAST         'line'
76	POP_JUMP_IF_TRUE  '92'

79	LOAD_CONST        -1
82	LOAD_FAST         'self'
85	STORE_ATTR        'done'

88	BREAK_LOOP        None
89	JUMP_FORWARD      '92'
92_0	COME_FROM         '89'

92	LOAD_FAST         'line'
95	LOAD_CONST        2
98	SLICE+2           None
99	LOAD_CONST        '--'
102	COMPARE_OP        '=='
105	POP_JUMP_IF_FALSE '170'
108	LOAD_FAST         'last_line_lfend'
111_0	COME_FROM         '105'
111	POP_JUMP_IF_FALSE '170'

114	LOAD_FAST         'line'
117	LOAD_ATTR         'strip'
120	CALL_FUNCTION_0   None
123	STORE_FAST        'strippedline'

126	LOAD_FAST         'strippedline'
129	LOAD_FAST         'next'
132	COMPARE_OP        '=='
135	POP_JUMP_IF_FALSE '142'

138	BREAK_LOOP        None
139	JUMP_FORWARD      '142'
142_0	COME_FROM         '139'

142	LOAD_FAST         'strippedline'
145	LOAD_FAST         'last'
148	COMPARE_OP        '=='
151	POP_JUMP_IF_FALSE '170'

154	LOAD_CONST        1
157	LOAD_FAST         'self'
160	STORE_ATTR        'done'

163	BREAK_LOOP        None
164	JUMP_ABSOLUTE     '170'
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	LOAD_FAST         'line'
173	LOAD_ATTR         'endswith'
176	LOAD_CONST        '\n'
179	CALL_FUNCTION_1   None
182	STORE_FAST        'last_line_lfend'
185	JUMP_BACK         '55'
188	POP_BLOCK         None
189_0	COME_FROM         '52'

Syntax error at or near `POP_BLOCK' token at offset 188

    def make_file(self, binary = None):
        """Overridable: return a readable & writable file.
        
        The file will be used as follows:
        - data is written to it
        - seek(0)
        - data is read from it
        
        The 'binary' argument is unused -- the file is always opened
        in binary mode.
        
        This version opens a temporary file for reading and writing,
        and immediately deletes (unlinks) it.  The trick (on Unix!) is
        that the file can still be used, but it can't be opened by
        another process, and it will automatically be deleted when it
        is closed or when the current process terminates.
        
        If you want a more permanent file, you derive a class which
        overrides this method.  If you want a visible temporary file
        that is nevertheless automatically deleted when the script
        terminates, try defining a __del__ method in a derived class
        which unlinks the temporary files you have created.
        
        """
        import tempfile
        return tempfile.TemporaryFile('w+b')


class FormContentDict(UserDict.UserDict):
    """Form content as dictionary with a list of values per field.
    
    form = FormContentDict()
    
    form[key] -> [value, value, ...]
    key in form -> Boolean
    form.keys() -> [key, key, ...]
    form.values() -> [[val, val, ...], [val, val, ...], ...]
    form.items() ->  [(key, [val, val, ...]), (key, [val, val, ...]), ...]
    form.dict == {key: [val, val, ...], ...}
    
    """

    def __init__(self, environ = os.environ, keep_blank_values = 0, strict_parsing = 0):
        self.dict = self.data = parse(environ=environ, keep_blank_values=keep_blank_values, strict_parsing=strict_parsing)
        self.query_string = environ['QUERY_STRING']


class SvFormContentDict(FormContentDict):
    """Form content as dictionary expecting a single value per field.
    
    If you only expect a single value for each field, then form[key]
    will return that single value.  It will raise an IndexError if
    that expectation is not true.  If you expect a field to have
    possible multiple values, than you can use form.getlist(key) to
    get all of the values.  values() and items() are a compromise:
    they return single strings where there is a single value, and
    lists of strings otherwise.
    
    """

    def __getitem__(self, key):
        if len(self.dict[key]) > 1:
            raise IndexError, 'expecting a single value'
        return self.dict[key][0]

    def getlist(self, key):
        return self.dict[key]

    def values(self):
        result = []
        for value in self.dict.values():
            if len(value) == 1:
                result.append(value[0])
            else:
                result.append(value)

        return result

    def items(self):
        result = []
        for key, value in self.dict.items():
            if len(value) == 1:
                result.append((key, value[0]))
            else:
                result.append((key, value))

        return result


class InterpFormContentDict(SvFormContentDict):
    """This class is present for backwards compatibility only."""

    def __getitem__(self, key):
        v = SvFormContentDict.__getitem__(self, key)
        if v[0] in '0123456789+-.':
            try:
                return int(v)
            except ValueError:
                try:
                    return float(v)
                except ValueError:
                    pass

        return v.strip()

    def values(self):
        result = []
        for key in self.keys():
            try:
                result.append(self[key])
            except IndexError:
                result.append(self.dict[key])

        return result

    def items(self):
        result = []
        for key in self.keys():
            try:
                result.append((key, self[key]))
            except IndexError:
                result.append((key, self.dict[key]))

        return result


class FormContent(FormContentDict):
    """This class is present for backwards compatibility only."""

    def values(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return None
            return None

    def indexed_value(self, key, location):
        if key in self.dict:
            if len(self.dict[key]) > location:
                return self.dict[key][location]
            else:
                return None
        else:
            return None
        return None

    def value(self, key):
        if key in self.dict:
            return self.dict[key][0]
        else:
            return None
            return None

    def length(self, key):
        return len(self.dict[key])

    def stripped(self, key):
        if key in self.dict:
            return self.dict[key][0].strip()
        else:
            return None
            return None

    def pars(self):
        return self.dict


def test(environ = os.environ):
    """Robust test CGI script, usable as main program.
    
    Write minimal HTTP headers and dump all information provided to
    the script in HTML form.
    
    """
    global maxlen
    print 'Content-type: text/html'
    print
    sys.stderr = sys.stdout
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
        print_environ_usage()

        def f():
            exec 'testing print_exception() -- <I>italics?</I>'

        def g(f = f):
            f()

        print '<H3>What follows is a test, not an actual exception:</H3>'
        g()
    except:
        print_exception()

    print '<H1>Second try with a small maxlen...</H1>'
    maxlen = 50
    try:
        form = FieldStorage()
        print_directory()
        print_arguments()
        print_form(form)
        print_environ(environ)
    except:
        print_exception()


def print_exception(type = None, value = None, tb = None, limit = None):
    if type is None:
        type, value, tb = sys.exc_info()
    import traceback
    print
    print '<H3>Traceback (most recent call last):</H3>'
    list = traceback.format_tb(tb, limit) + traceback.format_exception_only(type, value)
    print '<PRE>%s<B>%s</B></PRE>' % (escape(''.join(list[:-1])), escape(list[-1]))
    del tb
    return


def print_environ(environ = os.environ):
    """Dump the shell environment as HTML."""
    keys = environ.keys()
    keys.sort()
    print
    print '<H3>Shell Environment:</H3>'
    print '<DL>'
    for key in keys:
        print '<DT>', escape(key), '<DD>', escape(environ[key])

    print '</DL>'
    print


def print_form(form):
    """Dump the contents of a form as HTML."""
    keys = form.keys()
    keys.sort()
    print
    print '<H3>Form Contents:</H3>'
    if not keys:
        print '<P>No form fields.'
    print '<DL>'
    for key in keys:
        print '<DT>' + escape(key) + ':',
        value = form[key]
        print '<i>' + escape(repr(type(value))) + '</i>'
        print '<DD>' + escape(repr(value))

    print '</DL>'
    print


def print_directory():
    """Dump the current directory as HTML."""
    print
    print '<H3>Current Working Directory:</H3>'
    try:
        pwd = os.getcwd()
    except os.error as msg:
        print 'os.error:', escape(str(msg))
    else:
        print escape(pwd)

    print


def print_arguments():
    print
    print '<H3>Command Line Arguments:</H3>'
    print
    print sys.argv
    print


def print_environ_usage():
    """Dump a list of environment variables used by CGI as HTML."""
    print '\n<H3>These environment variables could have been set:</H3>\n<UL>\n<LI>AUTH_TYPE\n<LI>CONTENT_LENGTH\n<LI>CONTENT_TYPE\n<LI>DATE_GMT\n<LI>DATE_LOCAL\n<LI>DOCUMENT_NAME\n<LI>DOCUMENT_ROOT\n<LI>DOCUMENT_URI\n<LI>GATEWAY_INTERFACE\n<LI>LAST_MODIFIED\n<LI>PATH\n<LI>PATH_INFO\n<LI>PATH_TRANSLATED\n<LI>QUERY_STRING\n<LI>REMOTE_ADDR\n<LI>REMOTE_HOST\n<LI>REMOTE_IDENT\n<LI>REMOTE_USER\n<LI>REQUEST_METHOD\n<LI>SCRIPT_NAME\n<LI>SERVER_NAME\n<LI>SERVER_PORT\n<LI>SERVER_PROTOCOL\n<LI>SERVER_ROOT\n<LI>SERVER_SOFTWARE\n</UL>\nIn addition, HTTP headers sent by the server may be passed in the\nenvironment as well.  Here are some common variable names:\n<UL>\n<LI>HTTP_ACCEPT\n<LI>HTTP_CONNECTION\n<LI>HTTP_HOST\n<LI>HTTP_PRAGMA\n<LI>HTTP_REFERER\n<LI>HTTP_USER_AGENT\n</UL>\n'


def escape(s, quote = None):
    """Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true, the quotation mark character (")
    is also translated."""
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    if quote:
        s = s.replace('"', '&quot;')
    return s


def valid_boundary(s, _vb_pattern = '^[ -~]{0,200}[!-~]$'):
    import re
    return re.match(_vb_pattern, s)


if __name__ == '__main__':
    test()