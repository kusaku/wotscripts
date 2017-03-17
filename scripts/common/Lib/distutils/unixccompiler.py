# Embedded file name: scripts/common/Lib/distutils/unixccompiler.py
"""distutils.unixccompiler

Contains the UnixCCompiler class, a subclass of CCompiler that handles
the "typical" Unix-style command-line C compiler:
  * macros defined with -Dname[=value]
  * macros undefined with -Uname
  * include search directories specified with -Idir
  * libraries specified with -lllib
  * library search directories specified with -Ldir
  * compile handled by 'cc' (or similar) executable with -c option:
    compiles .c to .o
  * link static library handled by 'ar' command (possibly with 'ranlib')
  * link shared library handled by 'cc -shared'
"""
__revision__ = '$Id$'
import os, sys, re
from types import StringType, NoneType
from distutils import sysconfig
from distutils.dep_util import newer
from distutils.ccompiler import CCompiler, gen_preprocess_options, gen_lib_options
from distutils.errors import DistutilsExecError, CompileError, LibError, LinkError
from distutils import log

def _darwin_compiler_fixup--- This code section failed: ---

0	LOAD_CONST        0
3	DUP_TOP           None
4	STORE_FAST        'stripArch'
7	STORE_FAST        'stripSysroot'

10	LOAD_GLOBAL       'list'
13	LOAD_FAST         'compiler_so'
16	CALL_FUNCTION_1   None
19	STORE_FAST        'compiler_so'

22	LOAD_GLOBAL       'os'
25	LOAD_ATTR         'uname'
28	CALL_FUNCTION_0   None
31	LOAD_CONST        2
34	BINARY_SUBSCR     None
35	STORE_FAST        'kernel_version'

38	LOAD_GLOBAL       'int'
41	LOAD_FAST         'kernel_version'
44	LOAD_ATTR         'split'
47	LOAD_CONST        '.'
50	CALL_FUNCTION_1   None
53	LOAD_CONST        0
56	BINARY_SUBSCR     None
57	CALL_FUNCTION_1   None
60	STORE_FAST        'major_version'

63	LOAD_FAST         'major_version'
66	LOAD_CONST        8
69	COMPARE_OP        '<'
72	POP_JUMP_IF_FALSE '88'

75	LOAD_GLOBAL       'True'
78	DUP_TOP           None
79	STORE_FAST        'stripArch'
82	STORE_FAST        'stripSysroot'
85	JUMP_FORWARD      '112'

88	LOAD_CONST        '-arch'
91	LOAD_FAST         'cc_args'
94	COMPARE_OP        'in'
97	STORE_FAST        'stripArch'

100	LOAD_CONST        '-isysroot'
103	LOAD_FAST         'cc_args'
106	COMPARE_OP        'in'
109	STORE_FAST        'stripSysroot'
112_0	COME_FROM         '85'

112	LOAD_FAST         'stripArch'
115	POP_JUMP_IF_TRUE  '133'
118	LOAD_CONST        'ARCHFLAGS'
121	LOAD_GLOBAL       'os'
124	LOAD_ATTR         'environ'
127	COMPARE_OP        'in'
130_0	COME_FROM         '115'
130	POP_JUMP_IF_FALSE '197'

133	SETUP_LOOP        '197'

136	SETUP_EXCEPT      '172'

139	LOAD_FAST         'compiler_so'
142	LOAD_ATTR         'index'
145	LOAD_CONST        '-arch'
148	CALL_FUNCTION_1   None
151	STORE_FAST        'index'

154	LOAD_FAST         'compiler_so'
157	LOAD_FAST         'index'
160	LOAD_FAST         'index'
163	LOAD_CONST        2
166	BINARY_ADD        None
167	DELETE_SLICE+3    None
168	POP_BLOCK         None
169	JUMP_BACK         '136'
172_0	COME_FROM         '136'

172	DUP_TOP           None
173	LOAD_GLOBAL       'ValueError'
176	COMPARE_OP        'exception match'
179	POP_JUMP_IF_FALSE '189'
182	POP_TOP           None
183	POP_TOP           None
184	POP_TOP           None

185	BREAK_LOOP        None
186	JUMP_BACK         '136'
189	END_FINALLY       None
190_0	COME_FROM         '189'
190	JUMP_BACK         '136'
193	POP_BLOCK         None
194_0	COME_FROM         '133'
194	JUMP_FORWARD      '197'
197_0	COME_FROM         '194'

197	LOAD_CONST        'ARCHFLAGS'
200	LOAD_GLOBAL       'os'
203	LOAD_ATTR         'environ'
206	COMPARE_OP        'in'
209	POP_JUMP_IF_FALSE '245'
212	LOAD_FAST         'stripArch'
215	UNARY_NOT         None
216_0	COME_FROM         '209'
216	POP_JUMP_IF_FALSE '245'

219	LOAD_FAST         'compiler_so'
222	LOAD_GLOBAL       'os'
225	LOAD_ATTR         'environ'
228	LOAD_CONST        'ARCHFLAGS'
231	BINARY_SUBSCR     None
232	LOAD_ATTR         'split'
235	CALL_FUNCTION_0   None
238	BINARY_ADD        None
239	STORE_FAST        'compiler_so'
242	JUMP_FORWARD      '245'
245_0	COME_FROM         '242'

245	LOAD_FAST         'stripSysroot'
248	POP_JUMP_IF_FALSE '307'

251	SETUP_EXCEPT      '287'

254	LOAD_FAST         'compiler_so'
257	LOAD_ATTR         'index'
260	LOAD_CONST        '-isysroot'
263	CALL_FUNCTION_1   None
266	STORE_FAST        'index'

269	LOAD_FAST         'compiler_so'
272	LOAD_FAST         'index'
275	LOAD_FAST         'index'
278	LOAD_CONST        2
281	BINARY_ADD        None
282	DELETE_SLICE+3    None
283	POP_BLOCK         None
284	JUMP_ABSOLUTE     '307'
287_0	COME_FROM         '251'

287	DUP_TOP           None
288	LOAD_GLOBAL       'ValueError'
291	COMPARE_OP        'exception match'
294	POP_JUMP_IF_FALSE '303'
297	POP_TOP           None
298	POP_TOP           None
299	POP_TOP           None

300	JUMP_ABSOLUTE     '307'
303	END_FINALLY       None
304_0	COME_FROM         '303'
304	JUMP_FORWARD      '307'
307_0	COME_FROM         '304'

307	LOAD_CONST        None
310	STORE_FAST        'sysroot'

313	LOAD_CONST        '-isysroot'
316	LOAD_FAST         'cc_args'
319	COMPARE_OP        'in'
322	POP_JUMP_IF_FALSE '357'

325	LOAD_FAST         'cc_args'
328	LOAD_ATTR         'index'
331	LOAD_CONST        '-isysroot'
334	CALL_FUNCTION_1   None
337	STORE_FAST        'idx'

340	LOAD_FAST         'cc_args'
343	LOAD_FAST         'idx'
346	LOAD_CONST        1
349	BINARY_ADD        None
350	BINARY_SUBSCR     None
351	STORE_FAST        'sysroot'
354	JUMP_FORWARD      '401'

357	LOAD_CONST        '-isysroot'
360	LOAD_FAST         'compiler_so'
363	COMPARE_OP        'in'
366	POP_JUMP_IF_FALSE '401'

369	LOAD_FAST         'compiler_so'
372	LOAD_ATTR         'index'
375	LOAD_CONST        '-isysroot'
378	CALL_FUNCTION_1   None
381	STORE_FAST        'idx'

384	LOAD_FAST         'compiler_so'
387	LOAD_FAST         'idx'
390	LOAD_CONST        1
393	BINARY_ADD        None
394	BINARY_SUBSCR     None
395	STORE_FAST        'sysroot'
398	JUMP_FORWARD      '401'
401_0	COME_FROM         '354'
401_1	COME_FROM         '398'

401	LOAD_FAST         'sysroot'
404	POP_JUMP_IF_FALSE '458'
407	LOAD_GLOBAL       'os'
410	LOAD_ATTR         'path'
413	LOAD_ATTR         'isdir'
416	LOAD_FAST         'sysroot'
419	CALL_FUNCTION_1   None
422	UNARY_NOT         None
423_0	COME_FROM         '404'
423	POP_JUMP_IF_FALSE '458'

426	LOAD_GLOBAL       'log'
429	LOAD_ATTR         'warn'
432	LOAD_CONST        "Compiling with an SDK that doesn't seem to exist: %s"

435	LOAD_FAST         'sysroot'
438	CALL_FUNCTION_2   None
441	POP_TOP           None

442	LOAD_GLOBAL       'log'
445	LOAD_ATTR         'warn'
448	LOAD_CONST        'Please check your Xcode installation'
451	CALL_FUNCTION_1   None
454	POP_TOP           None
455	JUMP_FORWARD      '458'
458_0	COME_FROM         '455'

458	LOAD_FAST         'compiler_so'
461	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 193


class UnixCCompiler(CCompiler):
    compiler_type = 'unix'
    executables = {'preprocessor': None,
     'compiler': ['cc'],
     'compiler_so': ['cc'],
     'compiler_cxx': ['cc'],
     'linker_so': ['cc', '-shared'],
     'linker_exe': ['cc'],
     'archiver': ['ar', '-cr'],
     'ranlib': None}
    if sys.platform[:6] == 'darwin':
        executables['ranlib'] = ['ranlib']
    src_extensions = ['.c',
     '.C',
     '.cc',
     '.cxx',
     '.cpp',
     '.m']
    obj_extension = '.o'
    static_lib_extension = '.a'
    shared_lib_extension = '.so'
    dylib_lib_extension = '.dylib'
    static_lib_format = shared_lib_format = dylib_lib_format = 'lib%s%s'
    if sys.platform == 'cygwin':
        exe_extension = '.exe'

    def preprocess(self, source, output_file = None, macros = None, include_dirs = None, extra_preargs = None, extra_postargs = None):
        ignore, macros, include_dirs = self._fix_compile_args(None, macros, include_dirs)
        pp_opts = gen_preprocess_options(macros, include_dirs)
        pp_args = self.preprocessor + pp_opts
        if output_file:
            pp_args.extend(['-o', output_file])
        if extra_preargs:
            pp_args[:0] = extra_preargs
        if extra_postargs:
            pp_args.extend(extra_postargs)
        pp_args.append(source)
        if self.force or output_file is None or newer(source, output_file):
            if output_file:
                self.mkpath(os.path.dirname(output_file))
            try:
                self.spawn(pp_args)
            except DistutilsExecError as msg:
                raise CompileError, msg

        return

    def _compile(self, obj, src, ext, cc_args, extra_postargs, pp_opts):
        compiler_so = self.compiler_so
        if sys.platform == 'darwin':
            compiler_so = _darwin_compiler_fixup(compiler_so, cc_args + extra_postargs)
        try:
            self.spawn(compiler_so + cc_args + [src, '-o', obj] + extra_postargs)
        except DistutilsExecError as msg:
            raise CompileError, msg

    def create_static_lib(self, objects, output_libname, output_dir = None, debug = 0, target_lang = None):
        objects, output_dir = self._fix_object_args(objects, output_dir)
        output_filename = self.library_filename(output_libname, output_dir=output_dir)
        if self._need_link(objects, output_filename):
            self.mkpath(os.path.dirname(output_filename))
            self.spawn(self.archiver + [output_filename] + objects + self.objects)
            if self.ranlib:
                try:
                    self.spawn(self.ranlib + [output_filename])
                except DistutilsExecError as msg:
                    raise LibError, msg

        else:
            log.debug('skipping %s (up-to-date)', output_filename)

    def link(self, target_desc, objects, output_filename, output_dir = None, libraries = None, library_dirs = None, runtime_library_dirs = None, export_symbols = None, debug = 0, extra_preargs = None, extra_postargs = None, build_temp = None, target_lang = None):
        objects, output_dir = self._fix_object_args(objects, output_dir)
        libraries, library_dirs, runtime_library_dirs = self._fix_lib_args(libraries, library_dirs, runtime_library_dirs)
        lib_opts = gen_lib_options(self, library_dirs, runtime_library_dirs, libraries)
        if type(output_dir) not in (StringType, NoneType):
            raise TypeError, "'output_dir' must be a string or None"
        if output_dir is not None:
            output_filename = os.path.join(output_dir, output_filename)
        if self._need_link(objects, output_filename):
            ld_args = objects + self.objects + lib_opts + ['-o', output_filename]
            if debug:
                ld_args[:0] = ['-g']
            if extra_preargs:
                ld_args[:0] = extra_preargs
            if extra_postargs:
                ld_args.extend(extra_postargs)
            self.mkpath(os.path.dirname(output_filename))
            try:
                if target_desc == CCompiler.EXECUTABLE:
                    linker = self.linker_exe[:]
                else:
                    linker = self.linker_so[:]
                if target_lang == 'c++' and self.compiler_cxx:
                    i = 0
                    if os.path.basename(linker[0]) == 'env':
                        i = 1
                        while '=' in linker[i]:
                            i = i + 1

                    linker[i] = self.compiler_cxx[i]
                if sys.platform == 'darwin':
                    linker = _darwin_compiler_fixup(linker, ld_args)
                self.spawn(linker + ld_args)
            except DistutilsExecError as msg:
                raise LinkError, msg

        else:
            log.debug('skipping %s (up-to-date)', output_filename)
        return

    def library_dir_option(self, dir):
        return '-L' + dir

    def _is_gcc(self, compiler_name):
        return 'gcc' in compiler_name or 'g++' in compiler_name

    def runtime_library_dir_option(self, dir):
        compiler = os.path.basename(sysconfig.get_config_var('CC'))
        if sys.platform[:6] == 'darwin':
            return '-L' + dir
        elif sys.platform[:5] == 'hp-ux':
            if self._is_gcc(compiler):
                return ['-Wl,+s', '-L' + dir]
            return ['+s', '-L' + dir]
        elif sys.platform[:7] == 'irix646' or sys.platform[:6] == 'osf1V5':
            return ['-rpath', dir]
        elif self._is_gcc(compiler):
            return '-Wl,-R' + dir
        else:
            return '-R' + dir

    def library_option(self, lib):
        return '-l' + lib

    def find_library_file(self, dirs, lib, debug = 0):
        shared_f = self.library_filename(lib, lib_type='shared')
        dylib_f = self.library_filename(lib, lib_type='dylib')
        static_f = self.library_filename(lib, lib_type='static')
        if sys.platform == 'darwin':
            cflags = sysconfig.get_config_var('CFLAGS')
            m = re.search('-isysroot\\s+(\\S+)', cflags)
            if m is None:
                sysroot = '/'
            else:
                sysroot = m.group(1)
        for dir in dirs:
            shared = os.path.join(dir, shared_f)
            dylib = os.path.join(dir, dylib_f)
            static = os.path.join(dir, static_f)
            if sys.platform == 'darwin' and (dir.startswith('/System/') or dir.startswith('/usr/') and not dir.startswith('/usr/local/')):
                shared = os.path.join(sysroot, dir[1:], shared_f)
                dylib = os.path.join(sysroot, dir[1:], dylib_f)
                static = os.path.join(sysroot, dir[1:], static_f)
            if os.path.exists(dylib):
                return dylib
            if os.path.exists(shared):
                return shared
            if os.path.exists(static):
                return static

        return