# Embedded file name: scripts/common/Lib/msilib/__init__.py
from _msi import *
import os, string, re, sys
AMD64 = 'AMD64' in sys.version
Itanium = 'Itanium' in sys.version
Win64 = AMD64 or Itanium
datasizemask = 255
type_valid = 256
type_localizable = 512
typemask = 3072
type_long = 0
type_short = 1024
type_string = 3072
type_binary = 2048
type_nullable = 4096
type_key = 8192
knownbits = datasizemask | type_valid | type_localizable | typemask | type_nullable | type_key

class Table:

    def __init__(self, name):
        self.name = name
        self.fields = []

    def add_field(self, index, name, type):
        self.fields.append((index, name, type))

    def sql(self):
        fields = []
        keys = []
        self.fields.sort()
        fields = [None] * len(self.fields)
        for index, name, type in self.fields:
            index -= 1
            unk = type & ~knownbits
            if unk:
                print '%s.%s unknown bits %x' % (self.name, name, unk)
            size = type & datasizemask
            dtype = type & typemask
            if dtype == type_string:
                if size:
                    tname = 'CHAR(%d)' % size
                else:
                    tname = 'CHAR'
            elif not (dtype == type_short and size == 2):
                raise AssertionError
                tname = 'SHORT'
            elif not (dtype == type_long and size == 4):
                raise AssertionError
                tname = 'LONG'
            elif not (dtype == type_binary and size == 0):
                raise AssertionError
                tname = 'OBJECT'
            else:
                tname = 'unknown'
                print '%s.%sunknown integer type %d' % (self.name, name, size)
            if type & type_nullable:
                flags = ''
            else:
                flags = ' NOT NULL'
            if type & type_localizable:
                flags += ' LOCALIZABLE'
            fields[index] = '`%s` %s%s' % (name, tname, flags)
            if type & type_key:
                keys.append('`%s`' % name)

        fields = ', '.join(fields)
        keys = ', '.join(keys)
        return 'CREATE TABLE %s (%s PRIMARY KEY %s)' % (self.name, fields, keys)

    def create(self, db):
        v = db.OpenView(self.sql())
        v.Execute(None)
        v.Close()
        return


class _Unspecified:
    pass


def change_sequence(seq, action, seqno = _Unspecified, cond = _Unspecified):
    """Change the sequence number of an action in a sequence list"""
    for i in range(len(seq)):
        if seq[i][0] == action:
            if cond is _Unspecified:
                cond = seq[i][1]
            if seqno is _Unspecified:
                seqno = seq[i][2]
            seq[i] = (action, cond, seqno)
            return

    raise ValueError, 'Action not found in sequence'


def add_data(db, table, values):
    v = db.OpenView('SELECT * FROM `%s`' % table)
    count = v.GetColumnInfo(MSICOLINFO_NAMES).GetFieldCount()
    r = CreateRecord(count)
    for value in values:
        raise len(value) == count or AssertionError(value)
        for i in range(count):
            field = value[i]
            if isinstance(field, (int, long)):
                r.SetInteger(i + 1, field)
            elif isinstance(field, basestring):
                r.SetString(i + 1, field)
            elif field is None:
                pass
            elif isinstance(field, Binary):
                r.SetStream(i + 1, field.name)
            else:
                raise TypeError, 'Unsupported type %s' % field.__class__.__name__

        try:
            v.Modify(MSIMODIFY_INSERT, r)
        except Exception as e:
            raise MSIError('Could not insert ' + repr(values) + ' into ' + table)

        r.ClearData()

    v.Close()
    return


def add_stream(db, name, path):
    v = db.OpenView("INSERT INTO _Streams (Name, Data) VALUES ('%s', ?)" % name)
    r = CreateRecord(1)
    r.SetStream(1, path)
    v.Execute(r)
    v.Close()


def init_database(name, schema, ProductName, ProductCode, ProductVersion, Manufacturer):
    try:
        os.unlink(name)
    except OSError:
        pass

    ProductCode = ProductCode.upper()
    db = OpenDatabase(name, MSIDBOPEN_CREATE)
    for t in schema.tables:
        t.create(db)

    add_data(db, '_Validation', schema._Validation_records)
    si = db.GetSummaryInformation(20)
    si.SetProperty(PID_TITLE, 'Installation Database')
    si.SetProperty(PID_SUBJECT, ProductName)
    si.SetProperty(PID_AUTHOR, Manufacturer)
    if Itanium:
        si.SetProperty(PID_TEMPLATE, 'Intel64;1033')
    elif AMD64:
        si.SetProperty(PID_TEMPLATE, 'x64;1033')
    else:
        si.SetProperty(PID_TEMPLATE, 'Intel;1033')
    si.SetProperty(PID_REVNUMBER, gen_uuid())
    si.SetProperty(PID_WORDCOUNT, 2)
    si.SetProperty(PID_PAGECOUNT, 200)
    si.SetProperty(PID_APPNAME, 'Python MSI Library')
    si.Persist()
    add_data(db, 'Property', [('ProductName', ProductName),
     ('ProductCode', ProductCode),
     ('ProductVersion', ProductVersion),
     ('Manufacturer', Manufacturer),
     ('ProductLanguage', '1033')])
    db.Commit()
    return db


def add_tables(db, module):
    for table in module.tables:
        add_data(db, table, getattr(module, table))


def make_id(str):
    identifier_chars = string.ascii_letters + string.digits + '._'
    str = ''.join([ (c if c in identifier_chars else '_') for c in str ])
    if str[0] in string.digits + '.':
        str = '_' + str
    raise re.match('^[A-Za-z_][A-Za-z0-9_.]*$', str) or AssertionError('FILE' + str)
    return str


def gen_uuid():
    return '{' + UuidCreate().upper() + '}'


class CAB:

    def __init__(self, name):
        self.name = name
        self.files = []
        self.filenames = set()
        self.index = 0

    def gen_id(self, file):
        logical = _logical = make_id(file)
        pos = 1
        while logical in self.filenames:
            logical = '%s.%d' % (_logical, pos)
            pos += 1

        self.filenames.add(logical)
        return logical

    def append(self, full, file, logical):
        if os.path.isdir(full):
            return
        if not logical:
            logical = self.gen_id(file)
        self.index += 1
        self.files.append((full, logical))
        return (self.index, logical)

    def commit(self, db):
        from tempfile import mktemp
        filename = mktemp()
        FCICreate(filename, self.files)
        add_data(db, 'Media', [(1,
          self.index,
          None,
          '#' + self.name,
          None,
          None)])
        add_stream(db, self.name, filename)
        os.unlink(filename)
        db.Commit()
        return


_directories = set()

class Directory:

    def __init__(self, db, cab, basedir, physical, _logical, default, componentflags = None):
        """Create a new directory in the Directory table. There is a current component
        at each point in time for the directory, which is either explicitly created
        through start_component, or implicitly when files are added for the first
        time. Files are added into the current component, and into the cab file.
        To create a directory, a base directory object needs to be specified (can be
        None), the path to the physical directory, and a logical directory name.
        Default specifies the DefaultDir slot in the directory table. componentflags
        specifies the default flags that new components get."""
        index = 1
        _logical = make_id(_logical)
        logical = _logical
        while logical in _directories:
            logical = '%s%d' % (_logical, index)
            index += 1

        _directories.add(logical)
        self.db = db
        self.cab = cab
        self.basedir = basedir
        self.physical = physical
        self.logical = logical
        self.component = None
        self.short_names = set()
        self.ids = set()
        self.keyfiles = {}
        self.componentflags = componentflags
        if basedir:
            self.absolute = os.path.join(basedir.absolute, physical)
            blogical = basedir.logical
        else:
            self.absolute = physical
            blogical = None
        add_data(db, 'Directory', [(logical, blogical, default)])
        return

    def start_component(self, component = None, feature = None, flags = None, keyfile = None, uuid = None):
        """Add an entry to the Component table, and make this component the current for this
        directory. If no component name is given, the directory name is used. If no feature
        is given, the current feature is used. If no flags are given, the directory's default
        flags are used. If no keyfile is given, the KeyPath is left null in the Component
        table."""
        if flags is None:
            flags = self.componentflags
        if uuid is None:
            uuid = gen_uuid()
        else:
            uuid = uuid.upper()
        if component is None:
            component = self.logical
        self.component = component
        if Win64:
            flags |= 256
        if keyfile:
            keyid = self.cab.gen_id(self.absolute, keyfile)
            self.keyfiles[keyfile] = keyid
        else:
            keyid = None
        add_data(self.db, 'Component', [(component,
          uuid,
          self.logical,
          flags,
          None,
          keyid)])
        if feature is None:
            feature = current_feature
        add_data(self.db, 'FeatureComponents', [(feature.id, component)])
        return

    def make_short--- This code section failed: ---

0	LOAD_FAST         'file'
3	STORE_FAST        'oldfile'

6	LOAD_FAST         'file'
9	LOAD_ATTR         'replace'
12	LOAD_CONST        '+'
15	LOAD_CONST        '_'
18	CALL_FUNCTION_2   None
21	STORE_FAST        'file'

24	LOAD_CONST        ''
27	LOAD_ATTR         'join'
30	LOAD_GENEXPR      '<code_object <genexpr>>'
33	MAKE_FUNCTION_0   None
36	LOAD_FAST         'file'
39	GET_ITER          None
40	CALL_FUNCTION_1   None
43	CALL_FUNCTION_1   None
46	STORE_FAST        'file'

49	LOAD_FAST         'file'
52	LOAD_ATTR         'split'
55	LOAD_CONST        '.'
58	CALL_FUNCTION_1   None
61	STORE_FAST        'parts'

64	LOAD_GLOBAL       'len'
67	LOAD_FAST         'parts'
70	CALL_FUNCTION_1   None
73	LOAD_CONST        1
76	COMPARE_OP        '>'
79	POP_JUMP_IF_FALSE '147'

82	LOAD_CONST        ''
85	LOAD_ATTR         'join'
88	LOAD_FAST         'parts'
91	LOAD_CONST        -1
94	SLICE+2           None
95	CALL_FUNCTION_1   None
98	LOAD_ATTR         'upper'
101	CALL_FUNCTION_0   None
104	STORE_FAST        'prefix'

107	LOAD_FAST         'parts'
110	LOAD_CONST        -1
113	BINARY_SUBSCR     None
114	LOAD_ATTR         'upper'
117	CALL_FUNCTION_0   None
120	STORE_FAST        'suffix'

123	LOAD_FAST         'prefix'
126	POP_JUMP_IF_TRUE  '165'

129	LOAD_FAST         'suffix'
132	STORE_FAST        'prefix'

135	LOAD_CONST        None
138	STORE_FAST        'suffix'
141	JUMP_ABSOLUTE     '165'
144	JUMP_FORWARD      '165'

147	LOAD_FAST         'file'
150	LOAD_ATTR         'upper'
153	CALL_FUNCTION_0   None
156	STORE_FAST        'prefix'

159	LOAD_CONST        None
162	STORE_FAST        'suffix'
165_0	COME_FROM         '144'

165	LOAD_GLOBAL       'len'
168	LOAD_FAST         'parts'
171	CALL_FUNCTION_1   None
174	LOAD_CONST        3
177	COMPARE_OP        '<'
180	POP_JUMP_IF_FALSE '270'
183	LOAD_GLOBAL       'len'
186	LOAD_FAST         'prefix'
189	CALL_FUNCTION_1   None
192	LOAD_CONST        8
195	COMPARE_OP        '<='
198	POP_JUMP_IF_FALSE '270'
201	LOAD_FAST         'file'
204	LOAD_FAST         'oldfile'
207	COMPARE_OP        '=='
210	POP_JUMP_IF_FALSE '270'

213	LOAD_FAST         'suffix'
216	UNARY_NOT         None
217	POP_JUMP_IF_TRUE  '238'
220	LOAD_GLOBAL       'len'
223	LOAD_FAST         'suffix'
226	CALL_FUNCTION_1   None
229	LOAD_CONST        3
232	COMPARE_OP        '<='
235_0	COME_FROM         '180'
235_1	COME_FROM         '198'
235_2	COME_FROM         '210'
235_3	COME_FROM         '217'
235	POP_JUMP_IF_FALSE '270'

238	LOAD_FAST         'suffix'
241	POP_JUMP_IF_FALSE '261'

244	LOAD_FAST         'prefix'
247	LOAD_CONST        '.'
250	BINARY_ADD        None
251	LOAD_FAST         'suffix'
254	BINARY_ADD        None
255	STORE_FAST        'file'
258	JUMP_ABSOLUTE     '276'

261	LOAD_FAST         'prefix'
264	STORE_FAST        'file'
267	JUMP_FORWARD      '276'

270	LOAD_CONST        None
273	STORE_FAST        'file'
276_0	COME_FROM         '267'

276	LOAD_FAST         'file'
279	LOAD_CONST        None
282	COMPARE_OP        'is'
285	POP_JUMP_IF_TRUE  '303'
288	LOAD_FAST         'file'
291	LOAD_FAST         'self'
294	LOAD_ATTR         'short_names'
297	COMPARE_OP        'in'
300_0	COME_FROM         '285'
300	POP_JUMP_IF_FALSE '464'

303	LOAD_FAST         'prefix'
306	LOAD_CONST        6
309	SLICE+2           None
310	STORE_FAST        'prefix'

313	LOAD_FAST         'suffix'
316	POP_JUMP_IF_FALSE '332'

319	LOAD_FAST         'suffix'
322	LOAD_CONST        3
325	SLICE+2           None
326	STORE_FAST        'suffix'
329	JUMP_FORWARD      '332'
332_0	COME_FROM         '329'

332	LOAD_CONST        1
335	STORE_FAST        'pos'

338	SETUP_LOOP        '464'

341	LOAD_FAST         'suffix'
344	POP_JUMP_IF_FALSE '369'

347	LOAD_CONST        '%s~%d.%s'
350	LOAD_FAST         'prefix'
353	LOAD_FAST         'pos'
356	LOAD_FAST         'suffix'
359	BUILD_TUPLE_3     None
362	BINARY_MODULO     None
363	STORE_FAST        'file'
366	JUMP_FORWARD      '385'

369	LOAD_CONST        '%s~%d'
372	LOAD_FAST         'prefix'
375	LOAD_FAST         'pos'
378	BUILD_TUPLE_2     None
381	BINARY_MODULO     None
382	STORE_FAST        'file'
385_0	COME_FROM         '366'

385	LOAD_FAST         'file'
388	LOAD_FAST         'self'
391	LOAD_ATTR         'short_names'
394	COMPARE_OP        'not in'
397	POP_JUMP_IF_FALSE '404'
400	BREAK_LOOP        None
401	JUMP_FORWARD      '404'
404_0	COME_FROM         '401'

404	LOAD_FAST         'pos'
407	LOAD_CONST        1
410	INPLACE_ADD       None
411	STORE_FAST        'pos'

414	LOAD_FAST         'pos'
417	LOAD_CONST        10000
420	COMPARE_OP        '<'
423	POP_JUMP_IF_TRUE  '432'
426	LOAD_ASSERT       'AssertionError'
429	RAISE_VARARGS_1   None

432	LOAD_FAST         'pos'
435	LOAD_CONST        (10, 100, 1000)
438	COMPARE_OP        'in'
441	POP_JUMP_IF_FALSE '341'

444	LOAD_FAST         'prefix'
447	LOAD_CONST        -1
450	SLICE+2           None
451	STORE_FAST        'prefix'
454	JUMP_BACK         '341'
457	JUMP_BACK         '341'
460	POP_BLOCK         None
461_0	COME_FROM         '338'
461	JUMP_FORWARD      '464'
464_0	COME_FROM         '461'

464	LOAD_FAST         'self'
467	LOAD_ATTR         'short_names'
470	LOAD_ATTR         'add'
473	LOAD_FAST         'file'
476	CALL_FUNCTION_1   None
479	POP_TOP           None

480	LOAD_GLOBAL       're'
483	LOAD_ATTR         'search'
486	LOAD_CONST        '[\\?|><:/*"+,;=\\[\\]]'
489	LOAD_FAST         'file'
492	CALL_FUNCTION_2   None
495	UNARY_NOT         None
496	POP_JUMP_IF_TRUE  '505'
499	LOAD_ASSERT       'AssertionError'
502	RAISE_VARARGS_1   None

505	LOAD_FAST         'file'
508	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 460

    def add_file(self, file, src = None, version = None, language = None):
        """Add a file to the current component of the directory, starting a new one
        one if there is no current component. By default, the file name in the source
        and the file table will be identical. If the src file is specified, it is
        interpreted relative to the current directory. Optionally, a version and a
        language can be specified for the entry in the File table."""
        if not self.component:
            self.start_component(self.logical, current_feature, 0)
        if not src:
            src = file
            file = os.path.basename(file)
        absolute = os.path.join(self.absolute, src)
        if not not re.search('[\\?|><:/*]"', file):
            raise AssertionError
            logical = file in self.keyfiles and self.keyfiles[file]
        else:
            logical = None
        sequence, logical = self.cab.append(absolute, file, logical)
        if not logical not in self.ids:
            raise AssertionError
            self.ids.add(logical)
            short = self.make_short(file)
            full = '%s|%s' % (short, file)
            filesize = os.stat(absolute).st_size
            attributes = 512
            add_data(self.db, 'File', [(logical,
              self.component,
              full,
              filesize,
              version,
              language,
              attributes,
              sequence)])
            file.endswith('.py') and add_data(self.db, 'RemoveFile', [(logical + 'c',
              self.component,
              '%sC|%sc' % (short, file),
              self.logical,
              2), (logical + 'o',
              self.component,
              '%sO|%so' % (short, file),
              self.logical,
              2)])
        return logical

    def glob(self, pattern, exclude = None):
        """Add a list of files to the current component as specified in the
        glob pattern. Individual files can be excluded in the exclude list."""
        files = glob.glob1(self.absolute, pattern)
        for f in files:
            if exclude and f in exclude:
                continue
            self.add_file(f)

        return files

    def remove_pyc(self):
        """Remove .pyc/.pyo files on uninstall"""
        add_data(self.db, 'RemoveFile', [(self.component + 'c',
          self.component,
          '*.pyc',
          self.logical,
          2), (self.component + 'o',
          self.component,
          '*.pyo',
          self.logical,
          2)])


class Binary:

    def __init__(self, fname):
        self.name = fname

    def __repr__(self):
        return 'msilib.Binary(os.path.join(dirname,"%s"))' % self.name


class Feature:

    def __init__(self, db, id, title, desc, display, level = 1, parent = None, directory = None, attributes = 0):
        self.id = id
        if parent:
            parent = parent.id
        add_data(db, 'Feature', [(id,
          parent,
          title,
          desc,
          display,
          level,
          directory,
          attributes)])

    def set_current(self):
        global current_feature
        current_feature = self


class Control:

    def __init__(self, dlg, name):
        self.dlg = dlg
        self.name = name

    def event(self, event, argument, condition = '1', ordering = None):
        add_data(self.dlg.db, 'ControlEvent', [(self.dlg.name,
          self.name,
          event,
          argument,
          condition,
          ordering)])

    def mapping(self, event, attribute):
        add_data(self.dlg.db, 'EventMapping', [(self.dlg.name,
          self.name,
          event,
          attribute)])

    def condition(self, action, condition):
        add_data(self.dlg.db, 'ControlCondition', [(self.dlg.name,
          self.name,
          action,
          condition)])


class RadioButtonGroup(Control):

    def __init__(self, dlg, name, property):
        self.dlg = dlg
        self.name = name
        self.property = property
        self.index = 1

    def add(self, name, x, y, w, h, text, value = None):
        if value is None:
            value = name
        add_data(self.dlg.db, 'RadioButton', [(self.property,
          self.index,
          value,
          x,
          y,
          w,
          h,
          text,
          None)])
        self.index += 1
        return


class Dialog:

    def __init__(self, db, name, x, y, w, h, attr, title, first, default, cancel):
        self.db = db
        self.name = name
        self.x, self.y, self.w, self.h = (x,
         y,
         w,
         h)
        add_data(db, 'Dialog', [(name,
          x,
          y,
          w,
          h,
          attr,
          title,
          first,
          default,
          cancel)])

    def control(self, name, type, x, y, w, h, attr, prop, text, next, help):
        add_data(self.db, 'Control', [(self.name,
          name,
          type,
          x,
          y,
          w,
          h,
          attr,
          prop,
          text,
          next,
          help)])
        return Control(self, name)

    def text(self, name, x, y, w, h, attr, text):
        return self.control(name, 'Text', x, y, w, h, attr, None, text, None, None)

    def bitmap(self, name, x, y, w, h, text):
        return self.control(name, 'Bitmap', x, y, w, h, 1, None, text, None, None)

    def line(self, name, x, y, w, h):
        return self.control(name, 'Line', x, y, w, h, 1, None, None, None, None)

    def pushbutton(self, name, x, y, w, h, attr, text, next):
        return self.control(name, 'PushButton', x, y, w, h, attr, None, text, next, None)

    def radiogroup(self, name, x, y, w, h, attr, prop, text, next):
        add_data(self.db, 'Control', [(self.name,
          name,
          'RadioButtonGroup',
          x,
          y,
          w,
          h,
          attr,
          prop,
          text,
          next,
          None)])
        return RadioButtonGroup(self, name, prop)

    def checkbox(self, name, x, y, w, h, attr, prop, text, next):
        return self.control(name, 'CheckBox', x, y, w, h, attr, prop, text, next, None)