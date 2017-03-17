# Embedded file name: scripts/common/Lib/json/decoder.py
"""Implementation of JSONDecoder
"""
import re
import sys
import struct
from json import scanner
try:
    from _json import scanstring as c_scanstring
except ImportError:
    c_scanstring = None

__all__ = ['JSONDecoder']
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL

def _floatconstants():
    _BYTES = '7FF80000000000007FF0000000000000'.decode('hex')
    if sys.byteorder != 'big':
        _BYTES = _BYTES[:8][::-1] + _BYTES[8:][::-1]
    nan, inf = struct.unpack('dd', _BYTES)
    return (nan, inf, -inf)


NaN, PosInf, NegInf = _floatconstants()

def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return (lineno, colno)


def errmsg(msg, doc, pos, end = None):
    lineno, colno = linecol(doc, pos)
    if end is None:
        fmt = '{0}: line {1} column {2} (char {3})'
        return fmt.format(msg, lineno, colno, pos)
    else:
        endlineno, endcolno = linecol(doc, end)
        fmt = '{0}: line {1} column {2} - line {3} column {4} (char {5} - {6})'
        return fmt.format(msg, lineno, colno, endlineno, endcolno, pos, end)


_CONSTANTS = {'-Infinity': NegInf,
 'Infinity': PosInf,
 'NaN': NaN}
STRINGCHUNK = re.compile('(.*?)(["\\\\\\x00-\\x1f])', FLAGS)
BACKSLASH = {'"': u'"',
 '\\': u'\\',
 '/': u'/',
 'b': u'\x08',
 'f': u'\x0c',
 'n': u'\n',
 'r': u'\r',
 't': u'\t'}
DEFAULT_ENCODING = 'utf-8'

def py_scanstring--- This code section failed: ---

0	LOAD_FAST         'encoding'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	POP_JUMP_IF_FALSE '21'

12	LOAD_GLOBAL       'DEFAULT_ENCODING'
15	STORE_FAST        'encoding'
18	JUMP_FORWARD      '21'
21_0	COME_FROM         '18'

21	BUILD_LIST_0      None
24	STORE_FAST        'chunks'

27	LOAD_FAST         'chunks'
30	LOAD_ATTR         'append'
33	STORE_FAST        '_append'

36	LOAD_FAST         'end'
39	LOAD_CONST        1
42	BINARY_SUBTRACT   None
43	STORE_FAST        'begin'

46	SETUP_LOOP        '786'

49	LOAD_FAST         '_m'
52	LOAD_FAST         's'
55	LOAD_FAST         'end'
58	CALL_FUNCTION_2   None
61	STORE_FAST        'chunk'

64	LOAD_FAST         'chunk'
67	LOAD_CONST        None
70	COMPARE_OP        'is'
73	POP_JUMP_IF_FALSE '103'

76	LOAD_GLOBAL       'ValueError'

79	LOAD_GLOBAL       'errmsg'
82	LOAD_CONST        'Unterminated string starting at'
85	LOAD_FAST         's'
88	LOAD_FAST         'begin'
91	CALL_FUNCTION_3   None
94	CALL_FUNCTION_1   None
97	RAISE_VARARGS_1   None
100	JUMP_FORWARD      '103'
103_0	COME_FROM         '100'

103	LOAD_FAST         'chunk'
106	LOAD_ATTR         'end'
109	CALL_FUNCTION_0   None
112	STORE_FAST        'end'

115	LOAD_FAST         'chunk'
118	LOAD_ATTR         'groups'
121	CALL_FUNCTION_0   None
124	UNPACK_SEQUENCE_2 None
127	STORE_FAST        'content'
130	STORE_FAST        'terminator'

133	LOAD_FAST         'content'
136	POP_JUMP_IF_FALSE '185'

139	LOAD_GLOBAL       'isinstance'
142	LOAD_FAST         'content'
145	LOAD_GLOBAL       'unicode'
148	CALL_FUNCTION_2   None
151	POP_JUMP_IF_TRUE  '172'

154	LOAD_GLOBAL       'unicode'
157	LOAD_FAST         'content'
160	LOAD_FAST         'encoding'
163	CALL_FUNCTION_2   None
166	STORE_FAST        'content'
169	JUMP_FORWARD      '172'
172_0	COME_FROM         '169'

172	LOAD_FAST         '_append'
175	LOAD_FAST         'content'
178	CALL_FUNCTION_1   None
181	POP_TOP           None
182	JUMP_FORWARD      '185'
185_0	COME_FROM         '182'

185	LOAD_FAST         'terminator'
188	LOAD_CONST        '"'
191	COMPARE_OP        '=='
194	POP_JUMP_IF_FALSE '201'

197	BREAK_LOOP        None
198	JUMP_FORWARD      '277'

201	LOAD_FAST         'terminator'
204	LOAD_CONST        '\\'
207	COMPARE_OP        '!='
210	POP_JUMP_IF_FALSE '277'

213	LOAD_FAST         'strict'
216	POP_JUMP_IF_FALSE '261'

219	LOAD_CONST        'Invalid control character {0!r} at'
222	LOAD_ATTR         'format'
225	LOAD_FAST         'terminator'
228	CALL_FUNCTION_1   None
231	STORE_FAST        'msg'

234	LOAD_GLOBAL       'ValueError'
237	LOAD_GLOBAL       'errmsg'
240	LOAD_FAST         'msg'
243	LOAD_FAST         's'
246	LOAD_FAST         'end'
249	CALL_FUNCTION_3   None
252	CALL_FUNCTION_1   None
255	RAISE_VARARGS_1   None
258	JUMP_ABSOLUTE     '277'

261	LOAD_FAST         '_append'
264	LOAD_FAST         'terminator'
267	CALL_FUNCTION_1   None
270	POP_TOP           None

271	CONTINUE          '49'
274	JUMP_FORWARD      '277'
277_0	COME_FROM         '198'
277_1	COME_FROM         '274'

277	SETUP_EXCEPT      '294'

280	LOAD_FAST         's'
283	LOAD_FAST         'end'
286	BINARY_SUBSCR     None
287	STORE_FAST        'esc'
290	POP_BLOCK         None
291	JUMP_FORWARD      '335'
294_0	COME_FROM         '277'

294	DUP_TOP           None
295	LOAD_GLOBAL       'IndexError'
298	COMPARE_OP        'exception match'
301	POP_JUMP_IF_FALSE '334'
304	POP_TOP           None
305	POP_TOP           None
306	POP_TOP           None

307	LOAD_GLOBAL       'ValueError'

310	LOAD_GLOBAL       'errmsg'
313	LOAD_CONST        'Unterminated string starting at'
316	LOAD_FAST         's'
319	LOAD_FAST         'begin'
322	CALL_FUNCTION_3   None
325	CALL_FUNCTION_1   None
328	RAISE_VARARGS_1   None
331	JUMP_FORWARD      '335'
334	END_FINALLY       None
335_0	COME_FROM         '291'
335_1	COME_FROM         '334'

335	LOAD_FAST         'esc'
338	LOAD_CONST        'u'
341	COMPARE_OP        '!='
344	POP_JUMP_IF_FALSE '434'

347	SETUP_EXCEPT      '364'

350	LOAD_FAST         '_b'
353	LOAD_FAST         'esc'
356	BINARY_SUBSCR     None
357	STORE_FAST        'char'
360	POP_BLOCK         None
361	JUMP_FORWARD      '421'
364_0	COME_FROM         '347'

364	DUP_TOP           None
365	LOAD_GLOBAL       'KeyError'
368	COMPARE_OP        'exception match'
371	POP_JUMP_IF_FALSE '420'
374	POP_TOP           None
375	POP_TOP           None
376	POP_TOP           None

377	LOAD_CONST        'Invalid \\escape: '
380	LOAD_GLOBAL       'repr'
383	LOAD_FAST         'esc'
386	CALL_FUNCTION_1   None
389	BINARY_ADD        None
390	STORE_FAST        'msg'

393	LOAD_GLOBAL       'ValueError'
396	LOAD_GLOBAL       'errmsg'
399	LOAD_FAST         'msg'
402	LOAD_FAST         's'
405	LOAD_FAST         'end'
408	CALL_FUNCTION_3   None
411	CALL_FUNCTION_1   None
414	RAISE_VARARGS_1   None
417	JUMP_FORWARD      '421'
420	END_FINALLY       None
421_0	COME_FROM         '361'
421_1	COME_FROM         '420'

421	LOAD_FAST         'end'
424	LOAD_CONST        1
427	INPLACE_ADD       None
428	STORE_FAST        'end'
431	JUMP_FORWARD      '772'

434	LOAD_FAST         's'
437	LOAD_FAST         'end'
440	LOAD_CONST        1
443	BINARY_ADD        None
444	LOAD_FAST         'end'
447	LOAD_CONST        5
450	BINARY_ADD        None
451	SLICE+3           None
452	STORE_FAST        'esc'

455	LOAD_FAST         'end'
458	LOAD_CONST        5
461	BINARY_ADD        None
462	STORE_FAST        'next_end'

465	LOAD_GLOBAL       'len'
468	LOAD_FAST         'esc'
471	CALL_FUNCTION_1   None
474	LOAD_CONST        4
477	COMPARE_OP        '!='
480	POP_JUMP_IF_FALSE '516'

483	LOAD_CONST        'Invalid \\uXXXX escape'
486	STORE_FAST        'msg'

489	LOAD_GLOBAL       'ValueError'
492	LOAD_GLOBAL       'errmsg'
495	LOAD_FAST         'msg'
498	LOAD_FAST         's'
501	LOAD_FAST         'end'
504	CALL_FUNCTION_3   None
507	CALL_FUNCTION_1   None
510	RAISE_VARARGS_1   None
513	JUMP_FORWARD      '516'
516_0	COME_FROM         '513'

516	LOAD_GLOBAL       'int'
519	LOAD_FAST         'esc'
522	LOAD_CONST        16
525	CALL_FUNCTION_2   None
528	STORE_FAST        'uni'

531	LOAD_CONST        55296
534	LOAD_FAST         'uni'
537	DUP_TOP           None
538	ROT_THREE         None
539	COMPARE_OP        '<='
542	JUMP_IF_FALSE_OR_POP '554'
545	LOAD_CONST        56319
548	COMPARE_OP        '<='
551	JUMP_FORWARD      '556'
554_0	COME_FROM         '542'
554	ROT_TWO           None
555	POP_TOP           None
556_0	COME_FROM         '551'
556	POP_JUMP_IF_FALSE '754'
559	LOAD_GLOBAL       'sys'
562	LOAD_ATTR         'maxunicode'
565	LOAD_CONST        65535
568	COMPARE_OP        '>'
571_0	COME_FROM         '556'
571	POP_JUMP_IF_FALSE '754'

574	LOAD_CONST        'Invalid \\uXXXX\\uXXXX surrogate pair'
577	STORE_FAST        'msg'

580	LOAD_FAST         's'
583	LOAD_FAST         'end'
586	LOAD_CONST        5
589	BINARY_ADD        None
590	LOAD_FAST         'end'
593	LOAD_CONST        7
596	BINARY_ADD        None
597	SLICE+3           None
598	LOAD_CONST        '\\u'
601	COMPARE_OP        '=='
604	POP_JUMP_IF_TRUE  '634'

607	LOAD_GLOBAL       'ValueError'
610	LOAD_GLOBAL       'errmsg'
613	LOAD_FAST         'msg'
616	LOAD_FAST         's'
619	LOAD_FAST         'end'
622	CALL_FUNCTION_3   None
625	CALL_FUNCTION_1   None
628	RAISE_VARARGS_1   None
631	JUMP_FORWARD      '634'
634_0	COME_FROM         '631'

634	LOAD_FAST         's'
637	LOAD_FAST         'end'
640	LOAD_CONST        7
643	BINARY_ADD        None
644	LOAD_FAST         'end'
647	LOAD_CONST        11
650	BINARY_ADD        None
651	SLICE+3           None
652	STORE_FAST        'esc2'

655	LOAD_GLOBAL       'len'
658	LOAD_FAST         'esc2'
661	CALL_FUNCTION_1   None
664	LOAD_CONST        4
667	COMPARE_OP        '!='
670	POP_JUMP_IF_FALSE '700'

673	LOAD_GLOBAL       'ValueError'
676	LOAD_GLOBAL       'errmsg'
679	LOAD_FAST         'msg'
682	LOAD_FAST         's'
685	LOAD_FAST         'end'
688	CALL_FUNCTION_3   None
691	CALL_FUNCTION_1   None
694	RAISE_VARARGS_1   None
697	JUMP_FORWARD      '700'
700_0	COME_FROM         '697'

700	LOAD_GLOBAL       'int'
703	LOAD_FAST         'esc2'
706	LOAD_CONST        16
709	CALL_FUNCTION_2   None
712	STORE_FAST        'uni2'

715	LOAD_CONST        65536
718	LOAD_FAST         'uni'
721	LOAD_CONST        55296
724	BINARY_SUBTRACT   None
725	LOAD_CONST        10
728	BINARY_LSHIFT     None
729	LOAD_FAST         'uni2'
732	LOAD_CONST        56320
735	BINARY_SUBTRACT   None
736	BINARY_OR         None
737	BINARY_ADD        None
738	STORE_FAST        'uni'

741	LOAD_FAST         'next_end'
744	LOAD_CONST        6
747	INPLACE_ADD       None
748	STORE_FAST        'next_end'
751	JUMP_FORWARD      '754'
754_0	COME_FROM         '751'

754	LOAD_GLOBAL       'unichr'
757	LOAD_FAST         'uni'
760	CALL_FUNCTION_1   None
763	STORE_FAST        'char'

766	LOAD_FAST         'next_end'
769	STORE_FAST        'end'
772_0	COME_FROM         '431'

772	LOAD_FAST         '_append'
775	LOAD_FAST         'char'
778	CALL_FUNCTION_1   None
781	POP_TOP           None
782	JUMP_BACK         '49'
785	POP_BLOCK         None
786_0	COME_FROM         '46'

786	LOAD_CONST        u''
789	LOAD_ATTR         'join'
792	LOAD_FAST         'chunks'
795	CALL_FUNCTION_1   None
798	LOAD_FAST         'end'
801	BUILD_TUPLE_2     None
804	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 785


scanstring = c_scanstring or py_scanstring
WHITESPACE = re.compile('[ \\t\\n\\r]*', FLAGS)
WHITESPACE_STR = ' \t\n\r'

def JSONObject(s_and_end, encoding, strict, scan_once, object_hook, object_pairs_hook, _w = WHITESPACE.match, _ws = WHITESPACE_STR):
    s, end = s_and_end
    pairs = []
    pairs_append = pairs.append
    nextchar = s[end:end + 1]
    if nextchar != '"':
        if nextchar in _ws:
            end = _w(s, end).end()
            nextchar = s[end:end + 1]
        if nextchar == '}':
            if object_pairs_hook is not None:
                result = object_pairs_hook(pairs)
                return (result, end)
            pairs = {}
            if object_hook is not None:
                pairs = object_hook(pairs)
            return (pairs, end + 1)
        if nextchar != '"':
            raise ValueError(errmsg('Expecting property name', s, end))
    end += 1
    while True:
        key, end = scanstring(s, end, encoding, strict)
        if s[end:end + 1] != ':':
            end = _w(s, end).end()
            if s[end:end + 1] != ':':
                raise ValueError(errmsg('Expecting : delimiter', s, end))
        end += 1
        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

        try:
            value, end = scan_once(s, end)
        except StopIteration:
            raise ValueError(errmsg('Expecting object', s, end))

        pairs_append((key, value))
        try:
            nextchar = s[end]
            if nextchar in _ws:
                end = _w(s, end + 1).end()
                nextchar = s[end]
        except IndexError:
            nextchar = ''

        end += 1
        if nextchar == '}':
            break
        elif nextchar != ',':
            raise ValueError(errmsg('Expecting , delimiter', s, end - 1))
        try:
            nextchar = s[end]
            if nextchar in _ws:
                end += 1
                nextchar = s[end]
                if nextchar in _ws:
                    end = _w(s, end + 1).end()
                    nextchar = s[end]
        except IndexError:
            nextchar = ''

        end += 1
        if nextchar != '"':
            raise ValueError(errmsg('Expecting property name', s, end - 1))

    if object_pairs_hook is not None:
        result = object_pairs_hook(pairs)
        return (result, end)
    else:
        pairs = dict(pairs)
        if object_hook is not None:
            pairs = object_hook(pairs)
        return (pairs, end)


def JSONArray(s_and_end, scan_once, _w = WHITESPACE.match, _ws = WHITESPACE_STR):
    s, end = s_and_end
    values = []
    nextchar = s[end:end + 1]
    if nextchar in _ws:
        end = _w(s, end + 1).end()
        nextchar = s[end:end + 1]
    if nextchar == ']':
        return (values, end + 1)
    _append = values.append
    while True:
        try:
            value, end = scan_once(s, end)
        except StopIteration:
            raise ValueError(errmsg('Expecting object', s, end))

        _append(value)
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _w(s, end + 1).end()
            nextchar = s[end:end + 1]
        end += 1
        if nextchar == ']':
            break
        elif nextchar != ',':
            raise ValueError(errmsg('Expecting , delimiter', s, end))
        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

    return (values, end)


class JSONDecoder(object):
    """Simple JSON <http://json.org> decoder
    
    Performs the following translations in decoding by default:
    
    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | unicode           |
    +---------------+-------------------+
    | number (int)  | int, long         |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+
    
    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as
    their corresponding ``float`` values, which is outside the JSON spec.
    
    """

    def __init__(self, encoding = None, object_hook = None, parse_float = None, parse_int = None, parse_constant = None, strict = True, object_pairs_hook = None):
        r"""``encoding`` determines the encoding used to interpret any ``str``
        objects decoded by this instance (utf-8 by default).  It has no
        effect when decoding ``unicode`` objects.
        
        Note that currently only encodings that are a superset of ASCII work,
        strings of other encodings should be passed in as ``unicode``.
        
        ``object_hook``, if specified, will be called with the result
        of every JSON object decoded and its return value will be used in
        place of the given ``dict``.  This can be used to provide custom
        deserializations (e.g. to support JSON-RPC class hinting).
        
        ``object_pairs_hook``, if specified will be called with the result of
        every JSON object decoded with an ordered list of pairs.  The return
        value of ``object_pairs_hook`` will be used instead of the ``dict``.
        This feature can be used to implement custom decoders that rely on the
        order that the key and value pairs are decoded (for example,
        collections.OrderedDict will remember the order of insertion). If
        ``object_hook`` is also defined, the ``object_pairs_hook`` takes
        priority.
        
        ``parse_float``, if specified, will be called with the string
        of every JSON float to be decoded. By default this is equivalent to
        float(num_str). This can be used to use another datatype or parser
        for JSON floats (e.g. decimal.Decimal).
        
        ``parse_int``, if specified, will be called with the string
        of every JSON int to be decoded. By default this is equivalent to
        int(num_str). This can be used to use another datatype or parser
        for JSON integers (e.g. float).
        
        ``parse_constant``, if specified, will be called with one of the
        following strings: -Infinity, Infinity, NaN.
        This can be used to raise an exception if invalid JSON numbers
        are encountered.
        
        If ``strict`` is false (true is the default), then control
        characters will be allowed inside strings.  Control characters in
        this context are those with character codes in the 0-31 range,
        including ``'\t'`` (tab), ``'\n'``, ``'\r'`` and ``'\0'``.
        
        """
        self.encoding = encoding
        self.object_hook = object_hook
        self.object_pairs_hook = object_pairs_hook
        self.parse_float = parse_float or float
        self.parse_int = parse_int or int
        self.parse_constant = parse_constant or _CONSTANTS.__getitem__
        self.strict = strict
        self.parse_object = JSONObject
        self.parse_array = JSONArray
        self.parse_string = scanstring
        self.scan_once = scanner.make_scanner(self)

    def decode(self, s, _w = WHITESPACE.match):
        """Return the Python representation of ``s`` (a ``str`` or ``unicode``
        instance containing a JSON document)
        
        """
        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
        end = _w(s, end).end()
        if end != len(s):
            raise ValueError(errmsg('Extra data', s, end, len(s)))
        return obj

    def raw_decode(self, s, idx = 0):
        """Decode a JSON document from ``s`` (a ``str`` or ``unicode``
        beginning with a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
        
        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.
        
        """
        try:
            obj, end = self.scan_once(s, idx)
        except StopIteration:
            raise ValueError('No JSON object could be decoded')

        return (obj, end)