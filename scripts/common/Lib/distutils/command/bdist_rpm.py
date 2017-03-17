# Embedded file name: scripts/common/Lib/distutils/command/bdist_rpm.py
"""distutils.command.bdist_rpm

Implements the Distutils 'bdist_rpm' command (create RPM source and binary
distributions)."""
__revision__ = '$Id$'
import sys
import os
import string
from distutils.core import Command
from distutils.debug import DEBUG
from distutils.file_util import write_file
from distutils.errors import DistutilsOptionError, DistutilsPlatformError, DistutilsFileError, DistutilsExecError
from distutils import log

class bdist_rpm(Command):
    description = 'create an RPM distribution'
    user_options = [('bdist-base=', None, 'base directory for creating built distributions'),
     ('rpm-base=', None, 'base directory for creating RPMs (defaults to "rpm" under --bdist-base; must be specified for RPM 2)'),
     ('dist-dir=', 'd', 'directory to put final RPM files in (and .spec files if --spec-only)'),
     ('python=', None, 'path to Python interpreter to hard-code in the .spec file (default: "python")'),
     ('fix-python', None, 'hard-code the exact path to the current Python interpreter in the .spec file'),
     ('spec-only', None, 'only regenerate spec file'),
     ('source-only', None, 'only generate source RPM'),
     ('binary-only', None, 'only generate binary RPM'),
     ('use-bzip2', None, 'use bzip2 instead of gzip to create source distribution'),
     ('distribution-name=', None, 'name of the (Linux) distribution to which this RPM applies (*not* the name of the module distribution!)'),
     ('group=', None, 'package classification [default: "Development/Libraries"]'),
     ('release=', None, 'RPM release number'),
     ('serial=', None, 'RPM serial number'),
     ('vendor=', None, 'RPM "vendor" (eg. "Joe Blow <joe@example.com>") [default: maintainer or author from setup script]'),
     ('packager=', None, 'RPM packager (eg. "Jane Doe <jane@example.net>")[default: vendor]'),
     ('doc-files=', None, 'list of documentation files (space or comma-separated)'),
     ('changelog=', None, 'RPM changelog'),
     ('icon=', None, 'name of icon file'),
     ('provides=', None, 'capabilities provided by this package'),
     ('requires=', None, 'capabilities required by this package'),
     ('conflicts=', None, 'capabilities which conflict with this package'),
     ('build-requires=', None, 'capabilities required to build this package'),
     ('obsoletes=', None, 'capabilities made obsolete by this package'),
     ('no-autoreq', None, 'do not automatically calculate dependencies'),
     ('keep-temp', 'k', "don't clean up RPM build directory"),
     ('no-keep-temp', None, 'clean up RPM build directory [default]'),
     ('use-rpm-opt-flags', None, 'compile with RPM_OPT_FLAGS when building from source RPM'),
     ('no-rpm-opt-flags', None, 'do not pass any RPM CFLAGS to compiler'),
     ('rpm3-mode', None, 'RPM 3 compatibility mode (default)'),
     ('rpm2-mode', None, 'RPM 2 compatibility mode'),
     ('prep-script=', None, 'Specify a script for the PREP phase of RPM building'),
     ('build-script=', None, 'Specify a script for the BUILD phase of RPM building'),
     ('pre-install=', None, 'Specify a script for the pre-INSTALL phase of RPM building'),
     ('install-script=', None, 'Specify a script for the INSTALL phase of RPM building'),
     ('post-install=', None, 'Specify a script for the post-INSTALL phase of RPM building'),
     ('pre-uninstall=', None, 'Specify a script for the pre-UNINSTALL phase of RPM building'),
     ('post-uninstall=', None, 'Specify a script for the post-UNINSTALL phase of RPM building'),
     ('clean-script=', None, 'Specify a script for the CLEAN phase of RPM building'),
     ('verify-script=', None, 'Specify a script for the VERIFY phase of the RPM build'),
     ('force-arch=', None, 'Force an architecture onto the RPM build process'),
     ('quiet', 'q', 'Run the INSTALL phase of RPM building in quiet mode')]
    boolean_options = ['keep-temp',
     'use-rpm-opt-flags',
     'rpm3-mode',
     'no-autoreq',
     'quiet']
    negative_opt = {'no-keep-temp': 'keep-temp',
     'no-rpm-opt-flags': 'use-rpm-opt-flags',
     'rpm2-mode': 'rpm3-mode'}

    def initialize_options(self):
        self.bdist_base = None
        self.rpm_base = None
        self.dist_dir = None
        self.python = None
        self.fix_python = None
        self.spec_only = None
        self.binary_only = None
        self.source_only = None
        self.use_bzip2 = None
        self.distribution_name = None
        self.group = None
        self.release = None
        self.serial = None
        self.vendor = None
        self.packager = None
        self.doc_files = None
        self.changelog = None
        self.icon = None
        self.prep_script = None
        self.build_script = None
        self.install_script = None
        self.clean_script = None
        self.verify_script = None
        self.pre_install = None
        self.post_install = None
        self.pre_uninstall = None
        self.post_uninstall = None
        self.prep = None
        self.provides = None
        self.requires = None
        self.conflicts = None
        self.build_requires = None
        self.obsoletes = None
        self.keep_temp = 0
        self.use_rpm_opt_flags = 1
        self.rpm3_mode = 1
        self.no_autoreq = 0
        self.force_arch = None
        self.quiet = 0
        return

    def finalize_options(self):
        self.set_undefined_options('bdist', ('bdist_base', 'bdist_base'))
        if self.rpm_base is None:
            if not self.rpm3_mode:
                raise DistutilsOptionError, 'you must specify --rpm-base in RPM 2 mode'
            self.rpm_base = os.path.join(self.bdist_base, 'rpm')
        if self.python is None:
            if self.fix_python:
                self.python = sys.executable
            else:
                self.python = 'python'
        elif self.fix_python:
            raise DistutilsOptionError, '--python and --fix-python are mutually exclusive options'
        if os.name != 'posix':
            raise DistutilsPlatformError, "don't know how to create RPM distributions on platform %s" % os.name
        if self.binary_only and self.source_only:
            raise DistutilsOptionError, "cannot supply both '--source-only' and '--binary-only'"
        if not self.distribution.has_ext_modules():
            self.use_rpm_opt_flags = 0
        self.set_undefined_options('bdist', ('dist_dir', 'dist_dir'))
        self.finalize_package_data()
        return

    def finalize_package_data(self):
        self.ensure_string('group', 'Development/Libraries')
        self.ensure_string('vendor', '%s <%s>' % (self.distribution.get_contact(), self.distribution.get_contact_email()))
        self.ensure_string('packager')
        self.ensure_string_list('doc_files')
        if isinstance(self.doc_files, list):
            for readme in ('README', 'README.txt'):
                if os.path.exists(readme) and readme not in self.doc_files:
                    self.doc_files.append(readme)

        self.ensure_string('release', '1')
        self.ensure_string('serial')
        self.ensure_string('distribution_name')
        self.ensure_string('changelog')
        self.changelog = self._format_changelog(self.changelog)
        self.ensure_filename('icon')
        self.ensure_filename('prep_script')
        self.ensure_filename('build_script')
        self.ensure_filename('install_script')
        self.ensure_filename('clean_script')
        self.ensure_filename('verify_script')
        self.ensure_filename('pre_install')
        self.ensure_filename('post_install')
        self.ensure_filename('pre_uninstall')
        self.ensure_filename('post_uninstall')
        self.ensure_string_list('provides')
        self.ensure_string_list('requires')
        self.ensure_string_list('conflicts')
        self.ensure_string_list('build_requires')
        self.ensure_string_list('obsoletes')
        self.ensure_string('force_arch')

    def run--- This code section failed: ---

0	LOAD_GLOBAL       'DEBUG'
3	POP_JUMP_IF_FALSE '62'

6	LOAD_CONST        'before _get_package_data():'
9	PRINT_ITEM        None
10	PRINT_NEWLINE_CONT None

11	LOAD_CONST        'vendor ='
14	PRINT_ITEM        None
15	LOAD_FAST         'self'
18	LOAD_ATTR         'vendor'
21	PRINT_ITEM_CONT   None
22	PRINT_NEWLINE_CONT None

23	LOAD_CONST        'packager ='
26	PRINT_ITEM        None
27	LOAD_FAST         'self'
30	LOAD_ATTR         'packager'
33	PRINT_ITEM_CONT   None
34	PRINT_NEWLINE_CONT None

35	LOAD_CONST        'doc_files ='
38	PRINT_ITEM        None
39	LOAD_FAST         'self'
42	LOAD_ATTR         'doc_files'
45	PRINT_ITEM_CONT   None
46	PRINT_NEWLINE_CONT None

47	LOAD_CONST        'changelog ='
50	PRINT_ITEM        None
51	LOAD_FAST         'self'
54	LOAD_ATTR         'changelog'
57	PRINT_ITEM_CONT   None
58	PRINT_NEWLINE_CONT None
59	JUMP_FORWARD      '62'
62_0	COME_FROM         '59'

62	LOAD_FAST         'self'
65	LOAD_ATTR         'spec_only'
68	POP_JUMP_IF_FALSE '96'

71	LOAD_FAST         'self'
74	LOAD_ATTR         'dist_dir'
77	STORE_FAST        'spec_dir'

80	LOAD_FAST         'self'
83	LOAD_ATTR         'mkpath'
86	LOAD_FAST         'spec_dir'
89	CALL_FUNCTION_1   None
92	POP_TOP           None
93	JUMP_FORWARD      '174'

96	BUILD_MAP         None
99	STORE_FAST        'rpm_dir'

102	SETUP_LOOP        '164'
105	LOAD_CONST        ('SOURCES', 'SPECS', 'BUILD', 'RPMS', 'SRPMS')
108	GET_ITER          None
109	FOR_ITER          '163'
112	STORE_FAST        'd'

115	LOAD_GLOBAL       'os'
118	LOAD_ATTR         'path'
121	LOAD_ATTR         'join'
124	LOAD_FAST         'self'
127	LOAD_ATTR         'rpm_base'
130	LOAD_FAST         'd'
133	CALL_FUNCTION_2   None
136	LOAD_FAST         'rpm_dir'
139	LOAD_FAST         'd'
142	STORE_SUBSCR      None

143	LOAD_FAST         'self'
146	LOAD_ATTR         'mkpath'
149	LOAD_FAST         'rpm_dir'
152	LOAD_FAST         'd'
155	BINARY_SUBSCR     None
156	CALL_FUNCTION_1   None
159	POP_TOP           None
160	JUMP_BACK         '109'
163	POP_BLOCK         None
164_0	COME_FROM         '102'

164	LOAD_FAST         'rpm_dir'
167	LOAD_CONST        'SPECS'
170	BINARY_SUBSCR     None
171	STORE_FAST        'spec_dir'
174_0	COME_FROM         '93'

174	LOAD_GLOBAL       'os'
177	LOAD_ATTR         'path'
180	LOAD_ATTR         'join'
183	LOAD_FAST         'spec_dir'

186	LOAD_CONST        '%s.spec'
189	LOAD_FAST         'self'
192	LOAD_ATTR         'distribution'
195	LOAD_ATTR         'get_name'
198	CALL_FUNCTION_0   None
201	BINARY_MODULO     None
202	CALL_FUNCTION_2   None
205	STORE_FAST        'spec_path'

208	LOAD_FAST         'self'
211	LOAD_ATTR         'execute'
214	LOAD_GLOBAL       'write_file'

217	LOAD_FAST         'spec_path'

220	LOAD_FAST         'self'
223	LOAD_ATTR         '_make_spec_file'
226	CALL_FUNCTION_0   None
229	BUILD_TUPLE_2     None

232	LOAD_CONST        "writing '%s'"
235	LOAD_FAST         'spec_path'
238	BINARY_MODULO     None
239	CALL_FUNCTION_3   None
242	POP_TOP           None

243	LOAD_FAST         'self'
246	LOAD_ATTR         'spec_only'
249	POP_JUMP_IF_FALSE '256'

252	LOAD_CONST        None
255	RETURN_END_IF     None

256	LOAD_FAST         'self'
259	LOAD_ATTR         'distribution'
262	LOAD_ATTR         'dist_files'
265	SLICE+0           None
266	STORE_FAST        'saved_dist_files'

269	LOAD_FAST         'self'
272	LOAD_ATTR         'reinitialize_command'
275	LOAD_CONST        'sdist'
278	CALL_FUNCTION_1   None
281	STORE_FAST        'sdist'

284	LOAD_FAST         'self'
287	LOAD_ATTR         'use_bzip2'
290	POP_JUMP_IF_FALSE '308'

293	LOAD_CONST        'bztar'
296	BUILD_LIST_1      None
299	LOAD_FAST         'sdist'
302	STORE_ATTR        'formats'
305	JUMP_FORWARD      '320'

308	LOAD_CONST        'gztar'
311	BUILD_LIST_1      None
314	LOAD_FAST         'sdist'
317	STORE_ATTR        'formats'
320_0	COME_FROM         '305'

320	LOAD_FAST         'self'
323	LOAD_ATTR         'run_command'
326	LOAD_CONST        'sdist'
329	CALL_FUNCTION_1   None
332	POP_TOP           None

333	LOAD_FAST         'saved_dist_files'
336	LOAD_FAST         'self'
339	LOAD_ATTR         'distribution'
342	STORE_ATTR        'dist_files'

345	LOAD_FAST         'sdist'
348	LOAD_ATTR         'get_archive_files'
351	CALL_FUNCTION_0   None
354	LOAD_CONST        0
357	BINARY_SUBSCR     None
358	STORE_FAST        'source'

361	LOAD_FAST         'rpm_dir'
364	LOAD_CONST        'SOURCES'
367	BINARY_SUBSCR     None
368	STORE_FAST        'source_dir'

371	LOAD_FAST         'self'
374	LOAD_ATTR         'copy_file'
377	LOAD_FAST         'source'
380	LOAD_FAST         'source_dir'
383	CALL_FUNCTION_2   None
386	POP_TOP           None

387	LOAD_FAST         'self'
390	LOAD_ATTR         'icon'
393	POP_JUMP_IF_FALSE '458'

396	LOAD_GLOBAL       'os'
399	LOAD_ATTR         'path'
402	LOAD_ATTR         'exists'
405	LOAD_FAST         'self'
408	LOAD_ATTR         'icon'
411	CALL_FUNCTION_1   None
414	POP_JUMP_IF_FALSE '439'

417	LOAD_FAST         'self'
420	LOAD_ATTR         'copy_file'
423	LOAD_FAST         'self'
426	LOAD_ATTR         'icon'
429	LOAD_FAST         'source_dir'
432	CALL_FUNCTION_2   None
435	POP_TOP           None
436	JUMP_ABSOLUTE     '458'

439	LOAD_GLOBAL       'DistutilsFileError'

442	LOAD_CONST        "icon file '%s' does not exist"
445	LOAD_FAST         'self'
448	LOAD_ATTR         'icon'
451	BINARY_MODULO     None
452	RAISE_VARARGS_2   None
455	JUMP_FORWARD      '458'
458_0	COME_FROM         '455'

458	LOAD_GLOBAL       'log'
461	LOAD_ATTR         'info'
464	LOAD_CONST        'building RPMs'
467	CALL_FUNCTION_1   None
470	POP_TOP           None

471	LOAD_CONST        'rpm'
474	BUILD_LIST_1      None
477	STORE_FAST        'rpm_cmd'

480	LOAD_GLOBAL       'os'
483	LOAD_ATTR         'path'
486	LOAD_ATTR         'exists'
489	LOAD_CONST        '/usr/bin/rpmbuild'
492	CALL_FUNCTION_1   None
495	POP_JUMP_IF_TRUE  '516'

498	LOAD_GLOBAL       'os'
501	LOAD_ATTR         'path'
504	LOAD_ATTR         'exists'
507	LOAD_CONST        '/bin/rpmbuild'
510	CALL_FUNCTION_1   None
513_0	COME_FROM         '495'
513	POP_JUMP_IF_FALSE '528'

516	LOAD_CONST        'rpmbuild'
519	BUILD_LIST_1      None
522	STORE_FAST        'rpm_cmd'
525	JUMP_FORWARD      '528'
528_0	COME_FROM         '525'

528	LOAD_FAST         'self'
531	LOAD_ATTR         'source_only'
534	POP_JUMP_IF_FALSE '553'

537	LOAD_FAST         'rpm_cmd'
540	LOAD_ATTR         'append'
543	LOAD_CONST        '-bs'
546	CALL_FUNCTION_1   None
549	POP_TOP           None
550	JUMP_FORWARD      '591'

553	LOAD_FAST         'self'
556	LOAD_ATTR         'binary_only'
559	POP_JUMP_IF_FALSE '578'

562	LOAD_FAST         'rpm_cmd'
565	LOAD_ATTR         'append'
568	LOAD_CONST        '-bb'
571	CALL_FUNCTION_1   None
574	POP_TOP           None
575	JUMP_FORWARD      '591'

578	LOAD_FAST         'rpm_cmd'
581	LOAD_ATTR         'append'
584	LOAD_CONST        '-ba'
587	CALL_FUNCTION_1   None
590	POP_TOP           None
591_0	COME_FROM         '550'
591_1	COME_FROM         '575'

591	LOAD_FAST         'self'
594	LOAD_ATTR         'rpm3_mode'
597	POP_JUMP_IF_FALSE '641'

600	LOAD_FAST         'rpm_cmd'
603	LOAD_ATTR         'extend'
606	LOAD_CONST        '--define'

609	LOAD_CONST        '_topdir %s'
612	LOAD_GLOBAL       'os'
615	LOAD_ATTR         'path'
618	LOAD_ATTR         'abspath'
621	LOAD_FAST         'self'
624	LOAD_ATTR         'rpm_base'
627	CALL_FUNCTION_1   None
630	BINARY_MODULO     None
631	BUILD_LIST_2      None
634	CALL_FUNCTION_1   None
637	POP_TOP           None
638	JUMP_FORWARD      '641'
641_0	COME_FROM         '638'

641	LOAD_FAST         'self'
644	LOAD_ATTR         'keep_temp'
647	POP_JUMP_IF_TRUE  '666'

650	LOAD_FAST         'rpm_cmd'
653	LOAD_ATTR         'append'
656	LOAD_CONST        '--clean'
659	CALL_FUNCTION_1   None
662	POP_TOP           None
663	JUMP_FORWARD      '666'
666_0	COME_FROM         '663'

666	LOAD_FAST         'self'
669	LOAD_ATTR         'quiet'
672	POP_JUMP_IF_FALSE '691'

675	LOAD_FAST         'rpm_cmd'
678	LOAD_ATTR         'append'
681	LOAD_CONST        '--quiet'
684	CALL_FUNCTION_1   None
687	POP_TOP           None
688	JUMP_FORWARD      '691'
691_0	COME_FROM         '688'

691	LOAD_FAST         'rpm_cmd'
694	LOAD_ATTR         'append'
697	LOAD_FAST         'spec_path'
700	CALL_FUNCTION_1   None
703	POP_TOP           None

704	LOAD_CONST        '%{name}-%{version}-%{release}'
707	STORE_FAST        'nvr_string'

710	LOAD_FAST         'nvr_string'
713	LOAD_CONST        '.src.rpm'
716	BINARY_ADD        None
717	STORE_FAST        'src_rpm'

720	LOAD_CONST        '%{arch}/'
723	LOAD_FAST         'nvr_string'
726	BINARY_ADD        None
727	LOAD_CONST        '.%{arch}.rpm'
730	BINARY_ADD        None
731	STORE_FAST        'non_src_rpm'

734	LOAD_CONST        "rpm -q --qf '%s %s\\n' --specfile '%s'"

737	LOAD_FAST         'src_rpm'
740	LOAD_FAST         'non_src_rpm'
743	LOAD_FAST         'spec_path'
746	BUILD_TUPLE_3     None
749	BINARY_MODULO     None
750	STORE_FAST        'q_cmd'

753	LOAD_GLOBAL       'os'
756	LOAD_ATTR         'popen'
759	LOAD_FAST         'q_cmd'
762	CALL_FUNCTION_1   None
765	STORE_FAST        'out'

768	SETUP_FINALLY     '949'

771	BUILD_LIST_0      None
774	STORE_FAST        'binary_rpms'

777	LOAD_CONST        None
780	STORE_FAST        'source_rpm'

783	SETUP_LOOP        '902'

786	LOAD_FAST         'out'
789	LOAD_ATTR         'readline'
792	CALL_FUNCTION_0   None
795	STORE_FAST        'line'

798	LOAD_FAST         'line'
801	POP_JUMP_IF_TRUE  '808'

804	BREAK_LOOP        None
805	JUMP_FORWARD      '808'
808_0	COME_FROM         '805'

808	LOAD_GLOBAL       'string'
811	LOAD_ATTR         'split'
814	LOAD_GLOBAL       'string'
817	LOAD_ATTR         'strip'
820	LOAD_FAST         'line'
823	CALL_FUNCTION_1   None
826	CALL_FUNCTION_1   None
829	STORE_FAST        'l'

832	LOAD_GLOBAL       'len'
835	LOAD_FAST         'l'
838	CALL_FUNCTION_1   None
841	LOAD_CONST        2
844	COMPARE_OP        '=='
847	POP_JUMP_IF_TRUE  '856'
850	LOAD_ASSERT       'AssertionError'
853	RAISE_VARARGS_1   None

856	LOAD_FAST         'binary_rpms'
859	LOAD_ATTR         'append'
862	LOAD_FAST         'l'
865	LOAD_CONST        1
868	BINARY_SUBSCR     None
869	CALL_FUNCTION_1   None
872	POP_TOP           None

873	LOAD_FAST         'source_rpm'
876	LOAD_CONST        None
879	COMPARE_OP        'is'
882	POP_JUMP_IF_FALSE '786'

885	LOAD_FAST         'l'
888	LOAD_CONST        0
891	BINARY_SUBSCR     None
892	STORE_FAST        'source_rpm'
895	JUMP_BACK         '786'
898	JUMP_BACK         '786'
901	POP_BLOCK         None
902_0	COME_FROM         '783'

902	LOAD_FAST         'out'
905	LOAD_ATTR         'close'
908	CALL_FUNCTION_0   None
911	STORE_FAST        'status'

914	LOAD_FAST         'status'
917	POP_JUMP_IF_FALSE '945'

920	LOAD_GLOBAL       'DistutilsExecError'
923	LOAD_CONST        'Failed to execute: %s'
926	LOAD_GLOBAL       'repr'
929	LOAD_FAST         'q_cmd'
932	CALL_FUNCTION_1   None
935	BINARY_MODULO     None
936	CALL_FUNCTION_1   None
939	RAISE_VARARGS_1   None
942	JUMP_FORWARD      '945'
945_0	COME_FROM         '942'
945	POP_BLOCK         None
946	LOAD_CONST        None
949_0	COME_FROM         '768'

949	LOAD_FAST         'out'
952	LOAD_ATTR         'close'
955	CALL_FUNCTION_0   None
958	POP_TOP           None
959	END_FINALLY       None

960	LOAD_FAST         'self'
963	LOAD_ATTR         'spawn'
966	LOAD_FAST         'rpm_cmd'
969	CALL_FUNCTION_1   None
972	POP_TOP           None

973	LOAD_FAST         'self'
976	LOAD_ATTR         'dry_run'
979	POP_JUMP_IF_TRUE  '1159'

982	LOAD_FAST         'self'
985	LOAD_ATTR         'binary_only'
988	POP_JUMP_IF_TRUE  '1062'

991	LOAD_GLOBAL       'os'
994	LOAD_ATTR         'path'
997	LOAD_ATTR         'join'
1000	LOAD_FAST         'rpm_dir'
1003	LOAD_CONST        'SRPMS'
1006	BINARY_SUBSCR     None
1007	LOAD_FAST         'source_rpm'
1010	CALL_FUNCTION_2   None
1013	STORE_FAST        'srpm'

1016	LOAD_GLOBAL       'os'
1019	LOAD_ATTR         'path'
1022	LOAD_ATTR         'exists'
1025	LOAD_FAST         'srpm'
1028	CALL_FUNCTION_1   None
1031	POP_JUMP_IF_TRUE  '1040'
1034	LOAD_ASSERT       'AssertionError'
1037	RAISE_VARARGS_1   None

1040	LOAD_FAST         'self'
1043	LOAD_ATTR         'move_file'
1046	LOAD_FAST         'srpm'
1049	LOAD_FAST         'self'
1052	LOAD_ATTR         'dist_dir'
1055	CALL_FUNCTION_2   None
1058	POP_TOP           None
1059	JUMP_FORWARD      '1062'
1062_0	COME_FROM         '1059'

1062	LOAD_FAST         'self'
1065	LOAD_ATTR         'source_only'
1068	POP_JUMP_IF_TRUE  '1159'

1071	SETUP_LOOP        '1156'
1074	LOAD_FAST         'binary_rpms'
1077	GET_ITER          None
1078	FOR_ITER          '1152'
1081	STORE_FAST        'rpm'

1084	LOAD_GLOBAL       'os'
1087	LOAD_ATTR         'path'
1090	LOAD_ATTR         'join'
1093	LOAD_FAST         'rpm_dir'
1096	LOAD_CONST        'RPMS'
1099	BINARY_SUBSCR     None
1100	LOAD_FAST         'rpm'
1103	CALL_FUNCTION_2   None
1106	STORE_FAST        'rpm'

1109	LOAD_GLOBAL       'os'
1112	LOAD_ATTR         'path'
1115	LOAD_ATTR         'exists'
1118	LOAD_FAST         'rpm'
1121	CALL_FUNCTION_1   None
1124	POP_JUMP_IF_FALSE '1078'

1127	LOAD_FAST         'self'
1130	LOAD_ATTR         'move_file'
1133	LOAD_FAST         'rpm'
1136	LOAD_FAST         'self'
1139	LOAD_ATTR         'dist_dir'
1142	CALL_FUNCTION_2   None
1145	POP_TOP           None
1146	JUMP_BACK         '1078'
1149	JUMP_BACK         '1078'
1152	POP_BLOCK         None
1153_0	COME_FROM         '1071'
1153	JUMP_ABSOLUTE     '1159'
1156	JUMP_FORWARD      '1159'
1159_0	COME_FROM         '1156'
1159	LOAD_CONST        None
1162	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 901

    def _dist_path(self, path):
        return os.path.join(self.dist_dir, os.path.basename(path))

    def _make_spec_file(self):
        """Generate the text of an RPM spec file and return it as a
        list of strings (one per line).
        """
        spec_file = ['%define name ' + self.distribution.get_name(),
         '%define version ' + self.distribution.get_version().replace('-', '_'),
         '%define unmangled_version ' + self.distribution.get_version(),
         '%define release ' + self.release.replace('-', '_'),
         '',
         'Summary: ' + self.distribution.get_description()]
        spec_file.extend(['Name: %{name}', 'Version: %{version}', 'Release: %{release}'])
        if self.use_bzip2:
            spec_file.append('Source0: %{name}-%{unmangled_version}.tar.bz2')
        else:
            spec_file.append('Source0: %{name}-%{unmangled_version}.tar.gz')
        spec_file.extend(['License: ' + self.distribution.get_license(),
         'Group: ' + self.group,
         'BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot',
         'Prefix: %{_prefix}'])
        if not self.force_arch:
            if not self.distribution.has_ext_modules():
                spec_file.append('BuildArch: noarch')
        else:
            spec_file.append('BuildArch: %s' % self.force_arch)
        for field in ('Vendor', 'Packager', 'Provides', 'Requires', 'Conflicts', 'Obsoletes'):
            val = getattr(self, string.lower(field))
            if isinstance(val, list):
                spec_file.append('%s: %s' % (field, string.join(val)))
            elif val is not None:
                spec_file.append('%s: %s' % (field, val))

        if self.distribution.get_url() != 'UNKNOWN':
            spec_file.append('Url: ' + self.distribution.get_url())
        if self.distribution_name:
            spec_file.append('Distribution: ' + self.distribution_name)
        if self.build_requires:
            spec_file.append('BuildRequires: ' + string.join(self.build_requires))
        if self.icon:
            spec_file.append('Icon: ' + os.path.basename(self.icon))
        if self.no_autoreq:
            spec_file.append('AutoReq: 0')
        spec_file.extend(['', '%description', self.distribution.get_long_description()])
        def_setup_call = '%s %s' % (self.python, os.path.basename(sys.argv[0]))
        def_build = '%s build' % def_setup_call
        if self.use_rpm_opt_flags:
            def_build = 'env CFLAGS="$RPM_OPT_FLAGS" ' + def_build
        install_cmd = '%s install -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES' % def_setup_call
        script_options = [('prep', 'prep_script', '%setup -n %{name}-%{unmangled_version}'),
         ('build', 'build_script', def_build),
         ('install', 'install_script', install_cmd),
         ('clean', 'clean_script', 'rm -rf $RPM_BUILD_ROOT'),
         ('verifyscript', 'verify_script', None),
         ('pre', 'pre_install', None),
         ('post', 'post_install', None),
         ('preun', 'pre_uninstall', None),
         ('postun', 'post_uninstall', None)]
        for rpm_opt, attr, default in script_options:
            val = getattr(self, attr)
            if val or default:
                spec_file.extend(['', '%' + rpm_opt])
                if val:
                    spec_file.extend(string.split(open(val, 'r').read(), '\n'))
                else:
                    spec_file.append(default)

        spec_file.extend(['', '%files -f INSTALLED_FILES', '%defattr(-,root,root)'])
        if self.doc_files:
            spec_file.append('%doc ' + string.join(self.doc_files))
        if self.changelog:
            spec_file.extend(['', '%changelog'])
            spec_file.extend(self.changelog)
        return spec_file

    def _format_changelog(self, changelog):
        """Format the changelog correctly and convert it to a list of strings
        """
        if not changelog:
            return changelog
        new_changelog = []
        for line in string.split(string.strip(changelog), '\n'):
            line = string.strip(line)
            if line[0] == '*':
                new_changelog.extend(['', line])
            elif line[0] == '-':
                new_changelog.append(line)
            else:
                new_changelog.append('  ' + line)

        if not new_changelog[0]:
            del new_changelog[0]
        return new_changelog