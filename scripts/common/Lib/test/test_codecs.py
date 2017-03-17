# Embedded file name: scripts/common/Lib/test/test_codecs.py
from test import test_support
import unittest
import codecs
import locale
import sys, StringIO, _testcapi

class Queue(object):
    """
    queue: write bytes at one end, read bytes from the other end
    """

    def __init__(self):
        self._buffer = ''

    def write(self, chars):
        self._buffer += chars

    def read(self, size = -1):
        if size < 0:
            s = self._buffer
            self._buffer = ''
            return s
        else:
            s = self._buffer[:size]
            self._buffer = self._buffer[size:]
            return s


class ReadTest(unittest.TestCase):

    def check_partial(self, input, partialresults):
        q = Queue()
        r = codecs.getreader(self.encoding)(q)
        result = u''
        for c, partialresult in zip(input.encode(self.encoding), partialresults):
            q.write(c)
            result += r.read()
            self.assertEqual(result, partialresult)

        self.assertEqual(r.read(), u'')
        self.assertEqual(r.bytebuffer, '')
        self.assertEqual(r.charbuffer, u'')
        d = codecs.getincrementaldecoder(self.encoding)()
        result = u''
        for c, partialresult in zip(input.encode(self.encoding), partialresults):
            result += d.decode(c)
            self.assertEqual(result, partialresult)

        self.assertEqual(d.decode('', True), u'')
        self.assertEqual(d.buffer, '')
        d.reset()
        result = u''
        for c, partialresult in zip(input.encode(self.encoding), partialresults):
            result += d.decode(c)
            self.assertEqual(result, partialresult)

        self.assertEqual(d.decode('', True), u'')
        self.assertEqual(d.buffer, '')
        encoded = input.encode(self.encoding)
        self.assertEqual(input, u''.join(codecs.iterdecode(encoded, self.encoding)))

    def test_readline(self):

        def getreader(input):
            stream = StringIO.StringIO(input.encode(self.encoding))
            return codecs.getreader(self.encoding)(stream)

        def readalllines(input, keepends = True, size = None):
            reader = getreader(input)
            lines = []
            while True:
                line = reader.readline(size=size, keepends=keepends)
                if not line:
                    break
                lines.append(line)

            return '|'.join(lines)

        s = u'foo\nbar\r\nbaz\rspam\u2028eggs'
        sexpected = u'foo\n|bar\r\n|baz\r|spam\u2028|eggs'
        sexpectednoends = u'foo|bar|baz|spam|eggs'
        self.assertEqual(readalllines(s, True), sexpected)
        self.assertEqual(readalllines(s, False), sexpectednoends)
        self.assertEqual(readalllines(s, True, 10), sexpected)
        self.assertEqual(readalllines(s, False, 10), sexpectednoends)
        vw = []
        vwo = []
        for i, lineend in enumerate(u'\n \r\n \r \u2028'.split()):
            vw.append(i * 200 * u'\xc42' + lineend)
            vwo.append(i * 200 * u'\xc42')

        self.assertEqual(readalllines(''.join(vw), True), ''.join(vw))
        self.assertEqual(readalllines(''.join(vw), False), ''.join(vwo))
        for size in xrange(80):
            for lineend in u'\n \r\n \r \u2028'.split():
                s = 10 * (size * u'a' + lineend + u'xxx\n')
                reader = getreader(s)
                for i in xrange(10):
                    self.assertEqual(reader.readline(keepends=True), size * u'a' + lineend)

                reader = getreader(s)
                for i in xrange(10):
                    self.assertEqual(reader.readline(keepends=False), size * u'a')

        return

    def test_bug1175396(self):
        s = ['<%!--===================================================\r\n',
         '    BLOG index page: show recent articles,\r\n',
         "    today's articles, or articles of a specific date.\r\n",
         '========================================================--%>\r\n',
         '<%@inputencoding="ISO-8859-1"%>\r\n',
         '<%@pagetemplate=TEMPLATE.y%>\r\n',
         '<%@import=import frog.util, frog%>\r\n',
         '<%@import=import frog.objects%>\r\n',
         '<%@import=from frog.storageerrors import StorageError%>\r\n',
         '<%\r\n',
         '\r\n',
         'import logging\r\n',
         'log=logging.getLogger("Snakelets.logger")\r\n',
         '\r\n',
         '\r\n',
         'user=self.SessionCtx.user\r\n',
         'storageEngine=self.SessionCtx.storageEngine\r\n',
         '\r\n',
         '\r\n',
         'def readArticlesFromDate(date, count=None):\r\n',
         '    entryids=storageEngine.listBlogEntries(date)\r\n',
         '    entryids.reverse() # descending\r\n',
         '    if count:\r\n',
         '        entryids=entryids[:count]\r\n',
         '    try:\r\n',
         '        return [ frog.objects.BlogEntry.load(storageEngine, date, Id) for Id in entryids ]\r\n',
         '    except StorageError,x:\r\n',
         '        log.error("Error loading articles: "+str(x))\r\n',
         '        self.abort("cannot load articles")\r\n',
         '\r\n',
         'showdate=None\r\n',
         '\r\n',
         'arg=self.Request.getArg()\r\n',
         'if arg=="today":\r\n',
         "    #-------------------- TODAY'S ARTICLES\r\n",
         '    self.write("<h2>Today\'s articles</h2>")\r\n',
         '    showdate = frog.util.isodatestr() \r\n',
         '    entries = readArticlesFromDate(showdate)\r\n',
         'elif arg=="active":\r\n',
         '    #-------------------- ACTIVE ARTICLES redirect\r\n',
         '    self.Yredirect("active.y")\r\n',
         'elif arg=="login":\r\n',
         '    #-------------------- LOGIN PAGE redirect\r\n',
         '    self.Yredirect("login.y")\r\n',
         'elif arg=="date":\r\n',
         '    #-------------------- ARTICLES OF A SPECIFIC DATE\r\n',
         '    showdate = self.Request.getParameter("date")\r\n',
         '    self.write("<h2>Articles written on %s</h2>"% frog.util.mediumdatestr(showdate))\r\n',
         '    entries = readArticlesFromDate(showdate)\r\n',
         'else:\r\n',
         '    #-------------------- RECENT ARTICLES\r\n',
         '    self.write("<h2>Recent articles</h2>")\r\n',
         '    dates=storageEngine.listBlogEntryDates()\r\n',
         '    if dates:\r\n',
         '        entries=[]\r\n',
         '        SHOWAMOUNT=10\r\n',
         '        for showdate in dates:\r\n',
         '            entries.extend( readArticlesFromDate(showdate, SHOWAMOUNT-len(entries)) )\r\n',
         '            if len(entries)>=SHOWAMOUNT:\r\n',
         '                break\r\n',
         '                \r\n']
        stream = StringIO.StringIO(''.join(s).encode(self.encoding))
        reader = codecs.getreader(self.encoding)(stream)
        for i, line in enumerate(reader):
            self.assertEqual(line, s[i])

    def test_readlinequeue(self):
        q = Queue()
        writer = codecs.getwriter(self.encoding)(q)
        reader = codecs.getreader(self.encoding)(q)
        writer.write(u'foo\r')
        self.assertEqual(reader.readline(keepends=False), u'foo')
        writer.write(u'\nbar\r')
        self.assertEqual(reader.readline(keepends=False), u'')
        self.assertEqual(reader.readline(keepends=False), u'bar')
        writer.write(u'baz')
        self.assertEqual(reader.readline(keepends=False), u'baz')
        self.assertEqual(reader.readline(keepends=False), u'')
        writer.write(u'foo\r')
        self.assertEqual(reader.readline(keepends=True), u'foo\r')
        writer.write(u'\nbar\r')
        self.assertEqual(reader.readline(keepends=True), u'\n')
        self.assertEqual(reader.readline(keepends=True), u'bar\r')
        writer.write(u'baz')
        self.assertEqual(reader.readline(keepends=True), u'baz')
        self.assertEqual(reader.readline(keepends=True), u'')
        writer.write(u'foo\r\n')
        self.assertEqual(reader.readline(keepends=True), u'foo\r\n')

    def test_bug1098990_a(self):
        s1 = u'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy\r\n'
        s2 = u'offending line: ladfj askldfj klasdj fskla dfzaskdj fasklfj laskd fjasklfzzzzaa%whereisthis!!!\r\n'
        s3 = u'next line.\r\n'
        s = (s1 + s2 + s3).encode(self.encoding)
        stream = StringIO.StringIO(s)
        reader = codecs.getreader(self.encoding)(stream)
        self.assertEqual(reader.readline(), s1)
        self.assertEqual(reader.readline(), s2)
        self.assertEqual(reader.readline(), s3)
        self.assertEqual(reader.readline(), u'')

    def test_bug1098990_b(self):
        s1 = u'aaaaaaaaaaaaaaaaaaaaaaaa\r\n'
        s2 = u'bbbbbbbbbbbbbbbbbbbbbbbb\r\n'
        s3 = u'stillokay:bbbbxx\r\n'
        s4 = u'broken!!!!badbad\r\n'
        s5 = u'againokay.\r\n'
        s = (s1 + s2 + s3 + s4 + s5).encode(self.encoding)
        stream = StringIO.StringIO(s)
        reader = codecs.getreader(self.encoding)(stream)
        self.assertEqual(reader.readline(), s1)
        self.assertEqual(reader.readline(), s2)
        self.assertEqual(reader.readline(), s3)
        self.assertEqual(reader.readline(), s4)
        self.assertEqual(reader.readline(), s5)
        self.assertEqual(reader.readline(), u'')


class UTF32Test(ReadTest):
    encoding = 'utf-32'
    spamle = '\xff\xfe\x00\x00s\x00\x00\x00p\x00\x00\x00a\x00\x00\x00m\x00\x00\x00s\x00\x00\x00p\x00\x00\x00a\x00\x00\x00m\x00\x00\x00'
    spambe = '\x00\x00\xfe\xff\x00\x00\x00s\x00\x00\x00p\x00\x00\x00a\x00\x00\x00m\x00\x00\x00s\x00\x00\x00p\x00\x00\x00a\x00\x00\x00m'

    def test_only_one_bom(self):
        _, _, reader, writer = codecs.lookup(self.encoding)
        s = StringIO.StringIO()
        f = writer(s)
        f.write(u'spam')
        f.write(u'spam')
        d = s.getvalue()
        self.assertTrue(d == self.spamle or d == self.spambe)
        s = StringIO.StringIO(d)
        f = reader(s)
        self.assertEqual(f.read(), u'spamspam')

    def test_badbom(self):
        s = StringIO.StringIO('\xff\xff\xff\xff')
        f = codecs.getreader(self.encoding)(s)
        self.assertRaises(UnicodeError, f.read)
        s = StringIO.StringIO('\xff\xff\xff\xff\xff\xff\xff\xff')
        f = codecs.getreader(self.encoding)(s)
        self.assertRaises(UnicodeError, f.read)

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'',
         u'',
         u'',
         u'',
         u'',
         u'',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_handlers(self):
        self.assertEqual((u'\ufffd', 1), codecs.utf_32_decode('\x01', 'replace', True))
        self.assertEqual((u'', 1), codecs.utf_32_decode('\x01', 'ignore', True))

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_32_decode, '\xff', 'strict', True)

    def test_issue8941(self):
        encoded_le = '\xff\xfe\x00\x00' + '\x00\x00\x01\x00' * 1024
        self.assertEqual(u'\U00010000' * 1024, codecs.utf_32_decode(encoded_le)[0])
        encoded_be = '\x00\x00\xfe\xff' + '\x00\x01\x00\x00' * 1024
        self.assertEqual(u'\U00010000' * 1024, codecs.utf_32_decode(encoded_be)[0])


class UTF32LETest(ReadTest):
    encoding = 'utf-32-le'

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'',
         u'',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_simple(self):
        self.assertEqual(u'\U00010203'.encode(self.encoding), '\x03\x02\x01\x00')

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_32_le_decode, '\xff', 'strict', True)

    def test_issue8941(self):
        encoded = '\x00\x00\x01\x00' * 1024
        self.assertEqual(u'\U00010000' * 1024, codecs.utf_32_le_decode(encoded)[0])


class UTF32BETest(ReadTest):
    encoding = 'utf-32-be'

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'',
         u'',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_simple(self):
        self.assertEqual(u'\U00010203'.encode(self.encoding), '\x00\x01\x02\x03')

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_32_be_decode, '\xff', 'strict', True)

    def test_issue8941(self):
        encoded = '\x00\x01\x00\x00' * 1024
        self.assertEqual(u'\U00010000' * 1024, codecs.utf_32_be_decode(encoded)[0])


class UTF16Test(ReadTest):
    encoding = 'utf-16'
    spamle = '\xff\xfes\x00p\x00a\x00m\x00s\x00p\x00a\x00m\x00'
    spambe = '\xfe\xff\x00s\x00p\x00a\x00m\x00s\x00p\x00a\x00m'

    def test_only_one_bom(self):
        _, _, reader, writer = codecs.lookup(self.encoding)
        s = StringIO.StringIO()
        f = writer(s)
        f.write(u'spam')
        f.write(u'spam')
        d = s.getvalue()
        self.assertTrue(d == self.spamle or d == self.spambe)
        s = StringIO.StringIO(d)
        f = reader(s)
        self.assertEqual(f.read(), u'spamspam')

    def test_badbom(self):
        s = StringIO.StringIO('\xff\xff')
        f = codecs.getreader(self.encoding)(s)
        self.assertRaises(UnicodeError, f.read)
        s = StringIO.StringIO('\xff\xff\xff\xff')
        f = codecs.getreader(self.encoding)(s)
        self.assertRaises(UnicodeError, f.read)

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'',
         u'',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_handlers(self):
        self.assertEqual((u'\ufffd', 1), codecs.utf_16_decode('\x01', 'replace', True))
        self.assertEqual((u'', 1), codecs.utf_16_decode('\x01', 'ignore', True))

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_16_decode, '\xff', 'strict', True)

    def test_bug691291(self):
        s1 = u'Hello\r\nworld\r\n'
        s = s1.encode(self.encoding)
        self.addCleanup(test_support.unlink, test_support.TESTFN)
        with open(test_support.TESTFN, 'wb') as fp:
            fp.write(s)
        with codecs.open(test_support.TESTFN, 'U', encoding=self.encoding) as reader:
            self.assertEqual(reader.read(), s1)


class UTF16LETest(ReadTest):
    encoding = 'utf-16-le'

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_16_le_decode, '\xff', 'strict', True)


class UTF16BETest(ReadTest):
    encoding = 'utf-16-be'

    def test_partial(self):
        self.check_partial(u'\x00\xff\u0100\uffff', [u'',
         u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100',
         u'\x00\xff\u0100\uffff'])

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_16_be_decode, '\xff', 'strict', True)


class UTF8Test(ReadTest):
    encoding = 'utf-8'

    def test_partial(self):
        self.check_partial(u'\x00\xff\u07ff\u0800\uffff', [u'\x00',
         u'\x00',
         u'\x00\xff',
         u'\x00\xff',
         u'\x00\xff\u07ff',
         u'\x00\xff\u07ff',
         u'\x00\xff\u07ff',
         u'\x00\xff\u07ff\u0800',
         u'\x00\xff\u07ff\u0800',
         u'\x00\xff\u07ff\u0800',
         u'\x00\xff\u07ff\u0800\uffff'])


class UTF7Test(ReadTest):
    encoding = 'utf-7'

    def test_partial(self):
        self.check_partial(u'a+-b', [u'a',
         u'a',
         u'a+',
         u'a+-',
         u'a+-b'])


class UTF16ExTest(unittest.TestCase):

    def test_errors(self):
        self.assertRaises(UnicodeDecodeError, codecs.utf_16_ex_decode, '\xff', 'strict', 0, True)

    def test_bad_args(self):
        self.assertRaises(TypeError, codecs.utf_16_ex_decode)


class ReadBufferTest(unittest.TestCase):

    def test_array(self):
        import array
        self.assertEqual(codecs.readbuffer_encode(array.array('c', 'spam')), ('spam', 4))

    def test_empty(self):
        self.assertEqual(codecs.readbuffer_encode(''), ('', 0))

    def test_bad_args(self):
        self.assertRaises(TypeError, codecs.readbuffer_encode)
        self.assertRaises(TypeError, codecs.readbuffer_encode, 42)


class CharBufferTest(unittest.TestCase):

    def test_string(self):
        self.assertEqual(codecs.charbuffer_encode('spam'), ('spam', 4))

    def test_empty(self):
        self.assertEqual(codecs.charbuffer_encode(''), ('', 0))

    def test_bad_args(self):
        self.assertRaises(TypeError, codecs.charbuffer_encode)
        self.assertRaises(TypeError, codecs.charbuffer_encode, 42)


class UTF8SigTest(ReadTest):
    encoding = 'utf-8-sig'

    def test_partial(self):
        self.check_partial(u'\ufeff\x00\xff\u07ff\u0800\uffff', [u'',
         u'',
         u'',
         u'',
         u'',
         u'\ufeff',
         u'\ufeff\x00',
         u'\ufeff\x00',
         u'\ufeff\x00\xff',
         u'\ufeff\x00\xff',
         u'\ufeff\x00\xff\u07ff',
         u'\ufeff\x00\xff\u07ff',
         u'\ufeff\x00\xff\u07ff',
         u'\ufeff\x00\xff\u07ff\u0800',
         u'\ufeff\x00\xff\u07ff\u0800',
         u'\ufeff\x00\xff\u07ff\u0800',
         u'\ufeff\x00\xff\u07ff\u0800\uffff'])

    def test_bug1601501(self):
        unicode('\xef\xbb\xbf', 'utf-8-sig')

    def test_bom(self):
        d = codecs.getincrementaldecoder('utf-8-sig')()
        s = u'spam'
        self.assertEqual(d.decode(s.encode('utf-8-sig')), s)

    def test_stream_bom--- This code section failed: ---

0	LOAD_CONST        u'ABC\xa1\u2200XYZ'
3	STORE_FAST        'unistring'

6	LOAD_GLOBAL       'codecs'
9	LOAD_ATTR         'BOM_UTF8'
12	LOAD_CONST        'ABC\xc2\xa1\xe2\x88\x80XYZ'
15	BINARY_ADD        None
16	STORE_FAST        'bytestring'

19	LOAD_GLOBAL       'codecs'
22	LOAD_ATTR         'getreader'
25	LOAD_CONST        'utf-8-sig'
28	CALL_FUNCTION_1   None
31	STORE_FAST        'reader'

34	SETUP_LOOP        '219'
37	LOAD_CONST        None
40	BUILD_LIST_1      None
43	LOAD_GLOBAL       'range'
46	LOAD_CONST        1
49	LOAD_CONST        11
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
76	FOR_ITER          '218'
79	STORE_FAST        'sizehint'

82	LOAD_FAST         'reader'
85	LOAD_GLOBAL       'StringIO'
88	LOAD_ATTR         'StringIO'
91	LOAD_FAST         'bytestring'
94	CALL_FUNCTION_1   None
97	CALL_FUNCTION_1   None
100	STORE_FAST        'istream'

103	LOAD_GLOBAL       'StringIO'
106	LOAD_ATTR         'StringIO'
109	CALL_FUNCTION_0   None
112	STORE_FAST        'ostream'

115	SETUP_LOOP        '187'

118	LOAD_FAST         'sizehint'
121	LOAD_CONST        None
124	COMPARE_OP        'is not'
127	POP_JUMP_IF_FALSE '148'

130	LOAD_FAST         'istream'
133	LOAD_ATTR         'read'
136	LOAD_FAST         'sizehint'
139	CALL_FUNCTION_1   None
142	STORE_FAST        'data'
145	JUMP_FORWARD      '160'

148	LOAD_FAST         'istream'
151	LOAD_ATTR         'read'
154	CALL_FUNCTION_0   None
157	STORE_FAST        'data'
160_0	COME_FROM         '145'

160	LOAD_FAST         'data'
163	POP_JUMP_IF_TRUE  '170'

166	BREAK_LOOP        None
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	LOAD_FAST         'ostream'
173	LOAD_ATTR         'write'
176	LOAD_FAST         'data'
179	CALL_FUNCTION_1   None
182	POP_TOP           None
183	JUMP_BACK         '118'
186	POP_BLOCK         None
187_0	COME_FROM         '115'

187	LOAD_FAST         'ostream'
190	LOAD_ATTR         'getvalue'
193	CALL_FUNCTION_0   None
196	STORE_FAST        'got'

199	LOAD_FAST         'self'
202	LOAD_ATTR         'assertEqual'
205	LOAD_FAST         'got'
208	LOAD_FAST         'unistring'
211	CALL_FUNCTION_2   None
214	POP_TOP           None
215	JUMP_BACK         '76'
218	POP_BLOCK         None
219_0	COME_FROM         '34'
219	LOAD_CONST        None
222	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 186

    def test_stream_bare--- This code section failed: ---

0	LOAD_CONST        u'ABC\xa1\u2200XYZ'
3	STORE_FAST        'unistring'

6	LOAD_CONST        'ABC\xc2\xa1\xe2\x88\x80XYZ'
9	STORE_FAST        'bytestring'

12	LOAD_GLOBAL       'codecs'
15	LOAD_ATTR         'getreader'
18	LOAD_CONST        'utf-8-sig'
21	CALL_FUNCTION_1   None
24	STORE_FAST        'reader'

27	SETUP_LOOP        '212'
30	LOAD_CONST        None
33	BUILD_LIST_1      None
36	LOAD_GLOBAL       'range'
39	LOAD_CONST        1
42	LOAD_CONST        11
45	CALL_FUNCTION_2   None
48	BINARY_ADD        None

49	LOAD_CONST        64
52	LOAD_CONST        128
55	LOAD_CONST        256
58	LOAD_CONST        512
61	LOAD_CONST        1024
64	BUILD_LIST_5      None
67	BINARY_ADD        None
68	GET_ITER          None
69	FOR_ITER          '211'
72	STORE_FAST        'sizehint'

75	LOAD_FAST         'reader'
78	LOAD_GLOBAL       'StringIO'
81	LOAD_ATTR         'StringIO'
84	LOAD_FAST         'bytestring'
87	CALL_FUNCTION_1   None
90	CALL_FUNCTION_1   None
93	STORE_FAST        'istream'

96	LOAD_GLOBAL       'StringIO'
99	LOAD_ATTR         'StringIO'
102	CALL_FUNCTION_0   None
105	STORE_FAST        'ostream'

108	SETUP_LOOP        '180'

111	LOAD_FAST         'sizehint'
114	LOAD_CONST        None
117	COMPARE_OP        'is not'
120	POP_JUMP_IF_FALSE '141'

123	LOAD_FAST         'istream'
126	LOAD_ATTR         'read'
129	LOAD_FAST         'sizehint'
132	CALL_FUNCTION_1   None
135	STORE_FAST        'data'
138	JUMP_FORWARD      '153'

141	LOAD_FAST         'istream'
144	LOAD_ATTR         'read'
147	CALL_FUNCTION_0   None
150	STORE_FAST        'data'
153_0	COME_FROM         '138'

153	LOAD_FAST         'data'
156	POP_JUMP_IF_TRUE  '163'

159	BREAK_LOOP        None
160	JUMP_FORWARD      '163'
163_0	COME_FROM         '160'

163	LOAD_FAST         'ostream'
166	LOAD_ATTR         'write'
169	LOAD_FAST         'data'
172	CALL_FUNCTION_1   None
175	POP_TOP           None
176	JUMP_BACK         '111'
179	POP_BLOCK         None
180_0	COME_FROM         '108'

180	LOAD_FAST         'ostream'
183	LOAD_ATTR         'getvalue'
186	CALL_FUNCTION_0   None
189	STORE_FAST        'got'

192	LOAD_FAST         'self'
195	LOAD_ATTR         'assertEqual'
198	LOAD_FAST         'got'
201	LOAD_FAST         'unistring'
204	CALL_FUNCTION_2   None
207	POP_TOP           None
208	JUMP_BACK         '69'
211	POP_BLOCK         None
212_0	COME_FROM         '27'
212	LOAD_CONST        None
215	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 179


class EscapeDecodeTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(codecs.escape_decode(''), ('', 0))


class RecodingTest(unittest.TestCase):

    def test_recoding(self):
        f = StringIO.StringIO()
        f2 = codecs.EncodedFile(f, 'unicode_internal', 'utf-8')
        f2.write(u'a')
        f2.close()


punycode_testcases = [(u'\u0644\u064a\u0647\u0645\u0627\u0628\u062a\u0643\u0644\u0645\u0648\u0634\u0639\u0631\u0628\u064a\u061f', 'egbpdaj6bu4bxfgehfvwxn'),
 (u'\u4ed6\u4eec\u4e3a\u4ec0\u4e48\u4e0d\u8bf4\u4e2d\u6587', 'ihqwcrb4cv8a8dqg056pqjye'),
 (u'\u4ed6\u5011\u7232\u4ec0\u9ebd\u4e0d\u8aaa\u4e2d\u6587', 'ihqwctvzc91f659drss3x8bo0yb'),
 (u'Pro\u010dprost\u011bnemluv\xed\u010desky', 'Proprostnemluvesky-uyb24dma41a'),
 (u'\u05dc\u05de\u05d4\u05d4\u05dd\u05e4\u05e9\u05d5\u05d8\u05dc\u05d0\u05de\u05d3\u05d1\u05e8\u05d9\u05dd\u05e2\u05d1\u05e8\u05d9\u05ea', '4dbcagdahymbxekheh6e0a7fei0b'),
 (u'\u092f\u0939\u0932\u094b\u0917\u0939\u093f\u0928\u094d\u0926\u0940\u0915\u094d\u092f\u094b\u0902\u0928\u0939\u0940\u0902\u092c\u094b\u0932\u0938\u0915\u0924\u0947\u0939\u0948\u0902', 'i1baa7eci9glrd9b2ae1bj0hfcgg6iyaf8o0a1dig0cd'),
 (u'\u306a\u305c\u307f\u3093\u306a\u65e5\u672c\u8a9e\u3092\u8a71\u3057\u3066\u304f\u308c\u306a\u3044\u306e\u304b', 'n8jok5ay5dzabd5bym9f0cm5685rrjetr6pdxa'),
 (u'\uc138\uacc4\uc758\ubaa8\ub4e0\uc0ac\ub78c\ub4e4\uc774\ud55c\uad6d\uc5b4\ub97c\uc774\ud574\ud55c\ub2e4\uba74\uc5bc\ub9c8\ub098\uc88b\uc744\uae4c', '989aomsvi5e83db1d2a355cv1e0vak1dwrv93d5xbh15a0dt30a5jpsd879ccm6fea98c'),
 (u'\u043f\u043e\u0447\u0435\u043c\u0443\u0436\u0435\u043e\u043d\u0438\u043d\u0435\u0433\u043e\u0432\u043e\u0440\u044f\u0442\u043f\u043e\u0440\u0443\u0441\u0441\u043a\u0438', 'b1abfaaepdrnnbgefbaDotcwatmq2g4l'),
 (u'Porqu\xe9nopuedensimplementehablarenEspa\xf1ol', 'PorqunopuedensimplementehablarenEspaol-fmd56a'),
 (u'T\u1ea1isaoh\u1ecdkh\xf4ngth\u1ec3ch\u1ec9n\xf3iti\u1ebfngVi\u1ec7t', 'TisaohkhngthchnitingVit-kjcr8268qyxafd2f1b9g'),
 (u'3\u5e74B\u7d44\u91d1\u516b\u5148\u751f', '3B-ww4c5e180e575a65lsy2b'),
 (u'\u5b89\u5ba4\u5948\u7f8e\u6075-with-SUPER-MONKEYS', '-with-SUPER-MONKEYS-pc58ag80a8qai00g7n9n'),
 (u'Hello-Another-Way-\u305d\u308c\u305e\u308c\u306e\u5834\u6240', 'Hello-Another-Way--fc4qua05auwb3674vfr0b'),
 (u'\u3072\u3068\u3064\u5c4b\u6839\u306e\u4e0b2', '2-u9tlzr9756bt3uc0v'),
 (u'Maji\u3067Koi\u3059\u308b5\u79d2\u524d', 'MajiKoi5-783gue6qz075azm5e'),
 (u'\u30d1\u30d5\u30a3\u30fcde\u30eb\u30f3\u30d0', 'de-jg4avhby1noc0d'),
 (u'\u305d\u306e\u30b9\u30d4\u30fc\u30c9\u3067', 'd9juau41awczczp'),
 (u'-> $1.00 <-', '-> $1.00 <--')]
for i in punycode_testcases:
    if len(i) != 2:
        print repr(i)

class PunycodeTest(unittest.TestCase):

    def test_encode(self):
        for uni, puny in punycode_testcases:
            self.assertEqual(uni.encode('punycode').lower(), puny.lower())

    def test_decode(self):
        for uni, puny in punycode_testcases:
            self.assertEqual(uni, puny.decode('punycode'))


class UnicodeInternalTest(unittest.TestCase):

    def test_bug1251300(self):
        if sys.maxunicode > 65535:
            ok = [('\x00\x10\xff\xff', u'\U0010ffff'), ('\x00\x00\x01\x01', u'\u0101'), ('', u'')]
            not_ok = ['\x7f\xff\xff\xff',
             '\x80\x00\x00\x00',
             '\x81\x00\x00\x00',
             '\x00',
             '\x00\x00\x00\x00\x00']
            for internal, uni in ok:
                if sys.byteorder == 'little':
                    internal = ''.join(reversed(internal))
                self.assertEqual(uni, internal.decode('unicode_internal'))

            for internal in not_ok:
                if sys.byteorder == 'little':
                    internal = ''.join(reversed(internal))
                self.assertRaises(UnicodeDecodeError, internal.decode, 'unicode_internal')

    def test_decode_error_attributes(self):
        if sys.maxunicode > 65535:
            try:
                '\x00\x00\x00\x00\x00\x11\x11\x00'.decode('unicode_internal')
            except UnicodeDecodeError as ex:
                self.assertEqual('unicode_internal', ex.encoding)
                self.assertEqual('\x00\x00\x00\x00\x00\x11\x11\x00', ex.object)
                self.assertEqual(4, ex.start)
                self.assertEqual(8, ex.end)
            else:
                self.fail()

    def test_decode_callback(self):
        if sys.maxunicode > 65535:
            codecs.register_error('UnicodeInternalTest', codecs.ignore_errors)
            decoder = codecs.getdecoder('unicode_internal')
            ab = u'ab'.encode('unicode_internal')
            ignored = decoder('%s""""%s' % (ab[:4], ab[4:]), 'UnicodeInternalTest')
            self.assertEqual((u'ab', 12), ignored)

    def test_encode_length(self):
        encoder = codecs.getencoder('unicode_internal')
        self.assertEqual(encoder(u'a')[1], 1)
        self.assertEqual(encoder(u'\xe9\u0142')[1], 2)
        encoder = codecs.getencoder('string-escape')
        self.assertEqual(encoder('\\x00')[1], 4)


nameprep_tests = [('foo\xc2\xad\xcd\x8f\xe1\xa0\x86\xe1\xa0\x8bbar\xe2\x80\x8b\xe2\x81\xa0baz\xef\xb8\x80\xef\xb8\x88\xef\xb8\x8f\xef\xbb\xbf', 'foobarbaz'),
 ('CAFE', 'cafe'),
 ('\xc3\x9f', 'ss'),
 ('\xc4\xb0', 'i\xcc\x87'),
 ('\xc5\x83\xcd\xba', '\xc5\x84 \xce\xb9'),
 (None, None),
 ('j\xcc\x8c\xc2\xa0\xc2\xaa', '\xc7\xb0 a'),
 ('\xe1\xbe\xb7', '\xe1\xbe\xb6\xce\xb9'),
 ('\xc7\xb0', '\xc7\xb0'),
 ('\xce\x90', '\xce\x90'),
 ('\xce\xb0', '\xce\xb0'),
 ('\xe1\xba\x96', '\xe1\xba\x96'),
 ('\xe1\xbd\x96', '\xe1\xbd\x96'),
 (' ', ' '),
 ('\xc2\xa0', ' '),
 ('\xe1\x9a\x80', None),
 ('\xe2\x80\x80', ' '),
 ('\xe2\x80\x8b', ''),
 ('\xe3\x80\x80', ' '),
 ('\x10\x7f', '\x10\x7f'),
 ('\xc2\x85', None),
 ('\xe1\xa0\x8e', None),
 ('\xef\xbb\xbf', ''),
 ('\xf0\x9d\x85\xb5', None),
 ('\xef\x84\xa3', None),
 ('\xf3\xb1\x88\xb4', None),
 ('\xf4\x8f\x88\xb4', None),
 ('\xf2\x8f\xbf\xbe', None),
 ('\xf4\x8f\xbf\xbf', None),
 ('\xed\xbd\x82', None),
 ('\xef\xbf\xbd', None),
 ('\xe2\xbf\xb5', None),
 ('\xcd\x81', '\xcc\x81'),
 ('\xe2\x80\x8e', None),
 ('\xe2\x80\xaa', None),
 ('\xf3\xa0\x80\x81', None),
 ('\xf3\xa0\x81\x82', None),
 ('foo\xd6\xbebar', None),
 ('foo\xef\xb5\x90bar', None),
 ('foo\xef\xb9\xb6bar', 'foo \xd9\x8ebar'),
 ('\xd8\xa71', None),
 ('\xd8\xa71\xd8\xa8', '\xd8\xa71\xd8\xa8'),
 (None, None),
 ('X\xc2\xad\xc3\x9f\xc4\xb0\xe2\x84\xa1j\xcc\x8c\xc2\xa0\xc2\xaa\xce\xb0\xe2\x80\x80', 'xssi\xcc\x87tel\xc7\xb0 a\xce\xb0 '),
 ('X\xc3\x9f\xe3\x8c\x96\xc4\xb0\xe2\x84\xa1\xe2\x92\x9f\xe3\x8c\x80', 'xss\xe3\x82\xad\xe3\x83\xad\xe3\x83\xa1\xe3\x83\xbc\xe3\x83\x88\xe3\x83\xabi\xcc\x87tel(d)\xe3\x82\xa2\xe3\x83\x91\xe3\x83\xbc\xe3\x83\x88')]

class NameprepTest(unittest.TestCase):

    def test_nameprep(self):
        from encodings.idna import nameprep
        for pos, (orig, prepped) in enumerate(nameprep_tests):
            if orig is None:
                continue
            orig = unicode(orig, 'utf-8')
            if prepped is None:
                self.assertRaises(UnicodeError, nameprep, orig)
            else:
                prepped = unicode(prepped, 'utf-8')
                try:
                    self.assertEqual(nameprep(orig), prepped)
                except Exception as e:
                    raise test_support.TestFailed('Test 3.%d: %s' % (pos + 1, str(e)))

        return


class IDNACodecTest(unittest.TestCase):

    def test_builtin_decode(self):
        self.assertEqual(unicode('python.org', 'idna'), u'python.org')
        self.assertEqual(unicode('python.org.', 'idna'), u'python.org.')
        self.assertEqual(unicode('xn--pythn-mua.org', 'idna'), u'pyth\xf6n.org')
        self.assertEqual(unicode('xn--pythn-mua.org.', 'idna'), u'pyth\xf6n.org.')

    def test_builtin_encode(self):
        self.assertEqual(u'python.org'.encode('idna'), 'python.org')
        self.assertEqual('python.org.'.encode('idna'), 'python.org.')
        self.assertEqual(u'pyth\xf6n.org'.encode('idna'), 'xn--pythn-mua.org')
        self.assertEqual(u'pyth\xf6n.org.'.encode('idna'), 'xn--pythn-mua.org.')

    def test_stream(self):
        import StringIO
        r = codecs.getreader('idna')(StringIO.StringIO('abc'))
        r.read(3)
        self.assertEqual(r.read(), u'')

    def test_incremental_decode(self):
        self.assertEqual(''.join(codecs.iterdecode('python.org', 'idna')), u'python.org')
        self.assertEqual(''.join(codecs.iterdecode('python.org.', 'idna')), u'python.org.')
        self.assertEqual(''.join(codecs.iterdecode('xn--pythn-mua.org.', 'idna')), u'pyth\xf6n.org.')
        self.assertEqual(''.join(codecs.iterdecode('xn--pythn-mua.org.', 'idna')), u'pyth\xf6n.org.')
        decoder = codecs.getincrementaldecoder('idna')()
        self.assertEqual(decoder.decode('xn--xam'), u'')
        self.assertEqual(decoder.decode('ple-9ta.o'), u'\xe4xample.')
        self.assertEqual(decoder.decode(u'rg'), u'')
        self.assertEqual(decoder.decode(u'', True), u'org')
        decoder.reset()
        self.assertEqual(decoder.decode('xn--xam'), u'')
        self.assertEqual(decoder.decode('ple-9ta.o'), u'\xe4xample.')
        self.assertEqual(decoder.decode('rg.'), u'org.')
        self.assertEqual(decoder.decode('', True), u'')

    def test_incremental_encode(self):
        self.assertEqual(''.join(codecs.iterencode(u'python.org', 'idna')), 'python.org')
        self.assertEqual(''.join(codecs.iterencode(u'python.org.', 'idna')), 'python.org.')
        self.assertEqual(''.join(codecs.iterencode(u'pyth\xf6n.org.', 'idna')), 'xn--pythn-mua.org.')
        self.assertEqual(''.join(codecs.iterencode(u'pyth\xf6n.org.', 'idna')), 'xn--pythn-mua.org.')
        encoder = codecs.getincrementalencoder('idna')()
        self.assertEqual(encoder.encode(u'\xe4x'), '')
        self.assertEqual(encoder.encode(u'ample.org'), 'xn--xample-9ta.')
        self.assertEqual(encoder.encode(u'', True), 'org')
        encoder.reset()
        self.assertEqual(encoder.encode(u'\xe4x'), '')
        self.assertEqual(encoder.encode(u'ample.org.'), 'xn--xample-9ta.org.')
        self.assertEqual(encoder.encode(u'', True), '')


class CodecsModuleTest(unittest.TestCase):

    def test_decode(self):
        self.assertEqual(codecs.decode('\xe4\xf6\xfc', 'latin-1'), u'\xe4\xf6\xfc')
        self.assertRaises(TypeError, codecs.decode)
        self.assertEqual(codecs.decode('abc'), u'abc')
        self.assertRaises(UnicodeDecodeError, codecs.decode, '\xff', 'ascii')

    def test_encode(self):
        self.assertEqual(codecs.encode(u'\xe4\xf6\xfc', 'latin-1'), '\xe4\xf6\xfc')
        self.assertRaises(TypeError, codecs.encode)
        self.assertRaises(LookupError, codecs.encode, 'foo', '__spam__')
        self.assertEqual(codecs.encode(u'abc'), 'abc')
        self.assertRaises(UnicodeEncodeError, codecs.encode, u'\xffff', 'ascii')

    def test_register(self):
        self.assertRaises(TypeError, codecs.register)
        self.assertRaises(TypeError, codecs.register, 42)

    def test_lookup(self):
        self.assertRaises(TypeError, codecs.lookup)
        self.assertRaises(LookupError, codecs.lookup, '__spam__')
        self.assertRaises(LookupError, codecs.lookup, ' ')

    def test_getencoder(self):
        self.assertRaises(TypeError, codecs.getencoder)
        self.assertRaises(LookupError, codecs.getencoder, '__spam__')

    def test_getdecoder(self):
        self.assertRaises(TypeError, codecs.getdecoder)
        self.assertRaises(LookupError, codecs.getdecoder, '__spam__')

    def test_getreader(self):
        self.assertRaises(TypeError, codecs.getreader)
        self.assertRaises(LookupError, codecs.getreader, '__spam__')

    def test_getwriter(self):
        self.assertRaises(TypeError, codecs.getwriter)
        self.assertRaises(LookupError, codecs.getwriter, '__spam__')

    def test_lookup_issue1813(self):
        oldlocale = locale.getlocale(locale.LC_CTYPE)
        self.addCleanup(locale.setlocale, locale.LC_CTYPE, oldlocale)
        try:
            locale.setlocale(locale.LC_CTYPE, 'tr_TR')
        except locale.Error:
            self.skipTest('test needs Turkish locale')

        c = codecs.lookup('ASCII')
        self.assertEqual(c.name, 'ascii')


class StreamReaderTest(unittest.TestCase):

    def setUp(self):
        self.reader = codecs.getreader('utf-8')
        self.stream = StringIO.StringIO('\xed\x95\x9c\n\xea\xb8\x80')

    def test_readlines(self):
        f = self.reader(self.stream)
        self.assertEqual(f.readlines(), [u'\ud55c\n', u'\uae00'])


class EncodedFileTest(unittest.TestCase):

    def test_basic(self):
        f = StringIO.StringIO('\xed\x95\x9c\n\xea\xb8\x80')
        ef = codecs.EncodedFile(f, 'utf-16-le', 'utf-8')
        self.assertEqual(ef.read(), '\\\xd5\n\x00\x00\xae')
        f = StringIO.StringIO()
        ef = codecs.EncodedFile(f, 'utf-8', 'latin1')
        ef.write('\xc3\xbc')
        self.assertEqual(f.getvalue(), '\xfc')


class Str2StrTest(unittest.TestCase):

    def test_read(self):
        sin = '\x80'.encode('base64_codec')
        reader = codecs.getreader('base64_codec')(StringIO.StringIO(sin))
        sout = reader.read()
        self.assertEqual(sout, '\x80')
        self.assertIsInstance(sout, str)

    def test_readline(self):
        sin = '\x80'.encode('base64_codec')
        reader = codecs.getreader('base64_codec')(StringIO.StringIO(sin))
        sout = reader.readline()
        self.assertEqual(sout, '\x80')
        self.assertIsInstance(sout, str)


all_unicode_encodings = ['ascii',
 'base64_codec',
 'big5',
 'big5hkscs',
 'charmap',
 'cp037',
 'cp1006',
 'cp1026',
 'cp1140',
 'cp1250',
 'cp1251',
 'cp1252',
 'cp1253',
 'cp1254',
 'cp1255',
 'cp1256',
 'cp1257',
 'cp1258',
 'cp424',
 'cp437',
 'cp500',
 'cp720',
 'cp737',
 'cp775',
 'cp850',
 'cp852',
 'cp855',
 'cp856',
 'cp857',
 'cp858',
 'cp860',
 'cp861',
 'cp862',
 'cp863',
 'cp864',
 'cp865',
 'cp866',
 'cp869',
 'cp874',
 'cp875',
 'cp932',
 'cp949',
 'cp950',
 'euc_jis_2004',
 'euc_jisx0213',
 'euc_jp',
 'euc_kr',
 'gb18030',
 'gb2312',
 'gbk',
 'hex_codec',
 'hp_roman8',
 'hz',
 'idna',
 'iso2022_jp',
 'iso2022_jp_1',
 'iso2022_jp_2',
 'iso2022_jp_2004',
 'iso2022_jp_3',
 'iso2022_jp_ext',
 'iso2022_kr',
 'iso8859_1',
 'iso8859_10',
 'iso8859_11',
 'iso8859_13',
 'iso8859_14',
 'iso8859_15',
 'iso8859_16',
 'iso8859_2',
 'iso8859_3',
 'iso8859_4',
 'iso8859_5',
 'iso8859_6',
 'iso8859_7',
 'iso8859_8',
 'iso8859_9',
 'johab',
 'koi8_r',
 'koi8_u',
 'latin_1',
 'mac_cyrillic',
 'mac_greek',
 'mac_iceland',
 'mac_latin2',
 'mac_roman',
 'mac_turkish',
 'palmos',
 'ptcp154',
 'punycode',
 'raw_unicode_escape',
 'rot_13',
 'shift_jis',
 'shift_jis_2004',
 'shift_jisx0213',
 'tis_620',
 'unicode_escape',
 'unicode_internal',
 'utf_16',
 'utf_16_be',
 'utf_16_le',
 'utf_7',
 'utf_8']
if hasattr(codecs, 'mbcs_encode'):
    all_unicode_encodings.append('mbcs')
all_string_encodings = ['quopri_codec', 'string_escape', 'uu_codec']
broken_unicode_with_streams = ['base64_codec',
 'hex_codec',
 'punycode',
 'unicode_internal']
broken_incremental_coders = broken_unicode_with_streams[:]
only_strict_mode = ['idna', 'zlib_codec', 'bz2_codec']
try:
    import bz2
except ImportError:
    pass
else:
    all_unicode_encodings.append('bz2_codec')
    broken_unicode_with_streams.append('bz2_codec')

try:
    import zlib
except ImportError:
    pass
else:
    all_unicode_encodings.append('zlib_codec')
    broken_unicode_with_streams.append('zlib_codec')

class BasicUnicodeTest(unittest.TestCase):

    def test_basics(self):
        s = u'abc123'
        for encoding in all_unicode_encodings:
            name = codecs.lookup(encoding).name
            if encoding.endswith('_codec'):
                name += '_codec'
            elif encoding == 'latin_1':
                name = 'latin_1'
            self.assertEqual(encoding.replace('_', '-'), name.replace('_', '-'))
            bytes, size = codecs.getencoder(encoding)(s)
            self.assertEqual(size, len(s), '%r != %r (encoding=%r)' % (size, len(s), encoding))
            chars, size = codecs.getdecoder(encoding)(bytes)
            self.assertEqual(chars, s, '%r != %r (encoding=%r)' % (chars, s, encoding))
            if encoding not in broken_unicode_with_streams:
                q = Queue()
                writer = codecs.getwriter(encoding)(q)
                encodedresult = ''
                for c in s:
                    writer.write(c)
                    encodedresult += q.read()

                q = Queue()
                reader = codecs.getreader(encoding)(q)
                decodedresult = u''
                for c in encodedresult:
                    q.write(c)
                    decodedresult += reader.read()

                self.assertEqual(decodedresult, s, '%r != %r (encoding=%r)' % (decodedresult, s, encoding))
            if encoding not in broken_incremental_coders:
                try:
                    encoder = codecs.getincrementalencoder(encoding)()
                    cencoder = _testcapi.codec_incrementalencoder(encoding)
                except LookupError:
                    pass
                else:
                    encodedresult = ''
                    for c in s:
                        encodedresult += encoder.encode(c)

                    encodedresult += encoder.encode(u'', True)
                    decoder = codecs.getincrementaldecoder(encoding)()
                    decodedresult = u''
                    for c in encodedresult:
                        decodedresult += decoder.decode(c)

                    decodedresult += decoder.decode('', True)
                    self.assertEqual(decodedresult, s, '%r != %r (encoding=%r)' % (decodedresult, s, encoding))
                    encodedresult = ''
                    for c in s:
                        encodedresult += cencoder.encode(c)

                    encodedresult += cencoder.encode(u'', True)
                    cdecoder = _testcapi.codec_incrementaldecoder(encoding)
                    decodedresult = u''
                    for c in encodedresult:
                        decodedresult += cdecoder.decode(c)

                    decodedresult += cdecoder.decode('', True)
                    self.assertEqual(decodedresult, s, '%r != %r (encoding=%r)' % (decodedresult, s, encoding))
                    result = u''.join(codecs.iterdecode(codecs.iterencode(s, encoding), encoding))
                    self.assertEqual(result, s, '%r != %r (encoding=%r)' % (result, s, encoding))
                    result = u''.join(codecs.iterdecode(codecs.iterencode(u'', encoding), encoding))
                    self.assertEqual(result, u'')

                if encoding not in only_strict_mode:
                    try:
                        encoder = codecs.getincrementalencoder(encoding)('ignore')
                        cencoder = _testcapi.codec_incrementalencoder(encoding, 'ignore')
                    except LookupError:
                        pass
                    else:
                        encodedresult = ''.join((encoder.encode(c) for c in s))
                        decoder = codecs.getincrementaldecoder(encoding)('ignore')
                        decodedresult = u''.join((decoder.decode(c) for c in encodedresult))
                        self.assertEqual(decodedresult, s, '%r != %r (encoding=%r)' % (decodedresult, s, encoding))
                        encodedresult = ''.join((cencoder.encode(c) for c in s))
                        cdecoder = _testcapi.codec_incrementaldecoder(encoding, 'ignore')
                        decodedresult = u''.join((cdecoder.decode(c) for c in encodedresult))
                        self.assertEqual(decodedresult, s, '%r != %r (encoding=%r)' % (decodedresult, s, encoding))

    def test_seek(self):
        s = u'%s\n%s\n' % (100 * u'abc123', 100 * u'def456')
        for encoding in all_unicode_encodings:
            if encoding == 'idna':
                continue
            if encoding in broken_unicode_with_streams:
                continue
            reader = codecs.getreader(encoding)(StringIO.StringIO(s.encode(encoding)))
            for t in xrange(5):
                reader.seek(0, 0)
                line = reader.readline()
                self.assertEqual(s[:len(line)], line)

    def test_bad_decode_args(self):
        for encoding in all_unicode_encodings:
            decoder = codecs.getdecoder(encoding)
            self.assertRaises(TypeError, decoder)
            if encoding not in ('idna', 'punycode'):
                self.assertRaises(TypeError, decoder, 42)

    def test_bad_encode_args(self):
        for encoding in all_unicode_encodings:
            encoder = codecs.getencoder(encoding)
            self.assertRaises(TypeError, encoder)

    def test_encoding_map_type_initialized(self):
        from encodings import cp1140
        table_type = type(cp1140.encoding_table)
        self.assertEqual(table_type, table_type)


class BasicStrTest(unittest.TestCase):

    def test_basics(self):
        s = 'abc123'
        for encoding in all_string_encodings:
            bytes, size = codecs.getencoder(encoding)(s)
            self.assertEqual(size, len(s))
            chars, size = codecs.getdecoder(encoding)(bytes)
            self.assertEqual(chars, s, '%r != %r (encoding=%r)' % (chars, s, encoding))


class CharmapTest(unittest.TestCase):

    def test_decode_with_string_map(self):
        self.assertEqual(codecs.charmap_decode('\x00\x01\x02', 'strict', u'abc'), (u'abc', 3))
        self.assertEqual(codecs.charmap_decode('\x00\x01\x02', 'replace', u'ab'), (u'ab\ufffd', 3))
        self.assertEqual(codecs.charmap_decode('\x00\x01\x02', 'replace', u'ab\ufffe'), (u'ab\ufffd', 3))
        self.assertEqual(codecs.charmap_decode('\x00\x01\x02', 'ignore', u'ab'), (u'ab', 3))
        self.assertEqual(codecs.charmap_decode('\x00\x01\x02', 'ignore', u'ab\ufffe'), (u'ab', 3))
        allbytes = ''.join((chr(i) for i in xrange(256)))
        self.assertEqual(codecs.charmap_decode(allbytes, 'ignore', u''), (u'', len(allbytes)))


class WithStmtTest(unittest.TestCase):

    def test_encodedfile(self):
        f = StringIO.StringIO('\xc3\xbc')
        with codecs.EncodedFile(f, 'latin-1', 'utf-8') as ef:
            self.assertEqual(ef.read(), '\xfc')

    def test_streamreaderwriter(self):
        f = StringIO.StringIO('\xc3\xbc')
        info = codecs.lookup('utf-8')
        with codecs.StreamReaderWriter(f, info.streamreader, info.streamwriter, 'strict') as srw:
            self.assertEqual(srw.read(), u'\xfc')


class BomTest(unittest.TestCase):

    def test_seek0(self):
        data = u'1234567890'
        tests = ('utf-16', 'utf-16-le', 'utf-16-be', 'utf-32', 'utf-32-le', 'utf-32-be')
        self.addCleanup(test_support.unlink, test_support.TESTFN)
        for encoding in tests:
            with codecs.open(test_support.TESTFN, 'w+', encoding=encoding) as f:
                f.write(data)
                f.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data * 2)
                f.seek(0)
                self.assertEqual(f.read(), data * 2)
            with codecs.open(test_support.TESTFN, 'w+', encoding=encoding) as f:
                f.write(data[0])
                self.assertNotEqual(f.tell(), 0)
                f.seek(0)
                f.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data)
            with codecs.open(test_support.TESTFN, 'w+', encoding=encoding) as f:
                f.writer.write(data[0])
                self.assertNotEqual(f.writer.tell(), 0)
                f.writer.seek(0)
                f.writer.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data)
            with codecs.open(test_support.TESTFN, 'w+', encoding=encoding) as f:
                f.write(data)
                f.seek(f.tell())
                f.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data * 2)
            with codecs.open(test_support.TESTFN, 'w+', encoding=encoding) as f:
                f.writer.write(data)
                f.writer.seek(f.writer.tell())
                f.writer.write(data)
                f.seek(0)
                self.assertEqual(f.read(), data * 2)


def test_main():
    test_support.run_unittest(UTF32Test, UTF32LETest, UTF32BETest, UTF16Test, UTF16LETest, UTF16BETest, UTF8Test, UTF8SigTest, UTF7Test, UTF16ExTest, ReadBufferTest, CharBufferTest, EscapeDecodeTest, RecodingTest, PunycodeTest, UnicodeInternalTest, NameprepTest, IDNACodecTest, CodecsModuleTest, StreamReaderTest, EncodedFileTest, Str2StrTest, BasicUnicodeTest, BasicStrTest, CharmapTest, WithStmtTest, BomTest)


if __name__ == '__main__':
    test_main()