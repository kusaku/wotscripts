# Embedded file name: scripts/common/Lib/netrc.py
"""An object-oriented interface to .netrc files."""
import os, shlex
__all__ = ['netrc', 'NetrcParseError']

class NetrcParseError(Exception):
    """Exception raised on syntax errors in the .netrc file."""

    def __init__(self, msg, filename = None, lineno = None):
        self.filename = filename
        self.lineno = lineno
        self.msg = msg
        Exception.__init__(self, msg)

    def __str__(self):
        return '%s (%s, line %s)' % (self.msg, self.filename, self.lineno)


class netrc:

    def __init__(self, file = None):
        if file is None:
            try:
                file = os.path.join(os.environ['HOME'], '.netrc')
            except KeyError:
                raise IOError('Could not find .netrc: $HOME is not set')

        self.hosts = {}
        self.macros = {}
        with open(file) as fp:
            self._parse(file, fp)
        return

    def _parse--- This code section failed: ---

0	LOAD_GLOBAL       'shlex'
3	LOAD_ATTR         'shlex'
6	LOAD_FAST         'fp'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'lexer'

15	LOAD_FAST         'lexer'
18	DUP_TOP           None
19	LOAD_ATTR         'wordchars'
22	LOAD_CONST        '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
25	INPLACE_ADD       None
26	ROT_TWO           None
27	STORE_ATTR        'wordchars'

30	LOAD_FAST         'lexer'
33	LOAD_ATTR         'commenters'
36	LOAD_ATTR         'replace'
39	LOAD_CONST        '#'
42	LOAD_CONST        ''
45	CALL_FUNCTION_2   None
48	LOAD_FAST         'lexer'
51	STORE_ATTR        'commenters'

54	SETUP_LOOP        '650'

57	LOAD_FAST         'lexer'
60	LOAD_ATTR         'get_token'
63	CALL_FUNCTION_0   None
66	DUP_TOP           None
67	STORE_FAST        'toplevel'
70	STORE_FAST        'tt'

73	LOAD_FAST         'tt'
76	POP_JUMP_IF_TRUE  '83'

79	BREAK_LOOP        None
80	JUMP_FORWARD      '353'

83	LOAD_FAST         'tt'
86	LOAD_CONST        0
89	BINARY_SUBSCR     None
90	LOAD_CONST        '#'
93	COMPARE_OP        '=='
96	POP_JUMP_IF_FALSE '154'

99	LOAD_GLOBAL       'len'
102	LOAD_FAST         'tt'
105	CALL_FUNCTION_1   None
108	LOAD_CONST        1
111	BINARY_ADD        None
112	STORE_FAST        'pos'

115	LOAD_FAST         'lexer'
118	LOAD_ATTR         'instream'
121	LOAD_ATTR         'seek'
124	LOAD_FAST         'pos'
127	UNARY_NEGATIVE    None
128	LOAD_CONST        1
131	CALL_FUNCTION_2   None
134	POP_TOP           None

135	LOAD_FAST         'lexer'
138	LOAD_ATTR         'instream'
141	LOAD_ATTR         'readline'
144	CALL_FUNCTION_0   None
147	POP_TOP           None

148	CONTINUE          '57'
151	JUMP_FORWARD      '353'

154	LOAD_FAST         'tt'
157	LOAD_CONST        'machine'
160	COMPARE_OP        '=='
163	POP_JUMP_IF_FALSE '181'

166	LOAD_FAST         'lexer'
169	LOAD_ATTR         'get_token'
172	CALL_FUNCTION_0   None
175	STORE_FAST        'entryname'
178	JUMP_FORWARD      '353'

181	LOAD_FAST         'tt'
184	LOAD_CONST        'default'
187	COMPARE_OP        '=='
190	POP_JUMP_IF_FALSE '202'

193	LOAD_CONST        'default'
196	STORE_FAST        'entryname'
199	JUMP_FORWARD      '353'

202	LOAD_FAST         'tt'
205	LOAD_CONST        'macdef'
208	COMPARE_OP        '=='
211	POP_JUMP_IF_FALSE '328'

214	LOAD_FAST         'lexer'
217	LOAD_ATTR         'get_token'
220	CALL_FUNCTION_0   None
223	STORE_FAST        'entryname'

226	BUILD_LIST_0      None
229	LOAD_FAST         'self'
232	LOAD_ATTR         'macros'
235	LOAD_FAST         'entryname'
238	STORE_SUBSCR      None

239	LOAD_CONST        ' \t'
242	LOAD_FAST         'lexer'
245	STORE_ATTR        'whitespace'

248	SETUP_LOOP        '322'

251	LOAD_FAST         'lexer'
254	LOAD_ATTR         'instream'
257	LOAD_ATTR         'readline'
260	CALL_FUNCTION_0   None
263	STORE_FAST        'line'

266	LOAD_FAST         'line'
269	UNARY_NOT         None
270	POP_JUMP_IF_TRUE  '285'
273	LOAD_FAST         'line'
276	LOAD_CONST        '\n'
279	COMPARE_OP        '=='
282_0	COME_FROM         '270'
282	POP_JUMP_IF_FALSE '298'

285	LOAD_CONST        ' \t\r\n'
288	LOAD_FAST         'lexer'
291	STORE_ATTR        'whitespace'

294	BREAK_LOOP        None
295	JUMP_FORWARD      '298'
298_0	COME_FROM         '295'

298	LOAD_FAST         'self'
301	LOAD_ATTR         'macros'
304	LOAD_FAST         'entryname'
307	BINARY_SUBSCR     None
308	LOAD_ATTR         'append'
311	LOAD_FAST         'line'
314	CALL_FUNCTION_1   None
317	POP_TOP           None
318	JUMP_BACK         '251'
321	POP_BLOCK         None
322_0	COME_FROM         '248'

322	CONTINUE          '57'
325	JUMP_FORWARD      '353'

328	LOAD_GLOBAL       'NetrcParseError'

331	LOAD_CONST        'bad toplevel token %r'
334	LOAD_FAST         'tt'
337	BINARY_MODULO     None
338	LOAD_FAST         'file'
341	LOAD_FAST         'lexer'
344	LOAD_ATTR         'lineno'
347	CALL_FUNCTION_3   None
350	RAISE_VARARGS_1   None
353_0	COME_FROM         '80'
353_1	COME_FROM         '151'
353_2	COME_FROM         '178'
353_3	COME_FROM         '199'
353_4	COME_FROM         '325'

353	LOAD_CONST        ''
356	STORE_FAST        'login'

359	LOAD_CONST        None
362	DUP_TOP           None
363	STORE_FAST        'account'
366	STORE_FAST        'password'

369	BUILD_MAP         None
372	LOAD_FAST         'self'
375	LOAD_ATTR         'hosts'
378	LOAD_FAST         'entryname'
381	STORE_SUBSCR      None

382	SETUP_LOOP        '646'

385	LOAD_FAST         'lexer'
388	LOAD_ATTR         'get_token'
391	CALL_FUNCTION_0   None
394	STORE_FAST        'tt'

397	LOAD_FAST         'tt'
400	LOAD_ATTR         'startswith'
403	LOAD_CONST        '#'
406	CALL_FUNCTION_1   None
409	POP_JUMP_IF_TRUE  '436'

412	LOAD_FAST         'tt'
415	LOAD_CONST        ''
418	LOAD_CONST        'machine'
421	LOAD_CONST        'default'
424	LOAD_CONST        'macdef'
427	BUILD_SET_4       None
430	COMPARE_OP        'in'
433_0	COME_FROM         '409'
433	POP_JUMP_IF_FALSE '524'

436	LOAD_FAST         'password'
439	POP_JUMP_IF_FALSE '481'

442	LOAD_FAST         'login'
445	LOAD_FAST         'account'
448	LOAD_FAST         'password'
451	BUILD_TUPLE_3     None
454	LOAD_FAST         'self'
457	LOAD_ATTR         'hosts'
460	LOAD_FAST         'entryname'
463	STORE_SUBSCR      None

464	LOAD_FAST         'lexer'
467	LOAD_ATTR         'push_token'
470	LOAD_FAST         'tt'
473	CALL_FUNCTION_1   None
476	POP_TOP           None

477	BREAK_LOOP        None
478	JUMP_ABSOLUTE     '642'

481	LOAD_GLOBAL       'NetrcParseError'

484	LOAD_CONST        'malformed %s entry %s terminated by %s'

487	LOAD_FAST         'toplevel'
490	LOAD_FAST         'entryname'
493	LOAD_GLOBAL       'repr'
496	LOAD_FAST         'tt'
499	CALL_FUNCTION_1   None
502	BUILD_TUPLE_3     None
505	BINARY_MODULO     None

506	LOAD_FAST         'file'
509	LOAD_FAST         'lexer'
512	LOAD_ATTR         'lineno'
515	CALL_FUNCTION_3   None
518	RAISE_VARARGS_1   None
521	JUMP_BACK         '385'

524	LOAD_FAST         'tt'
527	LOAD_CONST        'login'
530	COMPARE_OP        '=='
533	POP_JUMP_IF_TRUE  '548'
536	LOAD_FAST         'tt'
539	LOAD_CONST        'user'
542	COMPARE_OP        '=='
545_0	COME_FROM         '533'
545	POP_JUMP_IF_FALSE '563'

548	LOAD_FAST         'lexer'
551	LOAD_ATTR         'get_token'
554	CALL_FUNCTION_0   None
557	STORE_FAST        'login'
560	JUMP_BACK         '385'

563	LOAD_FAST         'tt'
566	LOAD_CONST        'account'
569	COMPARE_OP        '=='
572	POP_JUMP_IF_FALSE '590'

575	LOAD_FAST         'lexer'
578	LOAD_ATTR         'get_token'
581	CALL_FUNCTION_0   None
584	STORE_FAST        'account'
587	JUMP_BACK         '385'

590	LOAD_FAST         'tt'
593	LOAD_CONST        'password'
596	COMPARE_OP        '=='
599	POP_JUMP_IF_FALSE '617'

602	LOAD_FAST         'lexer'
605	LOAD_ATTR         'get_token'
608	CALL_FUNCTION_0   None
611	STORE_FAST        'password'
614	JUMP_BACK         '385'

617	LOAD_GLOBAL       'NetrcParseError'
620	LOAD_CONST        'bad follower token %r'
623	LOAD_FAST         'tt'
626	BINARY_MODULO     None

627	LOAD_FAST         'file'
630	LOAD_FAST         'lexer'
633	LOAD_ATTR         'lineno'
636	CALL_FUNCTION_3   None
639	RAISE_VARARGS_1   None
642	JUMP_BACK         '385'
645	POP_BLOCK         None
646_0	COME_FROM         '382'
646	JUMP_BACK         '57'
649	POP_BLOCK         None
650_0	COME_FROM         '54'
650	LOAD_CONST        None
653	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 321

    def authenticators(self, host):
        """Return a (user, account, password) tuple for given host."""
        if host in self.hosts:
            return self.hosts[host]
        elif 'default' in self.hosts:
            return self.hosts['default']
        else:
            return None
            return None

    def __repr__(self):
        """Dump the class data in the format of a .netrc file."""
        rep = ''
        for host in self.hosts.keys():
            attrs = self.hosts[host]
            rep = rep + 'machine ' + host + '\n\tlogin ' + repr(attrs[0]) + '\n'
            if attrs[1]:
                rep = rep + 'account ' + repr(attrs[1])
            rep = rep + '\tpassword ' + repr(attrs[2]) + '\n'

        for macro in self.macros.keys():
            rep = rep + 'macdef ' + macro + '\n'
            for line in self.macros[macro]:
                rep = rep + line

            rep = rep + '\n'

        return rep


if __name__ == '__main__':
    print netrc()