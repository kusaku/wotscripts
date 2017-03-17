# Embedded file name: scripts/common/Lib/test/test_gzip.py
"""Test script for the gzip module.
"""
import unittest
from test import test_support
import os
import io
import struct
gzip = test_support.import_module('gzip')
data1 = '  int length=DEFAULTALLOC, err = Z_OK;\n  PyObject *RetVal;\n  int flushmode = Z_FINISH;\n  unsigned long start_total_out;\n\n'
data2 = '/* zlibmodule.c -- gzip-compatible data compression */\n/* See http://www.gzip.org/zlib/\n/* See http://www.winimage.com/zLibDll for Windows */\n'

class TestGzip(unittest.TestCase):
    filename = test_support.TESTFN

    def setUp(self):
        test_support.unlink(self.filename)

    def tearDown(self):
        test_support.unlink(self.filename)

    def test_write(self):
        with gzip.GzipFile(self.filename, 'wb') as f:
            f.write(data1 * 50)
            f.flush()
            f.fileno()
            if hasattr(os, 'fsync'):
                os.fsync(f.fileno())
            f.close()
        f.close()

    def test_read(self):
        self.test_write()
        with gzip.GzipFile(self.filename, 'r') as f:
            d = f.read()
        self.assertEqual(d, data1 * 50)

    def test_io_on_closed_object(self):
        self.test_write()
        f = gzip.GzipFile(self.filename, 'r')
        f.close()
        with self.assertRaises(ValueError):
            f.read(1)
        with self.assertRaises(ValueError):
            f.seek(0)
        with self.assertRaises(ValueError):
            f.tell()
        f = gzip.GzipFile(self.filename, 'w')
        f.close()
        with self.assertRaises(ValueError):
            f.write('')
        with self.assertRaises(ValueError):
            f.flush()

    def test_append(self):
        self.test_write()
        with gzip.GzipFile(self.filename, 'ab') as f:
            f.write(data2 * 15)
        with gzip.GzipFile(self.filename, 'rb') as f:
            d = f.read()
        self.assertEqual(d, data1 * 50 + data2 * 15)

    def test_many_append--- This code section failed: ---

0	LOAD_GLOBAL       'gzip'
3	LOAD_ATTR         'open'
6	LOAD_FAST         'self'
9	LOAD_ATTR         'filename'
12	LOAD_CONST        'wb'
15	LOAD_CONST        9
18	CALL_FUNCTION_3   None
21	SETUP_WITH        '44'
24	STORE_FAST        'f'

27	LOAD_FAST         'f'
30	LOAD_ATTR         'write'
33	LOAD_CONST        'a'
36	CALL_FUNCTION_1   None
39	POP_TOP           None
40	POP_BLOCK         None
41	LOAD_CONST        None
44_0	COME_FROM         '21'
44	WITH_CLEANUP      None
45	END_FINALLY       None

46	SETUP_LOOP        '118'
49	LOAD_GLOBAL       'range'
52	LOAD_CONST        0
55	LOAD_CONST        200
58	CALL_FUNCTION_2   None
61	GET_ITER          None
62	FOR_ITER          '117'
65	STORE_FAST        'i'

68	LOAD_GLOBAL       'gzip'
71	LOAD_ATTR         'open'
74	LOAD_FAST         'self'
77	LOAD_ATTR         'filename'
80	LOAD_CONST        'ab'
83	LOAD_CONST        9
86	CALL_FUNCTION_3   None
89	SETUP_WITH        '112'
92	STORE_FAST        'f'

95	LOAD_FAST         'f'
98	LOAD_ATTR         'write'
101	LOAD_CONST        'a'
104	CALL_FUNCTION_1   None
107	POP_TOP           None
108	POP_BLOCK         None
109	LOAD_CONST        None
112_0	COME_FROM         '89'
112	WITH_CLEANUP      None
113	END_FINALLY       None
114	JUMP_BACK         '62'
117	POP_BLOCK         None
118_0	COME_FROM         '46'

118	LOAD_GLOBAL       'gzip'
121	LOAD_ATTR         'open'
124	LOAD_FAST         'self'
127	LOAD_ATTR         'filename'
130	LOAD_CONST        'rb'
133	CALL_FUNCTION_2   None
136	SETUP_WITH        '194'
139	STORE_FAST        'zgfile'

142	LOAD_CONST        ''
145	STORE_FAST        'contents'

148	SETUP_LOOP        '190'

151	LOAD_FAST         'zgfile'
154	LOAD_ATTR         'read'
157	LOAD_CONST        8192
160	CALL_FUNCTION_1   None
163	STORE_FAST        'ztxt'

166	LOAD_FAST         'contents'
169	LOAD_FAST         'ztxt'
172	INPLACE_ADD       None
173	STORE_FAST        'contents'

176	LOAD_FAST         'ztxt'
179	POP_JUMP_IF_TRUE  '151'
182	BREAK_LOOP        None
183	JUMP_BACK         '151'
186	JUMP_BACK         '151'
189	POP_BLOCK         None
190_0	COME_FROM         '148'
190	POP_BLOCK         None
191	LOAD_CONST        None
194_0	COME_FROM         '136'
194	WITH_CLEANUP      None
195	END_FINALLY       None

196	LOAD_FAST         'self'
199	LOAD_ATTR         'assertEqual'
202	LOAD_FAST         'contents'
205	LOAD_CONST        'a'
208	LOAD_CONST        201
211	BINARY_MULTIPLY   None
212	CALL_FUNCTION_2   None
215	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 189

    def test_buffered_reader(self):
        self.test_write()
        with gzip.GzipFile(self.filename, 'rb') as f:
            with io.BufferedReader(f) as r:
                lines = [ line for line in r ]
        self.assertEqual(lines, 50 * data1.splitlines(True))

    def test_readline--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'test_write'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_GLOBAL       'gzip'
13	LOAD_ATTR         'GzipFile'
16	LOAD_FAST         'self'
19	LOAD_ATTR         'filename'
22	LOAD_CONST        'rb'
25	CALL_FUNCTION_2   None
28	SETUP_WITH        '128'
31	STORE_FAST        'f'

34	LOAD_CONST        0
37	STORE_FAST        'line_length'

40	SETUP_LOOP        '124'

43	LOAD_FAST         'f'
46	LOAD_ATTR         'readline'
49	LOAD_FAST         'line_length'
52	CALL_FUNCTION_1   None
55	STORE_FAST        'L'

58	LOAD_FAST         'L'
61	UNARY_NOT         None
62	POP_JUMP_IF_FALSE '81'
65	LOAD_FAST         'line_length'
68	LOAD_CONST        0
71	COMPARE_OP        '!='
74_0	COME_FROM         '62'
74	POP_JUMP_IF_FALSE '81'
77	BREAK_LOOP        None
78	JUMP_FORWARD      '81'
81_0	COME_FROM         '78'

81	LOAD_FAST         'self'
84	LOAD_ATTR         'assertTrue'
87	LOAD_GLOBAL       'len'
90	LOAD_FAST         'L'
93	CALL_FUNCTION_1   None
96	LOAD_FAST         'line_length'
99	COMPARE_OP        '<='
102	CALL_FUNCTION_1   None
105	POP_TOP           None

106	LOAD_FAST         'line_length'
109	LOAD_CONST        1
112	BINARY_ADD        None
113	LOAD_CONST        50
116	BINARY_MODULO     None
117	STORE_FAST        'line_length'
120	JUMP_BACK         '43'
123	POP_BLOCK         None
124_0	COME_FROM         '40'
124	POP_BLOCK         None
125	LOAD_CONST        None
128_0	COME_FROM         '28'
128	WITH_CLEANUP      None
129	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 123

    def test_readlines--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'test_write'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_GLOBAL       'gzip'
13	LOAD_ATTR         'GzipFile'
16	LOAD_FAST         'self'
19	LOAD_ATTR         'filename'
22	LOAD_CONST        'rb'
25	CALL_FUNCTION_2   None
28	SETUP_WITH        '50'
31	STORE_FAST        'f'

34	LOAD_FAST         'f'
37	LOAD_ATTR         'readlines'
40	CALL_FUNCTION_0   None
43	STORE_FAST        'L'
46	POP_BLOCK         None
47	LOAD_CONST        None
50_0	COME_FROM         '28'
50	WITH_CLEANUP      None
51	END_FINALLY       None

52	LOAD_GLOBAL       'gzip'
55	LOAD_ATTR         'GzipFile'
58	LOAD_FAST         'self'
61	LOAD_ATTR         'filename'
64	LOAD_CONST        'rb'
67	CALL_FUNCTION_2   None
70	SETUP_WITH        '118'
73	STORE_FAST        'f'

76	SETUP_LOOP        '114'

79	LOAD_FAST         'f'
82	LOAD_ATTR         'readlines'
85	LOAD_CONST        150
88	CALL_FUNCTION_1   None
91	STORE_FAST        'L'

94	LOAD_FAST         'L'
97	BUILD_LIST_0      None
100	COMPARE_OP        '=='
103	POP_JUMP_IF_FALSE '79'
106	BREAK_LOOP        None
107	JUMP_BACK         '79'
110	JUMP_BACK         '79'
113	POP_BLOCK         None
114_0	COME_FROM         '76'
114	POP_BLOCK         None
115	LOAD_CONST        None
118_0	COME_FROM         '70'
118	WITH_CLEANUP      None
119	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 113

    def test_seek_read--- This code section failed: ---

0	LOAD_FAST         'self'
3	LOAD_ATTR         'test_write'
6	CALL_FUNCTION_0   None
9	POP_TOP           None

10	LOAD_GLOBAL       'gzip'
13	LOAD_ATTR         'GzipFile'
16	LOAD_FAST         'self'
19	LOAD_ATTR         'filename'
22	CALL_FUNCTION_1   None
25	SETUP_WITH        '188'
28	STORE_FAST        'f'

31	SETUP_LOOP        '184'

34	LOAD_FAST         'f'
37	LOAD_ATTR         'tell'
40	CALL_FUNCTION_0   None
43	STORE_FAST        'oldpos'

46	LOAD_FAST         'f'
49	LOAD_ATTR         'readline'
52	CALL_FUNCTION_0   None
55	STORE_FAST        'line1'

58	LOAD_FAST         'line1'
61	POP_JUMP_IF_TRUE  '68'
64	BREAK_LOOP        None
65	JUMP_FORWARD      '68'
68_0	COME_FROM         '65'

68	LOAD_FAST         'f'
71	LOAD_ATTR         'tell'
74	CALL_FUNCTION_0   None
77	STORE_FAST        'newpos'

80	LOAD_FAST         'f'
83	LOAD_ATTR         'seek'
86	LOAD_FAST         'oldpos'
89	CALL_FUNCTION_1   None
92	POP_TOP           None

93	LOAD_GLOBAL       'len'
96	LOAD_FAST         'line1'
99	CALL_FUNCTION_1   None
102	LOAD_CONST        10
105	COMPARE_OP        '>'
108	POP_JUMP_IF_FALSE '120'

111	LOAD_CONST        10
114	STORE_FAST        'amount'
117	JUMP_FORWARD      '132'

120	LOAD_GLOBAL       'len'
123	LOAD_FAST         'line1'
126	CALL_FUNCTION_1   None
129	STORE_FAST        'amount'
132_0	COME_FROM         '117'

132	LOAD_FAST         'f'
135	LOAD_ATTR         'read'
138	LOAD_FAST         'amount'
141	CALL_FUNCTION_1   None
144	STORE_FAST        'line2'

147	LOAD_FAST         'self'
150	LOAD_ATTR         'assertEqual'
153	LOAD_FAST         'line1'
156	LOAD_FAST         'amount'
159	SLICE+2           None
160	LOAD_FAST         'line2'
163	CALL_FUNCTION_2   None
166	POP_TOP           None

167	LOAD_FAST         'f'
170	LOAD_ATTR         'seek'
173	LOAD_FAST         'newpos'
176	CALL_FUNCTION_1   None
179	POP_TOP           None
180	JUMP_BACK         '34'
183	POP_BLOCK         None
184_0	COME_FROM         '31'
184	POP_BLOCK         None
185	LOAD_CONST        None
188_0	COME_FROM         '25'
188	WITH_CLEANUP      None
189	END_FINALLY       None

Syntax error at or near `POP_BLOCK' token at offset 183

    def test_seek_whence(self):
        self.test_write()
        with gzip.GzipFile(self.filename) as f:
            f.read(10)
            f.seek(10, whence=1)
            y = f.read(10)
        self.assertEqual(y, data1[20:30])

    def test_seek_write(self):
        with gzip.GzipFile(self.filename, 'w') as f:
            for pos in range(0, 256, 16):
                f.seek(pos)
                f.write('GZ\n')

    def test_mode(self):
        self.test_write()
        with gzip.GzipFile(self.filename, 'r') as f:
            self.assertEqual(f.myfileobj.mode, 'rb')

    def test_1647484(self):
        for mode in ('wb', 'rb'):
            with gzip.GzipFile(self.filename, mode) as f:
                self.assertTrue(hasattr(f, 'name'))
                self.assertEqual(f.name, self.filename)

    def test_mtime(self):
        mtime = 123456789
        with gzip.GzipFile(self.filename, 'w', mtime=mtime) as fWrite:
            fWrite.write(data1)
        with gzip.GzipFile(self.filename) as fRead:
            dataRead = fRead.read()
            self.assertEqual(dataRead, data1)
            self.assertTrue(hasattr(fRead, 'mtime'))
            self.assertEqual(fRead.mtime, mtime)

    def test_metadata(self):
        mtime = 123456789
        with gzip.GzipFile(self.filename, 'w', mtime=mtime) as fWrite:
            fWrite.write(data1)
        with open(self.filename, 'rb') as fRead:
            idBytes = fRead.read(2)
            self.assertEqual(idBytes, '\x1f\x8b')
            cmByte = fRead.read(1)
            self.assertEqual(cmByte, '\x08')
            flagsByte = fRead.read(1)
            self.assertEqual(flagsByte, '\x08')
            mtimeBytes = fRead.read(4)
            self.assertEqual(mtimeBytes, struct.pack('<i', mtime))
            xflByte = fRead.read(1)
            self.assertEqual(xflByte, '\x02')
            osByte = fRead.read(1)
            self.assertEqual(osByte, '\xff')
            expected = self.filename.encode('Latin-1') + '\x00'
            nameBytes = fRead.read(len(expected))
            self.assertEqual(nameBytes, expected)
            fRead.seek(os.stat(self.filename).st_size - 8)
            crc32Bytes = fRead.read(4)
            self.assertEqual(crc32Bytes, '\xaf\xd7d\x83')
            isizeBytes = fRead.read(4)
            self.assertEqual(isizeBytes, struct.pack('<i', len(data1)))

    def test_with_open(self):
        with gzip.GzipFile(self.filename, 'wb') as f:
            f.write('xxx')
        f = gzip.GzipFile(self.filename, 'rb')
        f.close()
        try:
            with f:
                pass
        except ValueError:
            pass
        else:
            self.fail("__enter__ on a closed file didn't raise an exception")

        try:
            with gzip.GzipFile(self.filename, 'wb') as f:
                1 // 0
        except ZeroDivisionError:
            pass
        else:
            self.fail("1 // 0 didn't raise an exception")

    def test_zero_padded_file(self):
        with gzip.GzipFile(self.filename, 'wb') as f:
            f.write(data1 * 50)
        with open(self.filename, 'ab') as f:
            f.write('\x00' * 50)
        with gzip.GzipFile(self.filename, 'rb') as f:
            d = f.read()
            self.assertEqual(d, data1 * 50, 'Incorrect data in file')

    def test_fileobj_from_fdopen(self):
        fd = os.open(self.filename, os.O_WRONLY | os.O_CREAT)
        with os.fdopen(fd, 'wb') as f:
            with gzip.GzipFile(fileobj=f, mode='w') as g:
                self.assertEqual(g.name, '')


def test_main(verbose = None):
    test_support.run_unittest(TestGzip)


if __name__ == '__main__':
    test_main(verbose=True)