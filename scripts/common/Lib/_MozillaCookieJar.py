# Embedded file name: scripts/common/Lib/_MozillaCookieJar.py
"""Mozilla / Netscape cookie loading / saving."""
import re, time
from cookielib import _warn_unhandled_exception, FileCookieJar, LoadError, Cookie, MISSING_FILENAME_TEXT

class MozillaCookieJar(FileCookieJar):
    """
    
    WARNING: you may want to backup your browser's cookies file if you use
    this class to save cookies.  I *think* it works, but there have been
    bugs in the past!
    
    This class differs from CookieJar only in the format it uses to save and
    load cookies to and from a file.  This class uses the Mozilla/Netscape
    `cookies.txt' format.  lynx uses this file format, too.
    
    Don't expect cookies saved while the browser is running to be noticed by
    the browser (in fact, Mozilla on unix will overwrite your saved cookies if
    you change them on disk while it's running; on Windows, you probably can't
    save at all while the browser is running).
    
    Note that the Mozilla/Netscape format will downgrade RFC2965 cookies to
    Netscape cookies on saving.
    
    In particular, the cookie version and port number information is lost,
    together with information about whether or not Path, Port and Discard were
    specified by the Set-Cookie2 (or Set-Cookie) header, and whether or not the
    domain as set in the HTTP header started with a dot (yes, I'm aware some
    domains in Netscape files start with a dot and some don't -- trust me, you
    really don't want to know any more about this).
    
    Note that though Mozilla and Netscape use the same format, they use
    slightly different headers.  The class saves cookies using the Netscape
    header by default (Mozilla can cope with that).
    
    """
    magic_re = '#( Netscape)? HTTP Cookie File'
    header = '# Netscape HTTP Cookie File\n# http://www.netscape.com/newsref/std/cookie_spec.html\n# This is a generated file!  Do not edit.\n\n'

    def _really_load--- This code section failed: ---

0	LOAD_GLOBAL       'time'
3	LOAD_ATTR         'time'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'now'

12	LOAD_FAST         'f'
15	LOAD_ATTR         'readline'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'magic'

24	LOAD_GLOBAL       're'
27	LOAD_ATTR         'search'
30	LOAD_FAST         'self'
33	LOAD_ATTR         'magic_re'
36	LOAD_FAST         'magic'
39	CALL_FUNCTION_2   None
42	POP_JUMP_IF_TRUE  '74'

45	LOAD_FAST         'f'
48	LOAD_ATTR         'close'
51	CALL_FUNCTION_0   None
54	POP_TOP           None

55	LOAD_GLOBAL       'LoadError'

58	LOAD_CONST        '%r does not look like a Netscape format cookies file'

61	LOAD_FAST         'filename'
64	BINARY_MODULO     None
65	CALL_FUNCTION_1   None
68	RAISE_VARARGS_1   None
71	JUMP_FORWARD      '74'
74_0	COME_FROM         '71'

74	SETUP_EXCEPT      '462'

77	SETUP_LOOP        '458'

80	LOAD_FAST         'f'
83	LOAD_ATTR         'readline'
86	CALL_FUNCTION_0   None
89	STORE_FAST        'line'

92	LOAD_FAST         'line'
95	LOAD_CONST        ''
98	COMPARE_OP        '=='
101	POP_JUMP_IF_FALSE '108'
104	BREAK_LOOP        None
105	JUMP_FORWARD      '108'
108_0	COME_FROM         '105'

108	LOAD_FAST         'line'
111	LOAD_ATTR         'endswith'
114	LOAD_CONST        '\n'
117	CALL_FUNCTION_1   None
120	POP_JUMP_IF_FALSE '136'
123	LOAD_FAST         'line'
126	LOAD_CONST        -1
129	SLICE+2           None
130	STORE_FAST        'line'
133	JUMP_FORWARD      '136'
136_0	COME_FROM         '133'

136	LOAD_FAST         'line'
139	LOAD_ATTR         'strip'
142	CALL_FUNCTION_0   None
145	LOAD_ATTR         'startswith'
148	LOAD_CONST        ('#', '$')
151	CALL_FUNCTION_1   None
154	POP_JUMP_IF_TRUE  '80'

157	LOAD_FAST         'line'
160	LOAD_ATTR         'strip'
163	CALL_FUNCTION_0   None
166	LOAD_CONST        ''
169	COMPARE_OP        '=='
172_0	COME_FROM         '154'
172	POP_JUMP_IF_FALSE '181'

175	CONTINUE          '80'
178	JUMP_FORWARD      '181'
181_0	COME_FROM         '178'

181	LOAD_FAST         'line'
184	LOAD_ATTR         'split'
187	LOAD_CONST        '\t'
190	CALL_FUNCTION_1   None
193	UNPACK_SEQUENCE_7 None
196	STORE_FAST        'domain'
199	STORE_FAST        'domain_specified'
202	STORE_FAST        'path'
205	STORE_FAST        'secure'
208	STORE_FAST        'expires'
211	STORE_FAST        'name'
214	STORE_FAST        'value'

217	LOAD_FAST         'secure'
220	LOAD_CONST        'TRUE'
223	COMPARE_OP        '=='
226	STORE_FAST        'secure'

229	LOAD_FAST         'domain_specified'
232	LOAD_CONST        'TRUE'
235	COMPARE_OP        '=='
238	STORE_FAST        'domain_specified'

241	LOAD_FAST         'name'
244	LOAD_CONST        ''
247	COMPARE_OP        '=='
250	POP_JUMP_IF_FALSE '268'

253	LOAD_FAST         'value'
256	STORE_FAST        'name'

259	LOAD_CONST        None
262	STORE_FAST        'value'
265	JUMP_FORWARD      '268'
268_0	COME_FROM         '265'

268	LOAD_FAST         'domain'
271	LOAD_ATTR         'startswith'
274	LOAD_CONST        '.'
277	CALL_FUNCTION_1   None
280	STORE_FAST        'initial_dot'

283	LOAD_FAST         'domain_specified'
286	LOAD_FAST         'initial_dot'
289	COMPARE_OP        '=='
292	POP_JUMP_IF_TRUE  '301'
295	LOAD_ASSERT       'AssertionError'
298	RAISE_VARARGS_1   None

301	LOAD_GLOBAL       'False'
304	STORE_FAST        'discard'

307	LOAD_FAST         'expires'
310	LOAD_CONST        ''
313	COMPARE_OP        '=='
316	POP_JUMP_IF_FALSE '334'

319	LOAD_CONST        None
322	STORE_FAST        'expires'

325	LOAD_GLOBAL       'True'
328	STORE_FAST        'discard'
331	JUMP_FORWARD      '334'
334_0	COME_FROM         '331'

334	LOAD_GLOBAL       'Cookie'
337	LOAD_CONST        0
340	LOAD_FAST         'name'
343	LOAD_FAST         'value'

346	LOAD_CONST        None
349	LOAD_GLOBAL       'False'

352	LOAD_FAST         'domain'
355	LOAD_FAST         'domain_specified'
358	LOAD_FAST         'initial_dot'

361	LOAD_FAST         'path'
364	LOAD_GLOBAL       'False'

367	LOAD_FAST         'secure'

370	LOAD_FAST         'expires'

373	LOAD_FAST         'discard'

376	LOAD_CONST        None

379	LOAD_CONST        None

382	BUILD_MAP         None
385	CALL_FUNCTION_16  None
388	STORE_FAST        'c'

391	LOAD_FAST         'ignore_discard'
394	UNARY_NOT         None
395	POP_JUMP_IF_FALSE '413'
398	LOAD_FAST         'c'
401	LOAD_ATTR         'discard'
404_0	COME_FROM         '395'
404	POP_JUMP_IF_FALSE '413'

407	CONTINUE          '80'
410	JUMP_FORWARD      '413'
413_0	COME_FROM         '410'

413	LOAD_FAST         'ignore_expires'
416	UNARY_NOT         None
417	POP_JUMP_IF_FALSE '441'
420	LOAD_FAST         'c'
423	LOAD_ATTR         'is_expired'
426	LOAD_FAST         'now'
429	CALL_FUNCTION_1   None
432_0	COME_FROM         '417'
432	POP_JUMP_IF_FALSE '441'

435	CONTINUE          '80'
438	JUMP_FORWARD      '441'
441_0	COME_FROM         '438'

441	LOAD_FAST         'self'
444	LOAD_ATTR         'set_cookie'
447	LOAD_FAST         'c'
450	CALL_FUNCTION_1   None
453	POP_TOP           None
454	JUMP_BACK         '80'
457	POP_BLOCK         None
458_0	COME_FROM         '77'
458	POP_BLOCK         None
459	JUMP_FORWARD      '527'
462_0	COME_FROM         '74'

462	DUP_TOP           None
463	LOAD_GLOBAL       'IOError'
466	COMPARE_OP        'exception match'
469	POP_JUMP_IF_FALSE '481'
472	POP_TOP           None
473	POP_TOP           None
474	POP_TOP           None

475	RAISE_VARARGS_0   None
478	JUMP_FORWARD      '527'

481	DUP_TOP           None
482	LOAD_GLOBAL       'Exception'
485	COMPARE_OP        'exception match'
488	POP_JUMP_IF_FALSE '526'
491	POP_TOP           None
492	POP_TOP           None
493	POP_TOP           None

494	LOAD_GLOBAL       '_warn_unhandled_exception'
497	CALL_FUNCTION_0   None
500	POP_TOP           None

501	LOAD_GLOBAL       'LoadError'
504	LOAD_CONST        'invalid Netscape format cookies file %r: %r'

507	LOAD_FAST         'filename'
510	LOAD_FAST         'line'
513	BUILD_TUPLE_2     None
516	BINARY_MODULO     None
517	CALL_FUNCTION_1   None
520	RAISE_VARARGS_1   None
523	JUMP_FORWARD      '527'
526	END_FINALLY       None
527_0	COME_FROM         '459'
527_1	COME_FROM         '526'
527	LOAD_CONST        None
530	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 457

    def save(self, filename = None, ignore_discard = False, ignore_expires = False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        f = open(filename, 'w')
        try:
            f.write(self.header)
            now = time.time()
            for cookie in self:
                if not ignore_discard and cookie.discard:
                    continue
                if not ignore_expires and cookie.is_expired(now):
                    continue
                if cookie.secure:
                    secure = 'TRUE'
                else:
                    secure = 'FALSE'
                if cookie.domain.startswith('.'):
                    initial_dot = 'TRUE'
                else:
                    initial_dot = 'FALSE'
                if cookie.expires is not None:
                    expires = str(cookie.expires)
                else:
                    expires = ''
                if cookie.value is None:
                    name = ''
                    value = cookie.name
                else:
                    name = cookie.name
                    value = cookie.value
                f.write('\t'.join([cookie.domain,
                 initial_dot,
                 cookie.path,
                 secure,
                 expires,
                 name,
                 value]) + '\n')

        finally:
            f.close()

        return