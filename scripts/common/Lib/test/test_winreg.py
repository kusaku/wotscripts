# Embedded file name: scripts/common/Lib/test/test_winreg.py
import os, sys
import unittest
from test import test_support
threading = test_support.import_module('threading')
from platform import machine
test_support.import_module('_winreg')
from _winreg import *
try:
    REMOTE_NAME = sys.argv[sys.argv.index('--remote') + 1]
except (IndexError, ValueError):
    REMOTE_NAME = None

WIN_VER = sys.getwindowsversion()[:2]
WIN64_MACHINE = True if machine() == 'AMD64' else False
HAS_REFLECTION = True if WIN_VER < (6, 1) else False
test_key_name = 'SOFTWARE\\Python Registry Test Key - Delete Me'
test_reflect_key_name = 'SOFTWARE\\Classes\\Python Test Key - Delete Me'
test_data = [('Int Value', 45, REG_DWORD),
 ('String Val', 'A string value', REG_SZ),
 ('StringExpand', 'The path is %path%', REG_EXPAND_SZ),
 ('Multi-string', ['Lots',
   'of',
   'string',
   'values'], REG_MULTI_SZ),
 ('Raw Data', 'binary' + chr(0) + 'data', REG_BINARY),
 ('Big String', 'x' * 16383, REG_SZ),
 ('Big Binary', 'x' * 16384, REG_BINARY)]
if test_support.have_unicode:
    test_data += [(unicode('Unicode Val'), unicode('A Unicode value'), REG_SZ),
     ('UnicodeExpand', unicode('The path is %path%'), REG_EXPAND_SZ),
     ('Multi-unicode', [unicode('Lots'),
       unicode('of'),
       unicode('unicode'),
       unicode('values')], REG_MULTI_SZ),
     ('Multi-mixed', [unicode('Unicode'),
       unicode('and'),
       'string',
       'values'], REG_MULTI_SZ)]

class BaseWinregTests(unittest.TestCase):

    def setUp(self):
        self.delete_tree(HKEY_CURRENT_USER, test_key_name)

    def delete_tree(self, root, subkey):
        try:
            hkey = OpenKey(root, subkey, KEY_ALL_ACCESS)
        except WindowsError:
            return

        while True:
            try:
                subsubkey = EnumKey(hkey, 0)
            except WindowsError:
                break

            self.delete_tree(hkey, subsubkey)

        CloseKey(hkey)
        DeleteKey(root, subkey)

    def _write_test_data(self, root_key, CreateKey = CreateKey):
        SetValue(root_key, test_key_name, REG_SZ, 'Default value')
        key = CreateKey(root_key, test_key_name)
        sub_key = CreateKey(key, 'sub_key')
        for value_name, value_data, value_type in test_data:
            SetValueEx(sub_key, value_name, 0, value_type, value_data)

        nkeys, nvalues, since_mod = QueryInfoKey(key)
        self.assertEqual(nkeys, 1, 'Not the correct number of sub keys')
        self.assertEqual(nvalues, 1, 'Not the correct number of values')
        nkeys, nvalues, since_mod = QueryInfoKey(sub_key)
        self.assertEqual(nkeys, 0, 'Not the correct number of sub keys')
        self.assertEqual(nvalues, len(test_data), 'Not the correct number of values')
        int_sub_key = int(sub_key)
        CloseKey(sub_key)
        try:
            QueryInfoKey(int_sub_key)
            self.fail('It appears the CloseKey() function does not close the actual key!')
        except EnvironmentError:
            pass

        int_key = int(key)
        key.Close()
        try:
            QueryInfoKey(int_key)
            self.fail('It appears the key.Close() function does not close the actual key!')
        except EnvironmentError:
            pass

    def _read_test_data--- This code section failed: ---

0	LOAD_GLOBAL       'QueryValue'
3	LOAD_FAST         'root_key'
6	LOAD_GLOBAL       'test_key_name'
9	CALL_FUNCTION_2   None
12	STORE_FAST        'val'

15	LOAD_FAST         'self'
18	LOAD_ATTR         'assertEqual'
21	LOAD_FAST         'val'
24	LOAD_CONST        'Default value'

27	LOAD_CONST        "Registry didn't give back the correct value"
30	CALL_FUNCTION_3   None
33	POP_TOP           None

34	LOAD_FAST         'OpenKey'
37	LOAD_FAST         'root_key'
40	LOAD_GLOBAL       'test_key_name'
43	CALL_FUNCTION_2   None
46	STORE_FAST        'key'

49	LOAD_FAST         'OpenKey'
52	LOAD_FAST         'key'
55	LOAD_CONST        'sub_key'
58	CALL_FUNCTION_2   None
61	SETUP_WITH        '263'
64	STORE_FAST        'sub_key'

67	LOAD_CONST        0
70	STORE_FAST        'index'

73	SETUP_LOOP        '149'

76	SETUP_EXCEPT      '98'

79	LOAD_GLOBAL       'EnumValue'
82	LOAD_FAST         'sub_key'
85	LOAD_FAST         'index'
88	CALL_FUNCTION_2   None
91	STORE_FAST        'data'
94	POP_BLOCK         None
95	JUMP_FORWARD      '116'
98_0	COME_FROM         '76'

98	DUP_TOP           None
99	LOAD_GLOBAL       'EnvironmentError'
102	COMPARE_OP        'exception match'
105	POP_JUMP_IF_FALSE '115'
108	POP_TOP           None
109	POP_TOP           None
110	POP_TOP           None

111	BREAK_LOOP        None
112	JUMP_FORWARD      '116'
115	END_FINALLY       None
116_0	COME_FROM         '95'
116_1	COME_FROM         '115'

116	LOAD_FAST         'self'
119	LOAD_ATTR         'assertIn'
122	LOAD_FAST         'data'
125	LOAD_GLOBAL       'test_data'

128	LOAD_CONST        "Didn't read back the correct test data"
131	CALL_FUNCTION_3   None
134	POP_TOP           None

135	LOAD_FAST         'index'
138	LOAD_CONST        1
141	BINARY_ADD        None
142	STORE_FAST        'index'
145	JUMP_BACK         '76'
148	POP_BLOCK         None
149_0	COME_FROM         '73'

149	LOAD_FAST         'self'
152	LOAD_ATTR         'assertEqual'
155	LOAD_FAST         'index'
158	LOAD_GLOBAL       'len'
161	LOAD_GLOBAL       'test_data'
164	CALL_FUNCTION_1   None

167	LOAD_CONST        "Didn't read the correct number of items"
170	CALL_FUNCTION_3   None
173	POP_TOP           None

174	SETUP_LOOP        '259'
177	LOAD_GLOBAL       'test_data'
180	GET_ITER          None
181	FOR_ITER          '258'
184	UNPACK_SEQUENCE_3 None
187	STORE_FAST        'value_name'
190	STORE_FAST        'value_data'
193	STORE_FAST        'value_type'

196	LOAD_GLOBAL       'QueryValueEx'
199	LOAD_FAST         'sub_key'
202	LOAD_FAST         'value_name'
205	CALL_FUNCTION_2   None
208	UNPACK_SEQUENCE_2 None
211	STORE_FAST        'read_val'
214	STORE_FAST        'read_typ'

217	LOAD_FAST         'self'
220	LOAD_ATTR         'assertEqual'
223	LOAD_FAST         'read_val'
226	LOAD_FAST         'value_data'

229	LOAD_CONST        'Could not directly read the value'
232	CALL_FUNCTION_3   None
235	POP_TOP           None

236	LOAD_FAST         'self'
239	LOAD_ATTR         'assertEqual'
242	LOAD_FAST         'read_typ'
245	LOAD_FAST         'value_type'

248	LOAD_CONST        'Could not directly read the value'
251	CALL_FUNCTION_3   None
254	POP_TOP           None
255	JUMP_BACK         '181'
258	POP_BLOCK         None
259_0	COME_FROM         '174'
259	POP_BLOCK         None
260	LOAD_CONST        None
263_0	COME_FROM         '61'
263	WITH_CLEANUP      None
264	END_FINALLY       None

265	LOAD_FAST         'sub_key'
268	LOAD_ATTR         'Close'
271	CALL_FUNCTION_0   None
274	POP_TOP           None

275	LOAD_GLOBAL       'EnumKey'
278	LOAD_FAST         'key'
281	LOAD_CONST        0
284	CALL_FUNCTION_2   None
287	STORE_FAST        'read_val'

290	LOAD_FAST         'self'
293	LOAD_ATTR         'assertEqual'
296	LOAD_FAST         'read_val'
299	LOAD_CONST        'sub_key'
302	LOAD_CONST        'Read subkey value wrong'
305	CALL_FUNCTION_3   None
308	POP_TOP           None

309	SETUP_EXCEPT      '342'

312	LOAD_GLOBAL       'EnumKey'
315	LOAD_FAST         'key'
318	LOAD_CONST        1
321	CALL_FUNCTION_2   None
324	POP_TOP           None

325	LOAD_FAST         'self'
328	LOAD_ATTR         'fail'
331	LOAD_CONST        'Was able to get a second key when I only have one!'
334	CALL_FUNCTION_1   None
337	POP_TOP           None
338	POP_BLOCK         None
339	JUMP_FORWARD      '359'
342_0	COME_FROM         '309'

342	DUP_TOP           None
343	LOAD_GLOBAL       'EnvironmentError'
346	COMPARE_OP        'exception match'
349	POP_JUMP_IF_FALSE '358'
352	POP_TOP           None
353	POP_TOP           None
354	POP_TOP           None

355	JUMP_FORWARD      '359'
358	END_FINALLY       None
359_0	COME_FROM         '339'
359_1	COME_FROM         '358'

359	LOAD_FAST         'key'
362	LOAD_ATTR         'Close'
365	CALL_FUNCTION_0   None
368	POP_TOP           None

Syntax error at or near `POP_BLOCK' token at offset 148

    def _delete_test_data(self, root_key):
        key = OpenKey(root_key, test_key_name, 0, KEY_ALL_ACCESS)
        sub_key = OpenKey(key, 'sub_key', 0, KEY_ALL_ACCESS)
        for value_name, value_data, value_type in test_data:
            DeleteValue(sub_key, value_name)

        nkeys, nvalues, since_mod = QueryInfoKey(sub_key)
        self.assertEqual(nkeys, 0, 'subkey not empty before delete')
        self.assertEqual(nvalues, 0, 'subkey not empty before delete')
        sub_key.Close()
        DeleteKey(key, 'sub_key')
        try:
            DeleteKey(key, 'sub_key')
            self.fail('Deleting the key twice succeeded')
        except EnvironmentError:
            pass

        key.Close()
        DeleteKey(root_key, test_key_name)
        try:
            key = OpenKey(root_key, test_key_name)
            self.fail('Could open the non-existent key')
        except WindowsError:
            pass

    def _test_all(self, root_key):
        self._write_test_data(root_key)
        self._read_test_data(root_key)
        self._delete_test_data(root_key)


class LocalWinregTests(BaseWinregTests):

    def test_registry_works(self):
        self._test_all(HKEY_CURRENT_USER)

    def test_registry_works_extended_functions(self):
        cke = lambda key, sub_key: CreateKeyEx(key, sub_key, 0, KEY_ALL_ACCESS)
        self._write_test_data(HKEY_CURRENT_USER, cke)
        oke = lambda key, sub_key: OpenKeyEx(key, sub_key, 0, KEY_READ)
        self._read_test_data(HKEY_CURRENT_USER, oke)
        self._delete_test_data(HKEY_CURRENT_USER)

    def test_connect_registry_to_local_machine_works(self):
        h = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        self.assertNotEqual(h.handle, 0)
        h.Close()
        self.assertEqual(h.handle, 0)
        return

    def test_inexistant_remote_registry(self):
        connect = lambda : ConnectRegistry('abcdefghijkl', HKEY_CURRENT_USER)
        self.assertRaises(WindowsError, connect)

    def test_expand_environment_strings(self):
        r = ExpandEnvironmentStrings(u'%windir%\\test')
        self.assertEqual(type(r), unicode)
        self.assertEqual(r, os.environ['windir'] + '\\test')

    def test_context_manager(self):
        try:
            with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as h:
                self.assertNotEqual(h.handle, 0)
                raise WindowsError
        except WindowsError:
            self.assertEqual(h.handle, 0)

        return

    def test_changing_value(self):
        done = False

        class VeryActiveThread(threading.Thread):

            def run(self):
                with CreateKey(HKEY_CURRENT_USER, test_key_name) as key:
                    use_short = True
                    long_string = 'x' * 2000
                    while not done:
                        s = 'x' if use_short else long_string
                        use_short = not use_short
                        SetValue(key, 'changing_value', REG_SZ, s)

        thread = VeryActiveThread()
        thread.start()
        try:
            with CreateKey(HKEY_CURRENT_USER, test_key_name + '\\changing_value') as key:
                for _ in range(1000):
                    num_subkeys, num_values, t = QueryInfoKey(key)
                    for i in range(num_values):
                        name = EnumValue(key, i)
                        QueryValue(key, name[0])

        finally:
            done = True
            thread.join()
            with OpenKey(HKEY_CURRENT_USER, test_key_name, 0, KEY_ALL_ACCESS) as key:
                DeleteKey(key, 'changing_value')
            DeleteKey(HKEY_CURRENT_USER, test_key_name)

    def test_long_key(self):
        name = 'x' * 256
        try:
            with CreateKey(HKEY_CURRENT_USER, test_key_name) as key:
                SetValue(key, name, REG_SZ, 'x')
                num_subkeys, num_values, t = QueryInfoKey(key)
                EnumKey(key, 0)
        finally:
            with OpenKey(HKEY_CURRENT_USER, test_key_name, 0, KEY_ALL_ACCESS) as key:
                DeleteKey(key, name)
            DeleteKey(HKEY_CURRENT_USER, test_key_name)

    def test_dynamic_key(self):
        EnumValue(HKEY_PERFORMANCE_DATA, 0)
        QueryValueEx(HKEY_PERFORMANCE_DATA, None)
        return

    @unittest.skipUnless(WIN_VER < (5, 2), 'Requires Windows XP')
    def test_reflection_unsupported(self):
        try:
            with CreateKey(HKEY_CURRENT_USER, test_key_name) as ck:
                self.assertNotEqual(ck.handle, 0)
            key = OpenKey(HKEY_CURRENT_USER, test_key_name)
            self.assertNotEqual(key.handle, 0)
            with self.assertRaises(NotImplementedError):
                DisableReflectionKey(key)
            with self.assertRaises(NotImplementedError):
                EnableReflectionKey(key)
            with self.assertRaises(NotImplementedError):
                QueryReflectionKey(key)
            with self.assertRaises(NotImplementedError):
                DeleteKeyEx(HKEY_CURRENT_USER, test_key_name)
        finally:
            DeleteKey(HKEY_CURRENT_USER, test_key_name)


@unittest.skipUnless(REMOTE_NAME, 'Skipping remote registry tests')

class RemoteWinregTests(BaseWinregTests):

    def test_remote_registry_works(self):
        remote_key = ConnectRegistry(REMOTE_NAME, HKEY_CURRENT_USER)
        self._test_all(remote_key)


@unittest.skipUnless(WIN64_MACHINE, 'x64 specific registry tests')

class Win64WinregTests(BaseWinregTests):

    def test_reflection_functions(self):
        with OpenKey(HKEY_LOCAL_MACHINE, 'Software') as key:
            self.assertTrue(QueryReflectionKey(key))
            self.assertEqual(None, EnableReflectionKey(key))
            self.assertEqual(None, DisableReflectionKey(key))
            self.assertTrue(QueryReflectionKey(key))
        return

    @unittest.skipUnless(HAS_REFLECTION, "OS doesn't support reflection")
    def test_reflection(self):
        try:
            with CreateKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_ALL_ACCESS | KEY_WOW64_32KEY) as created_key:
                self.assertNotEqual(created_key.handle, 0)
                with OpenKey(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_ALL_ACCESS | KEY_WOW64_32KEY) as key:
                    self.assertNotEqual(key.handle, 0)
                SetValueEx(created_key, '', 0, REG_SZ, '32KEY')
                open_fail = lambda : OpenKey(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_READ | KEY_WOW64_64KEY)
                self.assertRaises(WindowsError, open_fail)
            with OpenKey(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_ALL_ACCESS | KEY_WOW64_64KEY) as key:
                self.assertNotEqual(key.handle, 0)
                self.assertEqual('32KEY', QueryValue(key, ''))
                SetValueEx(key, '', 0, REG_SZ, '64KEY')
            with OpenKey(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_READ | KEY_WOW64_32KEY) as key:
                self.assertEqual('64KEY', QueryValue(key, ''))
        finally:
            DeleteKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, KEY_WOW64_32KEY, 0)

    @unittest.skipUnless(HAS_REFLECTION, "OS doesn't support reflection")
    def test_disable_reflection(self):
        try:
            with CreateKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_ALL_ACCESS | KEY_WOW64_32KEY) as created_key:
                disabled = QueryReflectionKey(created_key)
                self.assertEqual(type(disabled), bool)
                self.assertFalse(disabled)
                DisableReflectionKey(created_key)
                self.assertTrue(QueryReflectionKey(created_key))
            open_fail = lambda : OpenKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_READ | KEY_WOW64_64KEY)
            self.assertRaises(WindowsError, open_fail)
            with OpenKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, 0, KEY_READ | KEY_WOW64_32KEY) as key:
                self.assertNotEqual(key.handle, 0)
        finally:
            DeleteKeyEx(HKEY_CURRENT_USER, test_reflect_key_name, KEY_WOW64_32KEY, 0)


def test_main():
    test_support.run_unittest(LocalWinregTests, RemoteWinregTests, Win64WinregTests)


if __name__ == '__main__':
    if not REMOTE_NAME:
        print 'Remote registry calls can be tested using',
        print "'test_winreg.py --remote \\\\machine_name'"
    test_main()