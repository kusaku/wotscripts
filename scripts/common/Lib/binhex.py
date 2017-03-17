# Embedded file name: scripts/common/Lib/binhex.py
"""Macintosh binhex compression/decompression.

easy interface:
binhex(inputfilename, outputfilename)
hexbin(inputfilename, outputfilename)
"""
import sys
import os
import struct
import binascii
__all__ = ['binhex', 'hexbin', 'Error']

class Error(Exception):
    pass


_DID_HEADER, _DID_DATA, _DID_RSRC = range(3)
REASONABLY_LARGE = 32768
LINELEN = 64
RUNCHAR = chr(144)
try:
    from Carbon.File import FSSpec, FInfo
    from MacOS import openrf

    def getfileinfo(name):
        finfo = FSSpec(name).FSpGetFInfo()
        dir, file = os.path.split(name)
        fp = open(name, 'rb')
        fp.seek(0, 2)
        dlen = fp.tell()
        fp = openrf(name, '*rb')
        fp.seek(0, 2)
        rlen = fp.tell()
        return (file,
         finfo,
         dlen,
         rlen)


    def openrsrc(name, *mode):
        if not mode:
            mode = '*rb'
        else:
            mode = '*' + mode[0]
        return openrf(name, mode)


except ImportError:

    class FInfo:

        def __init__(self):
            self.Type = '????'
            self.Creator = '????'
            self.Flags = 0


    def getfileinfo(name):
        finfo = FInfo()
        fp = open(name)
        data = open(name).read(256)
        for c in data:
            if not c.isspace() and (c < ' ' or ord(c) > 127):
                break
        else:
            finfo.Type = 'TEXT'

        fp.seek(0, 2)
        dsize = fp.tell()
        fp.close()
        dir, file = os.path.split(name)
        file = file.replace(':', '-', 1)
        return (file,
         finfo,
         dsize,
         0)


    class openrsrc:

        def __init__(self, *args):
            pass

        def read(self, *args):
            return ''

        def write(self, *args):
            pass

        def close(self):
            pass


class _Hqxcoderengine:
    """Write data to the coder in 3-byte chunks"""

    def __init__(self, ofp):
        self.ofp = ofp
        self.data = ''
        self.hqxdata = ''
        self.linelen = LINELEN - 1

    def write(self, data):
        self.data = self.data + data
        datalen = len(self.data)
        todo = datalen // 3 * 3
        data = self.data[:todo]
        self.data = self.data[todo:]
        if not data:
            return
        self.hqxdata = self.hqxdata + binascii.b2a_hqx(data)
        self._flush(0)

    def _flush(self, force):
        first = 0
        while first <= len(self.hqxdata) - self.linelen:
            last = first + self.linelen
            self.ofp.write(self.hqxdata[first:last] + '\n')
            self.linelen = LINELEN
            first = last

        self.hqxdata = self.hqxdata[first:]
        if force:
            self.ofp.write(self.hqxdata + ':\n')

    def close(self):
        if self.data:
            self.hqxdata = self.hqxdata + binascii.b2a_hqx(self.data)
        self._flush(1)
        self.ofp.close()
        del self.ofp


class _Rlecoderengine:
    """Write data to the RLE-coder in suitably large chunks"""

    def __init__(self, ofp):
        self.ofp = ofp
        self.data = ''

    def write(self, data):
        self.data = self.data + data
        if len(self.data) < REASONABLY_LARGE:
            return
        rledata = binascii.rlecode_hqx(self.data)
        self.ofp.write(rledata)
        self.data = ''

    def close(self):
        if self.data:
            rledata = binascii.rlecode_hqx(self.data)
            self.ofp.write(rledata)
        self.ofp.close()
        del self.ofp


class BinHex:

    def __init__(self, name_finfo_dlen_rlen, ofp):
        name, finfo, dlen, rlen = name_finfo_dlen_rlen
        if type(ofp) == type(''):
            ofname = ofp
            ofp = open(ofname, 'w')
        ofp.write('(This file must be converted with BinHex 4.0)\n\n:')
        hqxer = _Hqxcoderengine(ofp)
        self.ofp = _Rlecoderengine(hqxer)
        self.crc = 0
        if finfo is None:
            finfo = FInfo()
        self.dlen = dlen
        self.rlen = rlen
        self._writeinfo(name, finfo)
        self.state = _DID_HEADER
        return

    def _writeinfo(self, name, finfo):
        nl = len(name)
        if nl > 63:
            raise Error, 'Filename too long'
        d = chr(nl) + name + '\x00'
        d2 = finfo.Type + finfo.Creator
        d3 = struct.pack('>h', finfo.Flags)
        d4 = struct.pack('>ii', self.dlen, self.rlen)
        info = d + d2 + d3 + d4
        self._write(info)
        self._writecrc()

    def _write(self, data):
        self.crc = binascii.crc_hqx(data, self.crc)
        self.ofp.write(data)

    def _writecrc(self):
        if self.crc < 0:
            fmt = '>h'
        else:
            fmt = '>H'
        self.ofp.write(struct.pack(fmt, self.crc))
        self.crc = 0

    def write(self, data):
        if self.state != _DID_HEADER:
            raise Error, 'Writing data at the wrong time'
        self.dlen = self.dlen - len(data)
        self._write(data)

    def close_data(self):
        if self.dlen != 0:
            raise Error, 'Incorrect data size, diff=%r' % (self.rlen,)
        self._writecrc()
        self.state = _DID_DATA

    def write_rsrc(self, data):
        if self.state < _DID_DATA:
            self.close_data()
        if self.state != _DID_DATA:
            raise Error, 'Writing resource data at the wrong time'
        self.rlen = self.rlen - len(data)
        self._write(data)

    def close(self):
        if self.state < _DID_DATA:
            self.close_data()
        if self.state != _DID_DATA:
            raise Error, 'Close at the wrong time'
        if self.rlen != 0:
            raise Error, 'Incorrect resource-datasize, diff=%r' % (self.rlen,)
        self._writecrc()
        self.ofp.close()
        self.state = None
        del self.ofp
        return


def binhex--- This code section failed: ---

0	LOAD_GLOBAL       'getfileinfo'
3	LOAD_FAST         'inp'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'finfo'

12	LOAD_GLOBAL       'BinHex'
15	LOAD_FAST         'finfo'
18	LOAD_FAST         'out'
21	CALL_FUNCTION_2   None
24	STORE_FAST        'ofp'

27	LOAD_GLOBAL       'open'
30	LOAD_FAST         'inp'
33	LOAD_CONST        'rb'
36	CALL_FUNCTION_2   None
39	STORE_FAST        'ifp'

42	SETUP_LOOP        '87'

45	LOAD_FAST         'ifp'
48	LOAD_ATTR         'read'
51	LOAD_CONST        128000
54	CALL_FUNCTION_1   None
57	STORE_FAST        'd'

60	LOAD_FAST         'd'
63	POP_JUMP_IF_TRUE  '70'
66	BREAK_LOOP        None
67	JUMP_FORWARD      '70'
70_0	COME_FROM         '67'

70	LOAD_FAST         'ofp'
73	LOAD_ATTR         'write'
76	LOAD_FAST         'd'
79	CALL_FUNCTION_1   None
82	POP_TOP           None
83	JUMP_BACK         '45'
86	POP_BLOCK         None
87_0	COME_FROM         '42'

87	LOAD_FAST         'ofp'
90	LOAD_ATTR         'close_data'
93	CALL_FUNCTION_0   None
96	POP_TOP           None

97	LOAD_FAST         'ifp'
100	LOAD_ATTR         'close'
103	CALL_FUNCTION_0   None
106	POP_TOP           None

107	LOAD_GLOBAL       'openrsrc'
110	LOAD_FAST         'inp'
113	LOAD_CONST        'rb'
116	CALL_FUNCTION_2   None
119	STORE_FAST        'ifp'

122	SETUP_LOOP        '167'

125	LOAD_FAST         'ifp'
128	LOAD_ATTR         'read'
131	LOAD_CONST        128000
134	CALL_FUNCTION_1   None
137	STORE_FAST        'd'

140	LOAD_FAST         'd'
143	POP_JUMP_IF_TRUE  '150'
146	BREAK_LOOP        None
147	JUMP_FORWARD      '150'
150_0	COME_FROM         '147'

150	LOAD_FAST         'ofp'
153	LOAD_ATTR         'write_rsrc'
156	LOAD_FAST         'd'
159	CALL_FUNCTION_1   None
162	POP_TOP           None
163	JUMP_BACK         '125'
166	POP_BLOCK         None
167_0	COME_FROM         '122'

167	LOAD_FAST         'ofp'
170	LOAD_ATTR         'close'
173	CALL_FUNCTION_0   None
176	POP_TOP           None

177	LOAD_FAST         'ifp'
180	LOAD_ATTR         'close'
183	CALL_FUNCTION_0   None
186	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 86


class _Hqxdecoderengine:
    """Read data via the decoder in 4-byte chunks"""

    def __init__(self, ifp):
        self.ifp = ifp
        self.eof = 0

    def read--- This code section failed: ---

0	LOAD_CONST        ''
3	STORE_FAST        'decdata'

6	LOAD_FAST         'totalwtd'
9	STORE_FAST        'wtd'

12	SETUP_LOOP        '240'
15	LOAD_FAST         'wtd'
18	LOAD_CONST        0
21	COMPARE_OP        '>'
24	POP_JUMP_IF_FALSE '239'

27	LOAD_FAST         'self'
30	LOAD_ATTR         'eof'
33	POP_JUMP_IF_FALSE '40'
36	LOAD_FAST         'decdata'
39	RETURN_END_IF     None

40	LOAD_FAST         'wtd'
43	LOAD_CONST        2
46	BINARY_ADD        None
47	LOAD_CONST        3
50	BINARY_FLOOR_DIVIDE None
51	LOAD_CONST        4
54	BINARY_MULTIPLY   None
55	STORE_FAST        'wtd'

58	LOAD_FAST         'self'
61	LOAD_ATTR         'ifp'
64	LOAD_ATTR         'read'
67	LOAD_FAST         'wtd'
70	CALL_FUNCTION_1   None
73	STORE_FAST        'data'

76	SETUP_LOOP        '181'

79	SETUP_EXCEPT      '111'

82	LOAD_GLOBAL       'binascii'
85	LOAD_ATTR         'a2b_hqx'
88	LOAD_FAST         'data'
91	CALL_FUNCTION_1   None
94	UNPACK_SEQUENCE_2 None
97	STORE_FAST        'decdatacur'
100	LOAD_FAST         'self'
103	STORE_ATTR        'eof'

106	BREAK_LOOP        None
107	POP_BLOCK         None
108	JUMP_FORWARD      '131'
111_0	COME_FROM         '79'

111	DUP_TOP           None
112	LOAD_GLOBAL       'binascii'
115	LOAD_ATTR         'Incomplete'
118	COMPARE_OP        'exception match'
121	POP_JUMP_IF_FALSE '130'
124	POP_TOP           None
125	POP_TOP           None
126	POP_TOP           None

127	JUMP_FORWARD      '131'
130	END_FINALLY       None
131_0	COME_FROM         '108'
131_1	COME_FROM         '130'

131	LOAD_FAST         'self'
134	LOAD_ATTR         'ifp'
137	LOAD_ATTR         'read'
140	LOAD_CONST        1
143	CALL_FUNCTION_1   None
146	STORE_FAST        'newdata'

149	LOAD_FAST         'newdata'
152	POP_JUMP_IF_TRUE  '167'

155	LOAD_GLOBAL       'Error'

158	LOAD_CONST        'Premature EOF on binhex file'
161	RAISE_VARARGS_2   None
164	JUMP_FORWARD      '167'
167_0	COME_FROM         '164'

167	LOAD_FAST         'data'
170	LOAD_FAST         'newdata'
173	BINARY_ADD        None
174	STORE_FAST        'data'
177	JUMP_BACK         '79'
180	POP_BLOCK         None
181_0	COME_FROM         '76'

181	LOAD_FAST         'decdata'
184	LOAD_FAST         'decdatacur'
187	BINARY_ADD        None
188	STORE_FAST        'decdata'

191	LOAD_FAST         'totalwtd'
194	LOAD_GLOBAL       'len'
197	LOAD_FAST         'decdata'
200	CALL_FUNCTION_1   None
203	BINARY_SUBTRACT   None
204	STORE_FAST        'wtd'

207	LOAD_FAST         'decdata'
210	UNARY_NOT         None
211	POP_JUMP_IF_FALSE '15'
214	LOAD_FAST         'self'
217	LOAD_ATTR         'eof'
220	UNARY_NOT         None
221_0	COME_FROM         '211'
221	POP_JUMP_IF_FALSE '15'

224	LOAD_GLOBAL       'Error'
227	LOAD_CONST        'Premature EOF on binhex file'
230	RAISE_VARARGS_2   None
233	JUMP_BACK         '15'
236	JUMP_BACK         '15'
239	POP_BLOCK         None
240_0	COME_FROM         '12'

240	LOAD_FAST         'decdata'
243	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 180

    def close(self):
        self.ifp.close()


class _Rledecoderengine:
    """Read data via the RLE-coder"""

    def __init__(self, ifp):
        self.ifp = ifp
        self.pre_buffer = ''
        self.post_buffer = ''
        self.eof = 0

    def read(self, wtd):
        if wtd > len(self.post_buffer):
            self._fill(wtd - len(self.post_buffer))
        rv = self.post_buffer[:wtd]
        self.post_buffer = self.post_buffer[wtd:]
        return rv

    def _fill(self, wtd):
        self.pre_buffer = self.pre_buffer + self.ifp.read(wtd + 4)
        if self.ifp.eof:
            self.post_buffer = self.post_buffer + binascii.rledecode_hqx(self.pre_buffer)
            self.pre_buffer = ''
            return
        mark = len(self.pre_buffer)
        if self.pre_buffer[-3:] == RUNCHAR + '\x00' + RUNCHAR:
            mark = mark - 3
        elif self.pre_buffer[-1] == RUNCHAR:
            mark = mark - 2
        elif self.pre_buffer[-2:] == RUNCHAR + '\x00':
            mark = mark - 2
        elif self.pre_buffer[-2] == RUNCHAR:
            pass
        else:
            mark = mark - 1
        self.post_buffer = self.post_buffer + binascii.rledecode_hqx(self.pre_buffer[:mark])
        self.pre_buffer = self.pre_buffer[mark:]

    def close(self):
        self.ifp.close()


class HexBin:

    def __init__--- This code section failed: ---

0	LOAD_GLOBAL       'type'
3	LOAD_FAST         'ifp'
6	CALL_FUNCTION_1   None
9	LOAD_GLOBAL       'type'
12	LOAD_CONST        ''
15	CALL_FUNCTION_1   None
18	COMPARE_OP        '=='
21	POP_JUMP_IF_FALSE '39'

24	LOAD_GLOBAL       'open'
27	LOAD_FAST         'ifp'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'ifp'
36	JUMP_FORWARD      '39'
39_0	COME_FROM         '36'

39	SETUP_LOOP        '140'

42	LOAD_FAST         'ifp'
45	LOAD_ATTR         'read'
48	LOAD_CONST        1
51	CALL_FUNCTION_1   None
54	STORE_FAST        'ch'

57	LOAD_FAST         'ch'
60	POP_JUMP_IF_TRUE  '75'

63	LOAD_GLOBAL       'Error'
66	LOAD_CONST        'No binhex data found'
69	RAISE_VARARGS_2   None
72	JUMP_FORWARD      '75'
75_0	COME_FROM         '72'

75	LOAD_FAST         'ch'
78	LOAD_CONST        '\r'
81	COMPARE_OP        '=='
84	POP_JUMP_IF_FALSE '93'

87	CONTINUE          '42'
90	JUMP_FORWARD      '93'
93_0	COME_FROM         '90'

93	LOAD_FAST         'ch'
96	LOAD_CONST        ':'
99	COMPARE_OP        '=='
102	POP_JUMP_IF_FALSE '109'

105	BREAK_LOOP        None
106	JUMP_FORWARD      '109'
109_0	COME_FROM         '106'

109	LOAD_FAST         'ch'
112	LOAD_CONST        '\n'
115	COMPARE_OP        '!='
118	POP_JUMP_IF_FALSE '42'

121	LOAD_FAST         'ifp'
124	LOAD_ATTR         'readline'
127	CALL_FUNCTION_0   None
130	STORE_FAST        'dummy'
133	JUMP_BACK         '42'
136	JUMP_BACK         '42'
139	POP_BLOCK         None
140_0	COME_FROM         '39'

140	LOAD_GLOBAL       '_Hqxdecoderengine'
143	LOAD_FAST         'ifp'
146	CALL_FUNCTION_1   None
149	STORE_FAST        'hqxifp'

152	LOAD_GLOBAL       '_Rledecoderengine'
155	LOAD_FAST         'hqxifp'
158	CALL_FUNCTION_1   None
161	LOAD_FAST         'self'
164	STORE_ATTR        'ifp'

167	LOAD_CONST        0
170	LOAD_FAST         'self'
173	STORE_ATTR        'crc'

176	LOAD_FAST         'self'
179	LOAD_ATTR         '_readheader'
182	CALL_FUNCTION_0   None
185	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 139

    def _read(self, len):
        data = self.ifp.read(len)
        self.crc = binascii.crc_hqx(data, self.crc)
        return data

    def _checkcrc(self):
        filecrc = struct.unpack('>h', self.ifp.read(2))[0] & 65535
        self.crc = self.crc & 65535
        if filecrc != self.crc:
            raise Error, 'CRC error, computed %x, read %x' % (self.crc, filecrc)
        self.crc = 0

    def _readheader(self):
        len = self._read(1)
        fname = self._read(ord(len))
        rest = self._read(19)
        self._checkcrc()
        type = rest[1:5]
        creator = rest[5:9]
        flags = struct.unpack('>h', rest[9:11])[0]
        self.dlen = struct.unpack('>l', rest[11:15])[0]
        self.rlen = struct.unpack('>l', rest[15:19])[0]
        self.FName = fname
        self.FInfo = FInfo()
        self.FInfo.Creator = creator
        self.FInfo.Type = type
        self.FInfo.Flags = flags
        self.state = _DID_HEADER

    def read(self, *n):
        if self.state != _DID_HEADER:
            raise Error, 'Read data at wrong time'
        if n:
            n = n[0]
            n = min(n, self.dlen)
        else:
            n = self.dlen
        rv = ''
        while len(rv) < n:
            rv = rv + self._read(n - len(rv))

        self.dlen = self.dlen - n
        return rv

    def close_data(self):
        if self.state != _DID_HEADER:
            raise Error, 'close_data at wrong time'
        if self.dlen:
            dummy = self._read(self.dlen)
        self._checkcrc()
        self.state = _DID_DATA

    def read_rsrc(self, *n):
        if self.state == _DID_HEADER:
            self.close_data()
        if self.state != _DID_DATA:
            raise Error, 'Read resource data at wrong time'
        if n:
            n = n[0]
            n = min(n, self.rlen)
        else:
            n = self.rlen
        self.rlen = self.rlen - n
        return self._read(n)

    def close(self):
        if self.rlen:
            dummy = self.read_rsrc(self.rlen)
        self._checkcrc()
        self.state = _DID_RSRC
        self.ifp.close()


def hexbin--- This code section failed: ---

0	LOAD_GLOBAL       'HexBin'
3	LOAD_FAST         'inp'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'ifp'

12	LOAD_FAST         'ifp'
15	LOAD_ATTR         'FInfo'
18	STORE_FAST        'finfo'

21	LOAD_FAST         'out'
24	POP_JUMP_IF_TRUE  '39'

27	LOAD_FAST         'ifp'
30	LOAD_ATTR         'FName'
33	STORE_FAST        'out'
36	JUMP_FORWARD      '39'
39_0	COME_FROM         '36'

39	LOAD_GLOBAL       'open'
42	LOAD_FAST         'out'
45	LOAD_CONST        'wb'
48	CALL_FUNCTION_2   None
51	STORE_FAST        'ofp'

54	SETUP_LOOP        '99'

57	LOAD_FAST         'ifp'
60	LOAD_ATTR         'read'
63	LOAD_CONST        128000
66	CALL_FUNCTION_1   None
69	STORE_FAST        'd'

72	LOAD_FAST         'd'
75	POP_JUMP_IF_TRUE  '82'
78	BREAK_LOOP        None
79	JUMP_FORWARD      '82'
82_0	COME_FROM         '79'

82	LOAD_FAST         'ofp'
85	LOAD_ATTR         'write'
88	LOAD_FAST         'd'
91	CALL_FUNCTION_1   None
94	POP_TOP           None
95	JUMP_BACK         '57'
98	POP_BLOCK         None
99_0	COME_FROM         '54'

99	LOAD_FAST         'ofp'
102	LOAD_ATTR         'close'
105	CALL_FUNCTION_0   None
108	POP_TOP           None

109	LOAD_FAST         'ifp'
112	LOAD_ATTR         'close_data'
115	CALL_FUNCTION_0   None
118	POP_TOP           None

119	LOAD_FAST         'ifp'
122	LOAD_ATTR         'read_rsrc'
125	LOAD_CONST        128000
128	CALL_FUNCTION_1   None
131	STORE_FAST        'd'

134	LOAD_FAST         'd'
137	POP_JUMP_IF_FALSE '226'

140	LOAD_GLOBAL       'openrsrc'
143	LOAD_FAST         'out'
146	LOAD_CONST        'wb'
149	CALL_FUNCTION_2   None
152	STORE_FAST        'ofp'

155	LOAD_FAST         'ofp'
158	LOAD_ATTR         'write'
161	LOAD_FAST         'd'
164	CALL_FUNCTION_1   None
167	POP_TOP           None

168	SETUP_LOOP        '213'

171	LOAD_FAST         'ifp'
174	LOAD_ATTR         'read_rsrc'
177	LOAD_CONST        128000
180	CALL_FUNCTION_1   None
183	STORE_FAST        'd'

186	LOAD_FAST         'd'
189	POP_JUMP_IF_TRUE  '196'
192	BREAK_LOOP        None
193	JUMP_FORWARD      '196'
196_0	COME_FROM         '193'

196	LOAD_FAST         'ofp'
199	LOAD_ATTR         'write'
202	LOAD_FAST         'd'
205	CALL_FUNCTION_1   None
208	POP_TOP           None
209	JUMP_BACK         '171'
212	POP_BLOCK         None
213_0	COME_FROM         '168'

213	LOAD_FAST         'ofp'
216	LOAD_ATTR         'close'
219	CALL_FUNCTION_0   None
222	POP_TOP           None
223	JUMP_FORWARD      '226'
226_0	COME_FROM         '223'

226	LOAD_FAST         'ifp'
229	LOAD_ATTR         'close'
232	CALL_FUNCTION_0   None
235	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 98


def _test():
    fname = sys.argv[1]
    binhex(fname, fname + '.hqx')
    hexbin(fname + '.hqx', fname + '.viahqx')
    sys.exit(1)


if __name__ == '__main__':
    _test()