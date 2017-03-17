# Embedded file name: scripts/common/Lib/test/test_mutants.py
from test.test_support import verbose, TESTFN
import random
import os
dict1 = {}
dict2 = {}
dict1keys = []
dict2keys = []
mutate = 0

def maybe_mutate--- This code section failed: ---

0	LOAD_GLOBAL       'mutate'
3	POP_JUMP_IF_TRUE  '10'

6	LOAD_CONST        None
9	RETURN_END_IF     None

10	LOAD_GLOBAL       'random'
13	LOAD_ATTR         'random'
16	CALL_FUNCTION_0   None
19	LOAD_CONST        0.5
22	COMPARE_OP        '<'
25	POP_JUMP_IF_FALSE '32'

28	LOAD_CONST        None
31	RETURN_END_IF     None

32	LOAD_GLOBAL       'random'
35	LOAD_ATTR         'random'
38	CALL_FUNCTION_0   None
41	LOAD_CONST        0.5
44	COMPARE_OP        '<'
47	POP_JUMP_IF_FALSE '66'

50	LOAD_GLOBAL       'dict1'
53	LOAD_GLOBAL       'dict1keys'
56	ROT_TWO           None
57	STORE_FAST        'target'
60	STORE_FAST        'keys'
63	JUMP_FORWARD      '79'

66	LOAD_GLOBAL       'dict2'
69	LOAD_GLOBAL       'dict2keys'
72	ROT_TWO           None
73	STORE_FAST        'target'
76	STORE_FAST        'keys'
79_0	COME_FROM         '63'

79	LOAD_GLOBAL       'random'
82	LOAD_ATTR         'random'
85	CALL_FUNCTION_0   None
88	LOAD_CONST        0.2
91	COMPARE_OP        '<'
94	POP_JUMP_IF_FALSE '194'

97	LOAD_CONST        0
100	STORE_GLOBAL      'mutate'

103	SETUP_LOOP        '147'

106	LOAD_GLOBAL       'Horrid'
109	LOAD_GLOBAL       'random'
112	LOAD_ATTR         'randrange'
115	LOAD_CONST        100
118	CALL_FUNCTION_1   None
121	CALL_FUNCTION_1   None
124	STORE_FAST        'newkey'

127	LOAD_FAST         'newkey'
130	LOAD_FAST         'target'
133	COMPARE_OP        'not in'
136	POP_JUMP_IF_FALSE '106'

139	BREAK_LOOP        None
140	JUMP_BACK         '106'
143	JUMP_BACK         '106'
146	POP_BLOCK         None
147_0	COME_FROM         '103'

147	LOAD_GLOBAL       'Horrid'
150	LOAD_GLOBAL       'random'
153	LOAD_ATTR         'randrange'
156	LOAD_CONST        100
159	CALL_FUNCTION_1   None
162	CALL_FUNCTION_1   None
165	LOAD_FAST         'target'
168	LOAD_FAST         'newkey'
171	STORE_SUBSCR      None

172	LOAD_FAST         'keys'
175	LOAD_ATTR         'append'
178	LOAD_FAST         'newkey'
181	CALL_FUNCTION_1   None
184	POP_TOP           None

185	LOAD_CONST        1
188	STORE_GLOBAL      'mutate'
191	JUMP_FORWARD      '260'

194	LOAD_FAST         'keys'
197	POP_JUMP_IF_FALSE '260'

200	LOAD_CONST        0
203	STORE_GLOBAL      'mutate'

206	LOAD_GLOBAL       'random'
209	LOAD_ATTR         'randrange'
212	LOAD_GLOBAL       'len'
215	LOAD_FAST         'keys'
218	CALL_FUNCTION_1   None
221	CALL_FUNCTION_1   None
224	STORE_FAST        'i'

227	LOAD_FAST         'keys'
230	LOAD_FAST         'i'
233	BINARY_SUBSCR     None
234	STORE_FAST        'key'

237	LOAD_FAST         'target'
240	LOAD_FAST         'key'
243	DELETE_SUBSCR     None

244	LOAD_FAST         'keys'
247	LOAD_FAST         'i'
250	DELETE_SUBSCR     None

251	LOAD_CONST        1
254	STORE_GLOBAL      'mutate'
257	JUMP_FORWARD      '260'
260_0	COME_FROM         '191'
260_1	COME_FROM         '257'

Syntax error at or near `POP_BLOCK' token at offset 146


class Horrid:

    def __init__(self, i):
        self.i = i
        self.hashcode = random.randrange(1000000000)

    def __hash__(self):
        return 42
        return self.hashcode

    def __cmp__(self, other):
        maybe_mutate()
        return cmp(self.i, other.i)

    def __eq__(self, other):
        maybe_mutate()
        return self.i == other.i

    def __repr__(self):
        return 'Horrid(%d)' % self.i


def fill_dict(d, candidates, numentries):
    d.clear()
    for i in xrange(numentries):
        d[Horrid(random.choice(candidates))] = Horrid(random.choice(candidates))

    return d.keys()


def test_one(n):
    global mutate
    global dict1
    global dict2keys
    global dict2
    global dict1keys
    mutate = 0
    dict1keys = fill_dict(dict1, range(n), n)
    dict2keys = fill_dict(dict2, range(n), n)
    mutate = 1
    if verbose:
        print 'trying w/ lengths', len(dict1), len(dict2),
    while dict1 and len(dict1) == len(dict2):
        if verbose:
            print '.',
        if random.random() < 0.5:
            c = cmp(dict1, dict2)
        else:
            c = dict1 == dict2

    if verbose:
        print


def test(n):
    for i in xrange(n):
        test_one(random.randrange(1, 100))


test(100)

class Child:

    def __init__(self, parent):
        self.__dict__['parent'] = parent

    def __getattr__(self, attr):
        self.parent.a = 1
        self.parent.b = 1
        self.parent.c = 1
        self.parent.d = 1
        self.parent.e = 1
        self.parent.f = 1
        self.parent.g = 1
        self.parent.h = 1
        self.parent.i = 1
        return getattr(self.parent, attr)


class Parent:

    def __init__(self):
        self.a = Child(self)


f = open(TESTFN, 'w')
print >> f, Parent().__dict__
f.close()
os.unlink(TESTFN)
dict = {}
for i in range(1, 10):
    dict[i] = i

f = open(TESTFN, 'w')

class Machiavelli:

    def __repr__(self):
        dict.clear()
        print >> f
        return repr('machiavelli')

    def __hash__(self):
        return 0


dict[Machiavelli()] = Machiavelli()
print >> f, str(dict)
f.close()
os.unlink(TESTFN)
del f
del dict
dict = {}
for i in range(1, 10):
    dict[i] = i

class Machiavelli2:

    def __eq__(self, other):
        dict.clear()
        return 1

    def __hash__(self):
        return 0


dict[Machiavelli2()] = Machiavelli2()
try:
    dict[Machiavelli2()]
except KeyError:
    pass

del dict
dict = {}
for i in range(1, 10):
    dict[i] = i

class Machiavelli3:

    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        if self.id == other.id:
            dict.clear()
            return 1
        else:
            return 0

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.id)

    def __hash__(self):
        return 0


dict[Machiavelli3(1)] = Machiavelli3(0)
dict[Machiavelli3(2)] = Machiavelli3(0)
f = open(TESTFN, 'w')
try:
    print >> f, dict[Machiavelli3(2)]
except KeyError:
    pass
finally:
    f.close()
    os.unlink(TESTFN)

del dict
del dict1
del dict2
del dict1keys
del dict2keys