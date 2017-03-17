# Embedded file name: scripts/common/Lib/test/crashers/borrowed_ref_2.py
--- This code section failed: ---

0	LOAD_CONST        '\n_PyType_Lookup() returns a borrowed reference.\nThis attacks PyObject_GenericSetAttr().\n\nNB. on my machine this crashes in 2.5 debug but not release.\n'
3	STORE_NAME        '__doc__'

6	LOAD_CONST        'A'
9	LOAD_NAME         'object'
12	BUILD_TUPLE_1     None
15	LOAD_CONST        '<code_object A>'
18	MAKE_FUNCTION_0   None
21	CALL_FUNCTION_0   None
24	BUILD_CLASS       None
25	STORE_NAME        'A'

28	LOAD_CONST        'B'
31	LOAD_NAME         'object'
34	BUILD_TUPLE_1     None
37	LOAD_CONST        '<code_object B>'
40	MAKE_FUNCTION_0   None
43	CALL_FUNCTION_0   None
46	BUILD_CLASS       None
47	STORE_NAME        'B'

50	LOAD_CONST        'D'
53	LOAD_NAME         'object'
56	BUILD_TUPLE_1     None
59	LOAD_CONST        '<code_object D>'
62	MAKE_FUNCTION_0   None
65	CALL_FUNCTION_0   None
68	BUILD_CLASS       None
69	STORE_NAME        'D'

72	LOAD_CONST        'C'
75	LOAD_NAME         'object'
78	BUILD_TUPLE_1     None
81	LOAD_CONST        '<code_object C>'
84	MAKE_FUNCTION_0   None
87	CALL_FUNCTION_0   None
90	BUILD_CLASS       None
91	STORE_NAME        'C'

94	LOAD_NAME         'C'
97	CALL_FUNCTION_0   None
100	STORE_NAME        'c'

103	LOAD_NAME         'A'
106	CALL_FUNCTION_0   None
109	STORE_NAME        'a'

112	LOAD_NAME         'a'
115	LOAD_NAME         'a'
118	STORE_ATTR        'cycle'

121	LOAD_NAME         'B'
124	CALL_FUNCTION_0   None
127	LOAD_NAME         'a'
130	STORE_ATTR        'other'

133	LOAD_CONST        None
136	BUILD_LIST_1      None
139	LOAD_CONST        1000000
142	BINARY_MULTIPLY   None
143	STORE_NAME        'lst'

146	LOAD_CONST        0
149	STORE_NAME        'i'

152	DELETE_NAME       'a'

155	SETUP_LOOP        '194'

158	LOAD_CONST        42
161	LOAD_NAME         'c'
164	STORE_ATTR        'd'

167	LOAD_NAME         'c'
170	LOAD_ATTR         'g'
173	LOAD_NAME         'lst'
176	LOAD_NAME         'i'
179	STORE_SUBSCR      None

180	LOAD_NAME         'i'
183	LOAD_CONST        1
186	INPLACE_ADD       None
187	STORE_NAME        'i'
190	JUMP_BACK         '158'
193	POP_BLOCK         None
194_0	COME_FROM         '155'

Syntax error at or near `POP_BLOCK' token at offset 193

