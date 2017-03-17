# Embedded file name: scripts/common/Lib/encodings/punycode.py
""" Codec for the Punicode encoding, as specified in RFC 3492

Written by Martin v. L\xf6wis.
"""
import codecs

def segregate(str):
    """3.1 Basic code point segregation"""
    base = []
    extended = {}
    for c in str:
        if ord(c) < 128:
            base.append(c)
        else:
            extended[c] = 1

    extended = extended.keys()
    extended.sort()
    return (''.join(base).encode('ascii'), extended)


def selective_len(str, max):
    """Return the length of str, considering only characters below max."""
    res = 0
    for c in str:
        if ord(c) < max:
            res += 1

    return res


def selective_find--- This code section failed: ---

0	LOAD_GLOBAL       'len'
3	LOAD_FAST         'str'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'l'

12	SETUP_LOOP        '106'

15	LOAD_FAST         'pos'
18	LOAD_CONST        1
21	INPLACE_ADD       None
22	STORE_FAST        'pos'

25	LOAD_FAST         'pos'
28	LOAD_FAST         'l'
31	COMPARE_OP        '=='
34	POP_JUMP_IF_FALSE '41'

37	LOAD_CONST        (-1, -1)
40	RETURN_END_IF     None

41	LOAD_FAST         'str'
44	LOAD_FAST         'pos'
47	BINARY_SUBSCR     None
48	STORE_FAST        'c'

51	LOAD_FAST         'c'
54	LOAD_FAST         'char'
57	COMPARE_OP        '=='
60	POP_JUMP_IF_FALSE '77'

63	LOAD_FAST         'index'
66	LOAD_CONST        1
69	BINARY_ADD        None
70	LOAD_FAST         'pos'
73	BUILD_TUPLE_2     None
76	RETURN_END_IF     None

77	LOAD_FAST         'c'
80	LOAD_FAST         'char'
83	COMPARE_OP        '<'
86	POP_JUMP_IF_FALSE '15'

89	LOAD_FAST         'index'
92	LOAD_CONST        1
95	INPLACE_ADD       None
96	STORE_FAST        'index'
99	JUMP_BACK         '15'
102	JUMP_BACK         '15'
105	POP_BLOCK         None
106_0	COME_FROM         '12'

Syntax error at or near `POP_BLOCK' token at offset 105


def insertion_unsort--- This code section failed: ---

0	LOAD_CONST        128
3	STORE_FAST        'oldchar'

6	BUILD_LIST_0      None
9	STORE_FAST        'result'

12	LOAD_CONST        -1
15	STORE_FAST        'oldindex'

18	SETUP_LOOP        '189'
21	LOAD_FAST         'extended'
24	GET_ITER          None
25	FOR_ITER          '188'
28	STORE_FAST        'c'

31	LOAD_CONST        -1
34	DUP_TOP           None
35	STORE_FAST        'index'
38	STORE_FAST        'pos'

41	LOAD_GLOBAL       'ord'
44	LOAD_FAST         'c'
47	CALL_FUNCTION_1   None
50	STORE_FAST        'char'

53	LOAD_GLOBAL       'selective_len'
56	LOAD_FAST         'str'
59	LOAD_FAST         'char'
62	CALL_FUNCTION_2   None
65	STORE_FAST        'curlen'

68	LOAD_FAST         'curlen'
71	LOAD_CONST        1
74	BINARY_ADD        None
75	LOAD_FAST         'char'
78	LOAD_FAST         'oldchar'
81	BINARY_SUBTRACT   None
82	BINARY_MULTIPLY   None
83	STORE_FAST        'delta'

86	SETUP_LOOP        '179'

89	LOAD_GLOBAL       'selective_find'
92	LOAD_FAST         'str'
95	LOAD_FAST         'c'
98	LOAD_FAST         'index'
101	LOAD_FAST         'pos'
104	CALL_FUNCTION_4   None
107	UNPACK_SEQUENCE_2 None
110	STORE_FAST        'index'
113	STORE_FAST        'pos'

116	LOAD_FAST         'index'
119	LOAD_CONST        -1
122	COMPARE_OP        '=='
125	POP_JUMP_IF_FALSE '132'

128	BREAK_LOOP        None
129	JUMP_FORWARD      '132'
132_0	COME_FROM         '129'

132	LOAD_FAST         'delta'
135	LOAD_FAST         'index'
138	LOAD_FAST         'oldindex'
141	BINARY_SUBTRACT   None
142	INPLACE_ADD       None
143	STORE_FAST        'delta'

146	LOAD_FAST         'result'
149	LOAD_ATTR         'append'
152	LOAD_FAST         'delta'
155	LOAD_CONST        1
158	BINARY_SUBTRACT   None
159	CALL_FUNCTION_1   None
162	POP_TOP           None

163	LOAD_FAST         'index'
166	STORE_FAST        'oldindex'

169	LOAD_CONST        0
172	STORE_FAST        'delta'
175	JUMP_BACK         '89'
178	POP_BLOCK         None
179_0	COME_FROM         '86'

179	LOAD_FAST         'char'
182	STORE_FAST        'oldchar'
185	JUMP_BACK         '25'
188	POP_BLOCK         None
189_0	COME_FROM         '18'

189	LOAD_FAST         'result'
192	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 178


def T(j, bias):
    res = 36 * (j + 1) - bias
    if res < 1:
        return 1
    if res > 26:
        return 26
    return res


digits = 'abcdefghijklmnopqrstuvwxyz0123456789'

def generate_generalized_integer--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'result'

6	LOAD_CONST        0
9	STORE_FAST        'j'

12	SETUP_LOOP        '128'

15	LOAD_GLOBAL       'T'
18	LOAD_FAST         'j'
21	LOAD_FAST         'bias'
24	CALL_FUNCTION_2   None
27	STORE_FAST        't'

30	LOAD_FAST         'N'
33	LOAD_FAST         't'
36	COMPARE_OP        '<'
39	POP_JUMP_IF_FALSE '63'

42	LOAD_FAST         'result'
45	LOAD_ATTR         'append'
48	LOAD_GLOBAL       'digits'
51	LOAD_FAST         'N'
54	BINARY_SUBSCR     None
55	CALL_FUNCTION_1   None
58	POP_TOP           None

59	LOAD_FAST         'result'
62	RETURN_END_IF     None

63	LOAD_FAST         'result'
66	LOAD_ATTR         'append'
69	LOAD_GLOBAL       'digits'
72	LOAD_FAST         't'
75	LOAD_FAST         'N'
78	LOAD_FAST         't'
81	BINARY_SUBTRACT   None
82	LOAD_CONST        36
85	LOAD_FAST         't'
88	BINARY_SUBTRACT   None
89	BINARY_MODULO     None
90	BINARY_ADD        None
91	BINARY_SUBSCR     None
92	CALL_FUNCTION_1   None
95	POP_TOP           None

96	LOAD_FAST         'N'
99	LOAD_FAST         't'
102	BINARY_SUBTRACT   None
103	LOAD_CONST        36
106	LOAD_FAST         't'
109	BINARY_SUBTRACT   None
110	BINARY_FLOOR_DIVIDE None
111	STORE_FAST        'N'

114	LOAD_FAST         'j'
117	LOAD_CONST        1
120	INPLACE_ADD       None
121	STORE_FAST        'j'
124	JUMP_BACK         '15'
127	POP_BLOCK         None
128_0	COME_FROM         '12'

Syntax error at or near `POP_BLOCK' token at offset 127


def adapt(delta, first, numchars):
    if first:
        delta //= 700
    else:
        delta //= 2
    delta += delta // numchars
    divisions = 0
    while delta > 455:
        delta = delta // 35
        divisions += 36

    bias = divisions + 36 * delta // (delta + 38)
    return bias


def generate_integers(baselen, deltas):
    """3.4 Bias adaptation"""
    result = []
    bias = 72
    for points, delta in enumerate(deltas):
        s = generate_generalized_integer(delta, bias)
        result.extend(s)
        bias = adapt(delta, points == 0, baselen + points + 1)

    return ''.join(result)


def punycode_encode(text):
    base, extended = segregate(text)
    base = base.encode('ascii')
    deltas = insertion_unsort(text, extended)
    extended = generate_integers(len(base), deltas)
    if base:
        return base + '-' + extended
    return extended


def decode_generalized_number--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'result'

6	LOAD_CONST        1
9	STORE_FAST        'w'

12	LOAD_CONST        0
15	STORE_FAST        'j'

18	SETUP_LOOP        '312'

21	SETUP_EXCEPT      '44'

24	LOAD_GLOBAL       'ord'
27	LOAD_FAST         'extended'
30	LOAD_FAST         'extpos'
33	BINARY_SUBSCR     None
34	CALL_FUNCTION_1   None
37	STORE_FAST        'char'
40	POP_BLOCK         None
41	JUMP_FORWARD      '96'
44_0	COME_FROM         '21'

44	DUP_TOP           None
45	LOAD_GLOBAL       'IndexError'
48	COMPARE_OP        'exception match'
51	POP_JUMP_IF_FALSE '95'
54	POP_TOP           None
55	POP_TOP           None
56	POP_TOP           None

57	LOAD_FAST         'errors'
60	LOAD_CONST        'strict'
63	COMPARE_OP        '=='
66	POP_JUMP_IF_FALSE '81'

69	LOAD_GLOBAL       'UnicodeError'
72	LOAD_CONST        'incomplete punicode string'
75	RAISE_VARARGS_2   None
78	JUMP_FORWARD      '81'
81_0	COME_FROM         '78'

81	LOAD_FAST         'extpos'
84	LOAD_CONST        1
87	BINARY_ADD        None
88	LOAD_CONST        None
91	BUILD_TUPLE_2     None
94	RETURN_VALUE      None
95	END_FINALLY       None
96_0	COME_FROM         '41'
96_1	COME_FROM         '95'

96	LOAD_FAST         'extpos'
99	LOAD_CONST        1
102	INPLACE_ADD       None
103	STORE_FAST        'extpos'

106	LOAD_CONST        65
109	LOAD_FAST         'char'
112	DUP_TOP           None
113	ROT_THREE         None
114	COMPARE_OP        '<='
117	JUMP_IF_FALSE_OR_POP '129'
120	LOAD_CONST        90
123	COMPARE_OP        '<='
126	JUMP_FORWARD      '131'
129_0	COME_FROM         '117'
129	ROT_TWO           None
130	POP_TOP           None
131_0	COME_FROM         '126'
131	POP_JUMP_IF_FALSE '147'

134	LOAD_FAST         'char'
137	LOAD_CONST        65
140	BINARY_SUBTRACT   None
141	STORE_FAST        'digit'
144	JUMP_FORWARD      '233'

147	LOAD_CONST        48
150	LOAD_FAST         'char'
153	DUP_TOP           None
154	ROT_THREE         None
155	COMPARE_OP        '<='
158	JUMP_IF_FALSE_OR_POP '170'
161	LOAD_CONST        57
164	COMPARE_OP        '<='
167	JUMP_FORWARD      '172'
170_0	COME_FROM         '158'
170	ROT_TWO           None
171	POP_TOP           None
172_0	COME_FROM         '167'
172	POP_JUMP_IF_FALSE '188'

175	LOAD_FAST         'char'
178	LOAD_CONST        22
181	BINARY_SUBTRACT   None
182	STORE_FAST        'digit'
185	JUMP_FORWARD      '233'

188	LOAD_FAST         'errors'
191	LOAD_CONST        'strict'
194	COMPARE_OP        '=='
197	POP_JUMP_IF_FALSE '223'

200	LOAD_GLOBAL       'UnicodeError'
203	LOAD_CONST        "Invalid extended code point '%s'"

206	LOAD_FAST         'extended'
209	LOAD_FAST         'extpos'
212	BINARY_SUBSCR     None
213	BINARY_MODULO     None
214	CALL_FUNCTION_1   None
217	RAISE_VARARGS_1   None
220	JUMP_FORWARD      '233'

223	LOAD_FAST         'extpos'
226	LOAD_CONST        None
229	BUILD_TUPLE_2     None
232	RETURN_VALUE      None
233_0	COME_FROM         '144'
233_1	COME_FROM         '185'
233_2	COME_FROM         '220'

233	LOAD_GLOBAL       'T'
236	LOAD_FAST         'j'
239	LOAD_FAST         'bias'
242	CALL_FUNCTION_2   None
245	STORE_FAST        't'

248	LOAD_FAST         'result'
251	LOAD_FAST         'digit'
254	LOAD_FAST         'w'
257	BINARY_MULTIPLY   None
258	INPLACE_ADD       None
259	STORE_FAST        'result'

262	LOAD_FAST         'digit'
265	LOAD_FAST         't'
268	COMPARE_OP        '<'
271	POP_JUMP_IF_FALSE '284'

274	LOAD_FAST         'extpos'
277	LOAD_FAST         'result'
280	BUILD_TUPLE_2     None
283	RETURN_END_IF     None

284	LOAD_FAST         'w'
287	LOAD_CONST        36
290	LOAD_FAST         't'
293	BINARY_SUBTRACT   None
294	BINARY_MULTIPLY   None
295	STORE_FAST        'w'

298	LOAD_FAST         'j'
301	LOAD_CONST        1
304	INPLACE_ADD       None
305	STORE_FAST        'j'
308	JUMP_BACK         '21'
311	POP_BLOCK         None
312_0	COME_FROM         '18'
312	LOAD_CONST        None
315	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 311


def insertion_sort(base, extended, errors):
    """3.2 Insertion unsort coding"""
    char = 128
    pos = -1
    bias = 72
    extpos = 0
    while extpos < len(extended):
        newpos, delta = decode_generalized_number(extended, extpos, bias, errors)
        if delta is None:
            return base
        pos += delta + 1
        char += pos // (len(base) + 1)
        if char > 1114111:
            if errors == 'strict':
                raise UnicodeError, 'Invalid character U+%x' % char
            char = ord('?')
        pos = pos % (len(base) + 1)
        base = base[:pos] + unichr(char) + base[pos:]
        bias = adapt(delta, extpos == 0, len(base))
        extpos = newpos

    return base


def punycode_decode(text, errors):
    pos = text.rfind('-')
    if pos == -1:
        base = ''
        extended = text
    else:
        base = text[:pos]
        extended = text[pos + 1:]
    base = unicode(base, 'ascii', errors)
    extended = extended.upper()
    return insertion_sort(base, extended, errors)


class Codec(codecs.Codec):

    def encode(self, input, errors = 'strict'):
        res = punycode_encode(input)
        return (res, len(input))

    def decode(self, input, errors = 'strict'):
        if errors not in ('strict', 'replace', 'ignore'):
            raise UnicodeError, 'Unsupported error handling ' + errors
        res = punycode_decode(input, errors)
        return (res, len(input))


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final = False):
        return punycode_encode(input)


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final = False):
        if self.errors not in ('strict', 'replace', 'ignore'):
            raise UnicodeError, 'Unsupported error handling ' + self.errors
        return punycode_decode(input, self.errors)


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='punycode', encode=Codec().encode, decode=Codec().decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamwriter=StreamWriter, streamreader=StreamReader)