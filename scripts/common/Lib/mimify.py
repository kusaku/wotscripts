# Embedded file name: scripts/common/Lib/mimify.py
"""Mimification and unmimification of mail messages.

Decode quoted-printable parts of a mail message or encode using
quoted-printable.

Usage:
        mimify(input, output)
        unmimify(input, output, decode_base64 = 0)
to encode and decode respectively.  Input and output may be the name
of a file or an open file object.  Only a readline() method is used
on the input file, only a write() method is used on the output file.
When using file names, the input and output file names may be the
same.

Interactive usage:
        mimify.py -e [infile [outfile]]
        mimify.py -d [infile [outfile]]
to encode and decode respectively.  Infile defaults to standard
input and outfile to standard output.
"""
MAXLEN = 200
CHARSET = 'ISO-8859-1'
QUOTE = '> '
import re
import warnings
warnings.warn('the mimify module is deprecated; use the email package instead', DeprecationWarning, 2)
__all__ = ['mimify',
 'unmimify',
 'mime_encode_header',
 'mime_decode_header']
qp = re.compile('^content-transfer-encoding:\\s*quoted-printable', re.I)
base64_re = re.compile('^content-transfer-encoding:\\s*base64', re.I)
mp = re.compile('^content-type:.*multipart/.*boundary="?([^;"\n]*)', re.I | re.S)
chrset = re.compile('^(content-type:.*charset=")(us-ascii|iso-8859-[0-9]+)(".*)', re.I | re.S)
he = re.compile('^-*\n')
mime_code = re.compile('=([0-9a-f][0-9a-f])', re.I)
mime_head = re.compile('=\\?iso-8859-1\\?q\\?([^? \t\n]+)\\?=', re.I)
repl = re.compile('^subject:\\s+re: ', re.I)

class File:
    """A simple fake file object that knows about limited read-ahead and
    boundaries.  The only supported method is readline()."""

    def __init__(self, file, boundary):
        self.file = file
        self.boundary = boundary
        self.peek = None
        return

    def readline(self):
        if self.peek is not None:
            return ''
        else:
            line = self.file.readline()
            if not line:
                return line
            if self.boundary:
                if line == self.boundary + '\n':
                    self.peek = line
                    return ''
                if line == self.boundary + '--\n':
                    self.peek = line
                    return ''
            return line


class HeaderFile:

    def __init__(self, file):
        self.file = file
        self.peek = None
        return

    def readline--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'peek'
6	LOAD_CONST        None
9	COMPARE_OP        'is not'
12	POP_JUMP_IF_FALSE '36'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'peek'
21	STORE_FAST        'line'

24	LOAD_CONST        None
27	LOAD_FAST         'self'
30	STORE_ATTR        'peek'
33	JUMP_FORWARD      '51'

36	LOAD_FAST         'self'
39	LOAD_ATTR         'file'
42	LOAD_ATTR         'readline'
45	CALL_FUNCTION_0   None
48	STORE_FAST        'line'
51_0	COME_FROM         '33'

51	LOAD_FAST         'line'
54	POP_JUMP_IF_TRUE  '61'

57	LOAD_FAST         'line'
60	RETURN_END_IF     None

61	LOAD_GLOBAL       'he'
64	LOAD_ATTR         'match'
67	LOAD_FAST         'line'
70	CALL_FUNCTION_1   None
73	POP_JUMP_IF_FALSE '80'

76	LOAD_FAST         'line'
79	RETURN_END_IF     None

80	SETUP_LOOP        '190'

83	LOAD_FAST         'self'
86	LOAD_ATTR         'file'
89	LOAD_ATTR         'readline'
92	CALL_FUNCTION_0   None
95	LOAD_FAST         'self'
98	STORE_ATTR        'peek'

101	LOAD_GLOBAL       'len'
104	LOAD_FAST         'self'
107	LOAD_ATTR         'peek'
110	CALL_FUNCTION_1   None
113	LOAD_CONST        0
116	COMPARE_OP        '=='
119	POP_JUMP_IF_TRUE  '160'

122	LOAD_FAST         'self'
125	LOAD_ATTR         'peek'
128	LOAD_CONST        0
131	BINARY_SUBSCR     None
132	LOAD_CONST        ' '
135	COMPARE_OP        '!='
138	POP_JUMP_IF_FALSE '164'
141	LOAD_FAST         'self'
144	LOAD_ATTR         'peek'
147	LOAD_CONST        0
150	BINARY_SUBSCR     None
151	LOAD_CONST        '\t'
154	COMPARE_OP        '!='
157_0	COME_FROM         '119'
157_1	COME_FROM         '138'
157	POP_JUMP_IF_FALSE '164'

160	LOAD_FAST         'line'
163	RETURN_END_IF     None

164	LOAD_FAST         'line'
167	LOAD_FAST         'self'
170	LOAD_ATTR         'peek'
173	BINARY_ADD        None
174	STORE_FAST        'line'

177	LOAD_CONST        None
180	LOAD_FAST         'self'
183	STORE_ATTR        'peek'
186	JUMP_BACK         '83'
189	POP_BLOCK         None
190_0	COME_FROM         '80'
190	LOAD_CONST        None
193	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 189


def mime_decode--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'newline'

6	LOAD_CONST        0
9	STORE_FAST        'pos'

12	SETUP_LOOP        '122'

15	LOAD_GLOBAL       'mime_code'
18	LOAD_ATTR         'search'
21	LOAD_FAST         'line'
24	LOAD_FAST         'pos'
27	CALL_FUNCTION_2   None
30	STORE_FAST        'res'

33	LOAD_FAST         'res'
36	LOAD_CONST        None
39	COMPARE_OP        'is'
42	POP_JUMP_IF_FALSE '49'

45	BREAK_LOOP        None
46	JUMP_FORWARD      '49'
49_0	COME_FROM         '46'

49	LOAD_FAST         'newline'
52	LOAD_FAST         'line'
55	LOAD_FAST         'pos'
58	LOAD_FAST         'res'
61	LOAD_ATTR         'start'
64	LOAD_CONST        0
67	CALL_FUNCTION_1   None
70	SLICE+3           None
71	BINARY_ADD        None

72	LOAD_GLOBAL       'chr'
75	LOAD_GLOBAL       'int'
78	LOAD_FAST         'res'
81	LOAD_ATTR         'group'
84	LOAD_CONST        1
87	CALL_FUNCTION_1   None
90	LOAD_CONST        16
93	CALL_FUNCTION_2   None
96	CALL_FUNCTION_1   None
99	BINARY_ADD        None
100	STORE_FAST        'newline'

103	LOAD_FAST         'res'
106	LOAD_ATTR         'end'
109	LOAD_CONST        0
112	CALL_FUNCTION_1   None
115	STORE_FAST        'pos'
118	JUMP_BACK         '15'
121	POP_BLOCK         None
122_0	COME_FROM         '12'

122	LOAD_FAST         'newline'
125	LOAD_FAST         'line'
128	LOAD_FAST         'pos'
131	SLICE+1           None
132	BINARY_ADD        None
133	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 121


def mime_decode_header--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'newline'

6	LOAD_CONST        0
9	STORE_FAST        'pos'

12	SETUP_LOOP        '143'

15	LOAD_GLOBAL       'mime_head'
18	LOAD_ATTR         'search'
21	LOAD_FAST         'line'
24	LOAD_FAST         'pos'
27	CALL_FUNCTION_2   None
30	STORE_FAST        'res'

33	LOAD_FAST         'res'
36	LOAD_CONST        None
39	COMPARE_OP        'is'
42	POP_JUMP_IF_FALSE '49'

45	BREAK_LOOP        None
46	JUMP_FORWARD      '49'
49_0	COME_FROM         '46'

49	LOAD_FAST         'res'
52	LOAD_ATTR         'group'
55	LOAD_CONST        1
58	CALL_FUNCTION_1   None
61	STORE_FAST        'match'

64	LOAD_CONST        ' '
67	LOAD_ATTR         'join'
70	LOAD_FAST         'match'
73	LOAD_ATTR         'split'
76	LOAD_CONST        '_'
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_1   None
85	STORE_FAST        'match'

88	LOAD_FAST         'newline'
91	LOAD_FAST         'line'
94	LOAD_FAST         'pos'
97	LOAD_FAST         'res'
100	LOAD_ATTR         'start'
103	LOAD_CONST        0
106	CALL_FUNCTION_1   None
109	SLICE+3           None
110	BINARY_ADD        None
111	LOAD_GLOBAL       'mime_decode'
114	LOAD_FAST         'match'
117	CALL_FUNCTION_1   None
120	BINARY_ADD        None
121	STORE_FAST        'newline'

124	LOAD_FAST         'res'
127	LOAD_ATTR         'end'
130	LOAD_CONST        0
133	CALL_FUNCTION_1   None
136	STORE_FAST        'pos'
139	JUMP_BACK         '15'
142	POP_BLOCK         None
143_0	COME_FROM         '12'

143	LOAD_FAST         'newline'
146	LOAD_FAST         'line'
149	LOAD_FAST         'pos'
152	SLICE+1           None
153	BINARY_ADD        None
154	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 142


def unmimify_part--- This code section failed: ---

0	LOAD_CONST        None
3	STORE_FAST        'multipart'

6	LOAD_CONST        0
9	STORE_FAST        'quoted_printable'

12	LOAD_CONST        0
15	STORE_FAST        'is_base64'

18	LOAD_CONST        0
21	STORE_FAST        'is_repl'

24	LOAD_FAST         'ifile'
27	LOAD_ATTR         'boundary'
30	POP_JUMP_IF_FALSE '61'
33	LOAD_FAST         'ifile'
36	LOAD_ATTR         'boundary'
39	LOAD_CONST        2
42	SLICE+2           None
43	LOAD_GLOBAL       'QUOTE'
46	COMPARE_OP        '=='
49_0	COME_FROM         '30'
49	POP_JUMP_IF_FALSE '61'

52	LOAD_GLOBAL       'QUOTE'
55	STORE_FAST        'prefix'
58	JUMP_FORWARD      '67'

61	LOAD_CONST        ''
64	STORE_FAST        'prefix'
67_0	COME_FROM         '58'

67	LOAD_GLOBAL       'HeaderFile'
70	LOAD_FAST         'ifile'
73	CALL_FUNCTION_1   None
76	STORE_FAST        'hfile'

79	SETUP_LOOP        '349'

82	LOAD_FAST         'hfile'
85	LOAD_ATTR         'readline'
88	CALL_FUNCTION_0   None
91	STORE_FAST        'line'

94	LOAD_FAST         'line'
97	POP_JUMP_IF_TRUE  '104'

100	LOAD_CONST        None
103	RETURN_END_IF     None

104	LOAD_FAST         'prefix'
107	POP_JUMP_IF_FALSE '157'
110	LOAD_FAST         'line'
113	LOAD_GLOBAL       'len'
116	LOAD_FAST         'prefix'
119	CALL_FUNCTION_1   None
122	SLICE+2           None
123	LOAD_FAST         'prefix'
126	COMPARE_OP        '=='
129_0	COME_FROM         '107'
129	POP_JUMP_IF_FALSE '157'

132	LOAD_FAST         'line'
135	LOAD_GLOBAL       'len'
138	LOAD_FAST         'prefix'
141	CALL_FUNCTION_1   None
144	SLICE+1           None
145	STORE_FAST        'line'

148	LOAD_FAST         'prefix'
151	STORE_FAST        'pref'
154	JUMP_FORWARD      '163'

157	LOAD_CONST        ''
160	STORE_FAST        'pref'
163_0	COME_FROM         '154'

163	LOAD_GLOBAL       'mime_decode_header'
166	LOAD_FAST         'line'
169	CALL_FUNCTION_1   None
172	STORE_FAST        'line'

175	LOAD_GLOBAL       'qp'
178	LOAD_ATTR         'match'
181	LOAD_FAST         'line'
184	CALL_FUNCTION_1   None
187	POP_JUMP_IF_FALSE '202'

190	LOAD_CONST        1
193	STORE_FAST        'quoted_printable'

196	CONTINUE          '82'
199	JUMP_FORWARD      '202'
202_0	COME_FROM         '199'

202	LOAD_FAST         'decode_base64'
205	POP_JUMP_IF_FALSE '235'
208	LOAD_GLOBAL       'base64_re'
211	LOAD_ATTR         'match'
214	LOAD_FAST         'line'
217	CALL_FUNCTION_1   None
220_0	COME_FROM         '205'
220	POP_JUMP_IF_FALSE '235'

223	LOAD_CONST        1
226	STORE_FAST        'is_base64'

229	CONTINUE          '82'
232	JUMP_FORWARD      '235'
235_0	COME_FROM         '232'

235	LOAD_FAST         'ofile'
238	LOAD_ATTR         'write'
241	LOAD_FAST         'pref'
244	LOAD_FAST         'line'
247	BINARY_ADD        None
248	CALL_FUNCTION_1   None
251	POP_TOP           None

252	LOAD_FAST         'prefix'
255	UNARY_NOT         None
256	POP_JUMP_IF_FALSE '283'
259	LOAD_GLOBAL       'repl'
262	LOAD_ATTR         'match'
265	LOAD_FAST         'line'
268	CALL_FUNCTION_1   None
271_0	COME_FROM         '256'
271	POP_JUMP_IF_FALSE '283'

274	LOAD_CONST        1
277	STORE_FAST        'is_repl'
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'

283	LOAD_GLOBAL       'mp'
286	LOAD_ATTR         'match'
289	LOAD_FAST         'line'
292	CALL_FUNCTION_1   None
295	STORE_FAST        'mp_res'

298	LOAD_FAST         'mp_res'
301	POP_JUMP_IF_FALSE '326'

304	LOAD_CONST        '--'
307	LOAD_FAST         'mp_res'
310	LOAD_ATTR         'group'
313	LOAD_CONST        1
316	CALL_FUNCTION_1   None
319	BINARY_ADD        None
320	STORE_FAST        'multipart'
323	JUMP_FORWARD      '326'
326_0	COME_FROM         '323'

326	LOAD_GLOBAL       'he'
329	LOAD_ATTR         'match'
332	LOAD_FAST         'line'
335	CALL_FUNCTION_1   None
338	POP_JUMP_IF_FALSE '82'

341	BREAK_LOOP        None
342	JUMP_BACK         '82'
345	JUMP_BACK         '82'
348	POP_BLOCK         None
349_0	COME_FROM         '79'

349	LOAD_FAST         'is_repl'
352	POP_JUMP_IF_FALSE '376'
355	LOAD_FAST         'quoted_printable'
358	POP_JUMP_IF_TRUE  '367'
361	LOAD_FAST         'multipart'
364_0	COME_FROM         '352'
364_1	COME_FROM         '358'
364	POP_JUMP_IF_FALSE '376'

367	LOAD_CONST        0
370	STORE_FAST        'is_repl'
373	JUMP_FORWARD      '376'
376_0	COME_FROM         '373'

376	SETUP_LOOP        '835'

379	LOAD_FAST         'ifile'
382	LOAD_ATTR         'readline'
385	CALL_FUNCTION_0   None
388	STORE_FAST        'line'

391	LOAD_FAST         'line'
394	POP_JUMP_IF_TRUE  '401'

397	LOAD_CONST        None
400	RETURN_END_IF     None

401	LOAD_GLOBAL       're'
404	LOAD_ATTR         'sub'
407	LOAD_GLOBAL       'mime_head'
410	LOAD_CONST        '\\1'
413	LOAD_FAST         'line'
416	CALL_FUNCTION_3   None
419	STORE_FAST        'line'

422	LOAD_FAST         'prefix'
425	POP_JUMP_IF_FALSE '475'
428	LOAD_FAST         'line'
431	LOAD_GLOBAL       'len'
434	LOAD_FAST         'prefix'
437	CALL_FUNCTION_1   None
440	SLICE+2           None
441	LOAD_FAST         'prefix'
444	COMPARE_OP        '=='
447_0	COME_FROM         '425'
447	POP_JUMP_IF_FALSE '475'

450	LOAD_FAST         'line'
453	LOAD_GLOBAL       'len'
456	LOAD_FAST         'prefix'
459	CALL_FUNCTION_1   None
462	SLICE+1           None
463	STORE_FAST        'line'

466	LOAD_FAST         'prefix'
469	STORE_FAST        'pref'
472	JUMP_FORWARD      '481'

475	LOAD_CONST        ''
478	STORE_FAST        'pref'
481_0	COME_FROM         '472'

481	SETUP_LOOP        '633'
484	LOAD_FAST         'multipart'
487	POP_JUMP_IF_FALSE '632'

490	LOAD_FAST         'line'
493	LOAD_FAST         'multipart'
496	LOAD_CONST        '--\n'
499	BINARY_ADD        None
500	COMPARE_OP        '=='
503	POP_JUMP_IF_FALSE '539'

506	LOAD_FAST         'ofile'
509	LOAD_ATTR         'write'
512	LOAD_FAST         'pref'
515	LOAD_FAST         'line'
518	BINARY_ADD        None
519	CALL_FUNCTION_1   None
522	POP_TOP           None

523	LOAD_CONST        None
526	STORE_FAST        'multipart'

529	LOAD_CONST        None
532	STORE_FAST        'line'

535	BREAK_LOOP        None
536	JUMP_FORWARD      '539'
539_0	COME_FROM         '536'

539	LOAD_FAST         'line'
542	LOAD_FAST         'multipart'
545	LOAD_CONST        '\n'
548	BINARY_ADD        None
549	COMPARE_OP        '=='
552	POP_JUMP_IF_FALSE '628'

555	LOAD_FAST         'ofile'
558	LOAD_ATTR         'write'
561	LOAD_FAST         'pref'
564	LOAD_FAST         'line'
567	BINARY_ADD        None
568	CALL_FUNCTION_1   None
571	POP_TOP           None

572	LOAD_GLOBAL       'File'
575	LOAD_FAST         'ifile'
578	LOAD_FAST         'multipart'
581	CALL_FUNCTION_2   None
584	STORE_FAST        'nifile'

587	LOAD_GLOBAL       'unmimify_part'
590	LOAD_FAST         'nifile'
593	LOAD_FAST         'ofile'
596	LOAD_FAST         'decode_base64'
599	CALL_FUNCTION_3   None
602	POP_TOP           None

603	LOAD_FAST         'nifile'
606	LOAD_ATTR         'peek'
609	STORE_FAST        'line'

612	LOAD_FAST         'line'
615	POP_JUMP_IF_TRUE  '484'

618	BREAK_LOOP        None
619	JUMP_BACK         '484'

622	CONTINUE          '484'
625	JUMP_FORWARD      '628'
628_0	COME_FROM         '625'

628	BREAK_LOOP        None
629	JUMP_BACK         '484'
632	POP_BLOCK         None
633_0	COME_FROM         '481'

633	LOAD_FAST         'line'
636	POP_JUMP_IF_FALSE '756'
639	LOAD_FAST         'quoted_printable'
642_0	COME_FROM         '636'
642	POP_JUMP_IF_FALSE '756'

645	SETUP_LOOP        '741'
648	LOAD_FAST         'line'
651	LOAD_CONST        -2
654	SLICE+1           None
655	LOAD_CONST        '=\n'
658	COMPARE_OP        '=='
661	POP_JUMP_IF_FALSE '740'

664	LOAD_FAST         'line'
667	LOAD_CONST        -2
670	SLICE+2           None
671	STORE_FAST        'line'

674	LOAD_FAST         'ifile'
677	LOAD_ATTR         'readline'
680	CALL_FUNCTION_0   None
683	STORE_FAST        'newline'

686	LOAD_FAST         'newline'
689	LOAD_GLOBAL       'len'
692	LOAD_GLOBAL       'QUOTE'
695	CALL_FUNCTION_1   None
698	SLICE+2           None
699	LOAD_GLOBAL       'QUOTE'
702	COMPARE_OP        '=='
705	POP_JUMP_IF_FALSE '727'

708	LOAD_FAST         'newline'
711	LOAD_GLOBAL       'len'
714	LOAD_GLOBAL       'QUOTE'
717	CALL_FUNCTION_1   None
720	SLICE+1           None
721	STORE_FAST        'newline'
724	JUMP_FORWARD      '727'
727_0	COME_FROM         '724'

727	LOAD_FAST         'line'
730	LOAD_FAST         'newline'
733	BINARY_ADD        None
734	STORE_FAST        'line'
737	JUMP_BACK         '648'
740	POP_BLOCK         None
741_0	COME_FROM         '645'

741	LOAD_GLOBAL       'mime_decode'
744	LOAD_FAST         'line'
747	CALL_FUNCTION_1   None
750	STORE_FAST        'line'
753	JUMP_FORWARD      '756'
756_0	COME_FROM         '753'

756	LOAD_FAST         'line'
759	POP_JUMP_IF_FALSE '805'
762	LOAD_FAST         'is_base64'
765	POP_JUMP_IF_FALSE '805'
768	LOAD_FAST         'pref'
771	UNARY_NOT         None
772_0	COME_FROM         '759'
772_1	COME_FROM         '765'
772	POP_JUMP_IF_FALSE '805'

775	LOAD_CONST        -1
778	LOAD_CONST        None
781	IMPORT_NAME       'base64'
784	STORE_FAST        'base64'

787	LOAD_FAST         'base64'
790	LOAD_ATTR         'decodestring'
793	LOAD_FAST         'line'
796	CALL_FUNCTION_1   None
799	STORE_FAST        'line'
802	JUMP_FORWARD      '805'
805_0	COME_FROM         '802'

805	LOAD_FAST         'line'
808	POP_JUMP_IF_FALSE '379'

811	LOAD_FAST         'ofile'
814	LOAD_ATTR         'write'
817	LOAD_FAST         'pref'
820	LOAD_FAST         'line'
823	BINARY_ADD        None
824	CALL_FUNCTION_1   None
827	POP_TOP           None
828	JUMP_BACK         '379'
831	JUMP_BACK         '379'
834	POP_BLOCK         None
835_0	COME_FROM         '376'
835	LOAD_CONST        None
838	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 348


def unmimify(infile, outfile, decode_base64 = 0):
    """Convert quoted-printable parts of a MIME mail message to 8bit."""
    if type(infile) == type(''):
        ifile = open(infile)
        if type(outfile) == type('') and infile == outfile:
            import os
            d, f = os.path.split(infile)
            os.rename(infile, os.path.join(d, ',' + f))
    else:
        ifile = infile
    if type(outfile) == type(''):
        ofile = open(outfile, 'w')
    else:
        ofile = outfile
    nifile = File(ifile, None)
    unmimify_part(nifile, ofile, decode_base64)
    ofile.flush()
    return


mime_char = re.compile('[=\x7f-\xff]')
mime_header_char = re.compile('[=?\x7f-\xff]')

def mime_encode--- This code section failed: ---

0	LOAD_FAST         'header'
3	POP_JUMP_IF_FALSE '15'

6	LOAD_GLOBAL       'mime_header_char'
9	STORE_FAST        'reg'
12	JUMP_FORWARD      '21'

15	LOAD_GLOBAL       'mime_char'
18	STORE_FAST        'reg'
21_0	COME_FROM         '12'

21	LOAD_CONST        ''
24	STORE_FAST        'newline'

27	LOAD_CONST        0
30	STORE_FAST        'pos'

33	LOAD_GLOBAL       'len'
36	LOAD_FAST         'line'
39	CALL_FUNCTION_1   None
42	LOAD_CONST        5
45	COMPARE_OP        '>='
48	POP_JUMP_IF_FALSE '98'
51	LOAD_FAST         'line'
54	LOAD_CONST        5
57	SLICE+2           None
58	LOAD_CONST        'From '
61	COMPARE_OP        '=='
64_0	COME_FROM         '48'
64	POP_JUMP_IF_FALSE '98'

67	LOAD_CONST        '=%02x'
70	LOAD_GLOBAL       'ord'
73	LOAD_CONST        'F'
76	CALL_FUNCTION_1   None
79	BINARY_MODULO     None
80	LOAD_ATTR         'upper'
83	CALL_FUNCTION_0   None
86	STORE_FAST        'newline'

89	LOAD_CONST        1
92	STORE_FAST        'pos'
95	JUMP_FORWARD      '98'
98_0	COME_FROM         '95'

98	SETUP_LOOP        '209'

101	LOAD_FAST         'reg'
104	LOAD_ATTR         'search'
107	LOAD_FAST         'line'
110	LOAD_FAST         'pos'
113	CALL_FUNCTION_2   None
116	STORE_FAST        'res'

119	LOAD_FAST         'res'
122	LOAD_CONST        None
125	COMPARE_OP        'is'
128	POP_JUMP_IF_FALSE '135'

131	BREAK_LOOP        None
132	JUMP_FORWARD      '135'
135_0	COME_FROM         '132'

135	LOAD_FAST         'newline'
138	LOAD_FAST         'line'
141	LOAD_FAST         'pos'
144	LOAD_FAST         'res'
147	LOAD_ATTR         'start'
150	LOAD_CONST        0
153	CALL_FUNCTION_1   None
156	SLICE+3           None
157	BINARY_ADD        None

158	LOAD_CONST        '=%02x'
161	LOAD_GLOBAL       'ord'
164	LOAD_FAST         'res'
167	LOAD_ATTR         'group'
170	LOAD_CONST        0
173	CALL_FUNCTION_1   None
176	CALL_FUNCTION_1   None
179	BINARY_MODULO     None
180	LOAD_ATTR         'upper'
183	CALL_FUNCTION_0   None
186	BINARY_ADD        None
187	STORE_FAST        'newline'

190	LOAD_FAST         'res'
193	LOAD_ATTR         'end'
196	LOAD_CONST        0
199	CALL_FUNCTION_1   None
202	STORE_FAST        'pos'
205	JUMP_BACK         '101'
208	POP_BLOCK         None
209_0	COME_FROM         '98'

209	LOAD_FAST         'newline'
212	LOAD_FAST         'line'
215	LOAD_FAST         'pos'
218	SLICE+1           None
219	BINARY_ADD        None
220	STORE_FAST        'line'

223	LOAD_CONST        ''
226	STORE_FAST        'newline'

229	SETUP_LOOP        '351'
232	LOAD_GLOBAL       'len'
235	LOAD_FAST         'line'
238	CALL_FUNCTION_1   None
241	LOAD_CONST        75
244	COMPARE_OP        '>='
247	POP_JUMP_IF_FALSE '350'

250	LOAD_CONST        73
253	STORE_FAST        'i'

256	SETUP_LOOP        '309'
259	LOAD_FAST         'line'
262	LOAD_FAST         'i'
265	BINARY_SUBSCR     None
266	LOAD_CONST        '='
269	COMPARE_OP        '=='
272	POP_JUMP_IF_TRUE  '295'
275	LOAD_FAST         'line'
278	LOAD_FAST         'i'
281	LOAD_CONST        1
284	BINARY_SUBTRACT   None
285	BINARY_SUBSCR     None
286	LOAD_CONST        '='
289	COMPARE_OP        '=='
292_0	COME_FROM         '272'
292	POP_JUMP_IF_FALSE '308'

295	LOAD_FAST         'i'
298	LOAD_CONST        1
301	BINARY_SUBTRACT   None
302	STORE_FAST        'i'
305	JUMP_BACK         '259'
308	POP_BLOCK         None
309_0	COME_FROM         '256'

309	LOAD_FAST         'i'
312	LOAD_CONST        1
315	BINARY_ADD        None
316	STORE_FAST        'i'

319	LOAD_FAST         'newline'
322	LOAD_FAST         'line'
325	LOAD_FAST         'i'
328	SLICE+2           None
329	BINARY_ADD        None
330	LOAD_CONST        '=\n'
333	BINARY_ADD        None
334	STORE_FAST        'newline'

337	LOAD_FAST         'line'
340	LOAD_FAST         'i'
343	SLICE+1           None
344	STORE_FAST        'line'
347	JUMP_BACK         '232'
350	POP_BLOCK         None
351_0	COME_FROM         '229'

351	LOAD_FAST         'newline'
354	LOAD_FAST         'line'
357	BINARY_ADD        None
358	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 208


mime_header = re.compile('([ \t(]|^)([-a-zA-Z0-9_+]*[\x7f-\xff][-a-zA-Z0-9_+\x7f-\xff]*)(?=[ \t)]|\n)')

def mime_encode_header--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'newline'

6	LOAD_CONST        0
9	STORE_FAST        'pos'

12	SETUP_LOOP        '136'

15	LOAD_GLOBAL       'mime_header'
18	LOAD_ATTR         'search'
21	LOAD_FAST         'line'
24	LOAD_FAST         'pos'
27	CALL_FUNCTION_2   None
30	STORE_FAST        'res'

33	LOAD_FAST         'res'
36	LOAD_CONST        None
39	COMPARE_OP        'is'
42	POP_JUMP_IF_FALSE '49'

45	BREAK_LOOP        None
46	JUMP_FORWARD      '49'
49_0	COME_FROM         '46'

49	LOAD_CONST        '%s%s%s=?%s?Q?%s?='

52	LOAD_FAST         'newline'
55	LOAD_FAST         'line'
58	LOAD_FAST         'pos'
61	LOAD_FAST         'res'
64	LOAD_ATTR         'start'
67	LOAD_CONST        0
70	CALL_FUNCTION_1   None
73	SLICE+3           None
74	LOAD_FAST         'res'
77	LOAD_ATTR         'group'
80	LOAD_CONST        1
83	CALL_FUNCTION_1   None

86	LOAD_GLOBAL       'CHARSET'
89	LOAD_GLOBAL       'mime_encode'
92	LOAD_FAST         'res'
95	LOAD_ATTR         'group'
98	LOAD_CONST        2
101	CALL_FUNCTION_1   None
104	LOAD_CONST        1
107	CALL_FUNCTION_2   None
110	BUILD_TUPLE_5     None
113	BINARY_MODULO     None
114	STORE_FAST        'newline'

117	LOAD_FAST         'res'
120	LOAD_ATTR         'end'
123	LOAD_CONST        0
126	CALL_FUNCTION_1   None
129	STORE_FAST        'pos'
132	JUMP_BACK         '15'
135	POP_BLOCK         None
136_0	COME_FROM         '12'

136	LOAD_FAST         'newline'
139	LOAD_FAST         'line'
142	LOAD_FAST         'pos'
145	SLICE+1           None
146	BINARY_ADD        None
147	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 135


mv = re.compile('^mime-version:', re.I)
cte = re.compile('^content-transfer-encoding:', re.I)
iso_char = re.compile('[\x7f-\xff]')

def mimify_part--- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'has_cte'
7	DUP_TOP           None
8	STORE_FAST        'is_qp'
11	STORE_FAST        'is_base64'

14	LOAD_CONST        None
17	STORE_FAST        'multipart'

20	LOAD_CONST        0
23	DUP_TOP           None
24	STORE_FAST        'must_quote_body'
27	DUP_TOP           None
28	STORE_FAST        'must_quote_header'
31	STORE_FAST        'has_iso_chars'

34	BUILD_LIST_0      None
37	STORE_FAST        'header'

40	LOAD_CONST        ''
43	STORE_FAST        'header_end'

46	BUILD_LIST_0      None
49	STORE_FAST        'message'

52	LOAD_CONST        ''
55	STORE_FAST        'message_end'

58	LOAD_GLOBAL       'HeaderFile'
61	LOAD_FAST         'ifile'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'hfile'

70	SETUP_LOOP        '307'

73	LOAD_FAST         'hfile'
76	LOAD_ATTR         'readline'
79	CALL_FUNCTION_0   None
82	STORE_FAST        'line'

85	LOAD_FAST         'line'
88	POP_JUMP_IF_TRUE  '95'

91	BREAK_LOOP        None
92	JUMP_FORWARD      '95'
95_0	COME_FROM         '92'

95	LOAD_FAST         'must_quote_header'
98	UNARY_NOT         None
99	POP_JUMP_IF_FALSE '126'
102	LOAD_GLOBAL       'iso_char'
105	LOAD_ATTR         'search'
108	LOAD_FAST         'line'
111	CALL_FUNCTION_1   None
114_0	COME_FROM         '99'
114	POP_JUMP_IF_FALSE '126'

117	LOAD_CONST        1
120	STORE_FAST        'must_quote_header'
123	JUMP_FORWARD      '126'
126_0	COME_FROM         '123'

126	LOAD_GLOBAL       'mv'
129	LOAD_ATTR         'match'
132	LOAD_FAST         'line'
135	CALL_FUNCTION_1   None
138	POP_JUMP_IF_FALSE '150'

141	LOAD_CONST        1
144	STORE_FAST        'is_mime'
147	JUMP_FORWARD      '150'
150_0	COME_FROM         '147'

150	LOAD_GLOBAL       'cte'
153	LOAD_ATTR         'match'
156	LOAD_FAST         'line'
159	CALL_FUNCTION_1   None
162	POP_JUMP_IF_FALSE '222'

165	LOAD_CONST        1
168	STORE_FAST        'has_cte'

171	LOAD_GLOBAL       'qp'
174	LOAD_ATTR         'match'
177	LOAD_FAST         'line'
180	CALL_FUNCTION_1   None
183	POP_JUMP_IF_FALSE '195'

186	LOAD_CONST        1
189	STORE_FAST        'is_qp'
192	JUMP_ABSOLUTE     '222'

195	LOAD_GLOBAL       'base64_re'
198	LOAD_ATTR         'match'
201	LOAD_FAST         'line'
204	CALL_FUNCTION_1   None
207	POP_JUMP_IF_FALSE '222'

210	LOAD_CONST        1
213	STORE_FAST        'is_base64'
216	JUMP_ABSOLUTE     '222'
219	JUMP_FORWARD      '222'
222_0	COME_FROM         '219'

222	LOAD_GLOBAL       'mp'
225	LOAD_ATTR         'match'
228	LOAD_FAST         'line'
231	CALL_FUNCTION_1   None
234	STORE_FAST        'mp_res'

237	LOAD_FAST         'mp_res'
240	POP_JUMP_IF_FALSE '265'

243	LOAD_CONST        '--'
246	LOAD_FAST         'mp_res'
249	LOAD_ATTR         'group'
252	LOAD_CONST        1
255	CALL_FUNCTION_1   None
258	BINARY_ADD        None
259	STORE_FAST        'multipart'
262	JUMP_FORWARD      '265'
265_0	COME_FROM         '262'

265	LOAD_GLOBAL       'he'
268	LOAD_ATTR         'match'
271	LOAD_FAST         'line'
274	CALL_FUNCTION_1   None
277	POP_JUMP_IF_FALSE '290'

280	LOAD_FAST         'line'
283	STORE_FAST        'header_end'

286	BREAK_LOOP        None
287	JUMP_FORWARD      '290'
290_0	COME_FROM         '287'

290	LOAD_FAST         'header'
293	LOAD_ATTR         'append'
296	LOAD_FAST         'line'
299	CALL_FUNCTION_1   None
302	POP_TOP           None
303	JUMP_BACK         '73'
306	POP_BLOCK         None
307_0	COME_FROM         '70'

307	SETUP_LOOP        '625'

310	LOAD_FAST         'ifile'
313	LOAD_ATTR         'readline'
316	CALL_FUNCTION_0   None
319	STORE_FAST        'line'

322	LOAD_FAST         'line'
325	POP_JUMP_IF_TRUE  '332'

328	BREAK_LOOP        None
329	JUMP_FORWARD      '332'
332_0	COME_FROM         '329'

332	LOAD_FAST         'multipart'
335	POP_JUMP_IF_FALSE '393'

338	LOAD_FAST         'line'
341	LOAD_FAST         'multipart'
344	LOAD_CONST        '--\n'
347	BINARY_ADD        None
348	COMPARE_OP        '=='
351	POP_JUMP_IF_FALSE '364'

354	LOAD_FAST         'line'
357	STORE_FAST        'message_end'

360	BREAK_LOOP        None
361	JUMP_FORWARD      '364'
364_0	COME_FROM         '361'

364	LOAD_FAST         'line'
367	LOAD_FAST         'multipart'
370	LOAD_CONST        '\n'
373	BINARY_ADD        None
374	COMPARE_OP        '=='
377	POP_JUMP_IF_FALSE '393'

380	LOAD_FAST         'line'
383	STORE_FAST        'message_end'

386	BREAK_LOOP        None
387	JUMP_ABSOLUTE     '393'
390	JUMP_FORWARD      '393'
393_0	COME_FROM         '390'

393	LOAD_FAST         'is_base64'
396	POP_JUMP_IF_FALSE '418'

399	LOAD_FAST         'message'
402	LOAD_ATTR         'append'
405	LOAD_FAST         'line'
408	CALL_FUNCTION_1   None
411	POP_TOP           None

412	CONTINUE          '310'
415	JUMP_FORWARD      '418'
418_0	COME_FROM         '415'

418	LOAD_FAST         'is_qp'
421	POP_JUMP_IF_FALSE '535'

424	SETUP_LOOP        '520'
427	LOAD_FAST         'line'
430	LOAD_CONST        -2
433	SLICE+1           None
434	LOAD_CONST        '=\n'
437	COMPARE_OP        '=='
440	POP_JUMP_IF_FALSE '519'

443	LOAD_FAST         'line'
446	LOAD_CONST        -2
449	SLICE+2           None
450	STORE_FAST        'line'

453	LOAD_FAST         'ifile'
456	LOAD_ATTR         'readline'
459	CALL_FUNCTION_0   None
462	STORE_FAST        'newline'

465	LOAD_FAST         'newline'
468	LOAD_GLOBAL       'len'
471	LOAD_GLOBAL       'QUOTE'
474	CALL_FUNCTION_1   None
477	SLICE+2           None
478	LOAD_GLOBAL       'QUOTE'
481	COMPARE_OP        '=='
484	POP_JUMP_IF_FALSE '506'

487	LOAD_FAST         'newline'
490	LOAD_GLOBAL       'len'
493	LOAD_GLOBAL       'QUOTE'
496	CALL_FUNCTION_1   None
499	SLICE+1           None
500	STORE_FAST        'newline'
503	JUMP_FORWARD      '506'
506_0	COME_FROM         '503'

506	LOAD_FAST         'line'
509	LOAD_FAST         'newline'
512	BINARY_ADD        None
513	STORE_FAST        'line'
516	JUMP_BACK         '427'
519	POP_BLOCK         None
520_0	COME_FROM         '424'

520	LOAD_GLOBAL       'mime_decode'
523	LOAD_FAST         'line'
526	CALL_FUNCTION_1   None
529	STORE_FAST        'line'
532	JUMP_FORWARD      '535'
535_0	COME_FROM         '532'

535	LOAD_FAST         'message'
538	LOAD_ATTR         'append'
541	LOAD_FAST         'line'
544	CALL_FUNCTION_1   None
547	POP_TOP           None

548	LOAD_FAST         'has_iso_chars'
551	POP_JUMP_IF_TRUE  '585'

554	LOAD_GLOBAL       'iso_char'
557	LOAD_ATTR         'search'
560	LOAD_FAST         'line'
563	CALL_FUNCTION_1   None
566	POP_JUMP_IF_FALSE '585'

569	LOAD_CONST        1
572	DUP_TOP           None
573	STORE_FAST        'has_iso_chars'
576	STORE_FAST        'must_quote_body'
579	JUMP_ABSOLUTE     '585'
582	JUMP_FORWARD      '585'
585_0	COME_FROM         '582'

585	LOAD_FAST         'must_quote_body'
588	POP_JUMP_IF_TRUE  '310'

591	LOAD_GLOBAL       'len'
594	LOAD_FAST         'line'
597	CALL_FUNCTION_1   None
600	LOAD_GLOBAL       'MAXLEN'
603	COMPARE_OP        '>'
606	POP_JUMP_IF_FALSE '621'

609	LOAD_CONST        1
612	STORE_FAST        'must_quote_body'
615	JUMP_ABSOLUTE     '621'
618	JUMP_BACK         '310'
621	JUMP_BACK         '310'
624	POP_BLOCK         None
625_0	COME_FROM         '307'

625	SETUP_LOOP        '876'
628	LOAD_FAST         'header'
631	GET_ITER          None
632	FOR_ITER          '875'
635	STORE_FAST        'line'

638	LOAD_FAST         'must_quote_header'
641	POP_JUMP_IF_FALSE '659'

644	LOAD_GLOBAL       'mime_encode_header'
647	LOAD_FAST         'line'
650	CALL_FUNCTION_1   None
653	STORE_FAST        'line'
656	JUMP_FORWARD      '659'
659_0	COME_FROM         '656'

659	LOAD_GLOBAL       'chrset'
662	LOAD_ATTR         'match'
665	LOAD_FAST         'line'
668	CALL_FUNCTION_1   None
671	STORE_FAST        'chrset_res'

674	LOAD_FAST         'chrset_res'
677	POP_JUMP_IF_FALSE '781'

680	LOAD_FAST         'has_iso_chars'
683	POP_JUMP_IF_FALSE '756'

686	LOAD_FAST         'chrset_res'
689	LOAD_ATTR         'group'
692	LOAD_CONST        2
695	CALL_FUNCTION_1   None
698	LOAD_ATTR         'lower'
701	CALL_FUNCTION_0   None
704	LOAD_CONST        'us-ascii'
707	COMPARE_OP        '=='
710	POP_JUMP_IF_FALSE '778'

713	LOAD_CONST        '%s%s%s'
716	LOAD_FAST         'chrset_res'
719	LOAD_ATTR         'group'
722	LOAD_CONST        1
725	CALL_FUNCTION_1   None

728	LOAD_GLOBAL       'CHARSET'

731	LOAD_FAST         'chrset_res'
734	LOAD_ATTR         'group'
737	LOAD_CONST        3
740	CALL_FUNCTION_1   None
743	BUILD_TUPLE_3     None
746	BINARY_MODULO     None
747	STORE_FAST        'line'
750	JUMP_ABSOLUTE     '778'
753	JUMP_ABSOLUTE     '781'

756	LOAD_CONST        '%sus-ascii%s'
759	LOAD_FAST         'chrset_res'
762	LOAD_ATTR         'group'
765	LOAD_CONST        1
768	LOAD_CONST        3
771	CALL_FUNCTION_2   None
774	BINARY_MODULO     None
775	STORE_FAST        'line'
778	JUMP_FORWARD      '781'
781_0	COME_FROM         '778'

781	LOAD_FAST         'has_cte'
784	POP_JUMP_IF_FALSE '859'
787	LOAD_GLOBAL       'cte'
790	LOAD_ATTR         'match'
793	LOAD_FAST         'line'
796	CALL_FUNCTION_1   None
799_0	COME_FROM         '784'
799	POP_JUMP_IF_FALSE '859'

802	LOAD_CONST        'Content-Transfer-Encoding: '
805	STORE_FAST        'line'

808	LOAD_FAST         'is_base64'
811	POP_JUMP_IF_FALSE '827'

814	LOAD_FAST         'line'
817	LOAD_CONST        'base64\n'
820	BINARY_ADD        None
821	STORE_FAST        'line'
824	JUMP_ABSOLUTE     '859'

827	LOAD_FAST         'must_quote_body'
830	POP_JUMP_IF_FALSE '846'

833	LOAD_FAST         'line'
836	LOAD_CONST        'quoted-printable\n'
839	BINARY_ADD        None
840	STORE_FAST        'line'
843	JUMP_ABSOLUTE     '859'

846	LOAD_FAST         'line'
849	LOAD_CONST        '7bit\n'
852	BINARY_ADD        None
853	STORE_FAST        'line'
856	JUMP_FORWARD      '859'
859_0	COME_FROM         '856'

859	LOAD_FAST         'ofile'
862	LOAD_ATTR         'write'
865	LOAD_FAST         'line'
868	CALL_FUNCTION_1   None
871	POP_TOP           None
872	JUMP_BACK         '632'
875	POP_BLOCK         None
876_0	COME_FROM         '625'

876	LOAD_FAST         'must_quote_header'
879	POP_JUMP_IF_TRUE  '888'
882	LOAD_FAST         'must_quote_body'
885_0	COME_FROM         '879'
885	POP_JUMP_IF_FALSE '963'
888	LOAD_FAST         'is_mime'
891	UNARY_NOT         None
892_0	COME_FROM         '885'
892	POP_JUMP_IF_FALSE '963'

895	LOAD_FAST         'ofile'
898	LOAD_ATTR         'write'
901	LOAD_CONST        'Mime-Version: 1.0\n'
904	CALL_FUNCTION_1   None
907	POP_TOP           None

908	LOAD_FAST         'ofile'
911	LOAD_ATTR         'write'
914	LOAD_CONST        'Content-Type: text/plain; '
917	CALL_FUNCTION_1   None
920	POP_TOP           None

921	LOAD_FAST         'has_iso_chars'
924	POP_JUMP_IF_FALSE '947'

927	LOAD_FAST         'ofile'
930	LOAD_ATTR         'write'
933	LOAD_CONST        'charset="%s"\n'
936	LOAD_GLOBAL       'CHARSET'
939	BINARY_MODULO     None
940	CALL_FUNCTION_1   None
943	POP_TOP           None
944	JUMP_ABSOLUTE     '963'

947	LOAD_FAST         'ofile'
950	LOAD_ATTR         'write'
953	LOAD_CONST        'charset="us-ascii"\n'
956	CALL_FUNCTION_1   None
959	POP_TOP           None
960	JUMP_FORWARD      '963'
963_0	COME_FROM         '960'

963	LOAD_FAST         'must_quote_body'
966	POP_JUMP_IF_FALSE '992'
969	LOAD_FAST         'has_cte'
972	UNARY_NOT         None
973_0	COME_FROM         '966'
973	POP_JUMP_IF_FALSE '992'

976	LOAD_FAST         'ofile'
979	LOAD_ATTR         'write'
982	LOAD_CONST        'Content-Transfer-Encoding: quoted-printable\n'
985	CALL_FUNCTION_1   None
988	POP_TOP           None
989	JUMP_FORWARD      '992'
992_0	COME_FROM         '989'

992	LOAD_FAST         'ofile'
995	LOAD_ATTR         'write'
998	LOAD_FAST         'header_end'
1001	CALL_FUNCTION_1   None
1004	POP_TOP           None

1005	SETUP_LOOP        '1059'
1008	LOAD_FAST         'message'
1011	GET_ITER          None
1012	FOR_ITER          '1058'
1015	STORE_FAST        'line'

1018	LOAD_FAST         'must_quote_body'
1021	POP_JUMP_IF_FALSE '1042'

1024	LOAD_GLOBAL       'mime_encode'
1027	LOAD_FAST         'line'
1030	LOAD_CONST        0
1033	CALL_FUNCTION_2   None
1036	STORE_FAST        'line'
1039	JUMP_FORWARD      '1042'
1042_0	COME_FROM         '1039'

1042	LOAD_FAST         'ofile'
1045	LOAD_ATTR         'write'
1048	LOAD_FAST         'line'
1051	CALL_FUNCTION_1   None
1054	POP_TOP           None
1055	JUMP_BACK         '1012'
1058	POP_BLOCK         None
1059_0	COME_FROM         '1005'

1059	LOAD_FAST         'ofile'
1062	LOAD_ATTR         'write'
1065	LOAD_FAST         'message_end'
1068	CALL_FUNCTION_1   None
1071	POP_TOP           None

1072	LOAD_FAST         'message_end'
1075	STORE_FAST        'line'

1078	SETUP_LOOP        '1327'
1081	LOAD_FAST         'multipart'
1084	POP_JUMP_IF_FALSE '1326'

1087	LOAD_FAST         'line'
1090	LOAD_FAST         'multipart'
1093	LOAD_CONST        '--\n'
1096	BINARY_ADD        None
1097	COMPARE_OP        '=='
1100	POP_JUMP_IF_FALSE '1172'

1103	SETUP_LOOP        '1172'

1106	LOAD_FAST         'ifile'
1109	LOAD_ATTR         'readline'
1112	CALL_FUNCTION_0   None
1115	STORE_FAST        'line'

1118	LOAD_FAST         'line'
1121	POP_JUMP_IF_TRUE  '1128'

1124	LOAD_CONST        None
1127	RETURN_END_IF     None

1128	LOAD_FAST         'must_quote_body'
1131	POP_JUMP_IF_FALSE '1152'

1134	LOAD_GLOBAL       'mime_encode'
1137	LOAD_FAST         'line'
1140	LOAD_CONST        0
1143	CALL_FUNCTION_2   None
1146	STORE_FAST        'line'
1149	JUMP_FORWARD      '1152'
1152_0	COME_FROM         '1149'

1152	LOAD_FAST         'ofile'
1155	LOAD_ATTR         'write'
1158	LOAD_FAST         'line'
1161	CALL_FUNCTION_1   None
1164	POP_TOP           None
1165	JUMP_BACK         '1106'
1168	POP_BLOCK         None
1169_0	COME_FROM         '1103'
1169	JUMP_FORWARD      '1172'
1172_0	COME_FROM         '1169'

1172	LOAD_FAST         'line'
1175	LOAD_FAST         'multipart'
1178	LOAD_CONST        '\n'
1181	BINARY_ADD        None
1182	COMPARE_OP        '=='
1185	POP_JUMP_IF_FALSE '1257'

1188	LOAD_GLOBAL       'File'
1191	LOAD_FAST         'ifile'
1194	LOAD_FAST         'multipart'
1197	CALL_FUNCTION_2   None
1200	STORE_FAST        'nifile'

1203	LOAD_GLOBAL       'mimify_part'
1206	LOAD_FAST         'nifile'
1209	LOAD_FAST         'ofile'
1212	LOAD_CONST        1
1215	CALL_FUNCTION_3   None
1218	POP_TOP           None

1219	LOAD_FAST         'nifile'
1222	LOAD_ATTR         'peek'
1225	STORE_FAST        'line'

1228	LOAD_FAST         'line'
1231	POP_JUMP_IF_TRUE  '1238'

1234	BREAK_LOOP        None
1235	JUMP_FORWARD      '1238'
1238_0	COME_FROM         '1235'

1238	LOAD_FAST         'ofile'
1241	LOAD_ATTR         'write'
1244	LOAD_FAST         'line'
1247	CALL_FUNCTION_1   None
1250	POP_TOP           None

1251	CONTINUE          '1081'
1254	JUMP_FORWARD      '1257'
1257_0	COME_FROM         '1254'

1257	SETUP_LOOP        '1323'

1260	LOAD_FAST         'ifile'
1263	LOAD_ATTR         'readline'
1266	CALL_FUNCTION_0   None
1269	STORE_FAST        'line'

1272	LOAD_FAST         'line'
1275	POP_JUMP_IF_TRUE  '1282'

1278	LOAD_CONST        None
1281	RETURN_END_IF     None

1282	LOAD_FAST         'must_quote_body'
1285	POP_JUMP_IF_FALSE '1306'

1288	LOAD_GLOBAL       'mime_encode'
1291	LOAD_FAST         'line'
1294	LOAD_CONST        0
1297	CALL_FUNCTION_2   None
1300	STORE_FAST        'line'
1303	JUMP_FORWARD      '1306'
1306_0	COME_FROM         '1303'

1306	LOAD_FAST         'ofile'
1309	LOAD_ATTR         'write'
1312	LOAD_FAST         'line'
1315	CALL_FUNCTION_1   None
1318	POP_TOP           None
1319	JUMP_BACK         '1260'
1322	POP_BLOCK         None
1323_0	COME_FROM         '1257'
1323	JUMP_BACK         '1081'
1326	POP_BLOCK         None
1327_0	COME_FROM         '1078'
1327	LOAD_CONST        None
1330	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 306


def mimify(infile, outfile):
    """Convert 8bit parts of a MIME mail message to quoted-printable."""
    if type(infile) == type(''):
        ifile = open(infile)
        if type(outfile) == type('') and infile == outfile:
            import os
            d, f = os.path.split(infile)
            os.rename(infile, os.path.join(d, ',' + f))
    else:
        ifile = infile
    if type(outfile) == type(''):
        ofile = open(outfile, 'w')
    else:
        ofile = outfile
    nifile = File(ifile, None)
    mimify_part(nifile, ofile, 0)
    ofile.flush()
    return


import sys
if __name__ == '__main__' or len(sys.argv) > 0 and sys.argv[0] == 'mimify':
    import getopt
    usage = 'Usage: mimify [-l len] -[ed] [infile [outfile]]'
    decode_base64 = 0
    opts, args = getopt.getopt(sys.argv[1:], 'l:edb')
    if len(args) not in (0, 1, 2):
        print usage
        sys.exit(1)
    if (('-e', '') in opts) == (('-d', '') in opts) or ('-b', '') in opts and ('-d', '') not in opts:
        print usage
        sys.exit(1)
    for o, a in opts:
        if o == '-e':
            encode = mimify
        elif o == '-d':
            encode = unmimify
        elif o == '-l':
            try:
                MAXLEN = int(a)
            except (ValueError, OverflowError):
                print usage
                sys.exit(1)

        elif o == '-b':
            decode_base64 = 1

    if len(args) == 0:
        encode_args = (sys.stdin, sys.stdout)
    elif len(args) == 1:
        encode_args = (args[0], sys.stdout)
    else:
        encode_args = (args[0], args[1])
    if decode_base64:
        encode_args = encode_args + (decode_base64,)
    encode(*encode_args)