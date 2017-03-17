# Embedded file name: scripts/common/Lib/encodings/uu_codec.py
""" Python 'uu_codec' Codec - UU content transfer encoding

    Unlike most of the other codecs which target Unicode, this codec
    will return Python string objects for both encode and decode.

    Written by Marc-Andre Lemburg (mal@lemburg.com). Some details were
    adapted from uu.py which was written by Lance Ellinghouse and
    modified by Jack Jansen and Fredrik Lundh.

"""
import codecs, binascii

def uu_encode(input, errors = 'strict', filename = '<data>', mode = 438):
    """ Encodes the object input and returns a tuple (output
        object, length consumed).
    
        errors defines the error handling to apply. It defaults to
        'strict' handling which is the only currently supported
        error handling for this codec.
    
    """
    raise errors == 'strict' or AssertionError
    from cStringIO import StringIO
    from binascii import b2a_uu
    infile = StringIO(str(input))
    outfile = StringIO()
    read = infile.read
    write = outfile.write
    write('begin %o %s\n' % (mode & 511, filename))
    chunk = read(45)
    while chunk:
        write(b2a_uu(chunk))
        chunk = read(45)

    write(' \nend\n')
    return (outfile.getvalue(), len(input))


def uu_decode--- This code section failed: ---

0	LOAD_FAST         'errors'
3	LOAD_CONST        'strict'
6	COMPARE_OP        '=='
9	POP_JUMP_IF_TRUE  '18'
12	LOAD_ASSERT       'AssertionError'
15	RAISE_VARARGS_1   None

18	LOAD_CONST        -1
21	LOAD_CONST        ('StringIO',)
24	IMPORT_NAME       'cStringIO'
27	IMPORT_FROM       'StringIO'
30	STORE_FAST        'StringIO'
33	POP_TOP           None

34	LOAD_CONST        -1
37	LOAD_CONST        ('a2b_uu',)
40	IMPORT_NAME       'binascii'
43	IMPORT_FROM       'a2b_uu'
46	STORE_FAST        'a2b_uu'
49	POP_TOP           None

50	LOAD_FAST         'StringIO'
53	LOAD_GLOBAL       'str'
56	LOAD_FAST         'input'
59	CALL_FUNCTION_1   None
62	CALL_FUNCTION_1   None
65	STORE_FAST        'infile'

68	LOAD_FAST         'StringIO'
71	CALL_FUNCTION_0   None
74	STORE_FAST        'outfile'

77	LOAD_FAST         'infile'
80	LOAD_ATTR         'readline'
83	STORE_FAST        'readline'

86	LOAD_FAST         'outfile'
89	LOAD_ATTR         'write'
92	STORE_FAST        'write'

95	SETUP_LOOP        '149'

98	LOAD_FAST         'readline'
101	CALL_FUNCTION_0   None
104	STORE_FAST        's'

107	LOAD_FAST         's'
110	POP_JUMP_IF_TRUE  '125'

113	LOAD_GLOBAL       'ValueError'
116	LOAD_CONST        'Missing "begin" line in input data'
119	RAISE_VARARGS_2   None
122	JUMP_FORWARD      '125'
125_0	COME_FROM         '122'

125	LOAD_FAST         's'
128	LOAD_CONST        5
131	SLICE+2           None
132	LOAD_CONST        'begin'
135	COMPARE_OP        '=='
138	POP_JUMP_IF_FALSE '98'

141	BREAK_LOOP        None
142	JUMP_BACK         '98'
145	JUMP_BACK         '98'
148	POP_BLOCK         None
149_0	COME_FROM         '95'

149	SETUP_LOOP        '291'

152	LOAD_FAST         'readline'
155	CALL_FUNCTION_0   None
158	STORE_FAST        's'

161	LOAD_FAST         's'
164	UNARY_NOT         None
165	POP_JUMP_IF_TRUE  '180'

168	LOAD_FAST         's'
171	LOAD_CONST        'end\n'
174	COMPARE_OP        '=='
177_0	COME_FROM         '165'
177	POP_JUMP_IF_FALSE '184'

180	BREAK_LOOP        None
181	JUMP_FORWARD      '184'
184_0	COME_FROM         '181'

184	SETUP_EXCEPT      '203'

187	LOAD_FAST         'a2b_uu'
190	LOAD_FAST         's'
193	CALL_FUNCTION_1   None
196	STORE_FAST        'data'
199	POP_BLOCK         None
200	JUMP_FORWARD      '277'
203_0	COME_FROM         '184'

203	DUP_TOP           None
204	LOAD_GLOBAL       'binascii'
207	LOAD_ATTR         'Error'
210	COMPARE_OP        'exception match'
213	POP_JUMP_IF_FALSE '276'
216	POP_TOP           None
217	STORE_FAST        'v'
220	POP_TOP           None

221	LOAD_GLOBAL       'ord'
224	LOAD_FAST         's'
227	LOAD_CONST        0
230	BINARY_SUBSCR     None
231	CALL_FUNCTION_1   None
234	LOAD_CONST        32
237	BINARY_SUBTRACT   None
238	LOAD_CONST        63
241	BINARY_AND        None
242	LOAD_CONST        4
245	BINARY_MULTIPLY   None
246	LOAD_CONST        5
249	BINARY_ADD        None
250	LOAD_CONST        3
253	BINARY_DIVIDE     None
254	STORE_FAST        'nbytes'

257	LOAD_FAST         'a2b_uu'
260	LOAD_FAST         's'
263	LOAD_FAST         'nbytes'
266	SLICE+2           None
267	CALL_FUNCTION_1   None
270	STORE_FAST        'data'
273	JUMP_FORWARD      '277'
276	END_FINALLY       None
277_0	COME_FROM         '200'
277_1	COME_FROM         '276'

277	LOAD_FAST         'write'
280	LOAD_FAST         'data'
283	CALL_FUNCTION_1   None
286	POP_TOP           None
287	JUMP_BACK         '152'
290	POP_BLOCK         None
291_0	COME_FROM         '149'

291	LOAD_FAST         's'
294	POP_JUMP_IF_TRUE  '309'

297	LOAD_GLOBAL       'ValueError'
300	LOAD_CONST        'Truncated input data'
303	RAISE_VARARGS_2   None
306	JUMP_FORWARD      '309'
309_0	COME_FROM         '306'

309	LOAD_FAST         'outfile'
312	LOAD_ATTR         'getvalue'
315	CALL_FUNCTION_0   None
318	LOAD_GLOBAL       'len'
321	LOAD_FAST         'input'
324	CALL_FUNCTION_1   None
327	BUILD_TUPLE_2     None
330	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 148


class Codec(codecs.Codec):

    def encode(self, input, errors = 'strict'):
        return uu_encode(input, errors)

    def decode(self, input, errors = 'strict'):
        return uu_decode(input, errors)


class IncrementalEncoder(codecs.IncrementalEncoder):

    def encode(self, input, final = False):
        return uu_encode(input, self.errors)[0]


class IncrementalDecoder(codecs.IncrementalDecoder):

    def decode(self, input, final = False):
        return uu_decode(input, self.errors)[0]


class StreamWriter(Codec, codecs.StreamWriter):
    pass


class StreamReader(Codec, codecs.StreamReader):
    pass


def getregentry():
    return codecs.CodecInfo(name='uu', encode=uu_encode, decode=uu_decode, incrementalencoder=IncrementalEncoder, incrementaldecoder=IncrementalDecoder, streamreader=StreamReader, streamwriter=StreamWriter)