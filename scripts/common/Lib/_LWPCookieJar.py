# Embedded file name: scripts/common/Lib/_LWPCookieJar.py
"""Load / save to libwww-perl (LWP) format files.

Actually, the format is slightly extended from that used by LWP's
(libwww-perl's) HTTP::Cookies, to avoid losing some RFC 2965 information
not recorded by LWP.

It uses the version string "2.0", though really there isn't an LWP Cookies
2.0 format.  This indicates that there is extra information in here
(domain_dot and # port_spec) while still being compatible with
libwww-perl, I hope.

"""
import time, re
from cookielib import _warn_unhandled_exception, FileCookieJar, LoadError, Cookie, MISSING_FILENAME_TEXT, join_header_words, split_header_words, iso2time, time2isoz

def lwp_cookie_str(cookie):
    """Return string representation of Cookie in an the LWP cookie file format.
    
    Actually, the format is extended a bit -- see module docstring.
    
    """
    h = [(cookie.name, cookie.value), ('path', cookie.path), ('domain', cookie.domain)]
    if cookie.port is not None:
        h.append(('port', cookie.port))
    if cookie.path_specified:
        h.append(('path_spec', None))
    if cookie.port_specified:
        h.append(('port_spec', None))
    if cookie.domain_initial_dot:
        h.append(('domain_dot', None))
    if cookie.secure:
        h.append(('secure', None))
    if cookie.expires:
        h.append(('expires', time2isoz(float(cookie.expires))))
    if cookie.discard:
        h.append(('discard', None))
    if cookie.comment:
        h.append(('comment', cookie.comment))
    if cookie.comment_url:
        h.append(('commenturl', cookie.comment_url))
    keys = cookie._rest.keys()
    keys.sort()
    for k in keys:
        h.append((k, str(cookie._rest[k])))

    h.append(('version', str(cookie.version)))
    return join_header_words([h])


class LWPCookieJar(FileCookieJar):
    """
    The LWPCookieJar saves a sequence of"Set-Cookie3" lines.
    "Set-Cookie3" is the format used by the libwww-perl libary, not known
    to be compatible with any browser, but which is easy to read and
    doesn't lose information about RFC 2965 cookies.
    
    Additional methods
    
    as_lwp_str(ignore_discard=True, ignore_expired=True)
    
    """

    def as_lwp_str(self, ignore_discard = True, ignore_expires = True):
        """Return cookies as a string of "
        "-separated "Set-Cookie3" headers.
        
                ignore_discard and ignore_expires: see docstring for FileCookieJar.save
        
                """
        now = time.time()
        r = []
        for cookie in self:
            if not ignore_discard and cookie.discard:
                continue
            if not ignore_expires and cookie.is_expired(now):
                continue
            r.append('Set-Cookie3: %s' % lwp_cookie_str(cookie))

        return '\n'.join(r + [''])

    def save(self, filename = None, ignore_discard = False, ignore_expires = False):
        if filename is None:
            if self.filename is not None:
                filename = self.filename
            else:
                raise ValueError(MISSING_FILENAME_TEXT)
        f = open(filename, 'w')
        try:
            f.write('#LWP-Cookies-2.0\n')
            f.write(self.as_lwp_str(ignore_discard, ignore_expires))
        finally:
            f.close()

        return

    def _really_load--- This code section failed: ---

0	LOAD_FAST         'f'
3	LOAD_ATTR         'readline'
6	CALL_FUNCTION_0   None
9	STORE_FAST        'magic'

12	LOAD_GLOBAL       're'
15	LOAD_ATTR         'search'
18	LOAD_FAST         'self'
21	LOAD_ATTR         'magic_re'
24	LOAD_FAST         'magic'
27	CALL_FUNCTION_2   None
30	POP_JUMP_IF_TRUE  '58'

33	LOAD_CONST        '%r does not look like a Set-Cookie3 (LWP) format file'

36	LOAD_FAST         'filename'
39	BINARY_MODULO     None
40	STORE_FAST        'msg'

43	LOAD_GLOBAL       'LoadError'
46	LOAD_FAST         'msg'
49	CALL_FUNCTION_1   None
52	RAISE_VARARGS_1   None
55	JUMP_FORWARD      '58'
58_0	COME_FROM         '55'

58	LOAD_GLOBAL       'time'
61	LOAD_ATTR         'time'
64	CALL_FUNCTION_0   None
67	STORE_FAST        'now'

70	LOAD_CONST        'Set-Cookie3:'
73	STORE_FAST        'header'

76	LOAD_CONST        ('port_spec', 'path_spec', 'domain_dot', 'secure', 'discard')
79	STORE_FAST        'boolean_attrs'

82	LOAD_CONST        ('version', 'port', 'path', 'domain', 'expires', 'comment', 'commenturl')
85	STORE_FAST        'value_attrs'

88	SETUP_EXCEPT      '710'

91	SETUP_LOOP        '706'

94	LOAD_FAST         'f'
97	LOAD_ATTR         'readline'
100	CALL_FUNCTION_0   None
103	STORE_FAST        'line'

106	LOAD_FAST         'line'
109	LOAD_CONST        ''
112	COMPARE_OP        '=='
115	POP_JUMP_IF_FALSE '122'
118	BREAK_LOOP        None
119	JUMP_FORWARD      '122'
122_0	COME_FROM         '119'

122	LOAD_FAST         'line'
125	LOAD_ATTR         'startswith'
128	LOAD_FAST         'header'
131	CALL_FUNCTION_1   None
134	POP_JUMP_IF_TRUE  '143'

137	CONTINUE          '94'
140	JUMP_FORWARD      '143'
143_0	COME_FROM         '140'

143	LOAD_FAST         'line'
146	LOAD_GLOBAL       'len'
149	LOAD_FAST         'header'
152	CALL_FUNCTION_1   None
155	SLICE+1           None
156	LOAD_ATTR         'strip'
159	CALL_FUNCTION_0   None
162	STORE_FAST        'line'

165	SETUP_LOOP        '702'
168	LOAD_GLOBAL       'split_header_words'
171	LOAD_FAST         'line'
174	BUILD_LIST_1      None
177	CALL_FUNCTION_1   None
180	GET_ITER          None
181	FOR_ITER          '701'
184	STORE_FAST        'data'

187	LOAD_FAST         'data'
190	LOAD_CONST        0
193	BINARY_SUBSCR     None
194	UNPACK_SEQUENCE_2 None
197	STORE_FAST        'name'
200	STORE_FAST        'value'

203	BUILD_MAP         None
206	STORE_FAST        'standard'

209	BUILD_MAP         None
212	STORE_FAST        'rest'

215	SETUP_LOOP        '242'
218	LOAD_FAST         'boolean_attrs'
221	GET_ITER          None
222	FOR_ITER          '241'
225	STORE_FAST        'k'

228	LOAD_GLOBAL       'False'
231	LOAD_FAST         'standard'
234	LOAD_FAST         'k'
237	STORE_SUBSCR      None
238	JUMP_BACK         '222'
241	POP_BLOCK         None
242_0	COME_FROM         '215'

242	SETUP_LOOP        '416'
245	LOAD_FAST         'data'
248	LOAD_CONST        1
251	SLICE+1           None
252	GET_ITER          None
253	FOR_ITER          '415'
256	UNPACK_SEQUENCE_2 None
259	STORE_FAST        'k'
262	STORE_FAST        'v'

265	LOAD_FAST         'k'
268	LOAD_CONST        None
271	COMPARE_OP        'is not'
274	POP_JUMP_IF_FALSE '292'

277	LOAD_FAST         'k'
280	LOAD_ATTR         'lower'
283	CALL_FUNCTION_0   None
286	STORE_FAST        'lc'
289	JUMP_FORWARD      '298'

292	LOAD_CONST        None
295	STORE_FAST        'lc'
298_0	COME_FROM         '289'

298	LOAD_FAST         'lc'
301	LOAD_FAST         'value_attrs'
304	COMPARE_OP        'in'
307	POP_JUMP_IF_TRUE  '322'
310	LOAD_FAST         'lc'
313	LOAD_FAST         'boolean_attrs'
316	COMPARE_OP        'in'
319_0	COME_FROM         '307'
319	POP_JUMP_IF_FALSE '331'

322	LOAD_FAST         'lc'
325	STORE_FAST        'k'
328	JUMP_FORWARD      '331'
331_0	COME_FROM         '328'

331	LOAD_FAST         'k'
334	LOAD_FAST         'boolean_attrs'
337	COMPARE_OP        'in'
340	POP_JUMP_IF_FALSE '377'

343	LOAD_FAST         'v'
346	LOAD_CONST        None
349	COMPARE_OP        'is'
352	POP_JUMP_IF_FALSE '364'
355	LOAD_GLOBAL       'True'
358	STORE_FAST        'v'
361	JUMP_FORWARD      '364'
364_0	COME_FROM         '361'

364	LOAD_FAST         'v'
367	LOAD_FAST         'standard'
370	LOAD_FAST         'k'
373	STORE_SUBSCR      None
374	JUMP_BACK         '253'

377	LOAD_FAST         'k'
380	LOAD_FAST         'value_attrs'
383	COMPARE_OP        'in'
386	POP_JUMP_IF_FALSE '402'

389	LOAD_FAST         'v'
392	LOAD_FAST         'standard'
395	LOAD_FAST         'k'
398	STORE_SUBSCR      None
399	JUMP_BACK         '253'

402	LOAD_FAST         'v'
405	LOAD_FAST         'rest'
408	LOAD_FAST         'k'
411	STORE_SUBSCR      None
412	JUMP_BACK         '253'
415	POP_BLOCK         None
416_0	COME_FROM         '242'

416	LOAD_FAST         'standard'
419	LOAD_ATTR         'get'
422	STORE_FAST        'h'

425	LOAD_FAST         'h'
428	LOAD_CONST        'expires'
431	CALL_FUNCTION_1   None
434	STORE_FAST        'expires'

437	LOAD_FAST         'h'
440	LOAD_CONST        'discard'
443	CALL_FUNCTION_1   None
446	STORE_FAST        'discard'

449	LOAD_FAST         'expires'
452	LOAD_CONST        None
455	COMPARE_OP        'is not'
458	POP_JUMP_IF_FALSE '476'

461	LOAD_GLOBAL       'iso2time'
464	LOAD_FAST         'expires'
467	CALL_FUNCTION_1   None
470	STORE_FAST        'expires'
473	JUMP_FORWARD      '476'
476_0	COME_FROM         '473'

476	LOAD_FAST         'expires'
479	LOAD_CONST        None
482	COMPARE_OP        'is'
485	POP_JUMP_IF_FALSE '497'

488	LOAD_GLOBAL       'True'
491	STORE_FAST        'discard'
494	JUMP_FORWARD      '497'
497_0	COME_FROM         '494'

497	LOAD_FAST         'h'
500	LOAD_CONST        'domain'
503	CALL_FUNCTION_1   None
506	STORE_FAST        'domain'

509	LOAD_FAST         'domain'
512	LOAD_ATTR         'startswith'
515	LOAD_CONST        '.'
518	CALL_FUNCTION_1   None
521	STORE_FAST        'domain_specified'

524	LOAD_GLOBAL       'Cookie'
527	LOAD_FAST         'h'
530	LOAD_CONST        'version'
533	CALL_FUNCTION_1   None
536	LOAD_FAST         'name'
539	LOAD_FAST         'value'

542	LOAD_FAST         'h'
545	LOAD_CONST        'port'
548	CALL_FUNCTION_1   None
551	LOAD_FAST         'h'
554	LOAD_CONST        'port_spec'
557	CALL_FUNCTION_1   None

560	LOAD_FAST         'domain'
563	LOAD_FAST         'domain_specified'
566	LOAD_FAST         'h'
569	LOAD_CONST        'domain_dot'
572	CALL_FUNCTION_1   None

575	LOAD_FAST         'h'
578	LOAD_CONST        'path'
581	CALL_FUNCTION_1   None
584	LOAD_FAST         'h'
587	LOAD_CONST        'path_spec'
590	CALL_FUNCTION_1   None

593	LOAD_FAST         'h'
596	LOAD_CONST        'secure'
599	CALL_FUNCTION_1   None

602	LOAD_FAST         'expires'

605	LOAD_FAST         'discard'

608	LOAD_FAST         'h'
611	LOAD_CONST        'comment'
614	CALL_FUNCTION_1   None

617	LOAD_FAST         'h'
620	LOAD_CONST        'commenturl'
623	CALL_FUNCTION_1   None

626	LOAD_FAST         'rest'
629	CALL_FUNCTION_16  None
632	STORE_FAST        'c'

635	LOAD_FAST         'ignore_discard'
638	UNARY_NOT         None
639	POP_JUMP_IF_FALSE '657'
642	LOAD_FAST         'c'
645	LOAD_ATTR         'discard'
648_0	COME_FROM         '639'
648	POP_JUMP_IF_FALSE '657'

651	CONTINUE          '181'
654	JUMP_FORWARD      '657'
657_0	COME_FROM         '654'

657	LOAD_FAST         'ignore_expires'
660	UNARY_NOT         None
661	POP_JUMP_IF_FALSE '685'
664	LOAD_FAST         'c'
667	LOAD_ATTR         'is_expired'
670	LOAD_FAST         'now'
673	CALL_FUNCTION_1   None
676_0	COME_FROM         '661'
676	POP_JUMP_IF_FALSE '685'

679	CONTINUE          '181'
682	JUMP_FORWARD      '685'
685_0	COME_FROM         '682'

685	LOAD_FAST         'self'
688	LOAD_ATTR         'set_cookie'
691	LOAD_FAST         'c'
694	CALL_FUNCTION_1   None
697	POP_TOP           None
698	JUMP_BACK         '181'
701	POP_BLOCK         None
702_0	COME_FROM         '165'
702	JUMP_BACK         '94'
705	POP_BLOCK         None
706_0	COME_FROM         '91'
706	POP_BLOCK         None
707	JUMP_FORWARD      '775'
710_0	COME_FROM         '88'

710	DUP_TOP           None
711	LOAD_GLOBAL       'IOError'
714	COMPARE_OP        'exception match'
717	POP_JUMP_IF_FALSE '729'
720	POP_TOP           None
721	POP_TOP           None
722	POP_TOP           None

723	RAISE_VARARGS_0   None
726	JUMP_FORWARD      '775'

729	DUP_TOP           None
730	LOAD_GLOBAL       'Exception'
733	COMPARE_OP        'exception match'
736	POP_JUMP_IF_FALSE '774'
739	POP_TOP           None
740	POP_TOP           None
741	POP_TOP           None

742	LOAD_GLOBAL       '_warn_unhandled_exception'
745	CALL_FUNCTION_0   None
748	POP_TOP           None

749	LOAD_GLOBAL       'LoadError'
752	LOAD_CONST        'invalid Set-Cookie3 format file %r: %r'

755	LOAD_FAST         'filename'
758	LOAD_FAST         'line'
761	BUILD_TUPLE_2     None
764	BINARY_MODULO     None
765	CALL_FUNCTION_1   None
768	RAISE_VARARGS_1   None
771	JUMP_FORWARD      '775'
774	END_FINALLY       None
775_0	COME_FROM         '707'
775_1	COME_FROM         '774'
775	LOAD_CONST        None
778	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 705