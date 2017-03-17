# Embedded file name: scripts/common/Lib/distutils/sysconfig.py
"""Provide access to Python's configuration information.  The specific
configuration variables available depend heavily on the platform and
configuration.  The values may be retrieved using
get_config_var(name), and the list of variables is available via
get_config_vars().keys().  Additional convenience functions are also
available.

Written by:   Fred L. Drake, Jr.
Email:        <fdrake@acm.org>
"""
__revision__ = '$Id$'
import os
import re
import string
import sys
from distutils.errors import DistutilsPlatformError
PREFIX = os.path.normpath(sys.prefix)
EXEC_PREFIX = os.path.normpath(sys.exec_prefix)
project_base = os.path.dirname(os.path.abspath(sys.executable))
if os.name == 'nt' and 'pcbuild' in project_base[-8:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir))
if os.name == 'nt' and '\\pc\\v' in project_base[-10:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir, os.path.pardir))
if os.name == 'nt' and '\\pcbuild\\amd64' in project_base[-14:].lower():
    project_base = os.path.abspath(os.path.join(project_base, os.path.pardir, os.path.pardir))

def _python_build():
    for fn in ('Setup.dist', 'Setup.local'):
        if os.path.isfile(os.path.join(project_base, 'Modules', fn)):
            return True

    return False


python_build = _python_build()

def get_python_version():
    """Return a string containing the major and minor Python version,
    leaving off the patchlevel.  Sample return values could be '1.5'
    or '2.2'.
    """
    return sys.version[:3]


def get_python_inc(plat_specific = 0, prefix = None):
    """Return the directory containing installed Python header files.
    
    If 'plat_specific' is false (the default), this is the path to the
    non-platform-specific header files, i.e. Python.h and so on;
    otherwise, this is the path to platform-specific header files
    (namely pyconfig.h).
    
    If 'prefix' is supplied, use it instead of sys.prefix or
    sys.exec_prefix -- i.e., ignore 'plat_specific'.
    """
    if prefix is None:
        prefix = plat_specific and EXEC_PREFIX or PREFIX
    if os.name == 'posix':
        if python_build:
            buildir = os.path.dirname(sys.executable)
            if plat_specific:
                inc_dir = buildir
            else:
                srcdir = os.path.abspath(os.path.join(buildir, get_config_var('srcdir')))
                inc_dir = os.path.join(srcdir, 'Include')
            return inc_dir
        return os.path.join(prefix, 'include', 'python' + get_python_version())
    elif os.name == 'nt':
        return os.path.join(prefix, 'include')
    elif os.name == 'os2':
        return os.path.join(prefix, 'Include')
    else:
        raise DistutilsPlatformError("I don't know where Python installs its C header files on platform '%s'" % os.name)
        return


def get_python_lib(plat_specific = 0, standard_lib = 0, prefix = None):
    """Return the directory containing the Python library (standard or
    site additions).
    
    If 'plat_specific' is true, return the directory containing
    platform-specific modules, i.e. any module from a non-pure-Python
    module distribution; otherwise, return the platform-shared library
    directory.  If 'standard_lib' is true, return the directory
    containing standard Python library modules; otherwise, return the
    directory for site-specific modules.
    
    If 'prefix' is supplied, use it instead of sys.prefix or
    sys.exec_prefix -- i.e., ignore 'plat_specific'.
    """
    if prefix is None:
        prefix = plat_specific and EXEC_PREFIX or PREFIX
    if os.name == 'posix':
        libpython = os.path.join(prefix, 'lib', 'python' + get_python_version())
        if standard_lib:
            return libpython
        else:
            return os.path.join(libpython, 'site-packages')
    elif os.name == 'nt':
        if standard_lib:
            return os.path.join(prefix, 'Lib')
        elif get_python_version() < '2.2':
            return prefix
        else:
            return os.path.join(prefix, 'Lib', 'site-packages')
    elif os.name == 'os2':
        if standard_lib:
            return os.path.join(prefix, 'Lib')
        else:
            return os.path.join(prefix, 'Lib', 'site-packages')
    else:
        raise DistutilsPlatformError("I don't know where Python installs its library on platform '%s'" % os.name)
    return


_USE_CLANG = None

def customize_compiler(compiler):
    """Do any platform-specific customization of a CCompiler instance.
    
    Mainly needed on Unix, so we can plug in the information that
    varies across Unices and is stored in Python's Makefile.
    """
    global _USE_CLANG
    if compiler.compiler_type == 'unix':
        cc, cxx, opt, cflags, ccshared, ldshared, so_ext, ar, ar_flags = get_config_vars('CC', 'CXX', 'OPT', 'CFLAGS', 'CCSHARED', 'LDSHARED', 'SO', 'AR', 'ARFLAGS')
        newcc = None
        if 'CC' in os.environ:
            newcc = os.environ['CC']
        elif sys.platform == 'darwin' and cc == 'gcc-4.2':
            if _USE_CLANG is None:
                from distutils import log
                from subprocess import Popen, PIPE
                p = Popen('! type gcc-4.2 && type clang && exit 2', shell=True, stdout=PIPE, stderr=PIPE)
                p.wait()
                if p.returncode == 2:
                    _USE_CLANG = True
                    log.warn('gcc-4.2 not found, using clang instead')
                else:
                    _USE_CLANG = False
            if _USE_CLANG:
                newcc = 'clang'
        if newcc:
            if sys.platform == 'darwin' and 'LDSHARED' not in os.environ and ldshared.startswith(cc):
                ldshared = newcc + ldshared[len(cc):]
            cc = newcc
        if 'CXX' in os.environ:
            cxx = os.environ['CXX']
        if 'LDSHARED' in os.environ:
            ldshared = os.environ['LDSHARED']
        if 'CPP' in os.environ:
            cpp = os.environ['CPP']
        else:
            cpp = cc + ' -E'
        if 'LDFLAGS' in os.environ:
            ldshared = ldshared + ' ' + os.environ['LDFLAGS']
        if 'CFLAGS' in os.environ:
            cflags = opt + ' ' + os.environ['CFLAGS']
            ldshared = ldshared + ' ' + os.environ['CFLAGS']
        if 'CPPFLAGS' in os.environ:
            cpp = cpp + ' ' + os.environ['CPPFLAGS']
            cflags = cflags + ' ' + os.environ['CPPFLAGS']
            ldshared = ldshared + ' ' + os.environ['CPPFLAGS']
        if 'AR' in os.environ:
            ar = os.environ['AR']
        if 'ARFLAGS' in os.environ:
            archiver = ar + ' ' + os.environ['ARFLAGS']
        else:
            archiver = ar + ' ' + ar_flags
        cc_cmd = cc + ' ' + cflags
        compiler.set_executables(preprocessor=cpp, compiler=cc_cmd, compiler_so=cc_cmd + ' ' + ccshared, compiler_cxx=cxx, linker_so=ldshared, linker_exe=cc, archiver=archiver)
        compiler.shared_lib_extension = so_ext
    return


def get_config_h_filename():
    """Return full pathname of installed pyconfig.h file."""
    if python_build:
        if os.name == 'nt':
            inc_dir = os.path.join(project_base, 'PC')
        else:
            inc_dir = project_base
    else:
        inc_dir = get_python_inc(plat_specific=1)
    if get_python_version() < '2.2':
        config_h = 'config.h'
    else:
        config_h = 'pyconfig.h'
    return os.path.join(inc_dir, config_h)


def get_makefile_filename():
    """Return full pathname of installed Makefile from the Python build."""
    if python_build:
        return os.path.join(os.path.dirname(sys.executable), 'Makefile')
    lib_dir = get_python_lib(plat_specific=1, standard_lib=1)
    return os.path.join(lib_dir, 'config', 'Makefile')


def parse_config_h--- This code section failed: ---

0	LOAD_FAST         'g'
3	LOAD_CONST        None
6	COMPARE_OP        'is'
9	POP_JUMP_IF_FALSE '21'

12	BUILD_MAP         None
15	STORE_FAST        'g'
18	JUMP_FORWARD      '21'
21_0	COME_FROM         '18'

21	LOAD_GLOBAL       're'
24	LOAD_ATTR         'compile'
27	LOAD_CONST        '#define ([A-Z][A-Za-z0-9_]+) (.*)\n'
30	CALL_FUNCTION_1   None
33	STORE_FAST        'define_rx'

36	LOAD_GLOBAL       're'
39	LOAD_ATTR         'compile'
42	LOAD_CONST        '/[*] #undef ([A-Z][A-Za-z0-9_]+) [*]/\n'
45	CALL_FUNCTION_1   None
48	STORE_FAST        'undef_rx'

51	SETUP_LOOP        '217'

54	LOAD_FAST         'fp'
57	LOAD_ATTR         'readline'
60	CALL_FUNCTION_0   None
63	STORE_FAST        'line'

66	LOAD_FAST         'line'
69	POP_JUMP_IF_TRUE  '76'

72	BREAK_LOOP        None
73	JUMP_FORWARD      '76'
76_0	COME_FROM         '73'

76	LOAD_FAST         'define_rx'
79	LOAD_ATTR         'match'
82	LOAD_FAST         'line'
85	CALL_FUNCTION_1   None
88	STORE_FAST        'm'

91	LOAD_FAST         'm'
94	POP_JUMP_IF_FALSE '170'

97	LOAD_FAST         'm'
100	LOAD_ATTR         'group'
103	LOAD_CONST        1
106	LOAD_CONST        2
109	CALL_FUNCTION_2   None
112	UNPACK_SEQUENCE_2 None
115	STORE_FAST        'n'
118	STORE_FAST        'v'

121	SETUP_EXCEPT      '140'
124	LOAD_GLOBAL       'int'
127	LOAD_FAST         'v'
130	CALL_FUNCTION_1   None
133	STORE_FAST        'v'
136	POP_BLOCK         None
137	JUMP_FORWARD      '157'
140_0	COME_FROM         '121'

140	DUP_TOP           None
141	LOAD_GLOBAL       'ValueError'
144	COMPARE_OP        'exception match'
147	POP_JUMP_IF_FALSE '156'
150	POP_TOP           None
151	POP_TOP           None
152	POP_TOP           None
153	JUMP_FORWARD      '157'
156	END_FINALLY       None
157_0	COME_FROM         '137'
157_1	COME_FROM         '156'

157	LOAD_FAST         'v'
160	LOAD_FAST         'g'
163	LOAD_FAST         'n'
166	STORE_SUBSCR      None
167	JUMP_BACK         '54'

170	LOAD_FAST         'undef_rx'
173	LOAD_ATTR         'match'
176	LOAD_FAST         'line'
179	CALL_FUNCTION_1   None
182	STORE_FAST        'm'

185	LOAD_FAST         'm'
188	POP_JUMP_IF_FALSE '54'

191	LOAD_CONST        0
194	LOAD_FAST         'g'
197	LOAD_FAST         'm'
200	LOAD_ATTR         'group'
203	LOAD_CONST        1
206	CALL_FUNCTION_1   None
209	STORE_SUBSCR      None
210	JUMP_BACK         '54'
213	JUMP_BACK         '54'
216	POP_BLOCK         None
217_0	COME_FROM         '51'

217	LOAD_FAST         'g'
220	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 216


_variable_rx = re.compile('([a-zA-Z][a-zA-Z0-9_]+)\\s*=\\s*(.*)')
_findvar1_rx = re.compile('\\$\\(([A-Za-z][A-Za-z0-9_]*)\\)')
_findvar2_rx = re.compile('\\${([A-Za-z][A-Za-z0-9_]*)}')

def parse_makefile--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        ('TextFile',)
6	IMPORT_NAME       'distutils.text_file'
9	IMPORT_FROM       'TextFile'
12	STORE_FAST        'TextFile'
15	POP_TOP           None

16	LOAD_FAST         'TextFile'
19	LOAD_FAST         'fn'
22	LOAD_CONST        'strip_comments'
25	LOAD_CONST        1
28	LOAD_CONST        'skip_blanks'
31	LOAD_CONST        1
34	LOAD_CONST        'join_lines'
37	LOAD_CONST        1
40	CALL_FUNCTION_769 None
43	STORE_FAST        'fp'

46	LOAD_FAST         'g'
49	LOAD_CONST        None
52	COMPARE_OP        'is'
55	POP_JUMP_IF_FALSE '67'

58	BUILD_MAP         None
61	STORE_FAST        'g'
64	JUMP_FORWARD      '67'
67_0	COME_FROM         '64'

67	BUILD_MAP         None
70	STORE_FAST        'done'

73	BUILD_MAP         None
76	STORE_FAST        'notdone'

79	SETUP_LOOP        '285'

82	LOAD_FAST         'fp'
85	LOAD_ATTR         'readline'
88	CALL_FUNCTION_0   None
91	STORE_FAST        'line'

94	LOAD_FAST         'line'
97	LOAD_CONST        None
100	COMPARE_OP        'is'
103	POP_JUMP_IF_FALSE '110'

106	BREAK_LOOP        None
107	JUMP_FORWARD      '110'
110_0	COME_FROM         '107'

110	LOAD_GLOBAL       '_variable_rx'
113	LOAD_ATTR         'match'
116	LOAD_FAST         'line'
119	CALL_FUNCTION_1   None
122	STORE_FAST        'm'

125	LOAD_FAST         'm'
128	POP_JUMP_IF_FALSE '82'

131	LOAD_FAST         'm'
134	LOAD_ATTR         'group'
137	LOAD_CONST        1
140	LOAD_CONST        2
143	CALL_FUNCTION_2   None
146	UNPACK_SEQUENCE_2 None
149	STORE_FAST        'n'
152	STORE_FAST        'v'

155	LOAD_FAST         'v'
158	LOAD_ATTR         'strip'
161	CALL_FUNCTION_0   None
164	STORE_FAST        'v'

167	LOAD_FAST         'v'
170	LOAD_ATTR         'replace'
173	LOAD_CONST        '$$'
176	LOAD_CONST        ''
179	CALL_FUNCTION_2   None
182	STORE_FAST        'tmpv'

185	LOAD_CONST        '$'
188	LOAD_FAST         'tmpv'
191	COMPARE_OP        'in'
194	POP_JUMP_IF_FALSE '210'

197	LOAD_FAST         'v'
200	LOAD_FAST         'notdone'
203	LOAD_FAST         'n'
206	STORE_SUBSCR      None
207	JUMP_ABSOLUTE     '281'

210	SETUP_EXCEPT      '229'

213	LOAD_GLOBAL       'int'
216	LOAD_FAST         'v'
219	CALL_FUNCTION_1   None
222	STORE_FAST        'v'
225	POP_BLOCK         None
226	JUMP_FORWARD      '268'
229_0	COME_FROM         '210'

229	DUP_TOP           None
230	LOAD_GLOBAL       'ValueError'
233	COMPARE_OP        'exception match'
236	POP_JUMP_IF_FALSE '267'
239	POP_TOP           None
240	POP_TOP           None
241	POP_TOP           None

242	LOAD_FAST         'v'
245	LOAD_ATTR         'replace'
248	LOAD_CONST        '$$'
251	LOAD_CONST        '$'
254	CALL_FUNCTION_2   None
257	LOAD_FAST         'done'
260	LOAD_FAST         'n'
263	STORE_SUBSCR      None
264	JUMP_ABSOLUTE     '281'
267	END_FINALLY       None
268_0	COME_FROM         '226'

268	LOAD_FAST         'v'
271	LOAD_FAST         'done'
274	LOAD_FAST         'n'
277	STORE_SUBSCR      None
278_0	COME_FROM         '267'
278	JUMP_BACK         '82'
281	JUMP_BACK         '82'
284	POP_BLOCK         None
285_0	COME_FROM         '79'

285	SETUP_LOOP        '638'
288	LOAD_FAST         'notdone'
291	POP_JUMP_IF_FALSE '637'

294	SETUP_LOOP        '634'
297	LOAD_FAST         'notdone'
300	LOAD_ATTR         'keys'
303	CALL_FUNCTION_0   None
306	GET_ITER          None
307	FOR_ITER          '633'
310	STORE_FAST        'name'

313	LOAD_FAST         'notdone'
316	LOAD_FAST         'name'
319	BINARY_SUBSCR     None
320	STORE_FAST        'value'

323	LOAD_GLOBAL       '_findvar1_rx'
326	LOAD_ATTR         'search'
329	LOAD_FAST         'value'
332	CALL_FUNCTION_1   None
335	JUMP_IF_TRUE_OR_POP '350'
338	LOAD_GLOBAL       '_findvar2_rx'
341	LOAD_ATTR         'search'
344	LOAD_FAST         'value'
347	CALL_FUNCTION_1   None
350_0	COME_FROM         '335'
350	STORE_FAST        'm'

353	LOAD_FAST         'm'
356	POP_JUMP_IF_FALSE '623'

359	LOAD_FAST         'm'
362	LOAD_ATTR         'group'
365	LOAD_CONST        1
368	CALL_FUNCTION_1   None
371	STORE_FAST        'n'

374	LOAD_GLOBAL       'True'
377	STORE_FAST        'found'

380	LOAD_FAST         'n'
383	LOAD_FAST         'done'
386	COMPARE_OP        'in'
389	POP_JUMP_IF_FALSE '411'

392	LOAD_GLOBAL       'str'
395	LOAD_FAST         'done'
398	LOAD_FAST         'n'
401	BINARY_SUBSCR     None
402	CALL_FUNCTION_1   None
405	STORE_FAST        'item'
408	JUMP_FORWARD      '477'

411	LOAD_FAST         'n'
414	LOAD_FAST         'notdone'
417	COMPARE_OP        'in'
420	POP_JUMP_IF_FALSE '432'

423	LOAD_GLOBAL       'False'
426	STORE_FAST        'found'
429	JUMP_FORWARD      '477'

432	LOAD_FAST         'n'
435	LOAD_GLOBAL       'os'
438	LOAD_ATTR         'environ'
441	COMPARE_OP        'in'
444	POP_JUMP_IF_FALSE '463'

447	LOAD_GLOBAL       'os'
450	LOAD_ATTR         'environ'
453	LOAD_FAST         'n'
456	BINARY_SUBSCR     None
457	STORE_FAST        'item'
460	JUMP_FORWARD      '477'

463	LOAD_CONST        ''
466	DUP_TOP           None
467	LOAD_FAST         'done'
470	LOAD_FAST         'n'
473	STORE_SUBSCR      None
474	STORE_FAST        'item'
477_0	COME_FROM         '408'
477_1	COME_FROM         '429'
477_2	COME_FROM         '460'

477	LOAD_FAST         'found'
480	POP_JUMP_IF_FALSE '630'

483	LOAD_FAST         'value'
486	LOAD_FAST         'm'
489	LOAD_ATTR         'end'
492	CALL_FUNCTION_0   None
495	SLICE+1           None
496	STORE_FAST        'after'

499	LOAD_FAST         'value'
502	LOAD_FAST         'm'
505	LOAD_ATTR         'start'
508	CALL_FUNCTION_0   None
511	SLICE+2           None
512	LOAD_FAST         'item'
515	BINARY_ADD        None
516	LOAD_FAST         'after'
519	BINARY_ADD        None
520	STORE_FAST        'value'

523	LOAD_CONST        '$'
526	LOAD_FAST         'after'
529	COMPARE_OP        'in'
532	POP_JUMP_IF_FALSE '548'

535	LOAD_FAST         'value'
538	LOAD_FAST         'notdone'
541	LOAD_FAST         'name'
544	STORE_SUBSCR      None
545	JUMP_ABSOLUTE     '620'

548	SETUP_EXCEPT      '567'
551	LOAD_GLOBAL       'int'
554	LOAD_FAST         'value'
557	CALL_FUNCTION_1   None
560	STORE_FAST        'value'
563	POP_BLOCK         None
564	JUMP_FORWARD      '600'
567_0	COME_FROM         '548'

567	DUP_TOP           None
568	LOAD_GLOBAL       'ValueError'
571	COMPARE_OP        'exception match'
574	POP_JUMP_IF_FALSE '599'
577	POP_TOP           None
578	POP_TOP           None
579	POP_TOP           None

580	LOAD_FAST         'value'
583	LOAD_ATTR         'strip'
586	CALL_FUNCTION_0   None
589	LOAD_FAST         'done'
592	LOAD_FAST         'name'
595	STORE_SUBSCR      None
596	JUMP_FORWARD      '610'
599	END_FINALLY       None
600_0	COME_FROM         '564'

600	LOAD_FAST         'value'
603	LOAD_FAST         'done'
606	LOAD_FAST         'name'
609	STORE_SUBSCR      None
610_0	COME_FROM         '599'

610	LOAD_FAST         'notdone'
613	LOAD_FAST         'name'
616	DELETE_SUBSCR     None
617	JUMP_ABSOLUTE     '630'
620	JUMP_BACK         '307'

623	LOAD_FAST         'notdone'
626	LOAD_FAST         'name'
629	DELETE_SUBSCR     None
630	JUMP_BACK         '307'
633	POP_BLOCK         None
634_0	COME_FROM         '294'
634	JUMP_BACK         '288'
637	POP_BLOCK         None
638_0	COME_FROM         '285'

638	LOAD_FAST         'fp'
641	LOAD_ATTR         'close'
644	CALL_FUNCTION_0   None
647	POP_TOP           None

648	SETUP_LOOP        '711'
651	LOAD_FAST         'done'
654	LOAD_ATTR         'items'
657	CALL_FUNCTION_0   None
660	GET_ITER          None
661	FOR_ITER          '710'
664	UNPACK_SEQUENCE_2 None
667	STORE_FAST        'k'
670	STORE_FAST        'v'

673	LOAD_GLOBAL       'isinstance'
676	LOAD_FAST         'v'
679	LOAD_GLOBAL       'str'
682	CALL_FUNCTION_2   None
685	POP_JUMP_IF_FALSE '661'

688	LOAD_FAST         'v'
691	LOAD_ATTR         'strip'
694	CALL_FUNCTION_0   None
697	LOAD_FAST         'done'
700	LOAD_FAST         'k'
703	STORE_SUBSCR      None
704	JUMP_BACK         '661'
707	JUMP_BACK         '661'
710	POP_BLOCK         None
711_0	COME_FROM         '648'

711	LOAD_FAST         'g'
714	LOAD_ATTR         'update'
717	LOAD_FAST         'done'
720	CALL_FUNCTION_1   None
723	POP_TOP           None

724	LOAD_FAST         'g'
727	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 284


def expand_makefile_vars--- This code section failed: ---

0	SETUP_LOOP        '108'

3	LOAD_GLOBAL       '_findvar1_rx'
6	LOAD_ATTR         'search'
9	LOAD_FAST         's'
12	CALL_FUNCTION_1   None
15	JUMP_IF_TRUE_OR_POP '30'
18	LOAD_GLOBAL       '_findvar2_rx'
21	LOAD_ATTR         'search'
24	LOAD_FAST         's'
27	CALL_FUNCTION_1   None
30_0	COME_FROM         '15'
30	STORE_FAST        'm'

33	LOAD_FAST         'm'
36	POP_JUMP_IF_FALSE '103'

39	LOAD_FAST         'm'
42	LOAD_ATTR         'span'
45	CALL_FUNCTION_0   None
48	UNPACK_SEQUENCE_2 None
51	STORE_FAST        'beg'
54	STORE_FAST        'end'

57	LOAD_FAST         's'
60	LOAD_CONST        0
63	LOAD_FAST         'beg'
66	SLICE+3           None
67	LOAD_FAST         'vars'
70	LOAD_ATTR         'get'
73	LOAD_FAST         'm'
76	LOAD_ATTR         'group'
79	LOAD_CONST        1
82	CALL_FUNCTION_1   None
85	CALL_FUNCTION_1   None
88	BINARY_ADD        None
89	LOAD_FAST         's'
92	LOAD_FAST         'end'
95	SLICE+1           None
96	BINARY_ADD        None
97	STORE_FAST        's'
100	JUMP_BACK         '3'

103	BREAK_LOOP        None
104	JUMP_BACK         '3'
107	POP_BLOCK         None
108_0	COME_FROM         '0'

108	LOAD_FAST         's'
111	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 107


_config_vars = None

def _init_posix():
    """Initialize the module as appropriate for POSIX systems."""
    global _config_vars
    g = {}
    try:
        filename = get_makefile_filename()
        parse_makefile(filename, g)
    except IOError as msg:
        my_msg = 'invalid Python installation: unable to open %s' % filename
        if hasattr(msg, 'strerror'):
            my_msg = my_msg + ' (%s)' % msg.strerror
        raise DistutilsPlatformError(my_msg)

    try:
        filename = get_config_h_filename()
        parse_config_h(file(filename), g)
    except IOError as msg:
        my_msg = 'invalid Python installation: unable to open %s' % filename
        if hasattr(msg, 'strerror'):
            my_msg = my_msg + ' (%s)' % msg.strerror
        raise DistutilsPlatformError(my_msg)

    if python_build:
        g['LDSHARED'] = g['BLDSHARED']
    elif get_python_version() < '2.1':
        if sys.platform == 'aix4':
            python_lib = get_python_lib(standard_lib=1)
            ld_so_aix = os.path.join(python_lib, 'config', 'ld_so_aix')
            python_exp = os.path.join(python_lib, 'config', 'python.exp')
            g['LDSHARED'] = '%s %s -bI:%s' % (ld_so_aix, g['CC'], python_exp)
        elif sys.platform == 'beos':
            python_lib = get_python_lib(standard_lib=1)
            linkerscript_path = string.split(g['LDSHARED'])[0]
            linkerscript_name = os.path.basename(linkerscript_path)
            linkerscript = os.path.join(python_lib, 'config', linkerscript_name)
            g['LDSHARED'] = '%s -L%s/lib -lpython%s' % (linkerscript, PREFIX, get_python_version())
    _config_vars = g


def _init_nt():
    """Initialize the module as appropriate for NT"""
    global _config_vars
    g = {}
    g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
    g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)
    g['INCLUDEPY'] = get_python_inc(plat_specific=0)
    g['SO'] = '.pyd'
    g['EXE'] = '.exe'
    g['VERSION'] = get_python_version().replace('.', '')
    g['BINDIR'] = os.path.dirname(os.path.abspath(sys.executable))
    _config_vars = g


def _init_os2():
    """Initialize the module as appropriate for OS/2"""
    global _config_vars
    g = {}
    g['LIBDEST'] = get_python_lib(plat_specific=0, standard_lib=1)
    g['BINLIBDEST'] = get_python_lib(plat_specific=1, standard_lib=1)
    g['INCLUDEPY'] = get_python_inc(plat_specific=0)
    g['SO'] = '.pyd'
    g['EXE'] = '.exe'
    _config_vars = g


def get_config_vars(*args):
    """With no arguments, return a dictionary of all configuration
    variables relevant for the current platform.  Generally this includes
    everything needed to build extensions and install both pure modules and
    extensions.  On Unix, this means every variable defined in Python's
    installed Makefile; on Windows and Mac OS it's a much smaller set.
    
    With arguments, return a list of values that result from looking up
    each argument in the configuration variable dictionary.
    """
    global _config_vars
    if _config_vars is None:
        func = globals().get('_init_' + os.name)
        if func:
            func()
        else:
            _config_vars = {}
        _config_vars['prefix'] = PREFIX
        _config_vars['exec_prefix'] = EXEC_PREFIX
        if sys.platform == 'darwin':
            kernel_version = os.uname()[2]
            major_version = int(kernel_version.split('.')[0])
            if major_version < 8:
                for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED', 'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
                    flags = _config_vars[key]
                    flags = re.sub('-arch\\s+\\w+\\s', ' ', flags)
                    flags = re.sub('-isysroot [^ \t]*', ' ', flags)
                    _config_vars[key] = flags

            else:
                if 'ARCHFLAGS' in os.environ:
                    arch = os.environ['ARCHFLAGS']
                    for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED', 'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
                        flags = _config_vars[key]
                        flags = re.sub('-arch\\s+\\w+\\s', ' ', flags)
                        flags = flags + ' ' + arch
                        _config_vars[key] = flags

                m = re.search('-isysroot\\s+(\\S+)', _config_vars['CFLAGS'])
                if m is not None:
                    sdk = m.group(1)
                    if not os.path.exists(sdk):
                        for key in ('LDFLAGS', 'BASECFLAGS', 'LDSHARED', 'CFLAGS', 'PY_CFLAGS', 'BLDSHARED'):
                            flags = _config_vars[key]
                            flags = re.sub('-isysroot\\s+\\S+(\\s|$)', ' ', flags)
                            _config_vars[key] = flags

    if args:
        vals = []
        for name in args:
            vals.append(_config_vars.get(name))

        return vals
    else:
        return _config_vars
        return


def get_config_var(name):
    """Return the value of a single variable using the dictionary
    returned by 'get_config_vars()'.  Equivalent to
    get_config_vars().get(name)
    """
    return get_config_vars().get(name)