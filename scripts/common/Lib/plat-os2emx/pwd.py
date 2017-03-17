# Embedded file name: scripts/common/Lib/plat-os2emx/pwd.py
"""Replacement for pwd standard extension module, intended for use on
OS/2 and similar systems which don't normally have an /etc/passwd file.

The standard Unix password database is an ASCII text file with 7 fields
per record (line), separated by a colon:
  - user name (string)
  - password (encrypted string, or "*" or "")
  - user id (integer)
  - group id (integer)
  - description (usually user's name)
  - home directory (path to user's home directory)
  - shell (path to the user's login shell)

(see the section 8.1 of the Python Library Reference)

This implementation differs from the standard Unix implementation by
allowing use of the platform's native path separator character - ';' on OS/2,
DOS and MS-Windows - as the field separator in addition to the Unix
standard ":".  Additionally, when ":" is the separator path conversions
are applied to deal with any munging of the drive letter reference.

The module looks for the password database at the following locations
(in order first to last):
  - ${ETC_PASSWD}             (or %ETC_PASSWD%)
  - ${ETC}/passwd             (or %ETC%/passwd)
  - ${PYTHONHOME}/Etc/passwd  (or %PYTHONHOME%/Etc/passwd)

Classes
-------

None

Functions
---------

getpwuid(uid) -  return the record for user-id uid as a 7-tuple

getpwnam(name) - return the record for user 'name' as a 7-tuple

getpwall() -     return a list of 7-tuples, each tuple being one record
                 (NOTE: the order is arbitrary)

Attributes
----------

passwd_file -    the path of the password database file

"""
import os
__passwd_path = []
if os.environ.has_key('ETC_PASSWD'):
    __passwd_path.append(os.environ['ETC_PASSWD'])
if os.environ.has_key('ETC'):
    __passwd_path.append('%s/passwd' % os.environ['ETC'])
if os.environ.has_key('PYTHONHOME'):
    __passwd_path.append('%s/Etc/passwd' % os.environ['PYTHONHOME'])
passwd_file = None
for __i in __passwd_path:
    try:
        __f = open(__i, 'r')
        __f.close()
        passwd_file = __i
        break
    except:
        pass

def __nullpathconv(path):
    return path.replace(os.altsep, os.sep)


def __unixpathconv(path):
    if path[0] == '$':
        conv = path[1] + ':' + path[2:]
    elif path[1] == ';':
        conv = path[0] + ':' + path[2:]
    else:
        conv = path
    return conv.replace(os.altsep, os.sep)


__field_sep = {':': __unixpathconv}
if os.pathsep:
    if os.pathsep != ':':
        __field_sep[os.pathsep] = __nullpathconv

def __get_field_sep(record):
    fs = None
    for c in __field_sep.keys():
        if record.count(c) == 6:
            fs = c
            break

    if fs:
        return fs
    else:
        raise KeyError, '>> passwd database fields not delimited <<'
        return


class Passwd:

    def __init__(self, name, passwd, uid, gid, gecos, dir, shell):
        self.__dict__['pw_name'] = name
        self.__dict__['pw_passwd'] = passwd
        self.__dict__['pw_uid'] = uid
        self.__dict__['pw_gid'] = gid
        self.__dict__['pw_gecos'] = gecos
        self.__dict__['pw_dir'] = dir
        self.__dict__['pw_shell'] = shell
        self.__dict__['_record'] = (self.pw_name,
         self.pw_passwd,
         self.pw_uid,
         self.pw_gid,
         self.pw_gecos,
         self.pw_dir,
         self.pw_shell)

    def __len__(self):
        return 7

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


def __read_passwd_file--- This code section failed: ---

0	LOAD_GLOBAL       'passwd_file'
3	POP_JUMP_IF_FALSE '24'

6	LOAD_GLOBAL       'open'
9	LOAD_GLOBAL       'passwd_file'
12	LOAD_CONST        'r'
15	CALL_FUNCTION_2   None
18	STORE_FAST        'passwd'
21	JUMP_FORWARD      '33'

24	LOAD_GLOBAL       'KeyError'
27	LOAD_CONST        '>> no password database <<'
30	RAISE_VARARGS_2   None
33_0	COME_FROM         '21'

33	BUILD_MAP         None
36	STORE_FAST        'uidx'

39	BUILD_MAP         None
42	STORE_FAST        'namx'

45	LOAD_CONST        None
48	STORE_FAST        'sep'

51	SETUP_LOOP        '323'

54	LOAD_FAST         'passwd'
57	LOAD_ATTR         'readline'
60	CALL_FUNCTION_0   None
63	LOAD_ATTR         'strip'
66	CALL_FUNCTION_0   None
69	STORE_FAST        'entry'

72	LOAD_GLOBAL       'len'
75	LOAD_FAST         'entry'
78	CALL_FUNCTION_1   None
81	LOAD_CONST        6
84	COMPARE_OP        '>'
87	POP_JUMP_IF_FALSE '297'

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

132	SETUP_LOOP        '169'
135	LOAD_CONST        (2, 3)
138	GET_ITER          None
139	FOR_ITER          '168'
142	STORE_FAST        'i'

145	LOAD_GLOBAL       'int'
148	LOAD_FAST         'fields'
151	LOAD_FAST         'i'
154	BINARY_SUBSCR     None
155	CALL_FUNCTION_1   None
158	LOAD_FAST         'fields'
161	LOAD_FAST         'i'
164	STORE_SUBSCR      None
165	JUMP_BACK         '139'
168	POP_BLOCK         None
169_0	COME_FROM         '132'

169	SETUP_LOOP        '210'
172	LOAD_CONST        (5, 6)
175	GET_ITER          None
176	FOR_ITER          '209'
179	STORE_FAST        'i'

182	LOAD_GLOBAL       '__field_sep'
185	LOAD_FAST         'sep'
188	BINARY_SUBSCR     None
189	LOAD_FAST         'fields'
192	LOAD_FAST         'i'
195	BINARY_SUBSCR     None
196	CALL_FUNCTION_1   None
199	LOAD_FAST         'fields'
202	LOAD_FAST         'i'
205	STORE_SUBSCR      None
206	JUMP_BACK         '176'
209	POP_BLOCK         None
210_0	COME_FROM         '169'

210	LOAD_GLOBAL       'Passwd'
213	LOAD_FAST         'fields'
216	CALL_FUNCTION_VAR_0 None
219	STORE_FAST        'record'

222	LOAD_FAST         'uidx'
225	LOAD_ATTR         'has_key'
228	LOAD_FAST         'fields'
231	LOAD_CONST        2
234	BINARY_SUBSCR     None
235	CALL_FUNCTION_1   None
238	POP_JUMP_IF_TRUE  '258'

241	LOAD_FAST         'record'
244	LOAD_FAST         'uidx'
247	LOAD_FAST         'fields'
250	LOAD_CONST        2
253	BINARY_SUBSCR     None
254	STORE_SUBSCR      None
255	JUMP_FORWARD      '258'
258_0	COME_FROM         '255'

258	LOAD_FAST         'namx'
261	LOAD_ATTR         'has_key'
264	LOAD_FAST         'fields'
267	LOAD_CONST        0
270	BINARY_SUBSCR     None
271	CALL_FUNCTION_1   None
274	POP_JUMP_IF_TRUE  '319'

277	LOAD_FAST         'record'
280	LOAD_FAST         'namx'
283	LOAD_FAST         'fields'
286	LOAD_CONST        0
289	BINARY_SUBSCR     None
290	STORE_SUBSCR      None
291	JUMP_ABSOLUTE     '319'
294	JUMP_BACK         '54'

297	LOAD_GLOBAL       'len'
300	LOAD_FAST         'entry'
303	CALL_FUNCTION_1   None
306	LOAD_CONST        0
309	COMPARE_OP        '>'
312	POP_JUMP_IF_FALSE '318'

315	JUMP_BACK         '54'

318	BREAK_LOOP        None
319	JUMP_BACK         '54'
322	POP_BLOCK         None
323_0	COME_FROM         '51'

323	LOAD_FAST         'passwd'
326	LOAD_ATTR         'close'
329	CALL_FUNCTION_0   None
332	POP_TOP           None

333	LOAD_GLOBAL       'len'
336	LOAD_FAST         'uidx'
339	CALL_FUNCTION_1   None
342	LOAD_CONST        0
345	COMPARE_OP        '=='
348	POP_JUMP_IF_FALSE '360'

351	LOAD_GLOBAL       'KeyError'
354	RAISE_VARARGS_1   None
357	JUMP_FORWARD      '360'
360_0	COME_FROM         '357'

360	LOAD_FAST         'uidx'
363	LOAD_FAST         'namx'
366	BUILD_TUPLE_2     None
369	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 322


def getpwuid(uid):
    u, n = __read_passwd_file()
    return u[uid]


def getpwnam(name):
    u, n = __read_passwd_file()
    return n[name]


def getpwall():
    u, n = __read_passwd_file()
    return n.values()


if __name__ == '__main__':
    getpwall()