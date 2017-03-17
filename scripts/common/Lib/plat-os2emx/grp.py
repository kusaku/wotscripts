# Embedded file name: scripts/common/Lib/plat-os2emx/grp.py
"""Replacement for grp standard extension module, intended for use on
OS/2 and similar systems which don't normally have an /etc/group file.

The standard Unix group database is an ASCII text file with 4 fields per
record (line), separated by a colon:
  - group name (string)
  - group password (optional encrypted string)
  - group id (integer)
  - group members (comma delimited list of userids, with no spaces)

Note that members are only included in the group file for groups that
aren't their primary groups.
(see the section 8.2 of the Python Library Reference)

This implementation differs from the standard Unix implementation by
allowing use of the platform's native path separator character - ';' on OS/2,
DOS and MS-Windows - as the field separator in addition to the Unix
standard ":".

The module looks for the group database at the following locations
(in order first to last):
  - ${ETC_GROUP}              (or %ETC_GROUP%)
  - ${ETC}/group              (or %ETC%/group)
  - ${PYTHONHOME}/Etc/group   (or %PYTHONHOME%/Etc/group)

Classes
-------

None

Functions
---------

getgrgid(gid) -  return the record for group-id gid as a 4-tuple

getgrnam(name) - return the record for group 'name' as a 4-tuple

getgrall() -     return a list of 4-tuples, each tuple being one record
                 (NOTE: the order is arbitrary)

Attributes
----------

group_file -     the path of the group database file

"""
import os
__group_path = []
if os.environ.has_key('ETC_GROUP'):
    __group_path.append(os.environ['ETC_GROUP'])
if os.environ.has_key('ETC'):
    __group_path.append('%s/group' % os.environ['ETC'])
if os.environ.has_key('PYTHONHOME'):
    __group_path.append('%s/Etc/group' % os.environ['PYTHONHOME'])
group_file = None
for __i in __group_path:
    try:
        __f = open(__i, 'r')
        __f.close()
        group_file = __i
        break
    except:
        pass

__field_sep = [':']
if os.pathsep:
    if os.pathsep != ':':
        __field_sep.append(os.pathsep)

def __get_field_sep(record):
    fs = None
    for c in __field_sep:
        if record.count(c) == 3:
            fs = c
            break

    if fs:
        return fs
    else:
        raise KeyError, '>> group database fields not delimited <<'
        return


class Group:

    def __init__(self, name, passwd, gid, mem):
        self.__dict__['gr_name'] = name
        self.__dict__['gr_passwd'] = passwd
        self.__dict__['gr_gid'] = gid
        self.__dict__['gr_mem'] = mem
        self.__dict__['_record'] = (self.gr_name,
         self.gr_passwd,
         self.gr_gid,
         self.gr_mem)

    def __len__(self):
        return 4

    def __getitem__(self, key):
        return self._record[key]

    def __setattr__(self, name, value):
        raise AttributeError('attribute read-only: %s' % name)

    def __repr__(self):
        return str(self._record)

    def __cmp__(self, other):
        this = str(self._record)
        if this == other:
            return 0
        elif this < other:
            return -1
        else:
            return 1


def __read_group_file--- This code section failed: ---

0	LOAD_GLOBAL       'group_file'
3	POP_JUMP_IF_FALSE '24'

6	LOAD_GLOBAL       'open'
9	LOAD_GLOBAL       'group_file'
12	LOAD_CONST        'r'
15	CALL_FUNCTION_2   None
18	STORE_FAST        'group'
21	JUMP_FORWARD      '33'

24	LOAD_GLOBAL       'KeyError'
27	LOAD_CONST        '>> no group database <<'
30	RAISE_VARARGS_2   None
33_0	COME_FROM         '21'

33	BUILD_MAP         None
36	STORE_FAST        'gidx'

39	BUILD_MAP         None
42	STORE_FAST        'namx'

45	LOAD_CONST        None
48	STORE_FAST        'sep'

51	SETUP_LOOP        '313'

54	LOAD_FAST         'group'
57	LOAD_ATTR         'readline'
60	CALL_FUNCTION_0   None
63	LOAD_ATTR         'strip'
66	CALL_FUNCTION_0   None
69	STORE_FAST        'entry'

72	LOAD_GLOBAL       'len'
75	LOAD_FAST         'entry'
78	CALL_FUNCTION_1   None
81	LOAD_CONST        3
84	COMPARE_OP        '>'
87	POP_JUMP_IF_FALSE '287'

90	LOAD_FAST         'sep'
93	LOAD_CONST        None
96	COMPARE_OP        'is'
99	POP_JUMP_IF_FALSE '117'

102	LOAD_GLOBAL       '__get_field_sep'
105	LOAD_FAST         'entry'
108	CALL_FUNCTION_1   None
111	STORE_FAST        'sep'
114	JUMP_FORWARD      '117'
117_0	COME_FROM         '114'

117	LOAD_FAST         'entry'
120	LOAD_ATTR         'split'
123	LOAD_FAST         'sep'
126	CALL_FUNCTION_1   None
129	STORE_FAST        'fields'

132	LOAD_GLOBAL       'int'
135	LOAD_FAST         'fields'
138	LOAD_CONST        2
141	BINARY_SUBSCR     None
142	CALL_FUNCTION_1   None
145	LOAD_FAST         'fields'
148	LOAD_CONST        2
151	STORE_SUBSCR      None

152	BUILD_LIST_0      None
155	LOAD_FAST         'fields'
158	LOAD_CONST        3
161	BINARY_SUBSCR     None
162	LOAD_ATTR         'split'
165	LOAD_CONST        ','
168	CALL_FUNCTION_1   None
171	GET_ITER          None
172	FOR_ITER          '193'
175	STORE_FAST        'f'
178	LOAD_FAST         'f'
181	LOAD_ATTR         'strip'
184	CALL_FUNCTION_0   None
187	LIST_APPEND       None
190	JUMP_BACK         '172'
193	LOAD_FAST         'fields'
196	LOAD_CONST        3
199	STORE_SUBSCR      None

200	LOAD_GLOBAL       'Group'
203	LOAD_FAST         'fields'
206	CALL_FUNCTION_VAR_0 None
209	STORE_FAST        'record'

212	LOAD_FAST         'gidx'
215	LOAD_ATTR         'has_key'
218	LOAD_FAST         'fields'
221	LOAD_CONST        2
224	BINARY_SUBSCR     None
225	CALL_FUNCTION_1   None
228	POP_JUMP_IF_TRUE  '248'

231	LOAD_FAST         'record'
234	LOAD_FAST         'gidx'
237	LOAD_FAST         'fields'
240	LOAD_CONST        2
243	BINARY_SUBSCR     None
244	STORE_SUBSCR      None
245	JUMP_FORWARD      '248'
248_0	COME_FROM         '245'

248	LOAD_FAST         'namx'
251	LOAD_ATTR         'has_key'
254	LOAD_FAST         'fields'
257	LOAD_CONST        0
260	BINARY_SUBSCR     None
261	CALL_FUNCTION_1   None
264	POP_JUMP_IF_TRUE  '309'

267	LOAD_FAST         'record'
270	LOAD_FAST         'namx'
273	LOAD_FAST         'fields'
276	LOAD_CONST        0
279	BINARY_SUBSCR     None
280	STORE_SUBSCR      None
281	JUMP_ABSOLUTE     '309'
284	JUMP_BACK         '54'

287	LOAD_GLOBAL       'len'
290	LOAD_FAST         'entry'
293	CALL_FUNCTION_1   None
296	LOAD_CONST        0
299	COMPARE_OP        '>'
302	POP_JUMP_IF_FALSE '308'

305	JUMP_BACK         '54'

308	BREAK_LOOP        None
309	JUMP_BACK         '54'
312	POP_BLOCK         None
313_0	COME_FROM         '51'

313	LOAD_FAST         'group'
316	LOAD_ATTR         'close'
319	CALL_FUNCTION_0   None
322	POP_TOP           None

323	LOAD_GLOBAL       'len'
326	LOAD_FAST         'gidx'
329	CALL_FUNCTION_1   None
332	LOAD_CONST        0
335	COMPARE_OP        '=='
338	POP_JUMP_IF_FALSE '350'

341	LOAD_GLOBAL       'KeyError'
344	RAISE_VARARGS_1   None
347	JUMP_FORWARD      '350'
350_0	COME_FROM         '347'

350	LOAD_FAST         'gidx'
353	LOAD_FAST         'namx'
356	BUILD_TUPLE_2     None
359	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 312


def getgrgid(gid):
    g, n = __read_group_file()
    return g[gid]


def getgrnam(name):
    g, n = __read_group_file()
    return n[name]


def getgrall():
    g, n = __read_group_file()
    return g.values()


if __name__ == '__main__':
    getgrall()