# Embedded file name: scripts/common/Lib/plat-irix5/panelparser.py
from warnings import warnpy3k
warnpy3k('the panelparser module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
whitespace = ' \t\n'
operators = "()'"
separators = operators + whitespace + ';' + '"'

def tokenize_string(s):
    tokens = []
    while s:
        c = s[:1]
        if c in whitespace:
            s = s[1:]
        elif c == ';':
            s = ''
        elif c == '"':
            n = len(s)
            i = 1
            while i < n:
                c = s[i]
                i = i + 1
                if c == '"':
                    break
                if c == '\\':
                    i = i + 1

            tokens.append(s[:i])
            s = s[i:]
        elif c in operators:
            tokens.append(c)
            s = s[1:]
        else:
            n = len(s)
            i = 1
            while i < n:
                if s[i] in separators:
                    break
                i = i + 1

            tokens.append(s[:i])
            s = s[i:]

    return tokens


def tokenize_file--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'tokens'

6	SETUP_LOOP        '51'

9	LOAD_FAST         'fp'
12	LOAD_ATTR         'readline'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'line'

21	LOAD_FAST         'line'
24	POP_JUMP_IF_TRUE  '31'
27	BREAK_LOOP        None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_FAST         'tokens'
34	LOAD_GLOBAL       'tokenize_string'
37	LOAD_FAST         'line'
40	CALL_FUNCTION_1   None
43	BINARY_ADD        None
44	STORE_FAST        'tokens'
47	JUMP_BACK         '9'
50	POP_BLOCK         None
51_0	COME_FROM         '6'

51	LOAD_FAST         'tokens'
54	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 50


syntax_error = 'syntax error'

def parse_expr--- This code section failed: ---

0	LOAD_FAST         'tokens'
3	UNARY_NOT         None
4	POP_JUMP_IF_TRUE  '23'
7	LOAD_FAST         'tokens'
10	LOAD_CONST        0
13	BINARY_SUBSCR     None
14	LOAD_CONST        '('
17	COMPARE_OP        '!='
20_0	COME_FROM         '4'
20	POP_JUMP_IF_FALSE '35'

23	LOAD_GLOBAL       'syntax_error'
26	LOAD_CONST        'expected "("'
29	RAISE_VARARGS_2   None
32	JUMP_FORWARD      '35'
35_0	COME_FROM         '32'

35	LOAD_FAST         'tokens'
38	LOAD_CONST        1
41	SLICE+1           None
42	STORE_FAST        'tokens'

45	BUILD_LIST_0      None
48	STORE_FAST        'expr'

51	SETUP_LOOP        '183'

54	LOAD_FAST         'tokens'
57	POP_JUMP_IF_TRUE  '72'

60	LOAD_GLOBAL       'syntax_error'
63	LOAD_CONST        'missing ")"'
66	RAISE_VARARGS_2   None
69	JUMP_FORWARD      '72'
72_0	COME_FROM         '69'

72	LOAD_FAST         'tokens'
75	LOAD_CONST        0
78	BINARY_SUBSCR     None
79	LOAD_CONST        ')'
82	COMPARE_OP        '=='
85	POP_JUMP_IF_FALSE '102'

88	LOAD_FAST         'expr'
91	LOAD_FAST         'tokens'
94	LOAD_CONST        1
97	SLICE+1           None
98	BUILD_TUPLE_2     None
101	RETURN_END_IF     None

102	LOAD_FAST         'tokens'
105	LOAD_CONST        0
108	BINARY_SUBSCR     None
109	LOAD_CONST        '('
112	COMPARE_OP        '=='
115	POP_JUMP_IF_FALSE '152'

118	LOAD_GLOBAL       'parse_expr'
121	LOAD_FAST         'tokens'
124	CALL_FUNCTION_1   None
127	UNPACK_SEQUENCE_2 None
130	STORE_FAST        'subexpr'
133	STORE_FAST        'tokens'

136	LOAD_FAST         'expr'
139	LOAD_ATTR         'append'
142	LOAD_FAST         'subexpr'
145	CALL_FUNCTION_1   None
148	POP_TOP           None
149	JUMP_BACK         '54'

152	LOAD_FAST         'expr'
155	LOAD_ATTR         'append'
158	LOAD_FAST         'tokens'
161	LOAD_CONST        0
164	BINARY_SUBSCR     None
165	CALL_FUNCTION_1   None
168	POP_TOP           None

169	LOAD_FAST         'tokens'
172	LOAD_CONST        1
175	SLICE+1           None
176	STORE_FAST        'tokens'
179	JUMP_BACK         '54'
182	POP_BLOCK         None
183_0	COME_FROM         '51'

Syntax error at or near `POP_BLOCK' token at offset 182


def parse_file(fp):
    tokens = tokenize_file(fp)
    exprlist = []
    while tokens:
        expr, tokens = parse_expr(tokens)
        exprlist.append(expr)

    return exprlist