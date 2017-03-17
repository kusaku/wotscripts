# Embedded file name: scripts/common/Lib/lib2to3/pgen2/tokenize.py
"""Tokenization help for Python programs.

generate_tokens(readline) is a generator that breaks a stream of
text into Python tokens.  It accepts a readline-like method which is called
repeatedly to get the next line of input (or "" for EOF).  It generates
5-tuples with these members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators

Older entry points
    tokenize_loop(readline, tokeneater)
    tokenize(readline, tokeneater=printtoken)
are the same, except instead of generating tokens, tokeneater is a callback
function to which the 5 fields described above are passed as 5 arguments,
each time a new token is found."""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro'
import string, re
from codecs import BOM_UTF8, lookup
from lib2to3.pgen2.token import *
from . import token
__all__ = [ x for x in dir(token) if x[0] != '_' ] + ['tokenize', 'generate_tokens', 'untokenize']
del token
try:
    bytes
except NameError:
    bytes = str

def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '[a-zA-Z_]\\w*'
Binnumber = '0[bB][01]*'
Hexnumber = '0[xX][\\da-fA-F]*[lL]?'
Octnumber = '0[oO]?[0-7]*[lL]?'
Decnumber = '[1-9]\\d*[lL]?'
Intnumber = group(Binnumber, Hexnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?\\d+'
Pointfloat = group('\\d+\\.\\d*', '\\.\\d+') + maybe(Exponent)
Expfloat = '\\d+' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('\\d+[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group("[ubUB]?[rR]?'''", '[ubUB]?[rR]?"""')
String = group("[uU]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", '[uU]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '<>', '!=', '//=?', '->', '[+\\-*/%&|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '[:;.,`@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group("[uUbB]?[rR]?'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), '[uUbB]?[rR]?"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
tokenprog, pseudoprog, single3prog, double3prog = map(re.compile, (Token,
 PseudoToken,
 Single3,
 Double3))
endprogs = {"'": re.compile(Single),
 '"': re.compile(Double),
 "'''": single3prog,
 '"""': double3prog,
 "r'''": single3prog,
 'r"""': double3prog,
 "u'''": single3prog,
 'u"""': double3prog,
 "b'''": single3prog,
 'b"""': double3prog,
 "ur'''": single3prog,
 'ur"""': double3prog,
 "br'''": single3prog,
 'br"""': double3prog,
 "R'''": single3prog,
 'R"""': double3prog,
 "U'''": single3prog,
 'U"""': double3prog,
 "B'''": single3prog,
 'B"""': double3prog,
 "uR'''": single3prog,
 'uR"""': double3prog,
 "Ur'''": single3prog,
 'Ur"""': double3prog,
 "UR'''": single3prog,
 'UR"""': double3prog,
 "bR'''": single3prog,
 'bR"""': double3prog,
 "Br'''": single3prog,
 'Br"""': double3prog,
 "BR'''": single3prog,
 'BR"""': double3prog,
 'r': None,
 'R': None,
 'u': None,
 'U': None,
 'b': None,
 'B': None}
triple_quoted = {}
for t in ("'''", '"""', "r'''", 'r"""', "R'''", 'R"""', "u'''", 'u"""', "U'''", 'U"""', "b'''", 'b"""', "B'''", 'B"""', "ur'''", 'ur"""', "Ur'''", 'Ur"""', "uR'''", 'uR"""', "UR'''", 'UR"""', "br'''", 'br"""', "Br'''", 'Br"""', "bR'''", 'bR"""', "BR'''", 'BR"""'):
    triple_quoted[t] = t

single_quoted = {}
for t in ("'", '"', "r'", 'r"', "R'", 'R"', "u'", 'u"', "U'", 'U"', "b'", 'b"', "B'", 'B"', "ur'", 'ur"', "Ur'", 'Ur"', "uR'", 'uR"', "UR'", 'UR"', "br'", 'br"', "Br'", 'Br"', "bR'", 'bR"', "BR'", 'BR"'):
    single_quoted[t] = t

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


def printtoken(type, token, start, end, line):
    srow, scol = start
    erow, ecol = end
    print '%d,%d-%d,%d:\t%s\t%s' % (srow,
     scol,
     erow,
     ecol,
     tok_name[type],
     repr(token))


def tokenize(readline, tokeneater = printtoken):
    """
    The tokenize() function accepts two parameters: one representing the
    input stream, and one providing an output mechanism for tokenize().
    
    The first parameter, readline, must be a callable object which provides
    the same interface as the readline() method of built-in file objects.
    Each call to the function should return one line of input as a string.
    
    The second parameter, tokeneater, must also be a callable object. It is
    called once for each token, with five arguments, corresponding to the
    tuples generated by generate_tokens().
    """
    try:
        tokenize_loop(readline, tokeneater)
    except StopTokenizing:
        pass


def tokenize_loop(readline, tokeneater):
    for token_info in generate_tokens(readline):
        tokeneater(*token_info)


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0

    def add_whitespace(self, start):
        row, col = start
        if not row <= self.prev_row:
            raise AssertionError
            col_offset = col - self.prev_col
            col_offset and self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        for t in iterable:
            if len(t) == 2:
                self.compat(t, iterable)
                break
            tok_type, token, start, end, line = t
            self.add_whitespace(start)
            self.tokens.append(token)
            self.prev_row, self.prev_col = end
            if tok_type in (NEWLINE, NL):
                self.prev_row += 1
                self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        startline = False
        indents = []
        toks_append = self.tokens.append
        toknum, tokval = token
        if toknum in (NAME, NUMBER):
            tokval += ' '
        if toknum in (NEWLINE, NL):
            startline = True
        for tok in iterable:
            toknum, tokval = tok[:2]
            if toknum in (NAME, NUMBER):
                tokval += ' '
            if toknum == INDENT:
                indents.append(tokval)
                continue
            elif toknum == DEDENT:
                indents.pop()
                continue
            elif toknum in (NEWLINE, NL):
                startline = True
            elif startline and indents:
                toks_append(indents[-1])
                startline = False
            toks_append(tokval)


cookie_re = re.compile('coding[:=]\\s*([-\\w.]+)')

def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    enc = orig_enc[:12].lower().replace('_', '-')
    if enc == 'utf-8' or enc.startswith('utf-8-'):
        return 'utf-8'
    if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or enc.startswith(('latin-1-', 'iso-8859-1-', 'iso-latin-1-')):
        return 'iso-8859-1'
    return orig_enc


def detect_encoding(readline):
    """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file. It requires one argment, readline,
    in the same way as the tokenize() generator.
    
    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read
    in.
    
    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263. If both a bom and a cookie are present, but
    disagree, a SyntaxError will be raised. If the encoding cookie is an invalid
    charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.
    
    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    bom_found = False
    encoding = None
    default = 'utf-8'

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return bytes()

    def find_cookie(line):
        try:
            line_string = line.decode('ascii')
        except UnicodeDecodeError:
            return None

        matches = cookie_re.findall(line_string)
        if not matches:
            return None
        else:
            encoding = _get_normal_name(matches[0])
            try:
                codec = lookup(encoding)
            except LookupError:
                raise SyntaxError('unknown encoding: ' + encoding)

            if bom_found:
                if codec.name != 'utf-8':
                    raise SyntaxError('encoding problem: utf-8')
                encoding += '-sig'
            return encoding

    first = read_or_stop()
    if first.startswith(BOM_UTF8):
        bom_found = True
        first = first[3:]
        default = 'utf-8-sig'
    if not first:
        return (default, [])
    encoding = find_cookie(first)
    if encoding:
        return (encoding, [first])
    second = read_or_stop()
    if not second:
        return (default, [first])
    encoding = find_cookie(second)
    if encoding:
        return (encoding, [first, second])
    else:
        return (default, [first, second])


def untokenize(iterable):
    """Transform tokens back into Python source code.
    
    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.
    
    Round-trip invariant for full input:
        Untokenized source will match input source exactly
    
    Round-trip invariant for limited intput:
        # Output text will tokenize the back to the input
        t1 = [tok[:2] for tok in generate_tokens(f.readline)]
        newcode = untokenize(t1)
        readline = iter(newcode.splitlines(1)).next
        t2 = [tok[:2] for tokin generate_tokens(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    return ut.untokenize(iterable)


def generate_tokens--- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'lnum'
7	DUP_TOP           None
8	STORE_FAST        'parenlev'
11	STORE_FAST        'continued'

14	LOAD_GLOBAL       'string'
17	LOAD_ATTR         'ascii_letters'
20	LOAD_CONST        '_'
23	BINARY_ADD        None
24	LOAD_CONST        '0123456789'
27	ROT_TWO           None
28	STORE_FAST        'namechars'
31	STORE_FAST        'numchars'

34	LOAD_CONST        ('', 0)
37	UNPACK_SEQUENCE_2 None
40	STORE_FAST        'contstr'
43	STORE_FAST        'needcont'

46	LOAD_CONST        None
49	STORE_FAST        'contline'

52	LOAD_CONST        0
55	BUILD_LIST_1      None
58	STORE_FAST        'indents'

61	SETUP_LOOP        '1789'

64	SETUP_EXCEPT      '80'

67	LOAD_FAST         'readline'
70	CALL_FUNCTION_0   None
73	STORE_FAST        'line'
76	POP_BLOCK         None
77	JUMP_FORWARD      '103'
80_0	COME_FROM         '64'

80	DUP_TOP           None
81	LOAD_GLOBAL       'StopIteration'
84	COMPARE_OP        'exception match'
87	POP_JUMP_IF_FALSE '102'
90	POP_TOP           None
91	POP_TOP           None
92	POP_TOP           None

93	LOAD_CONST        ''
96	STORE_FAST        'line'
99	JUMP_FORWARD      '103'
102	END_FINALLY       None
103_0	COME_FROM         '77'
103_1	COME_FROM         '102'

103	LOAD_FAST         'lnum'
106	LOAD_CONST        1
109	BINARY_ADD        None
110	STORE_FAST        'lnum'

113	LOAD_CONST        0
116	LOAD_GLOBAL       'len'
119	LOAD_FAST         'line'
122	CALL_FUNCTION_1   None
125	ROT_TWO           None
126	STORE_FAST        'pos'
129	STORE_FAST        'max'

132	LOAD_FAST         'contstr'
135	POP_JUMP_IF_FALSE '379'

138	LOAD_FAST         'line'
141	POP_JUMP_IF_TRUE  '162'

144	LOAD_GLOBAL       'TokenError'
147	LOAD_CONST        'EOF in multi-line string'
150	LOAD_FAST         'strstart'
153	BUILD_TUPLE_2     None
156	RAISE_VARARGS_2   None
159	JUMP_FORWARD      '162'
162_0	COME_FROM         '159'

162	LOAD_FAST         'endprog'
165	LOAD_ATTR         'match'
168	LOAD_FAST         'line'
171	CALL_FUNCTION_1   None
174	STORE_FAST        'endmatch'

177	LOAD_FAST         'endmatch'
180	POP_JUMP_IF_FALSE '261'

183	LOAD_FAST         'endmatch'
186	LOAD_ATTR         'end'
189	LOAD_CONST        0
192	CALL_FUNCTION_1   None
195	DUP_TOP           None
196	STORE_FAST        'pos'
199	STORE_FAST        'end'

202	LOAD_GLOBAL       'STRING'
205	LOAD_FAST         'contstr'
208	LOAD_FAST         'line'
211	LOAD_FAST         'end'
214	SLICE+2           None
215	BINARY_ADD        None

216	LOAD_FAST         'strstart'
219	LOAD_FAST         'lnum'
222	LOAD_FAST         'end'
225	BUILD_TUPLE_2     None
228	LOAD_FAST         'contline'
231	LOAD_FAST         'line'
234	BINARY_ADD        None
235	BUILD_TUPLE_5     None
238	YIELD_VALUE       None
239	POP_TOP           None

240	LOAD_CONST        ('', 0)
243	UNPACK_SEQUENCE_2 None
246	STORE_FAST        'contstr'
249	STORE_FAST        'needcont'

252	LOAD_CONST        None
255	STORE_FAST        'contline'
258	JUMP_ABSOLUTE     '987'

261	LOAD_FAST         'needcont'
264	POP_JUMP_IF_FALSE '353'
267	LOAD_FAST         'line'
270	LOAD_CONST        -2
273	SLICE+1           None
274	LOAD_CONST        '\\\n'
277	COMPARE_OP        '!='
280	POP_JUMP_IF_FALSE '353'
283	LOAD_FAST         'line'
286	LOAD_CONST        -3
289	SLICE+1           None
290	LOAD_CONST        '\\\r\n'
293	COMPARE_OP        '!='
296_0	COME_FROM         '264'
296_1	COME_FROM         '280'
296	POP_JUMP_IF_FALSE '353'

299	LOAD_GLOBAL       'ERRORTOKEN'
302	LOAD_FAST         'contstr'
305	LOAD_FAST         'line'
308	BINARY_ADD        None

309	LOAD_FAST         'strstart'
312	LOAD_FAST         'lnum'
315	LOAD_GLOBAL       'len'
318	LOAD_FAST         'line'
321	CALL_FUNCTION_1   None
324	BUILD_TUPLE_2     None
327	LOAD_FAST         'contline'
330	BUILD_TUPLE_5     None
333	YIELD_VALUE       None
334	POP_TOP           None

335	LOAD_CONST        ''
338	STORE_FAST        'contstr'

341	LOAD_CONST        None
344	STORE_FAST        'contline'

347	CONTINUE          '64'
350	JUMP_ABSOLUTE     '987'

353	LOAD_FAST         'contstr'
356	LOAD_FAST         'line'
359	BINARY_ADD        None
360	STORE_FAST        'contstr'

363	LOAD_FAST         'contline'
366	LOAD_FAST         'line'
369	BINARY_ADD        None
370	STORE_FAST        'contline'

373	CONTINUE          '64'
376	JUMP_FORWARD      '987'

379	LOAD_FAST         'parenlev'
382	LOAD_CONST        0
385	COMPARE_OP        '=='
388	POP_JUMP_IF_FALSE '951'
391	LOAD_FAST         'continued'
394	UNARY_NOT         None
395_0	COME_FROM         '388'
395	POP_JUMP_IF_FALSE '951'

398	LOAD_FAST         'line'
401	POP_JUMP_IF_TRUE  '408'
404	BREAK_LOOP        None
405	JUMP_FORWARD      '408'
408_0	COME_FROM         '405'

408	LOAD_CONST        0
411	STORE_FAST        'column'

414	SETUP_LOOP        '535'
417	LOAD_FAST         'pos'
420	LOAD_FAST         'max'
423	COMPARE_OP        '<'
426	POP_JUMP_IF_FALSE '534'

429	LOAD_FAST         'line'
432	LOAD_FAST         'pos'
435	BINARY_SUBSCR     None
436	LOAD_CONST        ' '
439	COMPARE_OP        '=='
442	POP_JUMP_IF_FALSE '458'
445	LOAD_FAST         'column'
448	LOAD_CONST        1
451	BINARY_ADD        None
452	STORE_FAST        'column'
455	JUMP_FORWARD      '521'

458	LOAD_FAST         'line'
461	LOAD_FAST         'pos'
464	BINARY_SUBSCR     None
465	LOAD_CONST        '\t'
468	COMPARE_OP        '=='
471	POP_JUMP_IF_FALSE '495'
474	LOAD_FAST         'column'
477	LOAD_GLOBAL       'tabsize'
480	BINARY_FLOOR_DIVIDE None
481	LOAD_CONST        1
484	BINARY_ADD        None
485	LOAD_GLOBAL       'tabsize'
488	BINARY_MULTIPLY   None
489	STORE_FAST        'column'
492	JUMP_FORWARD      '521'

495	LOAD_FAST         'line'
498	LOAD_FAST         'pos'
501	BINARY_SUBSCR     None
502	LOAD_CONST        '\x0c'
505	COMPARE_OP        '=='
508	POP_JUMP_IF_FALSE '520'
511	LOAD_CONST        0
514	STORE_FAST        'column'
517	JUMP_FORWARD      '521'

520	BREAK_LOOP        None
521_0	COME_FROM         '455'
521_1	COME_FROM         '492'
521_2	COME_FROM         '517'

521	LOAD_FAST         'pos'
524	LOAD_CONST        1
527	BINARY_ADD        None
528	STORE_FAST        'pos'
531	JUMP_BACK         '417'
534	POP_BLOCK         None
535_0	COME_FROM         '414'

535	LOAD_FAST         'pos'
538	LOAD_FAST         'max'
541	COMPARE_OP        '=='
544	POP_JUMP_IF_FALSE '551'
547	BREAK_LOOP        None
548	JUMP_FORWARD      '551'
551_0	COME_FROM         '548'

551	LOAD_FAST         'line'
554	LOAD_FAST         'pos'
557	BINARY_SUBSCR     None
558	LOAD_CONST        '#\r\n'
561	COMPARE_OP        'in'
564	POP_JUMP_IF_FALSE '773'

567	LOAD_FAST         'line'
570	LOAD_FAST         'pos'
573	BINARY_SUBSCR     None
574	LOAD_CONST        '#'
577	COMPARE_OP        '=='
580	POP_JUMP_IF_FALSE '705'

583	LOAD_FAST         'line'
586	LOAD_FAST         'pos'
589	SLICE+1           None
590	LOAD_ATTR         'rstrip'
593	LOAD_CONST        '\r\n'
596	CALL_FUNCTION_1   None
599	STORE_FAST        'comment_token'

602	LOAD_FAST         'pos'
605	LOAD_GLOBAL       'len'
608	LOAD_FAST         'comment_token'
611	CALL_FUNCTION_1   None
614	BINARY_ADD        None
615	STORE_FAST        'nl_pos'

618	LOAD_GLOBAL       'COMMENT'
621	LOAD_FAST         'comment_token'

624	LOAD_FAST         'lnum'
627	LOAD_FAST         'pos'
630	BUILD_TUPLE_2     None
633	LOAD_FAST         'lnum'
636	LOAD_FAST         'pos'
639	LOAD_GLOBAL       'len'
642	LOAD_FAST         'comment_token'
645	CALL_FUNCTION_1   None
648	BINARY_ADD        None
649	BUILD_TUPLE_2     None
652	LOAD_FAST         'line'
655	BUILD_TUPLE_5     None
658	YIELD_VALUE       None
659	POP_TOP           None

660	LOAD_GLOBAL       'NL'
663	LOAD_FAST         'line'
666	LOAD_FAST         'nl_pos'
669	SLICE+1           None

670	LOAD_FAST         'lnum'
673	LOAD_FAST         'nl_pos'
676	BUILD_TUPLE_2     None
679	LOAD_FAST         'lnum'
682	LOAD_GLOBAL       'len'
685	LOAD_FAST         'line'
688	CALL_FUNCTION_1   None
691	BUILD_TUPLE_2     None
694	LOAD_FAST         'line'
697	BUILD_TUPLE_5     None
700	YIELD_VALUE       None
701	POP_TOP           None
702	JUMP_BACK         '64'

705	LOAD_GLOBAL       'NL'
708	LOAD_GLOBAL       'COMMENT'
711	BUILD_TUPLE_2     None
714	LOAD_FAST         'line'
717	LOAD_FAST         'pos'
720	BINARY_SUBSCR     None
721	LOAD_CONST        '#'
724	COMPARE_OP        '=='
727	BINARY_SUBSCR     None
728	LOAD_FAST         'line'
731	LOAD_FAST         'pos'
734	SLICE+1           None

735	LOAD_FAST         'lnum'
738	LOAD_FAST         'pos'
741	BUILD_TUPLE_2     None
744	LOAD_FAST         'lnum'
747	LOAD_GLOBAL       'len'
750	LOAD_FAST         'line'
753	CALL_FUNCTION_1   None
756	BUILD_TUPLE_2     None
759	LOAD_FAST         'line'
762	BUILD_TUPLE_5     None
765	YIELD_VALUE       None
766	POP_TOP           None

767	CONTINUE          '64'
770	JUMP_FORWARD      '773'
773_0	COME_FROM         '770'

773	LOAD_FAST         'column'
776	LOAD_FAST         'indents'
779	LOAD_CONST        -1
782	BINARY_SUBSCR     None
783	COMPARE_OP        '>'
786	POP_JUMP_IF_FALSE '841'

789	LOAD_FAST         'indents'
792	LOAD_ATTR         'append'
795	LOAD_FAST         'column'
798	CALL_FUNCTION_1   None
801	POP_TOP           None

802	LOAD_GLOBAL       'INDENT'
805	LOAD_FAST         'line'
808	LOAD_FAST         'pos'
811	SLICE+2           None
812	LOAD_FAST         'lnum'
815	LOAD_CONST        0
818	BUILD_TUPLE_2     None
821	LOAD_FAST         'lnum'
824	LOAD_FAST         'pos'
827	BUILD_TUPLE_2     None
830	LOAD_FAST         'line'
833	BUILD_TUPLE_5     None
836	YIELD_VALUE       None
837	POP_TOP           None
838	JUMP_FORWARD      '841'
841_0	COME_FROM         '838'

841	SETUP_LOOP        '987'
844	LOAD_FAST         'column'
847	LOAD_FAST         'indents'
850	LOAD_CONST        -1
853	BINARY_SUBSCR     None
854	COMPARE_OP        '<'
857	POP_JUMP_IF_FALSE '947'

860	LOAD_FAST         'column'
863	LOAD_FAST         'indents'
866	COMPARE_OP        'not in'
869	POP_JUMP_IF_FALSE '902'

872	LOAD_GLOBAL       'IndentationError'

875	LOAD_CONST        'unindent does not match any outer indentation level'

878	LOAD_CONST        '<tokenize>'
881	LOAD_FAST         'lnum'
884	LOAD_FAST         'pos'
887	LOAD_FAST         'line'
890	BUILD_TUPLE_4     None
893	CALL_FUNCTION_2   None
896	RAISE_VARARGS_1   None
899	JUMP_FORWARD      '902'
902_0	COME_FROM         '899'

902	LOAD_FAST         'indents'
905	LOAD_CONST        -1
908	SLICE+2           None
909	STORE_FAST        'indents'

912	LOAD_GLOBAL       'DEDENT'
915	LOAD_CONST        ''
918	LOAD_FAST         'lnum'
921	LOAD_FAST         'pos'
924	BUILD_TUPLE_2     None
927	LOAD_FAST         'lnum'
930	LOAD_FAST         'pos'
933	BUILD_TUPLE_2     None
936	LOAD_FAST         'line'
939	BUILD_TUPLE_5     None
942	YIELD_VALUE       None
943	POP_TOP           None
944	JUMP_BACK         '844'
947	POP_BLOCK         None
948_0	COME_FROM         '841'
948	JUMP_FORWARD      '987'

951	LOAD_FAST         'line'
954	POP_JUMP_IF_TRUE  '981'

957	LOAD_GLOBAL       'TokenError'
960	LOAD_CONST        'EOF in multi-line statement'
963	LOAD_FAST         'lnum'
966	LOAD_CONST        0
969	BUILD_TUPLE_2     None
972	BUILD_TUPLE_2     None
975	RAISE_VARARGS_2   None
978	JUMP_FORWARD      '981'
981_0	COME_FROM         '978'

981	LOAD_CONST        0
984	STORE_FAST        'continued'
987_0	COME_FROM         '376'
987_1	COME_FROM         '948'

987	SETUP_LOOP        '1785'
990	LOAD_FAST         'pos'
993	LOAD_FAST         'max'
996	COMPARE_OP        '<'
999	POP_JUMP_IF_FALSE '1784'

1002	LOAD_GLOBAL       'pseudoprog'
1005	LOAD_ATTR         'match'
1008	LOAD_FAST         'line'
1011	LOAD_FAST         'pos'
1014	CALL_FUNCTION_2   None
1017	STORE_FAST        'pseudomatch'

1020	LOAD_FAST         'pseudomatch'
1023	POP_JUMP_IF_FALSE '1731'

1026	LOAD_FAST         'pseudomatch'
1029	LOAD_ATTR         'span'
1032	LOAD_CONST        1
1035	CALL_FUNCTION_1   None
1038	UNPACK_SEQUENCE_2 None
1041	STORE_FAST        'start'
1044	STORE_FAST        'end'

1047	LOAD_FAST         'lnum'
1050	LOAD_FAST         'start'
1053	BUILD_TUPLE_2     None
1056	LOAD_FAST         'lnum'
1059	LOAD_FAST         'end'
1062	BUILD_TUPLE_2     None
1065	LOAD_FAST         'end'
1068	ROT_THREE         None
1069	ROT_TWO           None
1070	STORE_FAST        'spos'
1073	STORE_FAST        'epos'
1076	STORE_FAST        'pos'

1079	LOAD_FAST         'line'
1082	LOAD_FAST         'start'
1085	LOAD_FAST         'end'
1088	SLICE+3           None
1089	LOAD_FAST         'line'
1092	LOAD_FAST         'start'
1095	BINARY_SUBSCR     None
1096	ROT_TWO           None
1097	STORE_FAST        'token'
1100	STORE_FAST        'initial'

1103	LOAD_FAST         'initial'
1106	LOAD_FAST         'numchars'
1109	COMPARE_OP        'in'
1112	POP_JUMP_IF_TRUE  '1139'

1115	LOAD_FAST         'initial'
1118	LOAD_CONST        '.'
1121	COMPARE_OP        '=='
1124	POP_JUMP_IF_FALSE '1162'
1127	LOAD_FAST         'token'
1130	LOAD_CONST        '.'
1133	COMPARE_OP        '!='
1136_0	COME_FROM         '1112'
1136_1	COME_FROM         '1124'
1136	POP_JUMP_IF_FALSE '1162'

1139	LOAD_GLOBAL       'NUMBER'
1142	LOAD_FAST         'token'
1145	LOAD_FAST         'spos'
1148	LOAD_FAST         'epos'
1151	LOAD_FAST         'line'
1154	BUILD_TUPLE_5     None
1157	YIELD_VALUE       None
1158	POP_TOP           None
1159	JUMP_ABSOLUTE     '1781'

1162	LOAD_FAST         'initial'
1165	LOAD_CONST        '\r\n'
1168	COMPARE_OP        'in'
1171	POP_JUMP_IF_FALSE '1224'

1174	LOAD_GLOBAL       'NEWLINE'
1177	STORE_FAST        'newline'

1180	LOAD_FAST         'parenlev'
1183	LOAD_CONST        0
1186	COMPARE_OP        '>'
1189	POP_JUMP_IF_FALSE '1201'

1192	LOAD_GLOBAL       'NL'
1195	STORE_FAST        'newline'
1198	JUMP_FORWARD      '1201'
1201_0	COME_FROM         '1198'

1201	LOAD_FAST         'newline'
1204	LOAD_FAST         'token'
1207	LOAD_FAST         'spos'
1210	LOAD_FAST         'epos'
1213	LOAD_FAST         'line'
1216	BUILD_TUPLE_5     None
1219	YIELD_VALUE       None
1220	POP_TOP           None
1221	JUMP_ABSOLUTE     '1781'

1224	LOAD_FAST         'initial'
1227	LOAD_CONST        '#'
1230	COMPARE_OP        '=='
1233	POP_JUMP_IF_FALSE '1281'

1236	LOAD_FAST         'token'
1239	LOAD_ATTR         'endswith'
1242	LOAD_CONST        '\n'
1245	CALL_FUNCTION_1   None
1248	UNARY_NOT         None
1249	POP_JUMP_IF_TRUE  '1258'
1252	LOAD_ASSERT       'AssertionError'
1255	RAISE_VARARGS_1   None

1258	LOAD_GLOBAL       'COMMENT'
1261	LOAD_FAST         'token'
1264	LOAD_FAST         'spos'
1267	LOAD_FAST         'epos'
1270	LOAD_FAST         'line'
1273	BUILD_TUPLE_5     None
1276	YIELD_VALUE       None
1277	POP_TOP           None
1278	JUMP_ABSOLUTE     '1781'

1281	LOAD_FAST         'token'
1284	LOAD_GLOBAL       'triple_quoted'
1287	COMPARE_OP        'in'
1290	POP_JUMP_IF_FALSE '1416'

1293	LOAD_GLOBAL       'endprogs'
1296	LOAD_FAST         'token'
1299	BINARY_SUBSCR     None
1300	STORE_FAST        'endprog'

1303	LOAD_FAST         'endprog'
1306	LOAD_ATTR         'match'
1309	LOAD_FAST         'line'
1312	LOAD_FAST         'pos'
1315	CALL_FUNCTION_2   None
1318	STORE_FAST        'endmatch'

1321	LOAD_FAST         'endmatch'
1324	POP_JUMP_IF_FALSE '1384'

1327	LOAD_FAST         'endmatch'
1330	LOAD_ATTR         'end'
1333	LOAD_CONST        0
1336	CALL_FUNCTION_1   None
1339	STORE_FAST        'pos'

1342	LOAD_FAST         'line'
1345	LOAD_FAST         'start'
1348	LOAD_FAST         'pos'
1351	SLICE+3           None
1352	STORE_FAST        'token'

1355	LOAD_GLOBAL       'STRING'
1358	LOAD_FAST         'token'
1361	LOAD_FAST         'spos'
1364	LOAD_FAST         'lnum'
1367	LOAD_FAST         'pos'
1370	BUILD_TUPLE_2     None
1373	LOAD_FAST         'line'
1376	BUILD_TUPLE_5     None
1379	YIELD_VALUE       None
1380	POP_TOP           None
1381	JUMP_ABSOLUTE     '1728'

1384	LOAD_FAST         'lnum'
1387	LOAD_FAST         'start'
1390	BUILD_TUPLE_2     None
1393	STORE_FAST        'strstart'

1396	LOAD_FAST         'line'
1399	LOAD_FAST         'start'
1402	SLICE+1           None
1403	STORE_FAST        'contstr'

1406	LOAD_FAST         'line'
1409	STORE_FAST        'contline'

1412	BREAK_LOOP        None
1413	JUMP_ABSOLUTE     '1781'

1416	LOAD_FAST         'initial'
1419	LOAD_GLOBAL       'single_quoted'
1422	COMPARE_OP        'in'
1425	POP_JUMP_IF_TRUE  '1460'

1428	LOAD_FAST         'token'
1431	LOAD_CONST        2
1434	SLICE+2           None
1435	LOAD_GLOBAL       'single_quoted'
1438	COMPARE_OP        'in'
1441	POP_JUMP_IF_TRUE  '1460'

1444	LOAD_FAST         'token'
1447	LOAD_CONST        3
1450	SLICE+2           None
1451	LOAD_GLOBAL       'single_quoted'
1454	COMPARE_OP        'in'
1457_0	COME_FROM         '1425'
1457_1	COME_FROM         '1441'
1457	POP_JUMP_IF_FALSE '1576'

1460	LOAD_FAST         'token'
1463	LOAD_CONST        -1
1466	BINARY_SUBSCR     None
1467	LOAD_CONST        '\n'
1470	COMPARE_OP        '=='
1473	POP_JUMP_IF_FALSE '1553'

1476	LOAD_FAST         'lnum'
1479	LOAD_FAST         'start'
1482	BUILD_TUPLE_2     None
1485	STORE_FAST        'strstart'

1488	LOAD_GLOBAL       'endprogs'
1491	LOAD_FAST         'initial'
1494	BINARY_SUBSCR     None
1495	JUMP_IF_TRUE_OR_POP '1523'
1498	LOAD_GLOBAL       'endprogs'
1501	LOAD_FAST         'token'
1504	LOAD_CONST        1
1507	BINARY_SUBSCR     None
1508	BINARY_SUBSCR     None
1509	JUMP_IF_TRUE_OR_POP '1523'

1512	LOAD_GLOBAL       'endprogs'
1515	LOAD_FAST         'token'
1518	LOAD_CONST        2
1521	BINARY_SUBSCR     None
1522	BINARY_SUBSCR     None
1523_0	COME_FROM         '1495'
1523_1	COME_FROM         '1509'
1523	STORE_FAST        'endprog'

1526	LOAD_FAST         'line'
1529	LOAD_FAST         'start'
1532	SLICE+1           None
1533	LOAD_CONST        1
1536	ROT_TWO           None
1537	STORE_FAST        'contstr'
1540	STORE_FAST        'needcont'

1543	LOAD_FAST         'line'
1546	STORE_FAST        'contline'

1549	BREAK_LOOP        None
1550	JUMP_ABSOLUTE     '1728'

1553	LOAD_GLOBAL       'STRING'
1556	LOAD_FAST         'token'
1559	LOAD_FAST         'spos'
1562	LOAD_FAST         'epos'
1565	LOAD_FAST         'line'
1568	BUILD_TUPLE_5     None
1571	YIELD_VALUE       None
1572	POP_TOP           None
1573	JUMP_ABSOLUTE     '1781'

1576	LOAD_FAST         'initial'
1579	LOAD_FAST         'namechars'
1582	COMPARE_OP        'in'
1585	POP_JUMP_IF_FALSE '1611'

1588	LOAD_GLOBAL       'NAME'
1591	LOAD_FAST         'token'
1594	LOAD_FAST         'spos'
1597	LOAD_FAST         'epos'
1600	LOAD_FAST         'line'
1603	BUILD_TUPLE_5     None
1606	YIELD_VALUE       None
1607	POP_TOP           None
1608	JUMP_ABSOLUTE     '1781'

1611	LOAD_FAST         'initial'
1614	LOAD_CONST        '\\'
1617	COMPARE_OP        '=='
1620	POP_JUMP_IF_FALSE '1658'

1623	LOAD_GLOBAL       'NL'
1626	LOAD_FAST         'token'
1629	LOAD_FAST         'spos'
1632	LOAD_FAST         'lnum'
1635	LOAD_FAST         'pos'
1638	BUILD_TUPLE_2     None
1641	LOAD_FAST         'line'
1644	BUILD_TUPLE_5     None
1647	YIELD_VALUE       None
1648	POP_TOP           None

1649	LOAD_CONST        1
1652	STORE_FAST        'continued'
1655	JUMP_ABSOLUTE     '1781'

1658	LOAD_FAST         'initial'
1661	LOAD_CONST        '([{'
1664	COMPARE_OP        'in'
1667	POP_JUMP_IF_FALSE '1683'
1670	LOAD_FAST         'parenlev'
1673	LOAD_CONST        1
1676	BINARY_ADD        None
1677	STORE_FAST        'parenlev'
1680	JUMP_FORWARD      '1708'

1683	LOAD_FAST         'initial'
1686	LOAD_CONST        ')]}'
1689	COMPARE_OP        'in'
1692	POP_JUMP_IF_FALSE '1708'
1695	LOAD_FAST         'parenlev'
1698	LOAD_CONST        1
1701	BINARY_SUBTRACT   None
1702	STORE_FAST        'parenlev'
1705	JUMP_FORWARD      '1708'
1708_0	COME_FROM         '1680'
1708_1	COME_FROM         '1705'

1708	LOAD_GLOBAL       'OP'
1711	LOAD_FAST         'token'
1714	LOAD_FAST         'spos'
1717	LOAD_FAST         'epos'
1720	LOAD_FAST         'line'
1723	BUILD_TUPLE_5     None
1726	YIELD_VALUE       None
1727	POP_TOP           None
1728	JUMP_BACK         '990'

1731	LOAD_GLOBAL       'ERRORTOKEN'
1734	LOAD_FAST         'line'
1737	LOAD_FAST         'pos'
1740	BINARY_SUBSCR     None

1741	LOAD_FAST         'lnum'
1744	LOAD_FAST         'pos'
1747	BUILD_TUPLE_2     None
1750	LOAD_FAST         'lnum'
1753	LOAD_FAST         'pos'
1756	LOAD_CONST        1
1759	BINARY_ADD        None
1760	BUILD_TUPLE_2     None
1763	LOAD_FAST         'line'
1766	BUILD_TUPLE_5     None
1769	YIELD_VALUE       None
1770	POP_TOP           None

1771	LOAD_FAST         'pos'
1774	LOAD_CONST        1
1777	BINARY_ADD        None
1778	STORE_FAST        'pos'
1781	JUMP_BACK         '990'
1784	POP_BLOCK         None
1785_0	COME_FROM         '987'
1785	JUMP_BACK         '64'
1788	POP_BLOCK         None
1789_0	COME_FROM         '61'

1789	SETUP_LOOP        '1842'
1792	LOAD_FAST         'indents'
1795	LOAD_CONST        1
1798	SLICE+1           None
1799	GET_ITER          None
1800	FOR_ITER          '1841'
1803	STORE_FAST        'indent'

1806	LOAD_GLOBAL       'DEDENT'
1809	LOAD_CONST        ''
1812	LOAD_FAST         'lnum'
1815	LOAD_CONST        0
1818	BUILD_TUPLE_2     None
1821	LOAD_FAST         'lnum'
1824	LOAD_CONST        0
1827	BUILD_TUPLE_2     None
1830	LOAD_CONST        ''
1833	BUILD_TUPLE_5     None
1836	YIELD_VALUE       None
1837	POP_TOP           None
1838	JUMP_BACK         '1800'
1841	POP_BLOCK         None
1842_0	COME_FROM         '1789'

1842	LOAD_GLOBAL       'ENDMARKER'
1845	LOAD_CONST        ''
1848	LOAD_FAST         'lnum'
1851	LOAD_CONST        0
1854	BUILD_TUPLE_2     None
1857	LOAD_FAST         'lnum'
1860	LOAD_CONST        0
1863	BUILD_TUPLE_2     None
1866	LOAD_CONST        ''
1869	BUILD_TUPLE_5     None
1872	YIELD_VALUE       None
1873	POP_TOP           None
1874	LOAD_CONST        None
1877	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 1788


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        tokenize(open(sys.argv[1]).readline)
    else:
        tokenize(sys.stdin.readline)