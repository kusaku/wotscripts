# Embedded file name: scripts/common/Lib/distutils/extension.py
"""distutils.extension

Provides the Extension class, used to describe C/C++ extension
modules in setup scripts."""
__revision__ = '$Id$'
import os, string, sys
from types import *
try:
    import warnings
except ImportError:
    warnings = None

class Extension:
    """Just a collection of attributes that describes an extension
    module and everything needed to build it (hopefully in a portable
    way, but there are hooks that let you be as unportable as you need).
    
    Instance attributes:
      name : string
        the full name of the extension, including any packages -- ie.
        *not* a filename or pathname, but Python dotted name
      sources : [string]
        list of source filenames, relative to the distribution root
        (where the setup script lives), in Unix form (slash-separated)
        for portability.  Source files may be C, C++, SWIG (.i),
        platform-specific resource files, or whatever else is recognized
        by the "build_ext" command as source for a Python extension.
      include_dirs : [string]
        list of directories to search for C/C++ header files (in Unix
        form for portability)
      define_macros : [(name : string, value : string|None)]
        list of macros to define; each macro is defined using a 2-tuple,
        where 'value' is either the string to define it to or None to
        define it without a particular value (equivalent of "#define
        FOO" in source or -DFOO on Unix C compiler command line)
      undef_macros : [string]
        list of macros to undefine explicitly
      library_dirs : [string]
        list of directories to search for C/C++ libraries at link time
      libraries : [string]
        list of library names (not filenames or paths) to link against
      runtime_library_dirs : [string]
        list of directories to search for C/C++ libraries at run time
        (for shared extensions, this is when the extension is loaded)
      extra_objects : [string]
        list of extra files to link with (eg. object files not implied
        by 'sources', static library that must be explicitly specified,
        binary resource files, etc.)
      extra_compile_args : [string]
        any extra platform- and compiler-specific information to use
        when compiling the source files in 'sources'.  For platforms and
        compilers where "command line" makes sense, this is typically a
        list of command-line arguments, but for other platforms it could
        be anything.
      extra_link_args : [string]
        any extra platform- and compiler-specific information to use
        when linking object files together to create the extension (or
        to create a new static Python interpreter).  Similar
        interpretation as for 'extra_compile_args'.
      export_symbols : [string]
        list of symbols to be exported from a shared extension.  Not
        used on all platforms, and not generally necessary for Python
        extensions, which typically export exactly one symbol: "init" +
        extension_name.
      swig_opts : [string]
        any extra options to pass to SWIG if a source file has the .i
        extension.
      depends : [string]
        list of files that the extension depends on
      language : string
        extension language (i.e. "c", "c++", "objc"). Will be detected
        from the source extensions if not provided.
    """

    def __init__(self, name, sources, include_dirs = None, define_macros = None, undef_macros = None, library_dirs = None, libraries = None, runtime_library_dirs = None, extra_objects = None, extra_compile_args = None, extra_link_args = None, export_symbols = None, swig_opts = None, depends = None, language = None, **kw):
        if not type(name) is StringType:
            raise AssertionError("'name' must be a string")
            if not (type(sources) is ListType and map(type, sources) == [StringType] * len(sources)):
                raise AssertionError("'sources' must be a list of strings")
                self.name = name
                self.sources = sources
                self.include_dirs = include_dirs or []
                self.define_macros = define_macros or []
                self.undef_macros = undef_macros or []
                self.library_dirs = library_dirs or []
                self.libraries = libraries or []
                self.runtime_library_dirs = runtime_library_dirs or []
                self.extra_objects = extra_objects or []
                self.extra_compile_args = extra_compile_args or []
                self.extra_link_args = extra_link_args or []
                self.export_symbols = export_symbols or []
                self.swig_opts = swig_opts or []
                self.depends = depends or []
                self.language = language
                L = len(kw) and kw.keys()
                L.sort()
                L = map(repr, L)
                msg = 'Unknown Extension options: ' + string.join(L, ', ')
                warnings is not None and warnings.warn(msg)
            else:
                sys.stderr.write(msg + '\n')
        return


def read_setup_file--- This code section failed: ---

0	LOAD_CONST        -1
3	LOAD_CONST        ('parse_makefile', 'expand_makefile_vars', '_variable_rx')
6	IMPORT_NAME       'distutils.sysconfig'
9	IMPORT_FROM       'parse_makefile'
12	STORE_FAST        'parse_makefile'
15	IMPORT_FROM       'expand_makefile_vars'
18	STORE_FAST        'expand_makefile_vars'
21	IMPORT_FROM       '_variable_rx'
24	STORE_FAST        '_variable_rx'
27	POP_TOP           None

28	LOAD_CONST        -1
31	LOAD_CONST        ('TextFile',)
34	IMPORT_NAME       'distutils.text_file'
37	IMPORT_FROM       'TextFile'
40	STORE_FAST        'TextFile'
43	POP_TOP           None

44	LOAD_CONST        -1
47	LOAD_CONST        ('split_quoted',)
50	IMPORT_NAME       'distutils.util'
53	IMPORT_FROM       'split_quoted'
56	STORE_FAST        'split_quoted'
59	POP_TOP           None

60	LOAD_FAST         'parse_makefile'
63	LOAD_FAST         'filename'
66	CALL_FUNCTION_1   None
69	STORE_FAST        'vars'

72	LOAD_FAST         'TextFile'
75	LOAD_FAST         'filename'
78	LOAD_CONST        'strip_comments'

81	LOAD_CONST        1
84	LOAD_CONST        'skip_blanks'
87	LOAD_CONST        1
90	LOAD_CONST        'join_lines'
93	LOAD_CONST        1
96	LOAD_CONST        'lstrip_ws'

99	LOAD_CONST        1
102	LOAD_CONST        'rstrip_ws'
105	LOAD_CONST        1
108	CALL_FUNCTION_1281 None
111	STORE_FAST        'file'

114	SETUP_FINALLY     '982'

117	BUILD_LIST_0      None
120	STORE_FAST        'extensions'

123	SETUP_LOOP        '978'

126	LOAD_FAST         'file'
129	LOAD_ATTR         'readline'
132	CALL_FUNCTION_0   None
135	STORE_FAST        'line'

138	LOAD_FAST         'line'
141	LOAD_CONST        None
144	COMPARE_OP        'is'
147	POP_JUMP_IF_FALSE '154'

150	BREAK_LOOP        None
151	JUMP_FORWARD      '154'
154_0	COME_FROM         '151'

154	LOAD_FAST         '_variable_rx'
157	LOAD_ATTR         'match'
160	LOAD_FAST         'line'
163	CALL_FUNCTION_1   None
166	POP_JUMP_IF_FALSE '234'

169	CONTINUE          '126'

172	LOAD_FAST         'line'
175	LOAD_CONST        0
178	BINARY_SUBSCR     None
179	LOAD_FAST         'line'
182	LOAD_CONST        -1
185	BINARY_SUBSCR     None
186	DUP_TOP           None
187	ROT_THREE         None
188	COMPARE_OP        '=='
191	JUMP_IF_FALSE_OR_POP '203'
194	LOAD_CONST        '*'
197	COMPARE_OP        '=='
200	JUMP_FORWARD      '205'
203_0	COME_FROM         '191'
203	ROT_TWO           None
204	POP_TOP           None
205_0	COME_FROM         '200'
205	POP_JUMP_IF_FALSE '234'

208	LOAD_FAST         'file'
211	LOAD_ATTR         'warn'
214	LOAD_CONST        "'%s' lines not handled yet"
217	LOAD_FAST         'line'
220	BINARY_MODULO     None
221	CALL_FUNCTION_1   None
224	POP_TOP           None

225	CONTINUE          '126'
228	JUMP_ABSOLUTE     '234'
231	JUMP_FORWARD      '234'
234_0	COME_FROM         '231'

234	LOAD_FAST         'expand_makefile_vars'
237	LOAD_FAST         'line'
240	LOAD_FAST         'vars'
243	CALL_FUNCTION_2   None
246	STORE_FAST        'line'

249	LOAD_FAST         'split_quoted'
252	LOAD_FAST         'line'
255	CALL_FUNCTION_1   None
258	STORE_FAST        'words'

261	LOAD_FAST         'words'
264	LOAD_CONST        0
267	BINARY_SUBSCR     None
268	STORE_FAST        'module'

271	LOAD_GLOBAL       'Extension'
274	LOAD_FAST         'module'
277	BUILD_LIST_0      None
280	CALL_FUNCTION_2   None
283	STORE_FAST        'ext'

286	LOAD_CONST        None
289	STORE_FAST        'append_next_word'

292	SETUP_LOOP        '961'
295	LOAD_FAST         'words'
298	LOAD_CONST        1
301	SLICE+1           None
302	GET_ITER          None
303	FOR_ITER          '960'
306	STORE_FAST        'word'

309	LOAD_FAST         'append_next_word'
312	LOAD_CONST        None
315	COMPARE_OP        'is not'
318	POP_JUMP_IF_FALSE '346'

321	LOAD_FAST         'append_next_word'
324	LOAD_ATTR         'append'
327	LOAD_FAST         'word'
330	CALL_FUNCTION_1   None
333	POP_TOP           None

334	LOAD_CONST        None
337	STORE_FAST        'append_next_word'

340	CONTINUE          '303'
343	JUMP_FORWARD      '346'
346_0	COME_FROM         '343'

346	LOAD_GLOBAL       'os'
349	LOAD_ATTR         'path'
352	LOAD_ATTR         'splitext'
355	LOAD_FAST         'word'
358	CALL_FUNCTION_1   None
361	LOAD_CONST        1
364	BINARY_SUBSCR     None
365	STORE_FAST        'suffix'

368	LOAD_FAST         'word'
371	LOAD_CONST        0
374	LOAD_CONST        2
377	SLICE+3           None
378	STORE_FAST        'switch'
381	LOAD_FAST         'word'
384	LOAD_CONST        2
387	SLICE+1           None
388	STORE_FAST        'value'

391	LOAD_FAST         'suffix'
394	LOAD_CONST        ('.c', '.cc', '.cpp', '.cxx', '.c++', '.m', '.mm')
397	COMPARE_OP        'in'
400	POP_JUMP_IF_FALSE '422'

403	LOAD_FAST         'ext'
406	LOAD_ATTR         'sources'
409	LOAD_ATTR         'append'
412	LOAD_FAST         'word'
415	CALL_FUNCTION_1   None
418	POP_TOP           None
419	JUMP_BACK         '303'

422	LOAD_FAST         'switch'
425	LOAD_CONST        '-I'
428	COMPARE_OP        '=='
431	POP_JUMP_IF_FALSE '453'

434	LOAD_FAST         'ext'
437	LOAD_ATTR         'include_dirs'
440	LOAD_ATTR         'append'
443	LOAD_FAST         'value'
446	CALL_FUNCTION_1   None
449	POP_TOP           None
450	JUMP_BACK         '303'

453	LOAD_FAST         'switch'
456	LOAD_CONST        '-D'
459	COMPARE_OP        '=='
462	POP_JUMP_IF_FALSE '560'

465	LOAD_GLOBAL       'string'
468	LOAD_ATTR         'find'
471	LOAD_FAST         'value'
474	LOAD_CONST        '='
477	CALL_FUNCTION_2   None
480	STORE_FAST        'equals'

483	LOAD_FAST         'equals'
486	LOAD_CONST        -1
489	COMPARE_OP        '=='
492	POP_JUMP_IF_FALSE '520'

495	LOAD_FAST         'ext'
498	LOAD_ATTR         'define_macros'
501	LOAD_ATTR         'append'
504	LOAD_FAST         'value'
507	LOAD_CONST        None
510	BUILD_TUPLE_2     None
513	CALL_FUNCTION_1   None
516	POP_TOP           None
517	JUMP_ABSOLUTE     '957'

520	LOAD_FAST         'ext'
523	LOAD_ATTR         'define_macros'
526	LOAD_ATTR         'append'
529	LOAD_FAST         'value'
532	LOAD_CONST        0
535	LOAD_FAST         'equals'
538	SLICE+3           None

539	LOAD_FAST         'value'
542	LOAD_FAST         'equals'
545	LOAD_CONST        2
548	BINARY_ADD        None
549	SLICE+1           None
550	BUILD_TUPLE_2     None
553	CALL_FUNCTION_1   None
556	POP_TOP           None
557	JUMP_BACK         '303'

560	LOAD_FAST         'switch'
563	LOAD_CONST        '-U'
566	COMPARE_OP        '=='
569	POP_JUMP_IF_FALSE '591'

572	LOAD_FAST         'ext'
575	LOAD_ATTR         'undef_macros'
578	LOAD_ATTR         'append'
581	LOAD_FAST         'value'
584	CALL_FUNCTION_1   None
587	POP_TOP           None
588	JUMP_BACK         '303'

591	LOAD_FAST         'switch'
594	LOAD_CONST        '-C'
597	COMPARE_OP        '=='
600	POP_JUMP_IF_FALSE '622'

603	LOAD_FAST         'ext'
606	LOAD_ATTR         'extra_compile_args'
609	LOAD_ATTR         'append'
612	LOAD_FAST         'word'
615	CALL_FUNCTION_1   None
618	POP_TOP           None
619	JUMP_BACK         '303'

622	LOAD_FAST         'switch'
625	LOAD_CONST        '-l'
628	COMPARE_OP        '=='
631	POP_JUMP_IF_FALSE '653'

634	LOAD_FAST         'ext'
637	LOAD_ATTR         'libraries'
640	LOAD_ATTR         'append'
643	LOAD_FAST         'value'
646	CALL_FUNCTION_1   None
649	POP_TOP           None
650	JUMP_BACK         '303'

653	LOAD_FAST         'switch'
656	LOAD_CONST        '-L'
659	COMPARE_OP        '=='
662	POP_JUMP_IF_FALSE '684'

665	LOAD_FAST         'ext'
668	LOAD_ATTR         'library_dirs'
671	LOAD_ATTR         'append'
674	LOAD_FAST         'value'
677	CALL_FUNCTION_1   None
680	POP_TOP           None
681	JUMP_BACK         '303'

684	LOAD_FAST         'switch'
687	LOAD_CONST        '-R'
690	COMPARE_OP        '=='
693	POP_JUMP_IF_FALSE '715'

696	LOAD_FAST         'ext'
699	LOAD_ATTR         'runtime_library_dirs'
702	LOAD_ATTR         'append'
705	LOAD_FAST         'value'
708	CALL_FUNCTION_1   None
711	POP_TOP           None
712	JUMP_BACK         '303'

715	LOAD_FAST         'word'
718	LOAD_CONST        '-rpath'
721	COMPARE_OP        '=='
724	POP_JUMP_IF_FALSE '739'

727	LOAD_FAST         'ext'
730	LOAD_ATTR         'runtime_library_dirs'
733	STORE_FAST        'append_next_word'
736	JUMP_BACK         '303'

739	LOAD_FAST         'word'
742	LOAD_CONST        '-Xlinker'
745	COMPARE_OP        '=='
748	POP_JUMP_IF_FALSE '763'

751	LOAD_FAST         'ext'
754	LOAD_ATTR         'extra_link_args'
757	STORE_FAST        'append_next_word'
760	JUMP_BACK         '303'

763	LOAD_FAST         'word'
766	LOAD_CONST        '-Xcompiler'
769	COMPARE_OP        '=='
772	POP_JUMP_IF_FALSE '787'

775	LOAD_FAST         'ext'
778	LOAD_ATTR         'extra_compile_args'
781	STORE_FAST        'append_next_word'
784	JUMP_BACK         '303'

787	LOAD_FAST         'switch'
790	LOAD_CONST        '-u'
793	COMPARE_OP        '=='
796	POP_JUMP_IF_FALSE '836'

799	LOAD_FAST         'ext'
802	LOAD_ATTR         'extra_link_args'
805	LOAD_ATTR         'append'
808	LOAD_FAST         'word'
811	CALL_FUNCTION_1   None
814	POP_TOP           None

815	LOAD_FAST         'value'
818	POP_JUMP_IF_TRUE  '957'

821	LOAD_FAST         'ext'
824	LOAD_ATTR         'extra_link_args'
827	STORE_FAST        'append_next_word'
830	JUMP_ABSOLUTE     '957'
833	JUMP_BACK         '303'

836	LOAD_FAST         'word'
839	LOAD_CONST        '-Xcompiler'
842	COMPARE_OP        '=='
845	POP_JUMP_IF_FALSE '860'

848	LOAD_FAST         'ext'
851	LOAD_ATTR         'extra_compile_args'
854	STORE_FAST        'append_next_word'
857	JUMP_BACK         '303'

860	LOAD_FAST         'switch'
863	LOAD_CONST        '-u'
866	COMPARE_OP        '=='
869	POP_JUMP_IF_FALSE '909'

872	LOAD_FAST         'ext'
875	LOAD_ATTR         'extra_link_args'
878	LOAD_ATTR         'append'
881	LOAD_FAST         'word'
884	CALL_FUNCTION_1   None
887	POP_TOP           None

888	LOAD_FAST         'value'
891	POP_JUMP_IF_TRUE  '957'

894	LOAD_FAST         'ext'
897	LOAD_ATTR         'extra_link_args'
900	STORE_FAST        'append_next_word'
903	JUMP_ABSOLUTE     '957'
906	JUMP_BACK         '303'

909	LOAD_FAST         'suffix'
912	LOAD_CONST        ('.a', '.so', '.sl', '.o', '.dylib')
915	COMPARE_OP        'in'
918	POP_JUMP_IF_FALSE '940'

921	LOAD_FAST         'ext'
924	LOAD_ATTR         'extra_objects'
927	LOAD_ATTR         'append'
930	LOAD_FAST         'word'
933	CALL_FUNCTION_1   None
936	POP_TOP           None
937	JUMP_BACK         '303'

940	LOAD_FAST         'file'
943	LOAD_ATTR         'warn'
946	LOAD_CONST        "unrecognized argument '%s'"
949	LOAD_FAST         'word'
952	BINARY_MODULO     None
953	CALL_FUNCTION_1   None
956	POP_TOP           None
957	JUMP_BACK         '303'
960	POP_BLOCK         None
961_0	COME_FROM         '292'

961	LOAD_FAST         'extensions'
964	LOAD_ATTR         'append'
967	LOAD_FAST         'ext'
970	CALL_FUNCTION_1   None
973	POP_TOP           None
974	JUMP_BACK         '126'
977	POP_BLOCK         None
978_0	COME_FROM         '123'
978	POP_BLOCK         None
979	LOAD_CONST        None
982_0	COME_FROM         '114'

982	LOAD_FAST         'file'
985	LOAD_ATTR         'close'
988	CALL_FUNCTION_0   None
991	POP_TOP           None
992	END_FINALLY       None

993	LOAD_FAST         'extensions'
996	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 977