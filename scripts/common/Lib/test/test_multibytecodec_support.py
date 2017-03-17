# Embedded file name: scripts/common/Lib/test/test_multibytecodec_support.py
import codecs
import os
import re
import sys
import unittest
from httplib import HTTPException
from test import test_support
from StringIO import StringIO

class TestBase:
    encoding = ''
    codec = None
    tstring = ''
    codectests = None
    roundtriptest = 1
    has_iso10646 = 0
    xmlcharnametest = None
    unmappedunicode = u'\udeee'

    def setUp(self):
        if self.codec is None:
            self.codec = codecs.lookup(self.encoding)
        self.encode = self.codec.encode
        self.decode = self.codec.decode
        self.reader = self.codec.streamreader
        self.writer = self.codec.streamwriter
        self.incrementalencoder = self.codec.incrementalencoder
        self.incrementaldecoder = self.codec.incrementaldecoder
        return

    def test_chunkcoding(self):
        for native, utf8 in zip(*[ StringIO(f).readlines() for f in self.tstring ]):
            u = self.decode(native)[0]
            self.assertEqual(u, utf8.decode('utf-8'))
            if self.roundtriptest:
                self.assertEqual(native, self.encode(u)[0])

    def test_errorhandle(self):
        for source, scheme, expected in self.codectests:
            if isinstance(source, bytes):
                func = self.decode
            else:
                func = self.encode
            if expected:
                result = func(source, scheme)[0]
                if func is self.decode:
                    self.assertTrue(type(result) is unicode, type(result))
                    self.assertEqual(result, expected, '%r.decode(%r, %r)=%r != %r' % (source,
                     self.encoding,
                     scheme,
                     result,
                     expected))
                else:
                    self.assertTrue(type(result) is bytes, type(result))
                    self.assertEqual(result, expected, '%r.encode(%r, %r)=%r != %r' % (source,
                     self.encoding,
                     scheme,
                     result,
                     expected))
            else:
                self.assertRaises(UnicodeError, func, source, scheme)

    def test_xmlcharrefreplace(self):
        if self.has_iso10646:
            return
        s = u'\u0b13\u0b23\u0b60 nd eggs'
        self.assertEqual(self.encode(s, 'xmlcharrefreplace')[0], '&#2835;&#2851;&#2912; nd eggs')

    def test_customreplace_encode(self):
        if self.has_iso10646:
            return
        from htmlentitydefs import codepoint2name

        def xmlcharnamereplace(exc):
            if not isinstance(exc, UnicodeEncodeError):
                raise TypeError("don't know how to handle %r" % exc)
            l = []
            for c in exc.object[exc.start:exc.end]:
                if ord(c) in codepoint2name:
                    l.append(u'&%s;' % codepoint2name[ord(c)])
                else:
                    l.append(u'&#%d;' % ord(c))

            return (u''.join(l), exc.end)

        codecs.register_error('test.xmlcharnamereplace', xmlcharnamereplace)
        if self.xmlcharnametest:
            sin, sout = self.xmlcharnametest
        else:
            sin = u'\xab\u211c\xbb = \u2329\u1234\u232a'
            sout = '&laquo;&real;&raquo; = &lang;&#4660;&rang;'
        self.assertEqual(self.encode(sin, 'test.xmlcharnamereplace')[0], sout)

    def test_callback_wrong_objects(self):

        def myreplace(exc):
            return (ret, exc.end)

        codecs.register_error('test.cjktest', myreplace)
        for ret in ([1, 2, 3],
         [],
         None,
         object(),
         'string',
         ''):
            self.assertRaises(TypeError, self.encode, self.unmappedunicode, 'test.cjktest')

        return

    def test_callback_long_index(self):

        def myreplace(exc):
            return (u'x', long(exc.end))

        codecs.register_error('test.cjktest', myreplace)
        self.assertEqual(self.encode(u'abcd' + self.unmappedunicode + u'efgh', 'test.cjktest'), ('abcdxefgh', 9))

        def myreplace(exc):
            return (u'x', sys.maxint + 1)

        codecs.register_error('test.cjktest', myreplace)
        self.assertRaises(IndexError, self.encode, self.unmappedunicode, 'test.cjktest')

    def test_callback_None_index(self):

        def myreplace(exc):
            return (u'x', None)

        codecs.register_error('test.cjktest', myreplace)
        self.assertRaises(TypeError, self.encode, self.unmappedunicode, 'test.cjktest')

    def test_callback_backward_index(self):

        def myreplace(exc):
            if myreplace.limit > 0:
                myreplace.limit -= 1
                return (u'REPLACED', 0)
            else:
                return (u'TERMINAL', exc.end)

        myreplace.limit = 3
        codecs.register_error('test.cjktest', myreplace)
        self.assertEqual(self.encode(u'abcd' + self.unmappedunicode + u'efgh', 'test.cjktest'), ('abcdREPLACEDabcdREPLACEDabcdREPLACEDabcdTERMINALefgh', 9))

    def test_callback_forward_index(self):

        def myreplace(exc):
            return (u'REPLACED', exc.end + 2)

        codecs.register_error('test.cjktest', myreplace)
        self.assertEqual(self.encode(u'abcd' + self.unmappedunicode + u'efgh', 'test.cjktest'), ('abcdREPLACEDgh', 9))

    def test_callback_index_outofbound(self):

        def myreplace(exc):
            return (u'TERM', 100)

        codecs.register_error('test.cjktest', myreplace)
        self.assertRaises(IndexError, self.encode, self.unmappedunicode, 'test.cjktest')

    def test_incrementalencoder--- This code section failed: ---

0	LOAD_GLOBAL       'codecs'
3	LOAD_ATTR         'getreader'
6	LOAD_CONST        'utf-8'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'UTF8Reader'

15	SETUP_LOOP        '229'
18	LOAD_CONST        None
21	BUILD_LIST_1      None
24	LOAD_GLOBAL       'range'
27	LOAD_CONST        1
30	LOAD_CONST        33
33	CALL_FUNCTION_2   None
36	BINARY_ADD        None

37	LOAD_CONST        64
40	LOAD_CONST        128
43	LOAD_CONST        256
46	LOAD_CONST        512
49	LOAD_CONST        1024
52	BUILD_LIST_5      None
55	BINARY_ADD        None
56	GET_ITER          None
57	FOR_ITER          '228'
60	STORE_FAST        'sizehint'

63	LOAD_FAST         'UTF8Reader'
66	LOAD_GLOBAL       'StringIO'
69	LOAD_FAST         'self'
72	LOAD_ATTR         'tstring'
75	LOAD_CONST        1
78	BINARY_SUBSCR     None
79	CALL_FUNCTION_1   None
82	CALL_FUNCTION_1   None
85	STORE_FAST        'istream'

88	LOAD_GLOBAL       'StringIO'
91	CALL_FUNCTION_0   None
94	STORE_FAST        'ostream'

97	LOAD_FAST         'self'
100	LOAD_ATTR         'incrementalencoder'
103	CALL_FUNCTION_0   None
106	STORE_FAST        'encoder'

109	SETUP_LOOP        '196'

112	LOAD_FAST         'sizehint'
115	LOAD_CONST        None
118	COMPARE_OP        'is not'
121	POP_JUMP_IF_FALSE '142'

124	LOAD_FAST         'istream'
127	LOAD_ATTR         'read'
130	LOAD_FAST         'sizehint'
133	CALL_FUNCTION_1   None
136	STORE_FAST        'data'
139	JUMP_FORWARD      '154'

142	LOAD_FAST         'istream'
145	LOAD_ATTR         'read'
148	CALL_FUNCTION_0   None
151	STORE_FAST        'data'
154_0	COME_FROM         '139'

154	LOAD_FAST         'data'
157	POP_JUMP_IF_TRUE  '164'

160	BREAK_LOOP        None
161	JUMP_FORWARD      '164'
164_0	COME_FROM         '161'

164	LOAD_FAST         'encoder'
167	LOAD_ATTR         'encode'
170	LOAD_FAST         'data'
173	CALL_FUNCTION_1   None
176	STORE_FAST        'e'

179	LOAD_FAST         'ostream'
182	LOAD_ATTR         'write'
185	LOAD_FAST         'e'
188	CALL_FUNCTION_1   None
191	POP_TOP           None
192	JUMP_BACK         '112'
195	POP_BLOCK         None
196_0	COME_FROM         '109'

196	LOAD_FAST         'self'
199	LOAD_ATTR         'assertEqual'
202	LOAD_FAST         'ostream'
205	LOAD_ATTR         'getvalue'
208	CALL_FUNCTION_0   None
211	LOAD_FAST         'self'
214	LOAD_ATTR         'tstring'
217	LOAD_CONST        0
220	BINARY_SUBSCR     None
221	CALL_FUNCTION_2   None
224	POP_TOP           None
225	JUMP_BACK         '57'
228	POP_BLOCK         None
229_0	COME_FROM         '15'
229	LOAD_CONST        None
232	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 195

    def test_incrementaldecoder--- This code section failed: ---

0	LOAD_GLOBAL       'codecs'
3	LOAD_ATTR         'getwriter'
6	LOAD_CONST        'utf-8'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'UTF8Writer'

15	SETUP_LOOP        '205'
18	LOAD_CONST        None
21	LOAD_CONST        -1
24	BUILD_LIST_2      None
27	LOAD_GLOBAL       'range'
30	LOAD_CONST        1
33	LOAD_CONST        33
36	CALL_FUNCTION_2   None
39	BINARY_ADD        None

40	LOAD_CONST        64
43	LOAD_CONST        128
46	LOAD_CONST        256
49	LOAD_CONST        512
52	LOAD_CONST        1024
55	BUILD_LIST_5      None
58	BINARY_ADD        None
59	GET_ITER          None
60	FOR_ITER          '204'
63	STORE_FAST        'sizehint'

66	LOAD_GLOBAL       'StringIO'
69	LOAD_FAST         'self'
72	LOAD_ATTR         'tstring'
75	LOAD_CONST        0
78	BINARY_SUBSCR     None
79	CALL_FUNCTION_1   None
82	STORE_FAST        'istream'

85	LOAD_FAST         'UTF8Writer'
88	LOAD_GLOBAL       'StringIO'
91	CALL_FUNCTION_0   None
94	CALL_FUNCTION_1   None
97	STORE_FAST        'ostream'

100	LOAD_FAST         'self'
103	LOAD_ATTR         'incrementaldecoder'
106	CALL_FUNCTION_0   None
109	STORE_FAST        'decoder'

112	SETUP_LOOP        '172'

115	LOAD_FAST         'istream'
118	LOAD_ATTR         'read'
121	LOAD_FAST         'sizehint'
124	CALL_FUNCTION_1   None
127	STORE_FAST        'data'

130	LOAD_FAST         'data'
133	POP_JUMP_IF_TRUE  '140'

136	BREAK_LOOP        None
137	JUMP_BACK         '115'

140	LOAD_FAST         'decoder'
143	LOAD_ATTR         'decode'
146	LOAD_FAST         'data'
149	CALL_FUNCTION_1   None
152	STORE_FAST        'u'

155	LOAD_FAST         'ostream'
158	LOAD_ATTR         'write'
161	LOAD_FAST         'u'
164	CALL_FUNCTION_1   None
167	POP_TOP           None
168	JUMP_BACK         '115'
171	POP_BLOCK         None
172_0	COME_FROM         '112'

172	LOAD_FAST         'self'
175	LOAD_ATTR         'assertEqual'
178	LOAD_FAST         'ostream'
181	LOAD_ATTR         'getvalue'
184	CALL_FUNCTION_0   None
187	LOAD_FAST         'self'
190	LOAD_ATTR         'tstring'
193	LOAD_CONST        1
196	BINARY_SUBSCR     None
197	CALL_FUNCTION_2   None
200	POP_TOP           None
201	JUMP_BACK         '60'
204	POP_BLOCK         None
205_0	COME_FROM         '15'
205	LOAD_CONST        None
208	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 171

    def test_incrementalencoder_error_callback(self):
        inv = self.unmappedunicode
        e = self.incrementalencoder()
        self.assertRaises(UnicodeEncodeError, e.encode, inv, True)
        e.errors = 'ignore'
        self.assertEqual(e.encode(inv, True), '')
        e.reset()

        def tempreplace(exc):
            return (u'called', exc.end)

        codecs.register_error('test.incremental_error_callback', tempreplace)
        e.errors = 'test.incremental_error_callback'
        self.assertEqual(e.encode(inv, True), 'called')
        e.errors = 'ignore'
        self.assertEqual(e.encode(inv, True), '')

    def test_streamreader--- This code section failed: ---

0	LOAD_GLOBAL       'codecs'
3	LOAD_ATTR         'getwriter'
6	LOAD_CONST        'utf-8'
9	CALL_FUNCTION_1   None
12	STORE_FAST        'UTF8Writer'

15	SETUP_LOOP        '253'
18	LOAD_CONST        'read'
21	LOAD_CONST        'readline'
24	LOAD_CONST        'readlines'
27	BUILD_LIST_3      None
30	GET_ITER          None
31	FOR_ITER          '252'
34	STORE_FAST        'name'

37	SETUP_LOOP        '249'
40	LOAD_CONST        None
43	LOAD_CONST        -1
46	BUILD_LIST_2      None
49	LOAD_GLOBAL       'range'
52	LOAD_CONST        1
55	LOAD_CONST        33
58	CALL_FUNCTION_2   None
61	BINARY_ADD        None

62	LOAD_CONST        64
65	LOAD_CONST        128
68	LOAD_CONST        256
71	LOAD_CONST        512
74	LOAD_CONST        1024
77	BUILD_LIST_5      None
80	BINARY_ADD        None
81	GET_ITER          None
82	FOR_ITER          '248'
85	STORE_FAST        'sizehint'

88	LOAD_FAST         'self'
91	LOAD_ATTR         'reader'
94	LOAD_GLOBAL       'StringIO'
97	LOAD_FAST         'self'
100	LOAD_ATTR         'tstring'
103	LOAD_CONST        0
106	BINARY_SUBSCR     None
107	CALL_FUNCTION_1   None
110	CALL_FUNCTION_1   None
113	STORE_FAST        'istream'

116	LOAD_FAST         'UTF8Writer'
119	LOAD_GLOBAL       'StringIO'
122	CALL_FUNCTION_0   None
125	CALL_FUNCTION_1   None
128	STORE_FAST        'ostream'

131	LOAD_GLOBAL       'getattr'
134	LOAD_FAST         'istream'
137	LOAD_FAST         'name'
140	CALL_FUNCTION_2   None
143	STORE_FAST        'func'

146	SETUP_LOOP        '216'

149	LOAD_FAST         'func'
152	LOAD_FAST         'sizehint'
155	CALL_FUNCTION_1   None
158	STORE_FAST        'data'

161	LOAD_FAST         'data'
164	POP_JUMP_IF_TRUE  '171'

167	BREAK_LOOP        None
168	JUMP_FORWARD      '171'
171_0	COME_FROM         '168'

171	LOAD_FAST         'name'
174	LOAD_CONST        'readlines'
177	COMPARE_OP        '=='
180	POP_JUMP_IF_FALSE '199'

183	LOAD_FAST         'ostream'
186	LOAD_ATTR         'writelines'
189	LOAD_FAST         'data'
192	CALL_FUNCTION_1   None
195	POP_TOP           None
196	JUMP_BACK         '149'

199	LOAD_FAST         'ostream'
202	LOAD_ATTR         'write'
205	LOAD_FAST         'data'
208	CALL_FUNCTION_1   None
211	POP_TOP           None
212	JUMP_BACK         '149'
215	POP_BLOCK         None
216_0	COME_FROM         '146'

216	LOAD_FAST         'self'
219	LOAD_ATTR         'assertEqual'
222	LOAD_FAST         'ostream'
225	LOAD_ATTR         'getvalue'
228	CALL_FUNCTION_0   None
231	LOAD_FAST         'self'
234	LOAD_ATTR         'tstring'
237	LOAD_CONST        1
240	BINARY_SUBSCR     None
241	CALL_FUNCTION_2   None
244	POP_TOP           None
245	JUMP_BACK         '82'
248	POP_BLOCK         None
249_0	COME_FROM         '37'
249	JUMP_BACK         '31'
252	POP_BLOCK         None
253_0	COME_FROM         '15'
253	LOAD_CONST        None
256	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 215

    def test_streamwriter--- This code section failed: ---

0	LOAD_CONST        ('read', 'readline', 'readlines')
3	STORE_FAST        'readfuncs'

6	LOAD_GLOBAL       'codecs'
9	LOAD_ATTR         'getreader'
12	LOAD_CONST        'utf-8'
15	CALL_FUNCTION_1   None
18	STORE_FAST        'UTF8Reader'

21	SETUP_LOOP        '271'
24	LOAD_FAST         'readfuncs'
27	GET_ITER          None
28	FOR_ITER          '270'
31	STORE_FAST        'name'

34	SETUP_LOOP        '267'
37	LOAD_CONST        None
40	BUILD_LIST_1      None
43	LOAD_GLOBAL       'range'
46	LOAD_CONST        1
49	LOAD_CONST        33
52	CALL_FUNCTION_2   None
55	BINARY_ADD        None

56	LOAD_CONST        64
59	LOAD_CONST        128
62	LOAD_CONST        256
65	LOAD_CONST        512
68	LOAD_CONST        1024
71	BUILD_LIST_5      None
74	BINARY_ADD        None
75	GET_ITER          None
76	FOR_ITER          '266'
79	STORE_FAST        'sizehint'

82	LOAD_FAST         'UTF8Reader'
85	LOAD_GLOBAL       'StringIO'
88	LOAD_FAST         'self'
91	LOAD_ATTR         'tstring'
94	LOAD_CONST        1
97	BINARY_SUBSCR     None
98	CALL_FUNCTION_1   None
101	CALL_FUNCTION_1   None
104	STORE_FAST        'istream'

107	LOAD_FAST         'self'
110	LOAD_ATTR         'writer'
113	LOAD_GLOBAL       'StringIO'
116	CALL_FUNCTION_0   None
119	CALL_FUNCTION_1   None
122	STORE_FAST        'ostream'

125	LOAD_GLOBAL       'getattr'
128	LOAD_FAST         'istream'
131	LOAD_FAST         'name'
134	CALL_FUNCTION_2   None
137	STORE_FAST        'func'

140	SETUP_LOOP        '234'

143	LOAD_FAST         'sizehint'
146	LOAD_CONST        None
149	COMPARE_OP        'is not'
152	POP_JUMP_IF_FALSE '170'

155	LOAD_FAST         'func'
158	LOAD_FAST         'sizehint'
161	CALL_FUNCTION_1   None
164	STORE_FAST        'data'
167	JUMP_FORWARD      '179'

170	LOAD_FAST         'func'
173	CALL_FUNCTION_0   None
176	STORE_FAST        'data'
179_0	COME_FROM         '167'

179	LOAD_FAST         'data'
182	POP_JUMP_IF_TRUE  '189'

185	BREAK_LOOP        None
186	JUMP_FORWARD      '189'
189_0	COME_FROM         '186'

189	LOAD_FAST         'name'
192	LOAD_CONST        'readlines'
195	COMPARE_OP        '=='
198	POP_JUMP_IF_FALSE '217'

201	LOAD_FAST         'ostream'
204	LOAD_ATTR         'writelines'
207	LOAD_FAST         'data'
210	CALL_FUNCTION_1   None
213	POP_TOP           None
214	JUMP_BACK         '143'

217	LOAD_FAST         'ostream'
220	LOAD_ATTR         'write'
223	LOAD_FAST         'data'
226	CALL_FUNCTION_1   None
229	POP_TOP           None
230	JUMP_BACK         '143'
233	POP_BLOCK         None
234_0	COME_FROM         '140'

234	LOAD_FAST         'self'
237	LOAD_ATTR         'assertEqual'
240	LOAD_FAST         'ostream'
243	LOAD_ATTR         'getvalue'
246	CALL_FUNCTION_0   None
249	LOAD_FAST         'self'
252	LOAD_ATTR         'tstring'
255	LOAD_CONST        0
258	BINARY_SUBSCR     None
259	CALL_FUNCTION_2   None
262	POP_TOP           None
263	JUMP_BACK         '76'
266	POP_BLOCK         None
267_0	COME_FROM         '34'
267	JUMP_BACK         '28'
270	POP_BLOCK         None
271_0	COME_FROM         '21'
271	LOAD_CONST        None
274	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 233


class TestBase_Mapping(unittest.TestCase):
    pass_enctest = []
    pass_dectest = []
    supmaps = []
    codectests = []

    def __init__(self, *args, **kw):
        unittest.TestCase.__init__(self, *args, **kw)
        try:
            self.open_mapping_file().close()
        except (IOError, HTTPException):
            self.skipTest('Could not retrieve ' + self.mapfileurl)

    def open_mapping_file(self):
        return test_support.open_urlresource(self.mapfileurl)

    def test_mapping_file(self):
        if self.mapfileurl.endswith('.xml'):
            self._test_mapping_file_ucm()
        else:
            self._test_mapping_file_plain()

    def _test_mapping_file_plain(self):
        _unichr = lambda c: eval("u'\\U%08x'" % int(c, 16))
        unichrs = lambda s: u''.join((_unichr(c) for c in s.split('+')))
        urt_wa = {}
        with self.open_mapping_file() as f:
            for line in f:
                if not line:
                    break
                data = line.split('#')[0].strip().split()
                if len(data) != 2:
                    continue
                csetval = eval(data[0])
                if csetval <= 127:
                    csetch = chr(csetval & 255)
                elif csetval >= 16777216:
                    csetch = chr(csetval >> 24) + chr(csetval >> 16 & 255) + chr(csetval >> 8 & 255) + chr(csetval & 255)
                elif csetval >= 65536:
                    csetch = chr(csetval >> 16) + chr(csetval >> 8 & 255) + chr(csetval & 255)
                elif csetval >= 256:
                    csetch = chr(csetval >> 8) + chr(csetval & 255)
                else:
                    continue
                unich = unichrs(data[1])
                if unich == u'\ufffd' or unich in urt_wa:
                    continue
                urt_wa[unich] = csetch
                self._testpoint(csetch, unich)

    def _test_mapping_file_ucm(self):
        with self.open_mapping_file() as f:
            ucmdata = f.read()
        uc = re.findall('<a u="([A-F0-9]{4})" b="([0-9A-F ]+)"/>', ucmdata)
        for uni, coded in uc:
            unich = unichr(int(uni, 16))
            codech = ''.join((chr(int(c, 16)) for c in coded.split()))
            self._testpoint(codech, unich)

    def test_mapping_supplemental(self):
        for mapping in self.supmaps:
            self._testpoint(*mapping)

    def _testpoint(self, csetch, unich):
        if (csetch, unich) not in self.pass_enctest:
            try:
                self.assertEqual(unich.encode(self.encoding), csetch)
            except UnicodeError as exc:
                self.fail('Encoding failed while testing %s -> %s: %s' % (repr(unich), repr(csetch), exc.reason))

        if (csetch, unich) not in self.pass_dectest:
            try:
                self.assertEqual(csetch.decode(self.encoding), unich)
            except UnicodeError as exc:
                self.fail('Decoding failed while testing %s -> %s: %s' % (repr(csetch), repr(unich), exc.reason))

    def test_errorhandle(self):
        for source, scheme, expected in self.codectests:
            if isinstance(source, bytes):
                func = source.decode
            else:
                func = source.encode
            if expected:
                if isinstance(source, bytes):
                    result = func(self.encoding, scheme)
                    self.assertTrue(type(result) is unicode, type(result))
                    self.assertEqual(result, expected, '%r.decode(%r, %r)=%r != %r' % (source,
                     self.encoding,
                     scheme,
                     result,
                     expected))
                else:
                    result = func(self.encoding, scheme)
                    self.assertTrue(type(result) is bytes, type(result))
                    self.assertEqual(result, expected, '%r.encode(%r, %r)=%r != %r' % (source,
                     self.encoding,
                     scheme,
                     result,
                     expected))
            else:
                self.assertRaises(UnicodeError, func, self.encoding, scheme)


def load_teststring(name):
    dir = os.path.join(os.path.dirname(__file__), 'cjkencodings')
    with open(os.path.join(dir, name + '.txt'), 'rb') as f:
        encoded = f.read()
    with open(os.path.join(dir, name + '-utf8.txt'), 'rb') as f:
        utf8 = f.read()
    return (encoded, utf8)