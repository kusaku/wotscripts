# Embedded file name: scripts/common/Lib/markupbase.py
"""Shared support for scanning document type declarations in HTML and XHTML.

This module is used as a foundation for the HTMLParser and sgmllib
modules (indirectly, for htmllib as well).  It has no documented
public API and should not be used directly.

"""
import re
_declname_match = re.compile('[a-zA-Z][-_.a-zA-Z0-9]*\\s*').match
_declstringlit_match = re.compile('(\\\'[^\\\']*\\\'|"[^"]*")\\s*').match
_commentclose = re.compile('--\\s*>')
_markedsectionclose = re.compile(']\\s*]\\s*>')
_msmarkedsectionclose = re.compile(']\\s*>')
del re

class ParserBase:
    """Parser base class which provides some common support methods used
    by the SGML/HTML and XHTML parsers."""

    def __init__(self):
        if self.__class__ is ParserBase:
            raise RuntimeError('markupbase.ParserBase must be subclassed')

    def error(self, message):
        raise NotImplementedError('subclasses of ParserBase must override error()')

    def reset(self):
        self.lineno = 1
        self.offset = 0

    def getpos(self):
        """Return current line number and offset."""
        return (self.lineno, self.offset)

    def updatepos(self, i, j):
        if i >= j:
            return j
        rawdata = self.rawdata
        nlines = rawdata.count('\n', i, j)
        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex('\n', i, j)
            self.offset = j - (pos + 1)
        else:
            self.offset = self.offset + j - i
        return j

    _decl_otherchars = ''

    def parse_declaration(self, i):
        rawdata = self.rawdata
        j = i + 2
        if not rawdata[i:j] == '<!':
            raise AssertionError('unexpected call to parse_declaration')
            if rawdata[j:j + 1] == '>':
                return j + 1
            if rawdata[j:j + 1] in ('-', ''):
                return -1
            n = len(rawdata)
            if rawdata[j:j + 2] == '--':
                return self.parse_comment(i)
            if rawdata[j] == '[':
                return self.parse_marked_section(i)
            decltype, j = self._scan_name(j, i)
            if j < 0:
                return j
            self._decl_otherchars = decltype == 'doctype' and ''
        while j < n:
            c = rawdata[j]
            if c == '>':
                data = rawdata[i + 2:j]
                if decltype == 'doctype':
                    self.handle_decl(data)
                else:
                    self.unknown_decl(data)
                return j + 1
            if c in '"\'':
                m = _declstringlit_match(rawdata, j)
                if not m:
                    return -1
                j = m.end()
            elif c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                name, j = self._scan_name(j, i)
            elif c in self._decl_otherchars:
                j = j + 1
            elif c == '[':
                if decltype == 'doctype':
                    j = self._parse_doctype_subset(j + 1, i)
                elif decltype in ('attlist', 'linktype', 'link', 'element'):
                    self.error("unsupported '[' char in %s declaration" % decltype)
                else:
                    self.error("unexpected '[' char in declaration")
            else:
                self.error('unexpected %r char in declaration' % rawdata[j])
            if j < 0:
                return j

        return -1

    def parse_marked_section(self, i, report = 1):
        rawdata = self.rawdata
        if not rawdata[i:i + 3] == '<![':
            raise AssertionError('unexpected call to parse_marked_section()')
            sectName, j = self._scan_name(i + 3, i)
            if j < 0:
                return j
            if sectName in ('temp', 'cdata', 'ignore', 'include', 'rcdata'):
                match = _markedsectionclose.search(rawdata, i + 3)
            elif sectName in ('if', 'else', 'endif'):
                match = _msmarkedsectionclose.search(rawdata, i + 3)
            else:
                self.error('unknown status keyword %r in marked section' % rawdata[i + 3:j])
            if not match:
                return -1
            j = report and match.start(0)
            self.unknown_decl(rawdata[i + 3:j])
        return match.end(0)

    def parse_comment(self, i, report = 1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        match = _commentclose.search(rawdata, i + 4)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.handle_comment(rawdata[i + 4:j])
        return match.end(0)

    def _parse_doctype_subset(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        j = i
        while j < n:
            c = rawdata[j]
            if c == '<':
                s = rawdata[j:j + 2]
                if s == '<':
                    return -1
                if s != '<!':
                    self.updatepos(declstartpos, j + 1)
                    self.error('unexpected char in internal subset (in %r)' % s)
                if j + 2 == n:
                    return -1
                if j + 4 > n:
                    return -1
                if rawdata[j:j + 4] == '<!--':
                    j = self.parse_comment(j, report=0)
                    if j < 0:
                        return j
                    continue
                name, j = self._scan_name(j + 2, declstartpos)
                if j == -1:
                    return -1
                if name not in ('attlist', 'element', 'entity', 'notation'):
                    self.updatepos(declstartpos, j + 2)
                    self.error('unknown declaration %r in internal subset' % name)
                meth = getattr(self, '_parse_doctype_' + name)
                j = meth(j, declstartpos)
                if j < 0:
                    return j
            elif c == '%':
                if j + 1 == n:
                    return -1
                s, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j
                if rawdata[j] == ';':
                    j = j + 1
            elif c == ']':
                j = j + 1
                while j < n and rawdata[j].isspace():
                    j = j + 1

                if j < n:
                    if rawdata[j] == '>':
                        return j
                    self.updatepos(declstartpos, j)
                    self.error('unexpected char after internal subset')
                else:
                    return -1
            elif c.isspace():
                j = j + 1
            else:
                self.updatepos(declstartpos, j)
                self.error('unexpected char %r in internal subset' % c)

        return -1

    def _parse_doctype_element(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j == -1:
            return -1
        rawdata = self.rawdata
        if '>' in rawdata[j:]:
            return rawdata.find('>', j) + 1
        return -1

    def _parse_doctype_attlist--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'rawdata'
6	STORE_FAST        'rawdata'

9	LOAD_FAST         'self'
12	LOAD_ATTR         '_scan_name'
15	LOAD_FAST         'i'
18	LOAD_FAST         'declstartpos'
21	CALL_FUNCTION_2   None
24	UNPACK_SEQUENCE_2 None
27	STORE_FAST        'name'
30	STORE_FAST        'j'

33	LOAD_FAST         'rawdata'
36	LOAD_FAST         'j'
39	LOAD_FAST         'j'
42	LOAD_CONST        1
45	BINARY_ADD        None
46	SLICE+3           None
47	STORE_FAST        'c'

50	LOAD_FAST         'c'
53	LOAD_CONST        ''
56	COMPARE_OP        '=='
59	POP_JUMP_IF_FALSE '66'

62	LOAD_CONST        -1
65	RETURN_END_IF     None

66	LOAD_FAST         'c'
69	LOAD_CONST        '>'
72	COMPARE_OP        '=='
75	POP_JUMP_IF_FALSE '86'

78	LOAD_FAST         'j'
81	LOAD_CONST        1
84	BINARY_ADD        None
85	RETURN_END_IF     None

86	SETUP_LOOP        '539'

89	LOAD_FAST         'self'
92	LOAD_ATTR         '_scan_name'
95	LOAD_FAST         'j'
98	LOAD_FAST         'declstartpos'
101	CALL_FUNCTION_2   None
104	UNPACK_SEQUENCE_2 None
107	STORE_FAST        'name'
110	STORE_FAST        'j'

113	LOAD_FAST         'j'
116	LOAD_CONST        0
119	COMPARE_OP        '<'
122	POP_JUMP_IF_FALSE '129'

125	LOAD_FAST         'j'
128	RETURN_END_IF     None

129	LOAD_FAST         'rawdata'
132	LOAD_FAST         'j'
135	LOAD_FAST         'j'
138	LOAD_CONST        1
141	BINARY_ADD        None
142	SLICE+3           None
143	STORE_FAST        'c'

146	LOAD_FAST         'c'
149	LOAD_CONST        ''
152	COMPARE_OP        '=='
155	POP_JUMP_IF_FALSE '162'

158	LOAD_CONST        -1
161	RETURN_END_IF     None

162	LOAD_FAST         'c'
165	LOAD_CONST        '('
168	COMPARE_OP        '=='
171	POP_JUMP_IF_FALSE '276'

174	LOAD_CONST        ')'
177	LOAD_FAST         'rawdata'
180	LOAD_FAST         'j'
183	SLICE+1           None
184	COMPARE_OP        'in'
187	POP_JUMP_IF_FALSE '215'

190	LOAD_FAST         'rawdata'
193	LOAD_ATTR         'find'
196	LOAD_CONST        ')'
199	LOAD_FAST         'j'
202	CALL_FUNCTION_2   None
205	LOAD_CONST        1
208	BINARY_ADD        None
209	STORE_FAST        'j'
212	JUMP_FORWARD      '219'

215	LOAD_CONST        -1
218	RETURN_VALUE      None
219_0	COME_FROM         '212'

219	SETUP_LOOP        '259'
222	LOAD_FAST         'rawdata'
225	LOAD_FAST         'j'
228	LOAD_FAST         'j'
231	LOAD_CONST        1
234	BINARY_ADD        None
235	SLICE+3           None
236	LOAD_ATTR         'isspace'
239	CALL_FUNCTION_0   None
242	POP_JUMP_IF_FALSE '258'

245	LOAD_FAST         'j'
248	LOAD_CONST        1
251	BINARY_ADD        None
252	STORE_FAST        'j'
255	JUMP_BACK         '222'
258	POP_BLOCK         None
259_0	COME_FROM         '219'

259	LOAD_FAST         'rawdata'
262	LOAD_FAST         'j'
265	SLICE+1           None
266	POP_JUMP_IF_TRUE  '300'

269	LOAD_CONST        -1
272	RETURN_END_IF     None
273	JUMP_FORWARD      '300'

276	LOAD_FAST         'self'
279	LOAD_ATTR         '_scan_name'
282	LOAD_FAST         'j'
285	LOAD_FAST         'declstartpos'
288	CALL_FUNCTION_2   None
291	UNPACK_SEQUENCE_2 None
294	STORE_FAST        'name'
297	STORE_FAST        'j'
300_0	COME_FROM         '273'

300	LOAD_FAST         'rawdata'
303	LOAD_FAST         'j'
306	LOAD_FAST         'j'
309	LOAD_CONST        1
312	BINARY_ADD        None
313	SLICE+3           None
314	STORE_FAST        'c'

317	LOAD_FAST         'c'
320	POP_JUMP_IF_TRUE  '327'

323	LOAD_CONST        -1
326	RETURN_END_IF     None

327	LOAD_FAST         'c'
330	LOAD_CONST        '\'"'
333	COMPARE_OP        'in'
336	POP_JUMP_IF_FALSE '409'

339	LOAD_GLOBAL       '_declstringlit_match'
342	LOAD_FAST         'rawdata'
345	LOAD_FAST         'j'
348	CALL_FUNCTION_2   None
351	STORE_FAST        'm'

354	LOAD_FAST         'm'
357	POP_JUMP_IF_FALSE '375'

360	LOAD_FAST         'm'
363	LOAD_ATTR         'end'
366	CALL_FUNCTION_0   None
369	STORE_FAST        'j'
372	JUMP_FORWARD      '379'

375	LOAD_CONST        -1
378	RETURN_VALUE      None
379_0	COME_FROM         '372'

379	LOAD_FAST         'rawdata'
382	LOAD_FAST         'j'
385	LOAD_FAST         'j'
388	LOAD_CONST        1
391	BINARY_ADD        None
392	SLICE+3           None
393	STORE_FAST        'c'

396	LOAD_FAST         'c'
399	POP_JUMP_IF_TRUE  '409'

402	LOAD_CONST        -1
405	RETURN_END_IF     None
406	JUMP_FORWARD      '409'
409_0	COME_FROM         '406'

409	LOAD_FAST         'c'
412	LOAD_CONST        '#'
415	COMPARE_OP        '=='
418	POP_JUMP_IF_FALSE '515'

421	LOAD_FAST         'rawdata'
424	LOAD_FAST         'j'
427	SLICE+1           None
428	LOAD_CONST        '#'
431	COMPARE_OP        '=='
434	POP_JUMP_IF_FALSE '441'

437	LOAD_CONST        -1
440	RETURN_END_IF     None

441	LOAD_FAST         'self'
444	LOAD_ATTR         '_scan_name'
447	LOAD_FAST         'j'
450	LOAD_CONST        1
453	BINARY_ADD        None
454	LOAD_FAST         'declstartpos'
457	CALL_FUNCTION_2   None
460	UNPACK_SEQUENCE_2 None
463	STORE_FAST        'name'
466	STORE_FAST        'j'

469	LOAD_FAST         'j'
472	LOAD_CONST        0
475	COMPARE_OP        '<'
478	POP_JUMP_IF_FALSE '485'

481	LOAD_FAST         'j'
484	RETURN_END_IF     None

485	LOAD_FAST         'rawdata'
488	LOAD_FAST         'j'
491	LOAD_FAST         'j'
494	LOAD_CONST        1
497	BINARY_ADD        None
498	SLICE+3           None
499	STORE_FAST        'c'

502	LOAD_FAST         'c'
505	POP_JUMP_IF_TRUE  '515'

508	LOAD_CONST        -1
511	RETURN_END_IF     None
512	JUMP_FORWARD      '515'
515_0	COME_FROM         '512'

515	LOAD_FAST         'c'
518	LOAD_CONST        '>'
521	COMPARE_OP        '=='
524	POP_JUMP_IF_FALSE '89'

527	LOAD_FAST         'j'
530	LOAD_CONST        1
533	BINARY_ADD        None
534	RETURN_END_IF     None
535	JUMP_BACK         '89'
538	POP_BLOCK         None
539_0	COME_FROM         '86'

Syntax error at or near `POP_BLOCK' token at offset 538

    def _parse_doctype_notation--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         '_scan_name'
6	LOAD_FAST         'i'
9	LOAD_FAST         'declstartpos'
12	CALL_FUNCTION_2   None
15	UNPACK_SEQUENCE_2 None
18	STORE_FAST        'name'
21	STORE_FAST        'j'

24	LOAD_FAST         'j'
27	LOAD_CONST        0
30	COMPARE_OP        '<'
33	POP_JUMP_IF_FALSE '40'

36	LOAD_FAST         'j'
39	RETURN_END_IF     None

40	LOAD_FAST         'self'
43	LOAD_ATTR         'rawdata'
46	STORE_FAST        'rawdata'

49	SETUP_LOOP        '195'

52	LOAD_FAST         'rawdata'
55	LOAD_FAST         'j'
58	LOAD_FAST         'j'
61	LOAD_CONST        1
64	BINARY_ADD        None
65	SLICE+3           None
66	STORE_FAST        'c'

69	LOAD_FAST         'c'
72	POP_JUMP_IF_TRUE  '79'

75	LOAD_CONST        -1
78	RETURN_END_IF     None

79	LOAD_FAST         'c'
82	LOAD_CONST        '>'
85	COMPARE_OP        '=='
88	POP_JUMP_IF_FALSE '99'

91	LOAD_FAST         'j'
94	LOAD_CONST        1
97	BINARY_ADD        None
98	RETURN_END_IF     None

99	LOAD_FAST         'c'
102	LOAD_CONST        '\'"'
105	COMPARE_OP        'in'
108	POP_JUMP_IF_FALSE '151'

111	LOAD_GLOBAL       '_declstringlit_match'
114	LOAD_FAST         'rawdata'
117	LOAD_FAST         'j'
120	CALL_FUNCTION_2   None
123	STORE_FAST        'm'

126	LOAD_FAST         'm'
129	POP_JUMP_IF_TRUE  '136'

132	LOAD_CONST        -1
135	RETURN_END_IF     None

136	LOAD_FAST         'm'
139	LOAD_ATTR         'end'
142	CALL_FUNCTION_0   None
145	STORE_FAST        'j'
148	JUMP_BACK         '52'

151	LOAD_FAST         'self'
154	LOAD_ATTR         '_scan_name'
157	LOAD_FAST         'j'
160	LOAD_FAST         'declstartpos'
163	CALL_FUNCTION_2   None
166	UNPACK_SEQUENCE_2 None
169	STORE_FAST        'name'
172	STORE_FAST        'j'

175	LOAD_FAST         'j'
178	LOAD_CONST        0
181	COMPARE_OP        '<'
184	POP_JUMP_IF_FALSE '52'

187	LOAD_FAST         'j'
190	RETURN_END_IF     None
191	JUMP_BACK         '52'
194	POP_BLOCK         None
195_0	COME_FROM         '49'

Syntax error at or near `POP_BLOCK' token at offset 194

    def _parse_doctype_entity--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'rawdata'
6	STORE_FAST        'rawdata'

9	LOAD_FAST         'rawdata'
12	LOAD_FAST         'i'
15	LOAD_FAST         'i'
18	LOAD_CONST        1
21	BINARY_ADD        None
22	SLICE+3           None
23	LOAD_CONST        '%'
26	COMPARE_OP        '=='
29	POP_JUMP_IF_FALSE '105'

32	LOAD_FAST         'i'
35	LOAD_CONST        1
38	BINARY_ADD        None
39	STORE_FAST        'j'

42	SETUP_LOOP        '111'

45	LOAD_FAST         'rawdata'
48	LOAD_FAST         'j'
51	LOAD_FAST         'j'
54	LOAD_CONST        1
57	BINARY_ADD        None
58	SLICE+3           None
59	STORE_FAST        'c'

62	LOAD_FAST         'c'
65	POP_JUMP_IF_TRUE  '72'

68	LOAD_CONST        -1
71	RETURN_END_IF     None

72	LOAD_FAST         'c'
75	LOAD_ATTR         'isspace'
78	CALL_FUNCTION_0   None
81	POP_JUMP_IF_FALSE '97'

84	LOAD_FAST         'j'
87	LOAD_CONST        1
90	BINARY_ADD        None
91	STORE_FAST        'j'
94	JUMP_BACK         '45'

97	BREAK_LOOP        None
98	JUMP_BACK         '45'
101	POP_BLOCK         None
102_0	COME_FROM         '42'
102	JUMP_FORWARD      '111'

105	LOAD_FAST         'i'
108	STORE_FAST        'j'
111_0	COME_FROM         '102'

111	LOAD_FAST         'self'
114	LOAD_ATTR         '_scan_name'
117	LOAD_FAST         'j'
120	LOAD_FAST         'declstartpos'
123	CALL_FUNCTION_2   None
126	UNPACK_SEQUENCE_2 None
129	STORE_FAST        'name'
132	STORE_FAST        'j'

135	LOAD_FAST         'j'
138	LOAD_CONST        0
141	COMPARE_OP        '<'
144	POP_JUMP_IF_FALSE '151'

147	LOAD_FAST         'j'
150	RETURN_END_IF     None

151	SETUP_LOOP        '303'

154	LOAD_FAST         'self'
157	LOAD_ATTR         'rawdata'
160	LOAD_FAST         'j'
163	LOAD_FAST         'j'
166	LOAD_CONST        1
169	BINARY_ADD        None
170	SLICE+3           None
171	STORE_FAST        'c'

174	LOAD_FAST         'c'
177	POP_JUMP_IF_TRUE  '184'

180	LOAD_CONST        -1
183	RETURN_END_IF     None

184	LOAD_FAST         'c'
187	LOAD_CONST        '\'"'
190	COMPARE_OP        'in'
193	POP_JUMP_IF_FALSE '239'

196	LOAD_GLOBAL       '_declstringlit_match'
199	LOAD_FAST         'rawdata'
202	LOAD_FAST         'j'
205	CALL_FUNCTION_2   None
208	STORE_FAST        'm'

211	LOAD_FAST         'm'
214	POP_JUMP_IF_FALSE '232'

217	LOAD_FAST         'm'
220	LOAD_ATTR         'end'
223	CALL_FUNCTION_0   None
226	STORE_FAST        'j'
229	JUMP_ABSOLUTE     '299'

232	LOAD_CONST        -1
235	RETURN_VALUE      None
236	JUMP_BACK         '154'

239	LOAD_FAST         'c'
242	LOAD_CONST        '>'
245	COMPARE_OP        '=='
248	POP_JUMP_IF_FALSE '259'

251	LOAD_FAST         'j'
254	LOAD_CONST        1
257	BINARY_ADD        None
258	RETURN_END_IF     None

259	LOAD_FAST         'self'
262	LOAD_ATTR         '_scan_name'
265	LOAD_FAST         'j'
268	LOAD_FAST         'declstartpos'
271	CALL_FUNCTION_2   None
274	UNPACK_SEQUENCE_2 None
277	STORE_FAST        'name'
280	STORE_FAST        'j'

283	LOAD_FAST         'j'
286	LOAD_CONST        0
289	COMPARE_OP        '<'
292	POP_JUMP_IF_FALSE '154'

295	LOAD_FAST         'j'
298	RETURN_END_IF     None
299	JUMP_BACK         '154'
302	POP_BLOCK         None
303_0	COME_FROM         '151'

Syntax error at or near `POP_BLOCK' token at offset 101

    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return (None, -1)
        else:
            m = _declname_match(rawdata, i)
            if m:
                s = m.group()
                name = s.strip()
                if i + len(s) == n:
                    return (None, -1)
                return (name.lower(), m.end())
            self.updatepos(declstartpos, i)
            self.error('expected name token at %r' % rawdata[declstartpos:declstartpos + 20])
            return None

    def unknown_decl(self, data):
        pass