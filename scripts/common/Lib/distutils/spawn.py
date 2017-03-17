# Embedded file name: scripts/common/Lib/distutils/spawn.py
"""distutils.spawn

Provides the 'spawn()' function, a front-end to various platform-
specific functions for launching another program in a sub-process.
Also provides the 'find_executable()' to search the path for a given
executable name.
"""
__revision__ = '$Id$'
import sys
import os
from distutils.errors import DistutilsPlatformError, DistutilsExecError
from distutils import log

def spawn(cmd, search_path = 1, verbose = 0, dry_run = 0):
    """Run another program, specified as a command list 'cmd', in a new process.
    
    'cmd' is just the argument list for the new process, ie.
    cmd[0] is the program to run and cmd[1:] are the rest of its arguments.
    There is no way to run a program with a name different from that of its
    executable.
    
    If 'search_path' is true (the default), the system's executable
    search path will be used to find the program; otherwise, cmd[0]
    must be the exact path to the executable.  If 'dry_run' is true,
    the command will not actually be run.
    
    Raise DistutilsExecError if running the program fails in any way; just
    return on success.
    """
    if os.name == 'posix':
        _spawn_posix(cmd, search_path, dry_run=dry_run)
    elif os.name == 'nt':
        _spawn_nt(cmd, search_path, dry_run=dry_run)
    elif os.name == 'os2':
        _spawn_os2(cmd, search_path, dry_run=dry_run)
    else:
        raise DistutilsPlatformError, "don't know how to spawn programs on platform '%s'" % os.name


def _nt_quote_args(args):
    """Quote command-line arguments for DOS/Windows conventions.
    
    Just wraps every argument which contains blanks in double quotes, and
    returns a new argument list.
    """
    for i, arg in enumerate(args):
        if ' ' in arg:
            args[i] = '"%s"' % arg

    return args


def _spawn_nt(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    cmd = _nt_quote_args(cmd)
    if search_path:
        executable = find_executable(executable) or executable
    log.info(' '.join([executable] + cmd[1:]))
    if not dry_run:
        try:
            rc = os.spawnv(os.P_WAIT, executable, cmd)
        except OSError as exc:
            raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

        if rc != 0:
            raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)


def _spawn_os2(cmd, search_path = 1, verbose = 0, dry_run = 0):
    executable = cmd[0]
    if search_path:
        executable = find_executable(executable) or executable
    log.info(' '.join([executable] + cmd[1:]))
    if not dry_run:
        try:
            rc = os.spawnv(os.P_WAIT, executable, cmd)
        except OSError as exc:
            raise DistutilsExecError, "command '%s' failed: %s" % (cmd[0], exc[-1])

        if rc != 0:
            log.debug("command '%s' failed with exit status %d" % (cmd[0], rc))
            raise DistutilsExecError, "command '%s' failed with exit status %d" % (cmd[0], rc)


if sys.platform == 'darwin':
    from distutils import sysconfig
    _cfg_target = None
    _cfg_target_split = None

def _spawn_posix--- This code section failed: ---

0	LOAD_GLOBAL       'log'
3	LOAD_ATTR         'info'
6	LOAD_CONST        ' '
9	LOAD_ATTR         'join'
12	LOAD_FAST         'cmd'
15	CALL_FUNCTION_1   None
18	CALL_FUNCTION_1   None
21	POP_TOP           None

22	LOAD_FAST         'dry_run'
25	POP_JUMP_IF_FALSE '32'

28	LOAD_CONST        None
31	RETURN_END_IF     None

32	LOAD_FAST         'search_path'
35	POP_JUMP_IF_FALSE '47'
38	LOAD_GLOBAL       'os'
41	LOAD_ATTR         'execvp'
44_0	COME_FROM         '35'
44	JUMP_IF_TRUE_OR_POP '53'
47	LOAD_GLOBAL       'os'
50	LOAD_ATTR         'execv'
53_0	COME_FROM         '44'
53	STORE_FAST        'exec_fn'

56	LOAD_FAST         'cmd'
59	LOAD_CONST        0
62	BINARY_SUBSCR     None
63	LOAD_FAST         'cmd'
66	BUILD_LIST_2      None
69	STORE_FAST        'exec_args'

72	LOAD_GLOBAL       'sys'
75	LOAD_ATTR         'platform'
78	LOAD_CONST        'darwin'
81	COMPARE_OP        '=='
84	POP_JUMP_IF_FALSE '340'

87	LOAD_GLOBAL       '_cfg_target'
90	LOAD_CONST        None
93	COMPARE_OP        'is'
96	POP_JUMP_IF_FALSE '172'

99	LOAD_GLOBAL       'sysconfig'
102	LOAD_ATTR         'get_config_var'

105	LOAD_CONST        'MACOSX_DEPLOYMENT_TARGET'
108	CALL_FUNCTION_1   None
111	JUMP_IF_TRUE_OR_POP '117'
114	LOAD_CONST        ''
117_0	COME_FROM         '111'
117	STORE_GLOBAL      '_cfg_target'

120	LOAD_GLOBAL       '_cfg_target'
123	POP_JUMP_IF_FALSE '172'

126	BUILD_LIST_0      None
129	LOAD_GLOBAL       '_cfg_target'
132	LOAD_ATTR         'split'
135	LOAD_CONST        '.'
138	CALL_FUNCTION_1   None
141	GET_ITER          None
142	FOR_ITER          '163'
145	STORE_FAST        'x'
148	LOAD_GLOBAL       'int'
151	LOAD_FAST         'x'
154	CALL_FUNCTION_1   None
157	LIST_APPEND       None
160	JUMP_BACK         '142'
163	STORE_GLOBAL      '_cfg_target_split'
166	JUMP_ABSOLUTE     '172'
169	JUMP_FORWARD      '172'
172_0	COME_FROM         '169'

172	LOAD_GLOBAL       '_cfg_target'
175	POP_JUMP_IF_FALSE '340'

178	LOAD_GLOBAL       'os'
181	LOAD_ATTR         'environ'
184	LOAD_ATTR         'get'
187	LOAD_CONST        'MACOSX_DEPLOYMENT_TARGET'
190	LOAD_GLOBAL       '_cfg_target'
193	CALL_FUNCTION_2   None
196	STORE_FAST        'cur_target'

199	LOAD_GLOBAL       '_cfg_target_split'
202	BUILD_LIST_0      None
205	LOAD_FAST         'cur_target'
208	LOAD_ATTR         'split'
211	LOAD_CONST        '.'
214	CALL_FUNCTION_1   None
217	GET_ITER          None
218	FOR_ITER          '239'
221	STORE_FAST        'x'
224	LOAD_GLOBAL       'int'
227	LOAD_FAST         'x'
230	CALL_FUNCTION_1   None
233	LIST_APPEND       None
236	JUMP_BACK         '218'
239	COMPARE_OP        '>'
242	POP_JUMP_IF_FALSE '276'

245	LOAD_CONST        '$MACOSX_DEPLOYMENT_TARGET mismatch: now "%s" but "%s" during configure'

248	LOAD_FAST         'cur_target'
251	LOAD_GLOBAL       '_cfg_target'
254	BUILD_TUPLE_2     None
257	BINARY_MODULO     None
258	STORE_FAST        'my_msg'

261	LOAD_GLOBAL       'DistutilsPlatformError'
264	LOAD_FAST         'my_msg'
267	CALL_FUNCTION_1   None
270	RAISE_VARARGS_1   None
273	JUMP_FORWARD      '276'
276_0	COME_FROM         '273'

276	LOAD_GLOBAL       'dict'
279	LOAD_GLOBAL       'os'
282	LOAD_ATTR         'environ'
285	LOAD_CONST        'MACOSX_DEPLOYMENT_TARGET'

288	LOAD_FAST         'cur_target'
291	CALL_FUNCTION_257 None
294	STORE_FAST        'env'

297	LOAD_FAST         'search_path'
300	POP_JUMP_IF_FALSE '312'
303	LOAD_GLOBAL       'os'
306	LOAD_ATTR         'execvpe'
309_0	COME_FROM         '300'
309	JUMP_IF_TRUE_OR_POP '318'
312	LOAD_GLOBAL       'os'
315	LOAD_ATTR         'execve'
318_0	COME_FROM         '309'
318	STORE_FAST        'exec_fn'

321	LOAD_FAST         'exec_args'
324	LOAD_ATTR         'append'
327	LOAD_FAST         'env'
330	CALL_FUNCTION_1   None
333	POP_TOP           None
334	JUMP_ABSOLUTE     '340'
337	JUMP_FORWARD      '340'
340_0	COME_FROM         '337'

340	LOAD_GLOBAL       'os'
343	LOAD_ATTR         'fork'
346	CALL_FUNCTION_0   None
349	STORE_FAST        'pid'

352	LOAD_FAST         'pid'
355	LOAD_CONST        0
358	COMPARE_OP        '=='
361	POP_JUMP_IF_FALSE '486'

364	SETUP_EXCEPT      '381'

367	LOAD_FAST         'exec_fn'
370	LOAD_FAST         'exec_args'
373	CALL_FUNCTION_VAR_0 None
376	POP_TOP           None
377	POP_BLOCK         None
378	JUMP_FORWARD      '446'
381_0	COME_FROM         '364'

381	DUP_TOP           None
382	LOAD_GLOBAL       'OSError'
385	COMPARE_OP        'exception match'
388	POP_JUMP_IF_FALSE '445'
391	POP_TOP           None
392	STORE_FAST        'e'
395	POP_TOP           None

396	LOAD_GLOBAL       'sys'
399	LOAD_ATTR         'stderr'
402	LOAD_ATTR         'write'
405	LOAD_CONST        'unable to execute %s: %s\n'

408	LOAD_FAST         'cmd'
411	LOAD_CONST        0
414	BINARY_SUBSCR     None
415	LOAD_FAST         'e'
418	LOAD_ATTR         'strerror'
421	BUILD_TUPLE_2     None
424	BINARY_MODULO     None
425	CALL_FUNCTION_1   None
428	POP_TOP           None

429	LOAD_GLOBAL       'os'
432	LOAD_ATTR         '_exit'
435	LOAD_CONST        1
438	CALL_FUNCTION_1   None
441	POP_TOP           None
442	JUMP_FORWARD      '446'
445	END_FINALLY       None
446_0	COME_FROM         '378'
446_1	COME_FROM         '445'

446	LOAD_GLOBAL       'sys'
449	LOAD_ATTR         'stderr'
452	LOAD_ATTR         'write'
455	LOAD_CONST        'unable to execute %s for unknown reasons'
458	LOAD_FAST         'cmd'
461	LOAD_CONST        0
464	BINARY_SUBSCR     None
465	BINARY_MODULO     None
466	CALL_FUNCTION_1   None
469	POP_TOP           None

470	LOAD_GLOBAL       'os'
473	LOAD_ATTR         '_exit'
476	LOAD_CONST        1
479	CALL_FUNCTION_1   None
482	POP_TOP           None
483	JUMP_FORWARD      '772'

486	SETUP_LOOP        '772'

489	SETUP_EXCEPT      '520'

492	LOAD_GLOBAL       'os'
495	LOAD_ATTR         'waitpid'
498	LOAD_FAST         'pid'
501	LOAD_CONST        0
504	CALL_FUNCTION_2   None
507	UNPACK_SEQUENCE_2 None
510	STORE_FAST        'pid'
513	STORE_FAST        'status'
516	POP_BLOCK         None
517	JUMP_FORWARD      '602'
520_0	COME_FROM         '489'

520	DUP_TOP           None
521	LOAD_GLOBAL       'OSError'
524	COMPARE_OP        'exception match'
527	POP_JUMP_IF_FALSE '601'
530	POP_TOP           None
531	STORE_FAST        'exc'
534	POP_TOP           None

535	LOAD_CONST        -1
538	LOAD_CONST        None
541	IMPORT_NAME       'errno'
544	STORE_FAST        'errno'

547	LOAD_FAST         'exc'
550	LOAD_ATTR         'errno'
553	LOAD_FAST         'errno'
556	LOAD_ATTR         'EINTR'
559	COMPARE_OP        '=='
562	POP_JUMP_IF_FALSE '571'

565	CONTINUE          '489'
568	JUMP_FORWARD      '571'
571_0	COME_FROM         '568'

571	LOAD_GLOBAL       'DistutilsExecError'

574	LOAD_CONST        "command '%s' failed: %s"
577	LOAD_FAST         'cmd'
580	LOAD_CONST        0
583	BINARY_SUBSCR     None
584	LOAD_FAST         'exc'
587	LOAD_CONST        -1
590	BINARY_SUBSCR     None
591	BUILD_TUPLE_2     None
594	BINARY_MODULO     None
595	RAISE_VARARGS_2   None
598	JUMP_FORWARD      '602'
601	END_FINALLY       None
602_0	COME_FROM         '517'
602_1	COME_FROM         '601'

602	LOAD_GLOBAL       'os'
605	LOAD_ATTR         'WIFSIGNALED'
608	LOAD_FAST         'status'
611	CALL_FUNCTION_1   None
614	POP_JUMP_IF_FALSE '652'

617	LOAD_GLOBAL       'DistutilsExecError'

620	LOAD_CONST        "command '%s' terminated by signal %d"

623	LOAD_FAST         'cmd'
626	LOAD_CONST        0
629	BINARY_SUBSCR     None
630	LOAD_GLOBAL       'os'
633	LOAD_ATTR         'WTERMSIG'
636	LOAD_FAST         'status'
639	CALL_FUNCTION_1   None
642	BUILD_TUPLE_2     None
645	BINARY_MODULO     None
646	RAISE_VARARGS_2   None
649	JUMP_BACK         '489'

652	LOAD_GLOBAL       'os'
655	LOAD_ATTR         'WIFEXITED'
658	LOAD_FAST         'status'
661	CALL_FUNCTION_1   None
664	POP_JUMP_IF_FALSE '724'

667	LOAD_GLOBAL       'os'
670	LOAD_ATTR         'WEXITSTATUS'
673	LOAD_FAST         'status'
676	CALL_FUNCTION_1   None
679	STORE_FAST        'exit_status'

682	LOAD_FAST         'exit_status'
685	LOAD_CONST        0
688	COMPARE_OP        '=='
691	POP_JUMP_IF_FALSE '698'

694	LOAD_CONST        None
697	RETURN_END_IF     None

698	LOAD_GLOBAL       'DistutilsExecError'

701	LOAD_CONST        "command '%s' failed with exit status %d"

704	LOAD_FAST         'cmd'
707	LOAD_CONST        0
710	BINARY_SUBSCR     None
711	LOAD_FAST         'exit_status'
714	BUILD_TUPLE_2     None
717	BINARY_MODULO     None
718	RAISE_VARARGS_2   None
721	JUMP_BACK         '489'

724	LOAD_GLOBAL       'os'
727	LOAD_ATTR         'WIFSTOPPED'
730	LOAD_FAST         'status'
733	CALL_FUNCTION_1   None
736	POP_JUMP_IF_FALSE '745'

739	CONTINUE          '489'
742	JUMP_BACK         '489'

745	LOAD_GLOBAL       'DistutilsExecError'

748	LOAD_CONST        "unknown error executing '%s': termination status %d"

751	LOAD_FAST         'cmd'
754	LOAD_CONST        0
757	BINARY_SUBSCR     None
758	LOAD_FAST         'status'
761	BUILD_TUPLE_2     None
764	BINARY_MODULO     None
765	RAISE_VARARGS_2   None
768	JUMP_BACK         '489'
771	POP_BLOCK         None
772_0	COME_FROM         '483'
772_1	COME_FROM         '486'
772	LOAD_CONST        None
775	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 771


def find_executable(executable, path = None):
    """Tries to find 'executable' in the directories listed in 'path'.
    
    A string listing directories separated by 'os.pathsep'; defaults to
    os.environ['PATH'].  Returns the complete filename or None if not found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    base, ext = os.path.splitext(executable)
    if (sys.platform == 'win32' or os.name == 'os2') and ext != '.exe':
        executable = executable + '.exe'
    if not os.path.isfile(executable):
        for p in paths:
            f = os.path.join(p, executable)
            if os.path.isfile(f):
                return f

        return
    else:
        return executable
        return


global _cfg_target ## Warning: Unused globalglobal _cfg_target_split ## Warning: Unused global