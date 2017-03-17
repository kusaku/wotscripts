# Embedded file name: scripts/common/Lib/distutils/file_util.py
"""distutils.file_util

Utility functions for operating on single files.
"""
__revision__ = '$Id$'
import os
from distutils.errors import DistutilsFileError
from distutils import log
_copy_action = {None: 'copying',
 'hard': 'hard linking',
 'sym': 'symbolically linking'}

def _copy_file_contents--- This code section failed: ---

0	LOAD_CONST        None
3	STORE_FAST        'fsrc'

6	LOAD_CONST        None
9	STORE_FAST        'fdst'

12	SETUP_FINALLY     '413'

15	SETUP_EXCEPT      '37'

18	LOAD_GLOBAL       'open'
21	LOAD_FAST         'src'
24	LOAD_CONST        'rb'
27	CALL_FUNCTION_2   None
30	STORE_FAST        'fsrc'
33	POP_BLOCK         None
34	JUMP_FORWARD      '87'
37_0	COME_FROM         '15'

37	DUP_TOP           None
38	LOAD_GLOBAL       'os'
41	LOAD_ATTR         'error'
44	COMPARE_OP        'exception match'
47	POP_JUMP_IF_FALSE '86'
50	POP_TOP           None
51	UNPACK_SEQUENCE_2 None
54	STORE_FAST        'errno'
57	STORE_FAST        'errstr'
60	POP_TOP           None

61	LOAD_GLOBAL       'DistutilsFileError'
64	LOAD_CONST        "could not open '%s': %s"
67	LOAD_FAST         'src'
70	LOAD_FAST         'errstr'
73	BUILD_TUPLE_2     None
76	BINARY_MODULO     None
77	CALL_FUNCTION_1   None
80	RAISE_VARARGS_1   None
83	JUMP_FORWARD      '87'
86	END_FINALLY       None
87_0	COME_FROM         '34'
87_1	COME_FROM         '86'

87	LOAD_GLOBAL       'os'
90	LOAD_ATTR         'path'
93	LOAD_ATTR         'exists'
96	LOAD_FAST         'dst'
99	CALL_FUNCTION_1   None
102	POP_JUMP_IF_FALSE '178'

105	SETUP_EXCEPT      '125'

108	LOAD_GLOBAL       'os'
111	LOAD_ATTR         'unlink'
114	LOAD_FAST         'dst'
117	CALL_FUNCTION_1   None
120	POP_TOP           None
121	POP_BLOCK         None
122	JUMP_ABSOLUTE     '178'
125_0	COME_FROM         '105'

125	DUP_TOP           None
126	LOAD_GLOBAL       'os'
129	LOAD_ATTR         'error'
132	COMPARE_OP        'exception match'
135	POP_JUMP_IF_FALSE '174'
138	POP_TOP           None
139	UNPACK_SEQUENCE_2 None
142	STORE_FAST        'errno'
145	STORE_FAST        'errstr'
148	POP_TOP           None

149	LOAD_GLOBAL       'DistutilsFileError'

152	LOAD_CONST        "could not delete '%s': %s"
155	LOAD_FAST         'dst'
158	LOAD_FAST         'errstr'
161	BUILD_TUPLE_2     None
164	BINARY_MODULO     None
165	CALL_FUNCTION_1   None
168	RAISE_VARARGS_1   None
171	JUMP_ABSOLUTE     '178'
174	END_FINALLY       None
175_0	COME_FROM         '174'
175	JUMP_FORWARD      '178'
178_0	COME_FROM         '175'

178	SETUP_EXCEPT      '200'

181	LOAD_GLOBAL       'open'
184	LOAD_FAST         'dst'
187	LOAD_CONST        'wb'
190	CALL_FUNCTION_2   None
193	STORE_FAST        'fdst'
196	POP_BLOCK         None
197	JUMP_FORWARD      '250'
200_0	COME_FROM         '178'

200	DUP_TOP           None
201	LOAD_GLOBAL       'os'
204	LOAD_ATTR         'error'
207	COMPARE_OP        'exception match'
210	POP_JUMP_IF_FALSE '249'
213	POP_TOP           None
214	UNPACK_SEQUENCE_2 None
217	STORE_FAST        'errno'
220	STORE_FAST        'errstr'
223	POP_TOP           None

224	LOAD_GLOBAL       'DistutilsFileError'

227	LOAD_CONST        "could not create '%s': %s"
230	LOAD_FAST         'dst'
233	LOAD_FAST         'errstr'
236	BUILD_TUPLE_2     None
239	BINARY_MODULO     None
240	CALL_FUNCTION_1   None
243	RAISE_VARARGS_1   None
246	JUMP_FORWARD      '250'
249	END_FINALLY       None
250_0	COME_FROM         '197'
250_1	COME_FROM         '249'

250	SETUP_LOOP        '409'

253	SETUP_EXCEPT      '275'

256	LOAD_FAST         'fsrc'
259	LOAD_ATTR         'read'
262	LOAD_FAST         'buffer_size'
265	CALL_FUNCTION_1   None
268	STORE_FAST        'buf'
271	POP_BLOCK         None
272	JUMP_FORWARD      '325'
275_0	COME_FROM         '253'

275	DUP_TOP           None
276	LOAD_GLOBAL       'os'
279	LOAD_ATTR         'error'
282	COMPARE_OP        'exception match'
285	POP_JUMP_IF_FALSE '324'
288	POP_TOP           None
289	UNPACK_SEQUENCE_2 None
292	STORE_FAST        'errno'
295	STORE_FAST        'errstr'
298	POP_TOP           None

299	LOAD_GLOBAL       'DistutilsFileError'

302	LOAD_CONST        "could not read from '%s': %s"
305	LOAD_FAST         'src'
308	LOAD_FAST         'errstr'
311	BUILD_TUPLE_2     None
314	BINARY_MODULO     None
315	CALL_FUNCTION_1   None
318	RAISE_VARARGS_1   None
321	JUMP_FORWARD      '325'
324	END_FINALLY       None
325_0	COME_FROM         '272'
325_1	COME_FROM         '324'

325	LOAD_FAST         'buf'
328	POP_JUMP_IF_TRUE  '335'

331	BREAK_LOOP        None
332	JUMP_FORWARD      '335'
335_0	COME_FROM         '332'

335	SETUP_EXCEPT      '355'

338	LOAD_FAST         'fdst'
341	LOAD_ATTR         'write'
344	LOAD_FAST         'buf'
347	CALL_FUNCTION_1   None
350	POP_TOP           None
351	POP_BLOCK         None
352	JUMP_BACK         '253'
355_0	COME_FROM         '335'

355	DUP_TOP           None
356	LOAD_GLOBAL       'os'
359	LOAD_ATTR         'error'
362	COMPARE_OP        'exception match'
365	POP_JUMP_IF_FALSE '404'
368	POP_TOP           None
369	UNPACK_SEQUENCE_2 None
372	STORE_FAST        'errno'
375	STORE_FAST        'errstr'
378	POP_TOP           None

379	LOAD_GLOBAL       'DistutilsFileError'

382	LOAD_CONST        "could not write to '%s': %s"
385	LOAD_FAST         'dst'
388	LOAD_FAST         'errstr'
391	BUILD_TUPLE_2     None
394	BINARY_MODULO     None
395	CALL_FUNCTION_1   None
398	RAISE_VARARGS_1   None
401	JUMP_BACK         '253'
404	END_FINALLY       None
405_0	COME_FROM         '404'
405	JUMP_BACK         '253'
408	POP_BLOCK         None
409_0	COME_FROM         '250'
409	POP_BLOCK         None
410	LOAD_CONST        None
413_0	COME_FROM         '12'

413	LOAD_FAST         'fdst'
416	POP_JUMP_IF_FALSE '432'

419	LOAD_FAST         'fdst'
422	LOAD_ATTR         'close'
425	CALL_FUNCTION_0   None
428	POP_TOP           None
429	JUMP_FORWARD      '432'
432_0	COME_FROM         '429'

432	LOAD_FAST         'fsrc'
435	POP_JUMP_IF_FALSE '451'

438	LOAD_FAST         'fsrc'
441	LOAD_ATTR         'close'
444	CALL_FUNCTION_0   None
447	POP_TOP           None
448	JUMP_FORWARD      '451'
451_0	COME_FROM         '448'
451	END_FINALLY       None
452	LOAD_CONST        None
455	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 408


def copy_file(src, dst, preserve_mode = 1, preserve_times = 1, update = 0, link = None, verbose = 1, dry_run = 0):
    """Copy a file 'src' to 'dst'.
    
    If 'dst' is a directory, then 'src' is copied there with the same name;
    otherwise, it must be a filename.  (If the file exists, it will be
    ruthlessly clobbered.)  If 'preserve_mode' is true (the default),
    the file's mode (type and permission bits, or whatever is analogous on
    the current platform) is copied.  If 'preserve_times' is true (the
    default), the last-modified and last-access times are copied as well.
    If 'update' is true, 'src' will only be copied if 'dst' does not exist,
    or if 'dst' does exist but is older than 'src'.
    
    'link' allows you to make hard links (os.link) or symbolic links
    (os.symlink) instead of copying: set it to "hard" or "sym"; if it is
    None (the default), files are copied.  Don't set 'link' on systems that
    don't support it: 'copy_file()' doesn't check if hard or symbolic
    linking is available.
    
    Under Mac OS, uses the native file copy function in macostools; on
    other systems, uses '_copy_file_contents()' to copy file contents.
    
    Return a tuple (dest_name, copied): 'dest_name' is the actual name of
    the output file, and 'copied' is true if the file was copied (or would
    have been copied, if 'dry_run' true).
    """
    from distutils.dep_util import newer
    from stat import ST_ATIME, ST_MTIME, ST_MODE, S_IMODE
    if not os.path.isfile(src):
        raise DistutilsFileError("can't copy '%s': doesn't exist or not a regular file" % src)
    if os.path.isdir(dst):
        dir = dst
        dst = os.path.join(dst, os.path.basename(src))
    else:
        dir = os.path.dirname(dst)
    if update and not newer(src, dst):
        if verbose >= 1:
            log.debug('not copying %s (output up-to-date)', src)
        return (dst, 0)
    try:
        action = _copy_action[link]
    except KeyError:
        raise ValueError("invalid value '%s' for 'link' argument" % link)

    if verbose >= 1:
        if os.path.basename(dst) == os.path.basename(src):
            log.info('%s %s -> %s', action, src, dir)
        else:
            log.info('%s %s -> %s', action, src, dst)
    if dry_run:
        return (dst, 1)
    if link == 'hard':
        if not (os.path.exists(dst) and os.path.samefile(src, dst)):
            os.link(src, dst)
    elif link == 'sym':
        if not (os.path.exists(dst) and os.path.samefile(src, dst)):
            os.symlink(src, dst)
    else:
        _copy_file_contents(src, dst)
        if preserve_mode or preserve_times:
            st = os.stat(src)
            if preserve_times:
                os.utime(dst, (st[ST_ATIME], st[ST_MTIME]))
            if preserve_mode:
                os.chmod(dst, S_IMODE(st[ST_MODE]))
    return (dst, 1)


def move_file(src, dst, verbose = 1, dry_run = 0):
    """Move a file 'src' to 'dst'.
    
    If 'dst' is a directory, the file will be moved into it with the same
    name; otherwise, 'src' is just renamed to 'dst'.  Return the new
    full name of the file.
    
    Handles cross-device moves on Unix using 'copy_file()'.  What about
    other systems???
    """
    from os.path import exists, isfile, isdir, basename, dirname
    import errno
    if verbose >= 1:
        log.info('moving %s -> %s', src, dst)
    if dry_run:
        return dst
    if not isfile(src):
        raise DistutilsFileError("can't move '%s': not a regular file" % src)
    if isdir(dst):
        dst = os.path.join(dst, basename(src))
    elif exists(dst):
        raise DistutilsFileError("can't move '%s': destination '%s' already exists" % (src, dst))
    if not isdir(dirname(dst)):
        raise DistutilsFileError("can't move '%s': destination '%s' not a valid path" % (src, dst))
    copy_it = 0
    try:
        os.rename(src, dst)
    except os.error as (num, msg):
        if num == errno.EXDEV:
            copy_it = 1
        else:
            raise DistutilsFileError("couldn't move '%s' to '%s': %s" % (src, dst, msg))

    if copy_it:
        copy_file(src, dst, verbose=verbose)
        try:
            os.unlink(src)
        except os.error as (num, msg):
            try:
                os.unlink(dst)
            except os.error:
                pass

            raise DistutilsFileError(("couldn't move '%s' to '%s' by copy/delete: " + "delete '%s' failed: %s") % (src,
             dst,
             src,
             msg))

    return dst


def write_file(filename, contents):
    """Create a file with the specified name and write 'contents' (a
    sequence of strings without line terminators) to it.
    """
    f = open(filename, 'w')
    try:
        for line in contents:
            f.write(line + '\n')

    finally:
        f.close()