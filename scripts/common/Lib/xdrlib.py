# Embedded file name: scripts/common/Lib/xdrlib.py
"""Implements (a subset of) Sun XDR -- eXternal Data Representation.

See: RFC 1014

"""
import struct
try:
    from cStringIO import StringIO as _StringIO
except ImportError:
    from StringIO import StringIO as _StringIO

__all__ = ['Error',
 'Packer',
 'Unpacker',
 'ConversionError']

class Error(Exception):
    """Exception class for this module. Use:
    
    except xdrlib.Error, var:
        # var has the Error instance for the exception
    
    Public ivars:
        msg -- contains the message
    
    """

    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return repr(self.msg)

    def __str__(self):
        return str(self.msg)


class ConversionError(Error):
    pass


class Packer:
    """Pack various data representations into a buffer."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.__buf = _StringIO()

    def get_buffer(self):
        return self.__buf.getvalue()

    get_buf = get_buffer

    def pack_uint(self, x):
        self.__buf.write(struct.pack('>L', x))

    def pack_int(self, x):
        self.__buf.write(struct.pack('>l', x))

    pack_enum = pack_int

    def pack_bool(self, x):
        if x:
            self.__buf.write('\x00\x00\x00\x01')
        else:
            self.__buf.write('\x00\x00\x00\x00')

    def pack_uhyper(self, x):
        self.pack_uint(x >> 32 & 4294967295L)
        self.pack_uint(x & 4294967295L)

    pack_hyper = pack_uhyper

    def pack_float(self, x):
        try:
            self.__buf.write(struct.pack('>f', x))
        except struct.error as msg:
            raise ConversionError, msg

    def pack_double(self, x):
        try:
            self.__buf.write(struct.pack('>d', x))
        except struct.error as msg:
            raise ConversionError, msg

    def pack_fstring(self, n, s):
        if n < 0:
            raise ValueError, 'fstring size must be nonnegative'
        data = s[:n]
        n = (n + 3) // 4 * 4
        data = data + (n - len(data)) * '\x00'
        self.__buf.write(data)

    pack_fopaque = pack_fstring

    def pack_string(self, s):
        n = len(s)
        self.pack_uint(n)
        self.pack_fstring(n, s)

    pack_opaque = pack_string
    pack_bytes = pack_string

    def pack_list(self, list, pack_item):
        for item in list:
            self.pack_uint(1)
            pack_item(item)

        self.pack_uint(0)

    def pack_farray(self, n, list, pack_item):
        if len(list) != n:
            raise ValueError, 'wrong array size'
        for item in list:
            pack_item(item)

    def pack_array(self, list, pack_item):
        n = len(list)
        self.pack_uint(n)
        self.pack_farray(n, list, pack_item)


class Unpacker:
    """Unpacks various data representations from the given buffer."""

    def __init__(self, data):
        self.reset(data)

    def reset(self, data):
        self.__buf = data
        self.__pos = 0

    def get_position(self):
        return self.__pos

    def set_position(self, position):
        self.__pos = position

    def get_buffer(self):
        return self.__buf

    def done(self):
        if self.__pos < len(self.__buf):
            raise Error('unextracted data remains')

    def unpack_uint(self):
        i = self.__pos
        self.__pos = j = i + 4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        x = struct.unpack('>L', data)[0]
        try:
            return int(x)
        except OverflowError:
            return x

    def unpack_int(self):
        i = self.__pos
        self.__pos = j = i + 4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        return struct.unpack('>l', data)[0]

    unpack_enum = unpack_int

    def unpack_bool(self):
        return bool(self.unpack_int())

    def unpack_uhyper(self):
        hi = self.unpack_uint()
        lo = self.unpack_uint()
        return long(hi) << 32 | lo

    def unpack_hyper(self):
        x = self.unpack_uhyper()
        if x >= 9223372036854775808L:
            x = x - 18446744073709551616L
        return x

    def unpack_float(self):
        i = self.__pos
        self.__pos = j = i + 4
        data = self.__buf[i:j]
        if len(data) < 4:
            raise EOFError
        return struct.unpack('>f', data)[0]

    def unpack_double(self):
        i = self.__pos
        self.__pos = j = i + 8
        data = self.__buf[i:j]
        if len(data) < 8:
            raise EOFError
        return struct.unpack('>d', data)[0]

    def unpack_fstring(self, n):
        if n < 0:
            raise ValueError, 'fstring size must be nonnegative'
        i = self.__pos
        j = i + (n + 3) // 4 * 4
        if j > len(self.__buf):
            raise EOFError
        self.__pos = j
        return self.__buf[i:i + n]

    unpack_fopaque = unpack_fstring

    def unpack_string(self):
        n = self.unpack_uint()
        return self.unpack_fstring(n)

    unpack_opaque = unpack_string
    unpack_bytes = unpack_string

    def unpack_list--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'list'

6	SETUP_LOOP        '94'

9	LOAD_FAST         'self'
12	LOAD_ATTR         'unpack_uint'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'x'

21	LOAD_FAST         'x'
24	LOAD_CONST        0
27	COMPARE_OP        '=='
30	POP_JUMP_IF_FALSE '37'
33	BREAK_LOOP        None
34	JUMP_FORWARD      '37'
37_0	COME_FROM         '34'

37	LOAD_FAST         'x'
40	LOAD_CONST        1
43	COMPARE_OP        '!='
46	POP_JUMP_IF_FALSE '68'

49	LOAD_GLOBAL       'ConversionError'
52	LOAD_CONST        '0 or 1 expected, got %r'
55	LOAD_FAST         'x'
58	BUILD_TUPLE_1     None
61	BINARY_MODULO     None
62	RAISE_VARARGS_2   None
65	JUMP_FORWARD      '68'
68_0	COME_FROM         '65'

68	LOAD_FAST         'unpack_item'
71	CALL_FUNCTION_0   None
74	STORE_FAST        'item'

77	LOAD_FAST         'list'
80	LOAD_ATTR         'append'
83	LOAD_FAST         'item'
86	CALL_FUNCTION_1   None
89	POP_TOP           None
90	JUMP_BACK         '9'
93	POP_BLOCK         None
94_0	COME_FROM         '6'

94	LOAD_FAST         'list'
97	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 93

    def unpack_farray(self, n, unpack_item):
        list = []
        for i in range(n):
            list.append(unpack_item())

        return list

    def unpack_array(self, unpack_item):
        n = self.unpack_uint()
        return self.unpack_farray(n, unpack_item)