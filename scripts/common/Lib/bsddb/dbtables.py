# Embedded file name: scripts/common/Lib/bsddb/dbtables.py
_cvsid = '$Id$'
import re
import sys
import copy
import random
import struct
if sys.version_info[0] >= 3:
    import pickle
elif sys.version_info < (2, 6):
    import cPickle as pickle
else:
    import warnings
    w = warnings.catch_warnings()
    w.__enter__()
    try:
        warnings.filterwarnings('ignore', message='the cPickle module has been removed in Python 3.0', category=DeprecationWarning)
        import cPickle as pickle
    finally:
        w.__exit__()

    del w
try:
    from bsddb3 import db
except ImportError:
    from bsddb import db

class TableDBError(StandardError):
    pass


class TableAlreadyExists(TableDBError):
    pass


class Cond:
    """This condition matches everything"""

    def __call__(self, s):
        return 1


class ExactCond(Cond):
    """Acts as an exact match condition function"""

    def __init__(self, strtomatch):
        self.strtomatch = strtomatch

    def __call__(self, s):
        return s == self.strtomatch


class PrefixCond(Cond):
    """Acts as a condition function for matching a string prefix"""

    def __init__(self, prefix):
        self.prefix = prefix

    def __call__(self, s):
        return s[:len(self.prefix)] == self.prefix


class PostfixCond(Cond):
    """Acts as a condition function for matching a string postfix"""

    def __init__(self, postfix):
        self.postfix = postfix

    def __call__(self, s):
        return s[-len(self.postfix):] == self.postfix


class LikeCond(Cond):
    """
    Acts as a function that will match using an SQL 'LIKE' style
    string.  Case insensitive and % signs are wild cards.
    This isn't perfect but it should work for the simple common cases.
    """

    def __init__(self, likestr, re_flags = re.IGNORECASE):
        chars_to_escape = '.*+()[]?'
        for char in chars_to_escape:
            likestr = likestr.replace(char, '\\' + char)

        self.likestr = likestr.replace('%', '.*')
        self.re = re.compile('^' + self.likestr + '$', re_flags)

    def __call__(self, s):
        return self.re.match(s)


_table_names_key = '__TABLE_NAMES__'
_columns = '._COLUMNS__'

def _columns_key(table):
    return table + _columns


_data = '._DATA_.'
_rowid = '._ROWID_.'
_rowid_str_len = 8

def _data_key(table, col, rowid):
    return table + _data + col + _data + rowid


def _search_col_data_key(table, col):
    return table + _data + col + _data


def _search_all_data_key(table):
    return table + _data


def _rowid_key(table, rowid):
    return table + _rowid + rowid + _rowid


def _search_rowid_key(table):
    return table + _rowid


def contains_metastrings(s):
    """Verify that the given string does not contain any
    metadata strings that might interfere with dbtables database operation.
    """
    if s.find(_table_names_key) >= 0 or s.find(_columns) >= 0 or s.find(_data) >= 0 or s.find(_rowid) >= 0:
        return 1
    else:
        return 0


class bsdTableDB:

    def __init__(self, filename, dbhome, create = 0, truncate = 0, mode = 384, recover = 0, dbflags = 0):
        """bsdTableDB(filename, dbhome, create=0, truncate=0, mode=0600)
        
        Open database name in the dbhome Berkeley DB directory.
        Use keyword arguments when calling this constructor.
        """
        self.db = None
        myflags = db.DB_THREAD
        if create:
            myflags |= db.DB_CREATE
        flagsforenv = db.DB_INIT_MPOOL | db.DB_INIT_LOCK | db.DB_INIT_LOG | db.DB_INIT_TXN | dbflags
        try:
            dbflags |= db.DB_AUTO_COMMIT
        except AttributeError:
            pass

        if recover:
            flagsforenv = flagsforenv | db.DB_RECOVER
        self.env = db.DBEnv()
        self.env.set_lk_detect(db.DB_LOCK_DEFAULT)
        self.env.open(dbhome, myflags | flagsforenv)
        if truncate:
            myflags |= db.DB_TRUNCATE
        self.db = db.DB(self.env)
        self.db.set_get_returns_none(1)
        self.db.set_flags(db.DB_DUP)
        self.db.open(filename, db.DB_BTREE, dbflags | myflags, mode)
        self.dbfilename = filename
        if sys.version_info[0] >= 3:

            class cursor_py3k(object):

                def __init__(self, dbcursor):
                    self._dbcursor = dbcursor

                def close(self):
                    return self._dbcursor.close()

                def set_range(self, search):
                    v = self._dbcursor.set_range(bytes(search, 'iso8859-1'))
                    if v is not None:
                        v = (v[0].decode('iso8859-1'), v[1].decode('iso8859-1'))
                    return v

                def __next__(self):
                    v = getattr(self._dbcursor, 'next')()
                    if v is not None:
                        v = (v[0].decode('iso8859-1'), v[1].decode('iso8859-1'))
                    return v

            class db_py3k(object):

                def __init__(self, db):
                    self._db = db

                def cursor(self, txn = None):
                    return cursor_py3k(self._db.cursor(txn=txn))

                def has_key(self, key, txn = None):
                    return getattr(self._db, 'has_key')(bytes(key, 'iso8859-1'), txn=txn)

                def put(self, key, value, flags = 0, txn = None):
                    key = bytes(key, 'iso8859-1')
                    if value is not None:
                        value = bytes(value, 'iso8859-1')
                    return self._db.put(key, value, flags=flags, txn=txn)

                def put_bytes(self, key, value, txn = None):
                    key = bytes(key, 'iso8859-1')
                    return self._db.put(key, value, txn=txn)

                def get(self, key, txn = None, flags = 0):
                    key = bytes(key, 'iso8859-1')
                    v = self._db.get(key, txn=txn, flags=flags)
                    if v is not None:
                        v = v.decode('iso8859-1')
                    return v

                def get_bytes(self, key, txn = None, flags = 0):
                    key = bytes(key, 'iso8859-1')
                    return self._db.get(key, txn=txn, flags=flags)

                def delete(self, key, txn = None):
                    key = bytes(key, 'iso8859-1')
                    return self._db.delete(key, txn=txn)

                def close(self):
                    return self._db.close()

            self.db = db_py3k(self.db)
        txn = self.env.txn_begin()
        try:
            if not getattr(self.db, 'has_key')(_table_names_key, txn):
                getattr(self.db, 'put_bytes', self.db.put)(_table_names_key, pickle.dumps([], 1), txn=txn)
        except:
            txn.abort()
            raise
        else:
            txn.commit()

        self.__tablecolumns = {}
        return

    def __del__(self):
        self.close()

    def close(self):
        if self.db is not None:
            self.db.close()
            self.db = None
        if self.env is not None:
            self.env.close()
            self.env = None
        return

    def checkpoint(self, mins = 0):
        self.env.txn_checkpoint(mins)

    def sync(self):
        self.db.sync()

    def _db_print--- This code section failed: ---

0	LOAD_CONST        '******** Printing raw database for debugging ********'
3	PRINT_ITEM        None
4	PRINT_NEWLINE_CONT None

5	LOAD_FAST         'self'
8	LOAD_ATTR         'db'
11	LOAD_ATTR         'cursor'
14	CALL_FUNCTION_0   None
17	STORE_FAST        'cur'

20	SETUP_EXCEPT      '117'

23	LOAD_FAST         'cur'
26	LOAD_ATTR         'first'
29	CALL_FUNCTION_0   None
32	UNPACK_SEQUENCE_2 None
35	STORE_FAST        'key'
38	STORE_FAST        'data'

41	SETUP_LOOP        '113'

44	LOAD_GLOBAL       'repr'
47	BUILD_MAP         None
50	LOAD_FAST         'data'
53	LOAD_FAST         'key'
56	STORE_MAP         None
57	CALL_FUNCTION_1   None
60	PRINT_ITEM        None
61	PRINT_NEWLINE_CONT None

62	LOAD_FAST         'cur'
65	LOAD_ATTR         'next'
68	CALL_FUNCTION_0   None
71	STORE_FAST        'next'

74	LOAD_FAST         'next'
77	POP_JUMP_IF_FALSE '95'

80	LOAD_FAST         'next'
83	UNPACK_SEQUENCE_2 None
86	STORE_FAST        'key'
89	STORE_FAST        'data'
92	JUMP_BACK         '44'

95	LOAD_FAST         'cur'
98	LOAD_ATTR         'close'
101	CALL_FUNCTION_0   None
104	POP_TOP           None

105	LOAD_CONST        None
108	RETURN_VALUE      None
109	JUMP_BACK         '44'
112	POP_BLOCK         None
113_0	COME_FROM         '41'
113	POP_BLOCK         None
114	JUMP_FORWARD      '147'
117_0	COME_FROM         '20'

117	DUP_TOP           None
118	LOAD_GLOBAL       'db'
121	LOAD_ATTR         'DBNotFoundError'
124	COMPARE_OP        'exception match'
127	POP_JUMP_IF_FALSE '146'
130	POP_TOP           None
131	POP_TOP           None
132	POP_TOP           None

133	LOAD_FAST         'cur'
136	LOAD_ATTR         'close'
139	CALL_FUNCTION_0   None
142	POP_TOP           None
143	JUMP_FORWARD      '147'
146	END_FINALLY       None
147_0	COME_FROM         '114'
147_1	COME_FROM         '146'

Syntax error at or near `POP_BLOCK' token at offset 112

    def CreateTable(self, table, columns):
        """CreateTable(table, columns) - Create a new table in the database.
        
        raises TableDBError if it already exists or for other DB errors.
        """
        raise isinstance(columns, list) or AssertionError
        txn = None
        try:
            if contains_metastrings(table):
                raise ValueError('bad table name: contains reserved metastrings')
            for column in columns:
                if contains_metastrings(column):
                    raise ValueError('bad column name: contains reserved metastrings')

            columnlist_key = _columns_key(table)
            if getattr(self.db, 'has_key')(columnlist_key):
                raise TableAlreadyExists, 'table already exists'
            txn = self.env.txn_begin()
            getattr(self.db, 'put_bytes', self.db.put)(columnlist_key, pickle.dumps(columns, 1), txn=txn)
            tablelist = pickle.loads(getattr(self.db, 'get_bytes', self.db.get)(_table_names_key, txn=txn, flags=db.DB_RMW))
            tablelist.append(table)
            self.db.delete(_table_names_key, txn=txn)
            getattr(self.db, 'put_bytes', self.db.put)(_table_names_key, pickle.dumps(tablelist, 1), txn=txn)
            txn.commit()
            txn = None
        except db.DBError as dberror:
            if txn:
                txn.abort()
            if sys.version_info < (2, 6):
                raise TableDBError, dberror[1]
            else:
                raise TableDBError, dberror.args[1]

        return

    def ListTableColumns(self, table):
        """Return a list of columns in the given table.
        [] if the table doesn't exist.
        """
        if not isinstance(table, str):
            raise AssertionError
            if contains_metastrings(table):
                raise ValueError, 'bad table name: contains reserved metastrings'
            columnlist_key = _columns_key(table)
            return getattr(self.db, 'has_key')(columnlist_key) or []
        else:
            pickledcolumnlist = getattr(self.db, 'get_bytes', self.db.get)(columnlist_key)
            if pickledcolumnlist:
                return pickle.loads(pickledcolumnlist)
            return []

    def ListTables(self):
        """Return a list of tables in this database."""
        pickledtablelist = self.db.get_get(_table_names_key)
        if pickledtablelist:
            return pickle.loads(pickledtablelist)
        else:
            return []

    def CreateOrExtendTable(self, table, columns):
        """CreateOrExtendTable(table, columns)
        
        Create a new table in the database.
        
        If a table of this name already exists, extend it to have any
        additional columns present in the given list as well as
        all of its current columns.
        """
        raise isinstance(columns, list) or AssertionError
        try:
            self.CreateTable(table, columns)
        except TableAlreadyExists:
            txn = None
            try:
                columnlist_key = _columns_key(table)
                txn = self.env.txn_begin()
                oldcolumnlist = pickle.loads(getattr(self.db, 'get_bytes', self.db.get)(columnlist_key, txn=txn, flags=db.DB_RMW))
                oldcolumnhash = {}
                for c in oldcolumnlist:
                    oldcolumnhash[c] = c

                newcolumnlist = copy.copy(oldcolumnlist)
                for c in columns:
                    if c not in oldcolumnhash:
                        newcolumnlist.append(c)

                if newcolumnlist != oldcolumnlist:
                    self.db.delete(columnlist_key, txn=txn)
                    getattr(self.db, 'put_bytes', self.db.put)(columnlist_key, pickle.dumps(newcolumnlist, 1), txn=txn)
                txn.commit()
                txn = None
                self.__load_column_info(table)
            except db.DBError as dberror:
                if txn:
                    txn.abort()
                if sys.version_info < (2, 6):
                    raise TableDBError, dberror[1]
                else:
                    raise TableDBError, dberror.args[1]

        return

    def __load_column_info(self, table):
        """initialize the self.__tablecolumns dict"""
        try:
            tcolpickles = getattr(self.db, 'get_bytes', self.db.get)(_columns_key(table))
        except db.DBNotFoundError:
            raise TableDBError, 'unknown table: %r' % (table,)

        if not tcolpickles:
            raise TableDBError, 'unknown table: %r' % (table,)
        self.__tablecolumns[table] = pickle.loads(tcolpickles)

    def __new_rowid(self, table, txn):
        """Create a new unique row identifier"""
        unique = 0
        while not unique:
            blist = []
            for x in xrange(_rowid_str_len):
                blist.append(random.randint(0, 255))

            newid = struct.pack(('B' * _rowid_str_len), *blist)
            if sys.version_info[0] >= 3:
                newid = newid.decode('iso8859-1')
            try:
                self.db.put(_rowid_key(table, newid), None, txn=txn, flags=db.DB_NOOVERWRITE)
            except db.DBKeyExistError:
                pass
            else:
                unique = 1

        return newid

    def Insert(self, table, rowdict):
        """Insert(table, datadict) - Insert a new row into the table
        using the keys+values from rowdict as the column values.
        """
        txn = None
        try:
            if not getattr(self.db, 'has_key')(_columns_key(table)):
                raise TableDBError, 'unknown table'
            if table not in self.__tablecolumns:
                self.__load_column_info(table)
            for column in rowdict.keys():
                if not self.__tablecolumns[table].count(column):
                    raise TableDBError, 'unknown column: %r' % (column,)

            txn = self.env.txn_begin()
            rowid = self.__new_rowid(table, txn=txn)
            for column, dataitem in rowdict.items():
                self.db.put(_data_key(table, column, rowid), dataitem, txn=txn)

            txn.commit()
            txn = None
        except db.DBError as dberror:
            info = sys.exc_info()
            if txn:
                txn.abort()
                self.db.delete(_rowid_key(table, rowid))
            if sys.version_info < (2, 6):
                raise TableDBError, dberror[1], info[2]
            else:
                raise TableDBError, dberror.args[1], info[2]

        return

    def Modify(self, table, conditions = {}, mappings = {}):
        """Modify(table, conditions={}, mappings={}) - Modify items in rows matching 'conditions' using mapping functions in 'mappings'
        
        * table - the table name
        * conditions - a dictionary keyed on column names containing
          a condition callable expecting the data string as an
          argument and returning a boolean.
        * mappings - a dictionary keyed on column names containing a
          condition callable expecting the data string as an argument and
          returning the new string for that column.
        """
        try:
            matching_rowids = self.__Select(table, [], conditions)
            columns = mappings.keys()
            for rowid in matching_rowids.keys():
                txn = None
                try:
                    for column in columns:
                        txn = self.env.txn_begin()
                        try:
                            dataitem = self.db.get(_data_key(table, column, rowid), txn=txn)
                            self.db.delete(_data_key(table, column, rowid), txn=txn)
                        except db.DBNotFoundError:
                            dataitem = None

                        dataitem = mappings[column](dataitem)
                        if dataitem is not None:
                            self.db.put(_data_key(table, column, rowid), dataitem, txn=txn)
                        txn.commit()
                        txn = None

                except:
                    if txn:
                        txn.abort()
                    raise

        except db.DBError as dberror:
            if sys.version_info < (2, 6):
                raise TableDBError, dberror[1]
            else:
                raise TableDBError, dberror.args[1]

        return

    def Delete(self, table, conditions = {}):
        """Delete(table, conditions) - Delete items matching the given
        conditions from the table.
        
        * conditions - a dictionary keyed on column names containing
          condition functions expecting the data string as an
          argument and returning a boolean.
        """
        try:
            matching_rowids = self.__Select(table, [], conditions)
            columns = self.__tablecolumns[table]
            for rowid in matching_rowids.keys():
                txn = None
                try:
                    txn = self.env.txn_begin()
                    for column in columns:
                        try:
                            self.db.delete(_data_key(table, column, rowid), txn=txn)
                        except db.DBNotFoundError:
                            pass

                    try:
                        self.db.delete(_rowid_key(table, rowid), txn=txn)
                    except db.DBNotFoundError:
                        pass

                    txn.commit()
                    txn = None
                except db.DBError as dberror:
                    if txn:
                        txn.abort()
                    raise

        except db.DBError as dberror:
            if sys.version_info < (2, 6):
                raise TableDBError, dberror[1]
            else:
                raise TableDBError, dberror.args[1]

        return

    def Select(self, table, columns, conditions = {}):
        """Select(table, columns, conditions) - retrieve specific row data
        Returns a list of row column->value mapping dictionaries.
        
        * columns - a list of which column data to return.  If
          columns is None, all columns will be returned.
        * conditions - a dictionary keyed on column names
          containing callable conditions expecting the data string as an
          argument and returning a boolean.
        """
        try:
            if table not in self.__tablecolumns:
                self.__load_column_info(table)
            if columns is None:
                columns = self.__tablecolumns[table]
            matching_rowids = self.__Select(table, columns, conditions)
        except db.DBError as dberror:
            if sys.version_info < (2, 6):
                raise TableDBError, dberror[1]
            else:
                raise TableDBError, dberror.args[1]

        return matching_rowids.values()

    def __Select(self, table, columns, conditions):
        """__Select() - Used to implement Select and Delete (above)
        Returns a dictionary keyed on rowids containing dicts
        holding the row data for columns listed in the columns param
        that match the given conditions.
        * conditions is a dictionary keyed on column names
        containing callable conditions expecting the data string as an
        argument and returning a boolean.
        """
        if table not in self.__tablecolumns:
            self.__load_column_info(table)
        if columns is None:
            columns = self.tablecolumns[table]
        for column in columns + conditions.keys():
            if not self.__tablecolumns[table].count(column):
                raise TableDBError, 'unknown column: %r' % (column,)

        matching_rowids = {}
        rejected_rowids = {}

        def cmp_conditions(atuple, btuple):
            a = atuple[1]
            b = btuple[1]
            if type(a) is type(b):

                def cmp(a, b):
                    if a == b:
                        return 0
                    if a < b:
                        return -1
                    return 1

                if isinstance(a, PrefixCond) and isinstance(b, PrefixCond):
                    return cmp(len(b.prefix), len(a.prefix))
                if isinstance(a, LikeCond) and isinstance(b, LikeCond):
                    return cmp(len(b.likestr), len(a.likestr))
                return 0
            if isinstance(a, ExactCond):
                return -1
            if isinstance(b, ExactCond):
                return 1
            if isinstance(a, PrefixCond):
                return -1
            if isinstance(b, PrefixCond):
                return 1
            return 0

        if sys.version_info < (2, 6):
            conditionlist = conditions.items()
            conditionlist.sort(cmp_conditions)
        else:
            conditionlist = []
            for i in conditions.items():
                for j, k in enumerate(conditionlist):
                    r = cmp_conditions(k, i)
                    if r == 1:
                        conditionlist.insert(j, i)
                        break
                else:
                    conditionlist.append(i)

        cur = self.db.cursor()
        column_num = -1
        for column, condition in conditionlist:
            column_num = column_num + 1
            searchkey = _search_col_data_key(table, column)
            if column in columns:
                savethiscolumndata = 1
            else:
                savethiscolumndata = 0
            try:
                key, data = cur.set_range(searchkey)
                while key[:len(searchkey)] == searchkey:
                    rowid = key[-_rowid_str_len:]
                    if rowid not in rejected_rowids:
                        if not condition or condition(data):
                            if rowid not in matching_rowids:
                                matching_rowids[rowid] = {}
                            if savethiscolumndata:
                                matching_rowids[rowid][column] = data
                        else:
                            if rowid in matching_rowids:
                                del matching_rowids[rowid]
                            rejected_rowids[rowid] = rowid
                    key, data = cur.next()

            except db.DBError as dberror:
                if dberror.args[0] != db.DB_NOTFOUND:
                    raise
                continue

        cur.close()
        del rejected_rowids
        if len(columns) > 0:
            for rowid, rowdata in matching_rowids.items():
                for column in columns:
                    if column in rowdata:
                        continue
                    try:
                        rowdata[column] = self.db.get(_data_key(table, column, rowid))
                    except db.DBError as dberror:
                        if sys.version_info < (2, 6):
                            if dberror[0] != db.DB_NOTFOUND:
                                raise
                        elif dberror.args[0] != db.DB_NOTFOUND:
                            raise
                        rowdata[column] = None

        return matching_rowids

    def Drop--- This code section failed: ---

0	LOAD_CONST        None
3	STORE_FAST        'txn'

6	SETUP_EXCEPT      '504'

9	LOAD_FAST         'self'
12	LOAD_ATTR         'env'
15	LOAD_ATTR         'txn_begin'
18	CALL_FUNCTION_0   None
21	STORE_FAST        'txn'

24	LOAD_FAST         'self'
27	LOAD_ATTR         'db'
30	LOAD_ATTR         'delete'
33	LOAD_GLOBAL       '_columns_key'
36	LOAD_FAST         'table'
39	CALL_FUNCTION_1   None
42	LOAD_CONST        'txn'
45	LOAD_FAST         'txn'
48	CALL_FUNCTION_257 None
51	POP_TOP           None

52	LOAD_FAST         'self'
55	LOAD_ATTR         'db'
58	LOAD_ATTR         'cursor'
61	LOAD_FAST         'txn'
64	CALL_FUNCTION_1   None
67	STORE_FAST        'cur'

70	LOAD_GLOBAL       '_search_all_data_key'
73	LOAD_FAST         'table'
76	CALL_FUNCTION_1   None
79	STORE_FAST        'table_key'

82	SETUP_LOOP        '174'

85	SETUP_EXCEPT      '113'

88	LOAD_FAST         'cur'
91	LOAD_ATTR         'set_range'
94	LOAD_FAST         'table_key'
97	CALL_FUNCTION_1   None
100	UNPACK_SEQUENCE_2 None
103	STORE_FAST        'key'
106	STORE_FAST        'data'
109	POP_BLOCK         None
110	JUMP_FORWARD      '134'
113_0	COME_FROM         '85'

113	DUP_TOP           None
114	LOAD_GLOBAL       'db'
117	LOAD_ATTR         'DBNotFoundError'
120	COMPARE_OP        'exception match'
123	POP_JUMP_IF_FALSE '133'
126	POP_TOP           None
127	POP_TOP           None
128	POP_TOP           None

129	BREAK_LOOP        None
130	JUMP_FORWARD      '134'
133	END_FINALLY       None
134_0	COME_FROM         '110'
134_1	COME_FROM         '133'

134	LOAD_FAST         'key'
137	LOAD_GLOBAL       'len'
140	LOAD_FAST         'table_key'
143	CALL_FUNCTION_1   None
146	SLICE+2           None
147	LOAD_FAST         'table_key'
150	COMPARE_OP        '!='
153	POP_JUMP_IF_FALSE '160'

156	BREAK_LOOP        None
157	JUMP_FORWARD      '160'
160_0	COME_FROM         '157'

160	LOAD_FAST         'cur'
163	LOAD_ATTR         'delete'
166	CALL_FUNCTION_0   None
169	POP_TOP           None
170	JUMP_BACK         '85'
173	POP_BLOCK         None
174_0	COME_FROM         '82'

174	LOAD_GLOBAL       '_search_rowid_key'
177	LOAD_FAST         'table'
180	CALL_FUNCTION_1   None
183	STORE_FAST        'table_key'

186	SETUP_LOOP        '278'

189	SETUP_EXCEPT      '217'

192	LOAD_FAST         'cur'
195	LOAD_ATTR         'set_range'
198	LOAD_FAST         'table_key'
201	CALL_FUNCTION_1   None
204	UNPACK_SEQUENCE_2 None
207	STORE_FAST        'key'
210	STORE_FAST        'data'
213	POP_BLOCK         None
214	JUMP_FORWARD      '238'
217_0	COME_FROM         '189'

217	DUP_TOP           None
218	LOAD_GLOBAL       'db'
221	LOAD_ATTR         'DBNotFoundError'
224	COMPARE_OP        'exception match'
227	POP_JUMP_IF_FALSE '237'
230	POP_TOP           None
231	POP_TOP           None
232	POP_TOP           None

233	BREAK_LOOP        None
234	JUMP_FORWARD      '238'
237	END_FINALLY       None
238_0	COME_FROM         '214'
238_1	COME_FROM         '237'

238	LOAD_FAST         'key'
241	LOAD_GLOBAL       'len'
244	LOAD_FAST         'table_key'
247	CALL_FUNCTION_1   None
250	SLICE+2           None
251	LOAD_FAST         'table_key'
254	COMPARE_OP        '!='
257	POP_JUMP_IF_FALSE '264'

260	BREAK_LOOP        None
261	JUMP_FORWARD      '264'
264_0	COME_FROM         '261'

264	LOAD_FAST         'cur'
267	LOAD_ATTR         'delete'
270	CALL_FUNCTION_0   None
273	POP_TOP           None
274	JUMP_BACK         '189'
277	POP_BLOCK         None
278_0	COME_FROM         '186'

278	LOAD_FAST         'cur'
281	LOAD_ATTR         'close'
284	CALL_FUNCTION_0   None
287	POP_TOP           None

288	LOAD_GLOBAL       'pickle'
291	LOAD_ATTR         'loads'

294	LOAD_GLOBAL       'getattr'
297	LOAD_FAST         'self'
300	LOAD_ATTR         'db'
303	LOAD_CONST        'get_bytes'
306	LOAD_FAST         'self'
309	LOAD_ATTR         'db'
312	LOAD_ATTR         'get'
315	CALL_FUNCTION_3   None
318	LOAD_GLOBAL       '_table_names_key'
321	LOAD_CONST        'txn'

324	LOAD_FAST         'txn'
327	LOAD_CONST        'flags'
330	LOAD_GLOBAL       'db'
333	LOAD_ATTR         'DB_RMW'
336	CALL_FUNCTION_513 None
339	CALL_FUNCTION_1   None
342	STORE_FAST        'tablelist'

345	SETUP_EXCEPT      '365'

348	LOAD_FAST         'tablelist'
351	LOAD_ATTR         'remove'
354	LOAD_FAST         'table'
357	CALL_FUNCTION_1   None
360	POP_TOP           None
361	POP_BLOCK         None
362	JUMP_FORWARD      '382'
365_0	COME_FROM         '345'

365	DUP_TOP           None
366	LOAD_GLOBAL       'ValueError'
369	COMPARE_OP        'exception match'
372	POP_JUMP_IF_FALSE '381'
375	POP_TOP           None
376	POP_TOP           None
377	POP_TOP           None

378	JUMP_FORWARD      '382'
381	END_FINALLY       None
382_0	COME_FROM         '362'
382_1	COME_FROM         '381'

382	LOAD_FAST         'self'
385	LOAD_ATTR         'db'
388	LOAD_ATTR         'delete'
391	LOAD_GLOBAL       '_table_names_key'
394	LOAD_CONST        'txn'
397	LOAD_FAST         'txn'
400	CALL_FUNCTION_257 None
403	POP_TOP           None

404	LOAD_GLOBAL       'getattr'
407	LOAD_FAST         'self'
410	LOAD_ATTR         'db'
413	LOAD_CONST        'put_bytes'
416	LOAD_FAST         'self'
419	LOAD_ATTR         'db'
422	LOAD_ATTR         'put'
425	CALL_FUNCTION_3   None
428	LOAD_GLOBAL       '_table_names_key'

431	LOAD_GLOBAL       'pickle'
434	LOAD_ATTR         'dumps'
437	LOAD_FAST         'tablelist'
440	LOAD_CONST        1
443	CALL_FUNCTION_2   None
446	LOAD_CONST        'txn'
449	LOAD_FAST         'txn'
452	CALL_FUNCTION_258 None
455	POP_TOP           None

456	LOAD_FAST         'txn'
459	LOAD_ATTR         'commit'
462	CALL_FUNCTION_0   None
465	POP_TOP           None

466	LOAD_CONST        None
469	STORE_FAST        'txn'

472	LOAD_FAST         'table'
475	LOAD_FAST         'self'
478	LOAD_ATTR         '__tablecolumns'
481	COMPARE_OP        'in'
484	POP_JUMP_IF_FALSE '500'

487	LOAD_FAST         'self'
490	LOAD_ATTR         '__tablecolumns'
493	LOAD_FAST         'table'
496	DELETE_SUBSCR     None
497	JUMP_FORWARD      '500'
500_0	COME_FROM         '497'
500	POP_BLOCK         None
501	JUMP_FORWARD      '564'
504_0	COME_FROM         '6'

504	DUP_TOP           None
505	LOAD_GLOBAL       'db'
508	LOAD_ATTR         'DBError'
511	COMPARE_OP        'exception match'
514	POP_JUMP_IF_FALSE '563'
517	POP_TOP           None
518	STORE_FAST        'dberror'
521	POP_TOP           None

522	LOAD_FAST         'txn'
525	POP_JUMP_IF_FALSE '541'

528	LOAD_FAST         'txn'
531	LOAD_ATTR         'abort'
534	CALL_FUNCTION_0   None
537	POP_TOP           None
538	JUMP_FORWARD      '541'
541_0	COME_FROM         '538'

541	LOAD_GLOBAL       'TableDBError'
544	LOAD_FAST         'dberror'
547	LOAD_ATTR         'args'
550	LOAD_CONST        1
553	BINARY_SUBSCR     None
554	CALL_FUNCTION_1   None
557	RAISE_VARARGS_1   None
560	JUMP_FORWARD      '564'
563	END_FINALLY       None
564_0	COME_FROM         '501'
564_1	COME_FROM         '563'
564	LOAD_CONST        None
567	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 173