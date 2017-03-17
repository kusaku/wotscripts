# Embedded file name: scripts/common/Lib/test/test_bz2.py
from test import test_support
from test.test_support import TESTFN, import_module
import unittest
from cStringIO import StringIO
import os
import subprocess
import sys
try:
    import threading
except ImportError:
    threading = None

bz2 = import_module('bz2')
from bz2 import BZ2File, BZ2Compressor, BZ2Decompressor
has_cmdline_bunzip2 = sys.platform not in ('win32', 'os2emx', 'riscos')

class BaseTest(unittest.TestCase):
    """Base for other testcases."""
    TEXT = 'root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:\ndaemon:x:2:2:daemon:/sbin:\nadm:x:3:4:adm:/var/adm:\nlp:x:4:7:lp:/var/spool/lpd:\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:\nnews:x:9:13:news:/var/spool/news:\nuucp:x:10:14:uucp:/var/spool/uucp:\noperator:x:11:0:operator:/root:\ngames:x:12:100:games:/usr/games:\ngopher:x:13:30:gopher:/usr/lib/gopher-data:\nftp:x:14:50:FTP User:/var/ftp:/bin/bash\nnobody:x:65534:65534:Nobody:/home:\npostfix:x:100:101:postfix:/var/spool/postfix:\nniemeyer:x:500:500::/home/niemeyer:/bin/bash\npostgres:x:101:102:PostgreSQL Server:/var/lib/pgsql:/bin/bash\nmysql:x:102:103:MySQL server:/var/lib/mysql:/bin/bash\nwww:x:103:104::/var/www:/bin/false\n'
    DATA = 'BZh91AY&SY.\xc8N\x18\x00\x01>_\x80\x00\x10@\x02\xff\xf0\x01\x07n\x00?\xe7\xff\xe00\x01\x99\xaa\x00\xc0\x03F\x86\x8c#&\x83F\x9a\x03\x06\xa6\xd0\xa6\x93M\x0fQ\xa7\xa8\x06\x804hh\x12$\x11\xa4i4\xf14S\xd2<Q\xb5\x0fH\xd3\xd4\xdd\xd5\x87\xbb\xf8\x94\r\x8f\xafI\x12\xe1\xc9\xf8/E\x00pu\x89\x12]\xc9\xbbDL\nQ\x0e\t1\x12\xdf\xa0\xc0\x97\xac2O9\x89\x13\x94\x0e\x1c7\x0ed\x95I\x0c\xaaJ\xa4\x18L\x10\x05#\x9c\xaf\xba\xbc/\x97\x8a#C\xc8\xe1\x8cW\xf9\xe2\xd0\xd6M\xa7\x8bXa<e\x84t\xcbL\xb3\xa7\xd9\xcd\xd1\xcb\x84.\xaf\xb3\xab\xab\xad`n}\xa0lh\tE,\x8eZ\x15\x17VH>\x88\xe5\xcd9gd6\x0b\n\xe9\x9b\xd5\x8a\x99\xf7\x08.K\x8ev\xfb\xf7xw\xbb\xdf\xa1\x92\xf1\xdd|/";\xa2\xba\x9f\xd5\xb1#A\xb6\xf6\xb3o\xc9\xc5y\\\xebO\xe7\x85\x9a\xbc\xb6f8\x952\xd5\xd7"%\x89>V,\xf7\xa6z\xe2\x9f\xa3\xdf\x11\x11"\xd6E)I\xa9\x13^\xca\xf3r\xd0\x03U\x922\xf26\xec\xb6\xed\x8b\xc3U\x13\x9d\xc5\x170\xa4\xfa^\x92\xacDF\x8a\x97\xd6\x19\xfe\xdd\xb8\xbd\x1a\x9a\x19\xa3\x80ankR\x8b\xe5\xd83]\xa9\xc6\x08\x82f\xf6\xb9"6l$\xb8j@\xc0\x8a\xb0l1..\xbak\x83ls\x15\xbc\xf4\xc1\x13\xbe\xf8E\xb8\x9d\r\xa8\x9dk\x84\xd3n\xfa\xacQ\x07\xb1%y\xaav\xb4\x08\xe0z\x1b\x16\xf5\x04\xe9\xcc\xb9\x08z\x1en7.G\xfc]\xc9\x14\xe1B@\xbb!8`'
    DATA_CRLF = 'BZh91AY&SY\xaez\xbbN\x00\x01H\xdf\x80\x00\x12@\x02\xff\xf0\x01\x07n\x00?\xe7\xff\xe0@\x01\xbc\xc6`\x86*\x8d=M\xa9\x9a\x86\xd0L@\x0fI\xa6!\xa1\x13\xc8\x88jdi\x8d@\x03@\x1a\x1a\x0c\x0c\x83 \x00\xc4h2\x19\x01\x82D\x84e\t\xe8\x99\x89\x19\x1ah\x00\r\x1a\x11\xaf\x9b\x0fG\xf5(\x1b\x1f?\t\x12\xcf\xb5\xfc\x95E\x00ps\x89\x12^\xa4\xdd\xa2&\x05(\x87\x04\x98\x89u\xe40%\xb6\x19\'\x8c\xc4\x89\xca\x07\x0e\x1b!\x91UIFU%C\x994!DI\xd2\xfa\xf0\xf1N8W\xde\x13A\xf5\x9cr%?\x9f3;I45A\xd1\x8bT\xb1<l\xba\xcb_\xc00xY\x17r\x17\x88\x08\x08@\xa0\ry@\x10\x04$)`\xf2\xce\x89z\xb0s\xec\x9b.iW\x9d\x81\xb5-+t\x9f\x1a\'\x97dB\xf5x\xb5\xbe.[.\xd7\x0e\x81\xe7\x08\x1cN`\x88\x10\xca\x87\xc3!"\x80\x92R\xa1/\xd1\xc0\xe6mf\xac\xbd\x99\xcca\xb3\x8780>\xa4\xc7\x8d\x1a\\"\xad\xa1\xabyBg\x15\xb9l\x88\x88\x91k"\x94\xa4\xd4\x89\xae*\xa6\x0b\x10\x0c\xd6\xd4m\xe86\xec\xb5j\x8a\x86j\';\xca.\x01I\xf2\xaaJ\xe8\x88\x8cU+t3\xfb\x0c\n\xa33\x13r2\r\x16\xe0\xb3(\xbf\x1d\x83r\xe7M\xf0D\x1365\xd8\x88\xd3\xa4\x92\xcb2\x06\x04\\\xc1\xb0\xea//\xbek&\xd8\xe6+t\xe5\xa1\x13\xada\x16\xder5"w]\xa2i\xb7[\x97R \xe2IT\xcd;Z\x04dk4\xad\x8a\t\xd3\x81z\x10\xf1:^`\xab\x1f\xc5\xdc\x91N\x14$+\x9e\xae\xd3\x80'
    if has_cmdline_bunzip2:

        def decompress(self, data):
            pop = subprocess.Popen('bunzip2', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            pop.stdin.write(data)
            pop.stdin.close()
            ret = pop.stdout.read()
            pop.stdout.close()
            if pop.wait() != 0:
                ret = bz2.decompress(data)
            return ret

    else:

        def decompress(self, data):
            return bz2.decompress(data)


class BZ2FileTest(BaseTest):
    """Test BZ2File type miscellaneous methods."""

    def setUp(self):
        self.filename = TESTFN

    def tearDown(self):
        if os.path.isfile(self.filename):
            os.unlink(self.filename)

    def createTempFile(self, crlf = 0):
        with open(self.filename, 'wb') as f:
            if crlf:
                data = self.DATA_CRLF
            else:
                data = self.DATA
            f.write(data)

    def testRead(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertRaises(TypeError, bz2f.read, None)
            self.assertEqual(bz2f.read(), self.TEXT)
        return

    def testRead0(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertRaises(TypeError, bz2f.read, None)
            self.assertEqual(bz2f.read(0), '')
        return

    def testReadChunk10--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'createTempFile'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_GLOBAL       'BZ2File'
13	LOAD_FAST         'self'
16	LOAD_ATTR         'filename'
19	CALL_FUNCTION_1   None
22	SETUP_WITH        '99'
25	STORE_FAST        'bz2f'

28	LOAD_CONST        ''
31	STORE_FAST        'text'

34	SETUP_LOOP        '76'

37	LOAD_FAST         'bz2f'
40	LOAD_ATTR         'read'
43	LOAD_CONST        10
46	CALL_FUNCTION_1   None
49	STORE_FAST        'str'

52	LOAD_FAST         'str'
55	POP_JUMP_IF_TRUE  '62'

58	BREAK_LOOP        None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'text'
65	LOAD_FAST         'str'
68	INPLACE_ADD       None
69	STORE_FAST        'text'
72	JUMP_BACK         '37'
75	POP_BLOCK         None
76_0	COME_FROM         '34'

76	LOAD_FAST         'self'
79	LOAD_ATTR         'assertEqual'
82	LOAD_FAST         'text'
85	LOAD_FAST         'self'
88	LOAD_ATTR         'TEXT'
91	CALL_FUNCTION_2   None
94	POP_TOP           None
95	POP_BLOCK         None
96	LOAD_CONST        None
99_0	COME_FROM         '22'
99	WITH_CLEANUP      None
100	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 75

    def testRead100(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertEqual(bz2f.read(100), self.TEXT[:100])

    def testReadLine(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertRaises(TypeError, bz2f.readline, None)
            sio = StringIO(self.TEXT)
            for line in sio.readlines():
                self.assertEqual(bz2f.readline(), line)

        return

    def testReadLines(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertRaises(TypeError, bz2f.readlines, None)
            sio = StringIO(self.TEXT)
            self.assertEqual(bz2f.readlines(), sio.readlines())
        return

    def testIterator(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            sio = StringIO(self.TEXT)
            self.assertEqual(list(iter(bz2f)), sio.readlines())

    def testClosedIteratorDeadlock(self):
        self.createTempFile()
        bz2f = BZ2File(self.filename)
        bz2f.close()
        self.assertRaises(ValueError, bz2f.next)
        self.assertRaises(ValueError, bz2f.readlines)

    def testXReadLines(self):
        self.createTempFile()
        bz2f = BZ2File(self.filename)
        sio = StringIO(self.TEXT)
        self.assertEqual(list(bz2f.xreadlines()), sio.readlines())
        bz2f.close()

    def testUniversalNewlinesLF(self):
        self.createTempFile()
        bz2f = BZ2File(self.filename, 'rU')
        self.assertEqual(bz2f.read(), self.TEXT)
        self.assertEqual(bz2f.newlines, '\n')
        bz2f.close()

    def testUniversalNewlinesCRLF(self):
        self.createTempFile(crlf=1)
        bz2f = BZ2File(self.filename, 'rU')
        self.assertEqual(bz2f.read(), self.TEXT)
        self.assertEqual(bz2f.newlines, '\r\n')
        bz2f.close()

    def testWrite(self):
        with BZ2File(self.filename, 'w') as bz2f:
            self.assertRaises(TypeError, bz2f.write)
            bz2f.write(self.TEXT)
        with open(self.filename, 'rb') as f:
            self.assertEqual(self.decompress(f.read()), self.TEXT)

    def testWriteChunks10--- This code section failed: ---

0	LOAD_GLOBAL       'BZ2File'
3	LOAD_FAST         'self'
6	LOAD_ATTR         'filename'
9	LOAD_CONST        'w'
12	CALL_FUNCTION_2   None
15	SETUP_WITH        '99'
18	STORE_FAST        'bz2f'

21	LOAD_CONST        0
24	STORE_FAST        'n'

27	SETUP_LOOP        '95'

30	LOAD_FAST         'self'
33	LOAD_ATTR         'TEXT'
36	LOAD_FAST         'n'
39	LOAD_CONST        10
42	BINARY_MULTIPLY   None
43	LOAD_FAST         'n'
46	LOAD_CONST        1
49	BINARY_ADD        None
50	LOAD_CONST        10
53	BINARY_MULTIPLY   None
54	SLICE+3           None
55	STORE_FAST        'str'

58	LOAD_FAST         'str'
61	POP_JUMP_IF_TRUE  '68'

64	BREAK_LOOP        None
65	JUMP_FORWARD      '68'
68_0	COME_FROM         '65'

68	LOAD_FAST         'bz2f'
71	LOAD_ATTR         'write'
74	LOAD_FAST         'str'
77	CALL_FUNCTION_1   None
80	POP_TOP           None

81	LOAD_FAST         'n'
84	LOAD_CONST        1
87	INPLACE_ADD       None
88	STORE_FAST        'n'
91	JUMP_BACK         '30'
94	POP_BLOCK         None
95_0	COME_FROM         '27'
95	POP_BLOCK         None
96	LOAD_CONST        None
99_0	COME_FROM         '15'
99	WITH_CLEANUP      None
100	END_FINALLY       None

101	LOAD_GLOBAL       'open'
104	LOAD_FAST         'self'
107	LOAD_ATTR         'filename'
110	LOAD_CONST        'rb'
113	CALL_FUNCTION_2   None
116	SETUP_WITH        '160'
119	STORE_FAST        'f'

122	LOAD_FAST         'self'
125	LOAD_ATTR         'assertEqual'
128	LOAD_FAST         'self'
131	LOAD_ATTR         'decompress'
134	LOAD_FAST         'f'
137	LOAD_ATTR         'read'
140	CALL_FUNCTION_0   None
143	CALL_FUNCTION_1   None
146	LOAD_FAST         'self'
149	LOAD_ATTR         'TEXT'
152	CALL_FUNCTION_2   None
155	POP_TOP           None
156	POP_BLOCK         None
157	LOAD_CONST        None
160_0	COME_FROM         '116'
160	WITH_CLEANUP      None
161	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 94

    def testWriteLines(self):
        with BZ2File(self.filename, 'w') as bz2f:
            self.assertRaises(TypeError, bz2f.writelines)
            sio = StringIO(self.TEXT)
            bz2f.writelines(sio.readlines())
        self.assertRaises(ValueError, bz2f.writelines, ['a'])
        with open(self.filename, 'rb') as f:
            self.assertEqual(self.decompress(f.read()), self.TEXT)

    def testWriteMethodsOnReadOnlyFile(self):
        with BZ2File(self.filename, 'w') as bz2f:
            bz2f.write('abc')
        with BZ2File(self.filename, 'r') as bz2f:
            self.assertRaises(IOError, bz2f.write, 'a')
            self.assertRaises(IOError, bz2f.writelines, ['a'])

    def testSeekForward(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            self.assertRaises(TypeError, bz2f.seek)
            bz2f.seek(150)
            self.assertEqual(bz2f.read(), self.TEXT[150:])

    def testSeekBackwards(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            bz2f.read(500)
            bz2f.seek(-150, 1)
            self.assertEqual(bz2f.read(), self.TEXT[350:])

    def testSeekBackwardsFromEnd(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            bz2f.seek(-150, 2)
            self.assertEqual(bz2f.read(), self.TEXT[len(self.TEXT) - 150:])

    def testSeekPostEnd(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            bz2f.seek(150000)
            self.assertEqual(bz2f.tell(), len(self.TEXT))
            self.assertEqual(bz2f.read(), '')

    def testSeekPostEndTwice(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            bz2f.seek(150000)
            bz2f.seek(150000)
            self.assertEqual(bz2f.tell(), len(self.TEXT))
            self.assertEqual(bz2f.read(), '')

    def testSeekPreStart(self):
        self.createTempFile()
        with BZ2File(self.filename) as bz2f:
            bz2f.seek(-150)
            self.assertEqual(bz2f.tell(), 0)
            self.assertEqual(bz2f.read(), self.TEXT)

    def testOpenDel(self):
        self.createTempFile()
        for i in xrange(10000):
            o = BZ2File(self.filename)
            del o

    def testOpenNonexistent(self):
        self.assertRaises(IOError, BZ2File, '/non/existent')

    def testModeU(self):
        self.createTempFile()
        bz2f = BZ2File(self.filename, 'U')
        bz2f.close()
        f = file(self.filename)
        f.seek(0, 2)
        self.assertEqual(f.tell(), len(self.DATA))
        f.close()

    def testBug1191043(self):
        data = 'BZh91AY&SY\xd9b\x89]\x00\x00\x00\x03\x80\x04\x00\x02\x00\x0c\x00 \x00!\x9ah3M\x13<]\xc9\x14\xe1BCe\x8a%t'
        with open(self.filename, 'wb') as f:
            f.write(data)
        with BZ2File(self.filename) as bz2f:
            lines = bz2f.readlines()
        self.assertEqual(lines, ['Test'])
        with BZ2File(self.filename) as bz2f:
            xlines = list(bz2f.readlines())
        self.assertEqual(xlines, ['Test'])

    def testContextProtocol(self):
        f = None
        with BZ2File(self.filename, 'wb') as f:
            f.write('xxx')
        f = BZ2File(self.filename, 'rb')
        f.close()
        try:
            with f:
                pass
        except ValueError:
            pass
        else:
            self.fail("__enter__ on a closed file didn't raise an exception")

        try:
            with BZ2File(self.filename, 'wb') as f:
                1 // 0
        except ZeroDivisionError:
            pass
        else:
            self.fail("1 // 0 didn't raise an exception")

        return

    @unittest.skipUnless(threading, 'Threading required for this test.')
    def testThreading(self):
        data = '1' * 1048576
        nthreads = 10
        with bz2.BZ2File(self.filename, 'wb') as f:

            def comp():
                for i in range(5):
                    f.write(data)

            threads = [ threading.Thread(target=comp) for i in range(nthreads) ]
            for t in threads:
                t.start()

            for t in threads:
                t.join()

    def testMixedIterationReads(self):
        with bz2.BZ2File(self.filename, 'wb') as f:
            f.write(self.TEXT * 100)
        with bz2.BZ2File(self.filename, 'rb') as f:
            next(f)
            self.assertRaises(ValueError, f.read)
            self.assertRaises(ValueError, f.readline)
            self.assertRaises(ValueError, f.readlines)


class BZ2CompressorTest(BaseTest):

    def testCompress(self):
        bz2c = BZ2Compressor()
        self.assertRaises(TypeError, bz2c.compress)
        data = bz2c.compress(self.TEXT)
        data += bz2c.flush()
        self.assertEqual(self.decompress(data), self.TEXT)

    def testCompressChunks10--- This code section failed: ---

0	LOAD_GLOBAL       'BZ2Compressor'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'bz2c'

9	LOAD_CONST        0
12	STORE_FAST        'n'

15	LOAD_CONST        ''
18	STORE_FAST        'data'

21	SETUP_LOOP        '95'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'TEXT'
30	LOAD_FAST         'n'
33	LOAD_CONST        10
36	BINARY_MULTIPLY   None
37	LOAD_FAST         'n'
40	LOAD_CONST        1
43	BINARY_ADD        None
44	LOAD_CONST        10
47	BINARY_MULTIPLY   None
48	SLICE+3           None
49	STORE_FAST        'str'

52	LOAD_FAST         'str'
55	POP_JUMP_IF_TRUE  '62'

58	BREAK_LOOP        None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'data'
65	LOAD_FAST         'bz2c'
68	LOAD_ATTR         'compress'
71	LOAD_FAST         'str'
74	CALL_FUNCTION_1   None
77	INPLACE_ADD       None
78	STORE_FAST        'data'

81	LOAD_FAST         'n'
84	LOAD_CONST        1
87	INPLACE_ADD       None
88	STORE_FAST        'n'
91	JUMP_BACK         '24'
94	POP_BLOCK         None
95_0	COME_FROM         '21'

95	LOAD_FAST         'data'
98	LOAD_FAST         'bz2c'
101	LOAD_ATTR         'flush'
104	CALL_FUNCTION_0   None
107	INPLACE_ADD       None
108	STORE_FAST        'data'

111	LOAD_FAST         'self'
114	LOAD_ATTR         'assertEqual'
117	LOAD_FAST         'self'
120	LOAD_ATTR         'decompress'
123	LOAD_FAST         'data'
126	CALL_FUNCTION_1   None
129	LOAD_FAST         'self'
132	LOAD_ATTR         'TEXT'
135	CALL_FUNCTION_2   None
138	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 94


class BZ2DecompressorTest(BaseTest):

    def test_Constructor(self):
        self.assertRaises(TypeError, BZ2Decompressor, 42)

    def testDecompress(self):
        bz2d = BZ2Decompressor()
        self.assertRaises(TypeError, bz2d.decompress)
        text = bz2d.decompress(self.DATA)
        self.assertEqual(text, self.TEXT)

    def testDecompressChunks10--- This code section failed: ---

0	LOAD_GLOBAL       'BZ2Decompressor'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'bz2d'

9	LOAD_CONST        ''
12	STORE_FAST        'text'

15	LOAD_CONST        0
18	STORE_FAST        'n'

21	SETUP_LOOP        '95'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'DATA'
30	LOAD_FAST         'n'
33	LOAD_CONST        10
36	BINARY_MULTIPLY   None
37	LOAD_FAST         'n'
40	LOAD_CONST        1
43	BINARY_ADD        None
44	LOAD_CONST        10
47	BINARY_MULTIPLY   None
48	SLICE+3           None
49	STORE_FAST        'str'

52	LOAD_FAST         'str'
55	POP_JUMP_IF_TRUE  '62'

58	BREAK_LOOP        None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'text'
65	LOAD_FAST         'bz2d'
68	LOAD_ATTR         'decompress'
71	LOAD_FAST         'str'
74	CALL_FUNCTION_1   None
77	INPLACE_ADD       None
78	STORE_FAST        'text'

81	LOAD_FAST         'n'
84	LOAD_CONST        1
87	INPLACE_ADD       None
88	STORE_FAST        'n'
91	JUMP_BACK         '24'
94	POP_BLOCK         None
95_0	COME_FROM         '21'

95	LOAD_FAST         'self'
98	LOAD_ATTR         'assertEqual'
101	LOAD_FAST         'text'
104	LOAD_FAST         'self'
107	LOAD_ATTR         'TEXT'
110	CALL_FUNCTION_2   None
113	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 94

    def testDecompressUnusedData(self):
        bz2d = BZ2Decompressor()
        unused_data = 'this is unused data'
        text = bz2d.decompress(self.DATA + unused_data)
        self.assertEqual(text, self.TEXT)
        self.assertEqual(bz2d.unused_data, unused_data)

    def testEOFError(self):
        bz2d = BZ2Decompressor()
        text = bz2d.decompress(self.DATA)
        self.assertRaises(EOFError, bz2d.decompress, 'anything')


class FuncTest(BaseTest):
    """Test module functions"""

    def testCompress(self):
        data = bz2.compress(self.TEXT)
        self.assertEqual(self.decompress(data), self.TEXT)

    def testDecompress(self):
        text = bz2.decompress(self.DATA)
        self.assertEqual(text, self.TEXT)

    def testDecompressEmpty(self):
        text = bz2.decompress('')
        self.assertEqual(text, '')

    def testDecompressIncomplete(self):
        self.assertRaises(ValueError, bz2.decompress, self.DATA[:-10])


def test_main():
    test_support.run_unittest(BZ2FileTest, BZ2CompressorTest, BZ2DecompressorTest, FuncTest)
    test_support.reap_children()


if __name__ == '__main__':
    test_main()