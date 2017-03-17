# Embedded file name: scripts/common/Lib/mailcap.py
"""Mailcap file handling.  See RFC 1524."""
import os
__all__ = ['getcaps', 'findmatch']

def getcaps():
    """Return a dictionary containing the mailcap database.
    
    The dictionary maps a MIME type (in all lowercase, e.g. 'text/plain')
    to a list of dictionaries corresponding to mailcap entries.  The list
    collects all the entries for that MIME type from all available mailcap
    files.  Each dictionary contains key-value pairs for that MIME type,
    where the viewing command is stored with the key "view".
    
    """
    caps = {}
    for mailcap in listmailcapfiles():
        try:
            fp = open(mailcap, 'r')
        except IOError:
            continue

        morecaps = readmailcapfile(fp)
        fp.close()
        for key, value in morecaps.iteritems():
            if key not in caps:
                caps[key] = value
            else:
                caps[key] = caps[key] + value

    return caps


def listmailcapfiles():
    """Return a list of all mailcap files found on the system."""
    if 'MAILCAPS' in os.environ:
        str = os.environ['MAILCAPS']
        mailcaps = str.split(':')
    else:
        if 'HOME' in os.environ:
            home = os.environ['HOME']
        else:
            home = '.'
        mailcaps = [home + '/.mailcap',
         '/etc/mailcap',
         '/usr/etc/mailcap',
         '/usr/local/etc/mailcap']
    return mailcaps


def readmailcapfile--- This code section failed: ---

0	BUILD_MAP         None
3	STORE_FAST        'caps'

6	SETUP_LOOP        '311'

9	LOAD_FAST         'fp'
12	LOAD_ATTR         'readline'
15	CALL_FUNCTION_0   None
18	STORE_FAST        'line'

21	LOAD_FAST         'line'
24	POP_JUMP_IF_TRUE  '31'
27	BREAK_LOOP        None
28	JUMP_FORWARD      '31'
31_0	COME_FROM         '28'

31	LOAD_FAST         'line'
34	LOAD_CONST        0
37	BINARY_SUBSCR     None
38	LOAD_CONST        '#'
41	COMPARE_OP        '=='
44	POP_JUMP_IF_TRUE  '9'
47	LOAD_FAST         'line'
50	LOAD_ATTR         'strip'
53	CALL_FUNCTION_0   None
56	LOAD_CONST        ''
59	COMPARE_OP        '=='
62_0	COME_FROM         '44'
62	POP_JUMP_IF_FALSE '71'

65	CONTINUE          '9'
68	JUMP_FORWARD      '71'
71_0	COME_FROM         '68'

71	LOAD_FAST         'line'
74	STORE_FAST        'nextline'

77	SETUP_LOOP        '141'
80	LOAD_FAST         'nextline'
83	LOAD_CONST        -2
86	SLICE+1           None
87	LOAD_CONST        '\\\n'
90	COMPARE_OP        '=='
93	POP_JUMP_IF_FALSE '140'

96	LOAD_FAST         'fp'
99	LOAD_ATTR         'readline'
102	CALL_FUNCTION_0   None
105	STORE_FAST        'nextline'

108	LOAD_FAST         'nextline'
111	POP_JUMP_IF_TRUE  '123'
114	LOAD_CONST        '\n'
117	STORE_FAST        'nextline'
120	JUMP_FORWARD      '123'
123_0	COME_FROM         '120'

123	LOAD_FAST         'line'
126	LOAD_CONST        -2
129	SLICE+2           None
130	LOAD_FAST         'nextline'
133	BINARY_ADD        None
134	STORE_FAST        'line'
137	JUMP_BACK         '80'
140	POP_BLOCK         None
141_0	COME_FROM         '77'

141	LOAD_GLOBAL       'parseline'
144	LOAD_FAST         'line'
147	CALL_FUNCTION_1   None
150	UNPACK_SEQUENCE_2 None
153	STORE_FAST        'key'
156	STORE_FAST        'fields'

159	LOAD_FAST         'key'
162	JUMP_IF_FALSE_OR_POP '168'
165	LOAD_FAST         'fields'
168_0	COME_FROM         '162'
168	POP_JUMP_IF_TRUE  '177'

171	CONTINUE          '9'
174	JUMP_FORWARD      '177'
177_0	COME_FROM         '174'

177	LOAD_FAST         'key'
180	LOAD_ATTR         'split'
183	LOAD_CONST        '/'
186	CALL_FUNCTION_1   None
189	STORE_FAST        'types'

192	SETUP_LOOP        '241'
195	LOAD_GLOBAL       'range'
198	LOAD_GLOBAL       'len'
201	LOAD_FAST         'types'
204	CALL_FUNCTION_1   None
207	CALL_FUNCTION_1   None
210	GET_ITER          None
211	FOR_ITER          '240'
214	STORE_FAST        'j'

217	LOAD_FAST         'types'
220	LOAD_FAST         'j'
223	BINARY_SUBSCR     None
224	LOAD_ATTR         'strip'
227	CALL_FUNCTION_0   None
230	LOAD_FAST         'types'
233	LOAD_FAST         'j'
236	STORE_SUBSCR      None
237	JUMP_BACK         '211'
240	POP_BLOCK         None
241_0	COME_FROM         '192'

241	LOAD_CONST        '/'
244	LOAD_ATTR         'join'
247	LOAD_FAST         'types'
250	CALL_FUNCTION_1   None
253	LOAD_ATTR         'lower'
256	CALL_FUNCTION_0   None
259	STORE_FAST        'key'

262	LOAD_FAST         'key'
265	LOAD_FAST         'caps'
268	COMPARE_OP        'in'
271	POP_JUMP_IF_FALSE '294'

274	LOAD_FAST         'caps'
277	LOAD_FAST         'key'
280	BINARY_SUBSCR     None
281	LOAD_ATTR         'append'
284	LOAD_FAST         'fields'
287	CALL_FUNCTION_1   None
290	POP_TOP           None
291	JUMP_BACK         '9'

294	LOAD_FAST         'fields'
297	BUILD_LIST_1      None
300	LOAD_FAST         'caps'
303	LOAD_FAST         'key'
306	STORE_SUBSCR      None
307	JUMP_BACK         '9'
310	POP_BLOCK         None
311_0	COME_FROM         '6'

311	LOAD_FAST         'caps'
314	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 310


def parseline(line):
    """Parse one entry in a mailcap file and return a dictionary.
    
    The viewing command is stored as the value with the key "view",
    and the rest of the fields produce key-value pairs in the dict.
    """
    fields = []
    i, n = 0, len(line)
    while i < n:
        field, i = parsefield(line, i, n)
        fields.append(field)
        i = i + 1

    if len(fields) < 2:
        return (None, None)
    else:
        key, view, rest = fields[0], fields[1], fields[2:]
        fields = {'view': view}
        for field in rest:
            i = field.find('=')
            if i < 0:
                fkey = field
                fvalue = ''
            else:
                fkey = field[:i].strip()
                fvalue = field[i + 1:].strip()
            if fkey in fields:
                pass
            else:
                fields[fkey] = fvalue

        return (key, fields)


def parsefield(line, i, n):
    """Separate one key-value pair in a mailcap entry."""
    start = i
    while i < n:
        c = line[i]
        if c == ';':
            break
        elif c == '\\':
            i = i + 2
        else:
            i = i + 1

    return (line[start:i].strip(), i)


def findmatch(caps, MIMEtype, key = 'view', filename = '/dev/null', plist = []):
    """Find a match for a mailcap entry.
    
    Return a tuple containing the command line, and the mailcap entry
    used; (None, None) if no match is found.  This may invoke the
    'test' command of several matching entries before deciding which
    entry to use.
    
    """
    entries = lookup(caps, MIMEtype, key)
    for e in entries:
        if 'test' in e:
            test = subst(e['test'], filename, plist)
            if test and os.system(test) != 0:
                continue
        command = subst(e[key], MIMEtype, filename, plist)
        return (command, e)

    return (None, None)


def lookup(caps, MIMEtype, key = None):
    entries = []
    if MIMEtype in caps:
        entries = entries + caps[MIMEtype]
    MIMEtypes = MIMEtype.split('/')
    MIMEtype = MIMEtypes[0] + '/*'
    if MIMEtype in caps:
        entries = entries + caps[MIMEtype]
    if key is not None:
        entries = filter(lambda e, key = key: key in e, entries)
    return entries


def subst(field, MIMEtype, filename, plist = []):
    res = ''
    i, n = 0, len(field)
    while i < n:
        c = field[i]
        i = i + 1
        if c != '%':
            if c == '\\':
                c = field[i:i + 1]
                i = i + 1
            res = res + c
        else:
            c = field[i]
            i = i + 1
            if c == '%':
                res = res + c
            elif c == 's':
                res = res + filename
            elif c == 't':
                res = res + MIMEtype
            elif c == '{':
                start = i
                while i < n and field[i] != '}':
                    i = i + 1

                name = field[start:i]
                i = i + 1
                res = res + findparam(name, plist)
            else:
                res = res + '%' + c

    return res


def findparam(name, plist):
    name = name.lower() + '='
    n = len(name)
    for p in plist:
        if p[:n].lower() == name:
            return p[n:]

    return ''


def test():
    import sys
    caps = getcaps()
    if not sys.argv[1:]:
        show(caps)
        return
    for i in range(1, len(sys.argv), 2):
        args = sys.argv[i:i + 2]
        if len(args) < 2:
            print 'usage: mailcap [MIMEtype file] ...'
            return
        MIMEtype = args[0]
        file = args[1]
        command, e = findmatch(caps, MIMEtype, 'view', file)
        if not command:
            print 'No viewer found for', type
        else:
            print 'Executing:', command
            sts = os.system(command)
            if sts:
                print 'Exit status:', sts


def show(caps):
    print 'Mailcap files:'
    for fn in listmailcapfiles():
        print '\t' + fn

    print
    if not caps:
        caps = getcaps()
    print 'Mailcap entries:'
    print
    ckeys = caps.keys()
    ckeys.sort()
    for type in ckeys:
        print type
        entries = caps[type]
        for e in entries:
            keys = e.keys()
            keys.sort()
            for k in keys:
                print '  %-15s' % k, e[k]

            print


if __name__ == '__main__':
    test()