# Embedded file name: scripts/common/Lib/plat-irix6/flp.py
from warnings import warnpy3k
warnpy3k('the flp module has been removed in Python 3.0', stacklevel=2)
del warnpy3k
import os
import sys
import FL
SPLITLINE = '--------------------'
FORMLINE = '=============== FORM ==============='
ENDLINE = '=============================='

class error(Exception):
    pass


def parse_form(filename, formname):
    forms = checkcache(filename)
    if forms is None:
        forms = parse_forms(filename)
    if forms.has_key(formname):
        return forms[formname]
    else:
        raise error, 'No such form in fd file'
        return


def parse_forms(filename):
    forms = checkcache(filename)
    if forms is not None:
        return forms
    else:
        fp = _open_formfile(filename)
        nforms = _parse_fd_header(fp)
        forms = {}
        for i in range(nforms):
            form = _parse_fd_form(fp, None)
            forms[form[0].Name] = form

        writecache(filename, forms)
        return forms


MAGIC = '.fdc'
_internal_cache = {}

def checkcache(filename):
    if _internal_cache.has_key(filename):
        altforms = _internal_cache[filename]
        return _unpack_cache(altforms)
    else:
        import marshal
        fp, filename = _open_formfile2(filename)
        fp.close()
        cachename = filename + 'c'
        try:
            fp = open(cachename, 'r')
        except IOError:
            return

        try:
            if fp.read(4) != MAGIC:
                print 'flp: bad magic word in cache file', cachename
                return
            cache_mtime = rdlong(fp)
            file_mtime = getmtime(filename)
            if cache_mtime != file_mtime:
                return
            altforms = marshal.load(fp)
            return _unpack_cache(altforms)
        finally:
            fp.close()

        return


def _unpack_cache(altforms):
    forms = {}
    for name in altforms.keys():
        altobj, altlist = altforms[name]
        obj = _newobj()
        obj.make(altobj)
        list = []
        for altobj in altlist:
            nobj = _newobj()
            nobj.make(altobj)
            list.append(nobj)

        forms[name] = (obj, list)

    return forms


def rdlong(fp):
    s = fp.read(4)
    if len(s) != 4:
        return None
    else:
        a, b, c, d = (s[0],
         s[1],
         s[2],
         s[3])
        return ord(a) << 24 | ord(b) << 16 | ord(c) << 8 | ord(d)


def wrlong(fp, x):
    a, b, c, d = (x >> 24 & 255,
     x >> 16 & 255,
     x >> 8 & 255,
     x & 255)
    fp.write(chr(a) + chr(b) + chr(c) + chr(d))


def getmtime(filename):
    import os
    from stat import ST_MTIME
    try:
        return os.stat(filename)[ST_MTIME]
    except os.error:
        return

    return


def writecache(filename, forms):
    import marshal
    fp, filename = _open_formfile2(filename)
    fp.close()
    cachename = filename + 'c'
    try:
        fp = open(cachename, 'w')
    except IOError:
        print "flp: can't create cache file", cachename
        return

    fp.write('\x00\x00\x00\x00')
    wrlong(fp, getmtime(filename))
    altforms = _pack_cache(forms)
    marshal.dump(altforms, fp)
    fp.seek(0)
    fp.write(MAGIC)
    fp.close()


def freeze(filename):
    forms = parse_forms(filename)
    altforms = _pack_cache(forms)
    print 'import flp'
    print 'flp._internal_cache[', repr(filename), '] =', altforms


def _pack_cache(forms):
    altforms = {}
    for name in forms.keys():
        obj, list = forms[name]
        altobj = obj.__dict__
        altlist = []
        for obj in list:
            altlist.append(obj.__dict__)

        altforms[name] = (altobj, altlist)

    return altforms


def _open_formfile(filename):
    return _open_formfile2(filename)[0]


def _open_formfile2(filename):
    if filename[-3:] != '.fd':
        filename = filename + '.fd'
    if filename[0] == '/':
        try:
            fp = open(filename, 'r')
        except IOError:
            fp = None

    else:
        for pc in sys.path:
            pn = os.path.join(pc, filename)
            try:
                fp = open(pn, 'r')
                filename = pn
                break
            except IOError:
                fp = None

    if fp is None:
        raise error, 'Cannot find forms file ' + filename
    return (fp, filename)


def _parse_fd_header--- This code section failed: ---

0	LOAD_GLOBAL       '_parse_1_line'
3	LOAD_FAST         'file'
6	CALL_FUNCTION_1   None
9	STORE_FAST        'datum'

12	LOAD_FAST         'datum'
15	LOAD_CONST        ('Magic', 12321)
18	COMPARE_OP        '!='
21	POP_JUMP_IF_FALSE '36'

24	LOAD_GLOBAL       'error'
27	LOAD_CONST        'Not a forms definition file'
30	RAISE_VARARGS_2   None
33	JUMP_FORWARD      '36'
36_0	COME_FROM         '33'

36	SETUP_LOOP        '99'

39	LOAD_GLOBAL       '_parse_1_line'
42	LOAD_FAST         'file'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'datum'

51	LOAD_GLOBAL       'type'
54	LOAD_FAST         'datum'
57	CALL_FUNCTION_1   None
60	LOAD_GLOBAL       'type'
63	LOAD_CONST        ()
66	CALL_FUNCTION_1   None
69	COMPARE_OP        '=='
72	POP_JUMP_IF_FALSE '39'
75	LOAD_FAST         'datum'
78	LOAD_CONST        0
81	BINARY_SUBSCR     None
82	LOAD_CONST        'Numberofforms'
85	COMPARE_OP        '=='
88_0	COME_FROM         '72'
88	POP_JUMP_IF_FALSE '39'

91	BREAK_LOOP        None
92	JUMP_BACK         '39'
95	JUMP_BACK         '39'
98	POP_BLOCK         None
99_0	COME_FROM         '36'

99	LOAD_FAST         'datum'
102	LOAD_CONST        1
105	BINARY_SUBSCR     None
106	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 98


def _parse_fd_form(file, name):
    datum = _parse_1_line(file)
    if datum != FORMLINE:
        raise error, 'Missing === FORM === line'
    form = _parse_object(file)
    if form.Name == name or name is None:
        objs = []
        for j in range(form.Numberofobjects):
            obj = _parse_object(file)
            objs.append(obj)

        return (form, objs)
    else:
        for j in range(form.Numberofobjects):
            _skip_object(file)

        return


class _newobj:

    def add(self, name, value):
        self.__dict__[name] = value

    def make(self, dict):
        for name in dict.keys():
            self.add(name, dict[name])


def _parse_string(str):
    if '\\' in str:
        s = "'" + str + "'"
        try:
            return eval(s)
        except:
            pass

    return str


def _parse_num(str):
    return eval(str)


def _parse_numlist(str):
    slist = str.split()
    nlist = []
    for i in slist:
        nlist.append(_parse_num(i))

    return nlist


_parse_func = {'Name': _parse_string,
 'Box': _parse_numlist,
 'Colors': _parse_numlist,
 'Label': _parse_string,
 'Name': _parse_string,
 'Callback': _parse_string,
 'Argument': _parse_string}
import re
prog = re.compile('^([^:]*): *(.*)')

def _parse_line(line):
    match = prog.match(line)
    if not match:
        return line
    name, value = match.group(1, 2)
    if name[0] == 'N':
        name = ''.join(name.split())
        name = name.lower()
    name = name.capitalize()
    try:
        pf = _parse_func[name]
    except KeyError:
        pf = _parse_num

    value = pf(value)
    return (name, value)


def _readline(file):
    line = file.readline()
    if not line:
        raise EOFError
    return line[:-1]


def _parse_1_line(file):
    line = _readline(file)
    while line == '':
        line = _readline(file)

    return _parse_line(line)


def _skip_object(file):
    line = ''
    while line not in (SPLITLINE, FORMLINE, ENDLINE):
        pos = file.tell()
        line = _readline(file)

    if line == FORMLINE:
        file.seek(pos)


def _parse_object--- This code section failed: ---

0	LOAD_GLOBAL       '_newobj'
3	CALL_FUNCTION_0   None
6	STORE_FAST        'obj'

9	SETUP_LOOP        '175'

12	LOAD_FAST         'file'
15	LOAD_ATTR         'tell'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'pos'

24	LOAD_GLOBAL       '_parse_1_line'
27	LOAD_FAST         'file'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'datum'

36	LOAD_FAST         'datum'
39	LOAD_GLOBAL       'SPLITLINE'
42	LOAD_GLOBAL       'FORMLINE'
45	LOAD_GLOBAL       'ENDLINE'
48	BUILD_TUPLE_3     None
51	COMPARE_OP        'in'
54	POP_JUMP_IF_FALSE '89'

57	LOAD_FAST         'datum'
60	LOAD_GLOBAL       'FORMLINE'
63	COMPARE_OP        '=='
66	POP_JUMP_IF_FALSE '85'

69	LOAD_FAST         'file'
72	LOAD_ATTR         'seek'
75	LOAD_FAST         'pos'
78	CALL_FUNCTION_1   None
81	POP_TOP           None
82	JUMP_FORWARD      '85'
85_0	COME_FROM         '82'

85	LOAD_FAST         'obj'
88	RETURN_END_IF     None

89	LOAD_GLOBAL       'type'
92	LOAD_FAST         'datum'
95	CALL_FUNCTION_1   None
98	LOAD_GLOBAL       'type'
101	LOAD_CONST        ()
104	CALL_FUNCTION_1   None
107	COMPARE_OP        'is not'
110	POP_JUMP_IF_TRUE  '131'
113	LOAD_GLOBAL       'len'
116	LOAD_FAST         'datum'
119	CALL_FUNCTION_1   None
122	LOAD_CONST        2
125	COMPARE_OP        '!='
128_0	COME_FROM         '110'
128	POP_JUMP_IF_FALSE '147'

131	LOAD_GLOBAL       'error'
134	LOAD_CONST        'Parse error, illegal line in object: '
137	LOAD_FAST         'datum'
140	BINARY_ADD        None
141	RAISE_VARARGS_2   None
144	JUMP_FORWARD      '147'
147_0	COME_FROM         '144'

147	LOAD_FAST         'obj'
150	LOAD_ATTR         'add'
153	LOAD_FAST         'datum'
156	LOAD_CONST        0
159	BINARY_SUBSCR     None
160	LOAD_FAST         'datum'
163	LOAD_CONST        1
166	BINARY_SUBSCR     None
167	CALL_FUNCTION_2   None
170	POP_TOP           None
171	JUMP_BACK         '12'
174	POP_BLOCK         None
175_0	COME_FROM         '9'

Syntax error at or near `POP_BLOCK' token at offset 174


def create_full_form(inst, (fdata, odatalist)):
    form = create_form(fdata)
    exec 'inst.' + fdata.Name + ' = form\n'
    for odata in odatalist:
        create_object_instance(inst, form, odata)


def merge_full_form(inst, form, (fdata, odatalist)):
    exec 'inst.' + fdata.Name + ' = form\n'
    if odatalist[0].Class != FL.BOX:
        raise error, 'merge_full_form() expects FL.BOX as first obj'
    for odata in odatalist[1:]:
        create_object_instance(inst, form, odata)


def create_form(fdata):
    import fl
    return fl.make_form(FL.NO_BOX, fdata.Width, fdata.Height)


def create_object(form, odata):
    obj = _create_object(form, odata)
    if odata.Callback:
        raise error, 'Creating free object with callback'
    return obj


def create_object_instance(inst, form, odata):
    obj = _create_object(form, odata)
    if odata.Callback:
        cbfunc = eval('inst.' + odata.Callback)
        obj.set_call_back(cbfunc, odata.Argument)
    if odata.Name:
        exec 'inst.' + odata.Name + ' = obj\n'


def _create_object(form, odata):
    crfunc = _select_crfunc(form, odata.Class)
    obj = crfunc(odata.Type, odata.Box[0], odata.Box[1], odata.Box[2], odata.Box[3], odata.Label)
    if odata.Class not in (FL.BEGIN_GROUP, FL.END_GROUP):
        obj.boxtype = odata.Boxtype
        obj.col1 = odata.Colors[0]
        obj.col2 = odata.Colors[1]
        obj.align = odata.Alignment
        obj.lstyle = odata.Style
        obj.lsize = odata.Size
        obj.lcol = odata.Lcol
    return obj


def _select_crfunc(fm, cl):
    if cl == FL.BEGIN_GROUP:
        return fm.bgn_group
    if cl == FL.END_GROUP:
        return fm.end_group
    if cl == FL.BITMAP:
        return fm.add_bitmap
    if cl == FL.BOX:
        return fm.add_box
    if cl == FL.BROWSER:
        return fm.add_browser
    if cl == FL.BUTTON:
        return fm.add_button
    if cl == FL.CHART:
        return fm.add_chart
    if cl == FL.CHOICE:
        return fm.add_choice
    if cl == FL.CLOCK:
        return fm.add_clock
    if cl == FL.COUNTER:
        return fm.add_counter
    if cl == FL.DIAL:
        return fm.add_dial
    if cl == FL.FREE:
        return fm.add_free
    if cl == FL.INPUT:
        return fm.add_input
    if cl == FL.LIGHTBUTTON:
        return fm.add_lightbutton
    if cl == FL.MENU:
        return fm.add_menu
    if cl == FL.POSITIONER:
        return fm.add_positioner
    if cl == FL.ROUNDBUTTON:
        return fm.add_roundbutton
    if cl == FL.SLIDER:
        return fm.add_slider
    if cl == FL.VALSLIDER:
        return fm.add_valslider
    if cl == FL.TEXT:
        return fm.add_text
    if cl == FL.TIMER:
        return fm.add_timer
    raise error, 'Unknown object type: %r' % (cl,)


def test():
    import time
    t0 = time.time()
    if len(sys.argv) == 2:
        forms = parse_forms(sys.argv[1])
        t1 = time.time()
        print 'parse time:', 0.001 * (t1 - t0), 'sec.'
        keys = forms.keys()
        keys.sort()
        for i in keys:
            _printform(forms[i])

    elif len(sys.argv) == 3:
        form = parse_form(sys.argv[1], sys.argv[2])
        t1 = time.time()
        print 'parse time:', round(t1 - t0, 3), 'sec.'
        _printform(form)
    else:
        print 'Usage: test fdfile [form]'


def _printform(form):
    f = form[0]
    objs = form[1]
    print 'Form ', f.Name, ', size: ', f.Width, f.Height, ' Nobj ', f.Numberofobjects
    for i in objs:
        print '  Obj ', i.Name, ' type ', i.Class, i.Type
        print '    Box ', i.Box, ' btype ', i.Boxtype
        print '    Label ', i.Label, ' size/style/col/align ', i.Size, i.Style, i.Lcol, i.Alignment
        print '    cols ', i.Colors
        print '    cback ', i.Callback, i.Argument