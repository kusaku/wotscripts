# Embedded file name: scripts/common/pydev/pydevd_file_utils.py
r"""
    This module provides utilities to get the absolute filenames so that we can be sure that:
        - The case of a file will match the actual file in the filesystem (otherwise breakpoints won't be hit).
        - Providing means for the user to make path conversions when doing a remote debugging session in
          one machine and debugging in another.

    To do that, the PATHS_FROM_ECLIPSE_TO_PYTHON constant must be filled with the appropriate paths.

    @note:
        in this context, the server is where your python process is running
        and the client is where eclipse is running.

    E.g.:
        If the server (your python process) has the structure
            /user/projects/my_project/src/package/module1.py

        and the client has:
            c:\my_project\src\package\module1.py

        the PATHS_FROM_ECLIPSE_TO_PYTHON would have to be:
            PATHS_FROM_ECLIPSE_TO_PYTHON = [(r'c:\my_project\src', r'/user/projects/my_project/src')]

    @note: DEBUG_CLIENT_SERVER_TRANSLATION can be set to True to debug the result of those translations

    @note: the case of the paths is important! Note that this can be tricky to get right when one machine
    uses a case-independent filesystem and the other uses a case-dependent filesystem (if the system being
    debugged is case-independent, 'normcase()' should be used on the paths defined in PATHS_FROM_ECLIPSE_TO_PYTHON).

    @note: all the paths with breakpoints must be translated (otherwise they won't be found in the server)

    @note: to enable remote debugging in the target machine (pydev extensions in the eclipse installation)
        import pydevd;pydevd.settrace(host, stdoutToServer, stderrToServer, port, suspend)

        see parameter docs on pydevd.py

    @note: for doing a remote debugging session, all the pydevd_ files must be on the server accessible
        through the PYTHONPATH (and the PATHS_FROM_ECLIPSE_TO_PYTHON only needs to be set on the target
        machine for the paths that'll actually have breakpoints).
"""
from _pydevd_bundle.pydevd_constants import *
from _pydev_bundle._pydev_filesystem_encoding import getfilesystemencoding
import os.path
import sys
import traceback
import ResMgr
import bwpydevd
os_normcase = os.path.normcase
basename = os.path.basename
exists = os.path.exists
join = os.path.join
try:
    rPath = os.path.realpath
except:
    rPath = os.path.abspath

PATHS_FROM_ECLIPSE_TO_PYTHON = bwpydevd.REPLACE_PATHS
normcase = os_normcase

def norm_case(filename):
    filename = os_normcase(filename)
    enc = getfilesystemencoding()
    if IS_PY3K or enc is None or enc.lower() == 'utf-8':
        return filename
    else:
        try:
            return filename.decode(enc).lower().encode(enc)
        except:
            return filename

        return


def set_ide_os(os):
    """
    We need to set the IDE os because the host where the code is running may be
    actually different from the client (and the point is that we want the proper
    paths to translate from the client to the server).
    """
    global PATHS_FROM_ECLIPSE_TO_PYTHON
    global normcase
    if os == 'UNIX':
        normcase = lambda f: f
    elif sys.platform == 'win32':
        normcase = norm_case
    else:
        normcase = os_normcase
    i = 0
    for path in PATHS_FROM_ECLIPSE_TO_PYTHON[:]:
        PATHS_FROM_ECLIPSE_TO_PYTHON[i] = (normcase(path[0]), normcase(path[1]))
        i += 1


DEBUG_CLIENT_SERVER_TRANSLATION = False
NORM_PATHS_CONTAINER = {}
NORM_PATHS_AND_BASE_CONTAINER = {}
NORM_FILENAME_TO_SERVER_CONTAINER = {}
NORM_FILENAME_TO_CLIENT_CONTAINER = {}

def _NormFile(filename):
    abs_path, real_path = _NormPaths(filename)
    return real_path


def _AbsFile(filename):
    abs_path, real_path = _NormPaths(filename)
    return abs_path


def _NormPaths(filename):
    try:
        return NORM_PATHS_CONTAINER[filename]
    except KeyError:
        filename = ResMgr.resolveToAbsolutePath(filename)
        abs_path = _NormPath(filename, os.path.abspath)
        real_path = _NormPath(filename, rPath)
        NORM_PATHS_CONTAINER[filename] = (abs_path, real_path)
        return (abs_path, real_path)


def _NormPath(filename, normpath):
    r = normcase(normpath(filename))
    ind = r.find('.zip')
    if ind == -1:
        ind = r.find('.egg')
    if ind != -1:
        ind += 4
        zip_path = r[:ind]
        if r[ind] == '!':
            ind += 1
        inner_path = r[ind:]
        if inner_path.startswith('/') or inner_path.startswith('\\'):
            inner_path = inner_path[1:]
        r = join(zip_path, inner_path)
    return r


ZIP_SEARCH_CACHE = {}

def exists(file):
    if os.path.exists(file):
        return file
    else:
        ind = file.find('.zip')
        if ind == -1:
            ind = file.find('.egg')
        if ind != -1:
            ind += 4
            zip_path = file[:ind]
            if file[ind] == '!':
                ind += 1
            inner_path = file[ind:]
            try:
                zip = ZIP_SEARCH_CACHE[zip_path]
            except KeyError:
                try:
                    import zipfile
                    zip = zipfile.ZipFile(zip_path, 'r')
                    ZIP_SEARCH_CACHE[zip_path] = zip
                except:
                    return

            try:
                if inner_path.startswith('/') or inner_path.startswith('\\'):
                    inner_path = inner_path[1:]
                info = zip.getinfo(inner_path.replace('\\', '/'))
                return join(zip_path, inner_path)
            except KeyError:
                return

        return


try:
    try:
        code = rPath.func_code
    except AttributeError:
        code = rPath.__code__

    if not exists(_NormFile(code.co_filename)):
        sys.stderr.write('-------------------------------------------------------------------------------\n')
        sys.stderr.write('pydev debugger: CRITICAL WARNING: This version of python seems to be incorrectly compiled (internal generated filenames are not absolute)\n')
        sys.stderr.write('pydev debugger: The debugger may still function, but it will work slower and may miss breakpoints.\n')
        sys.stderr.write('pydev debugger: Related bug: http://bugs.python.org/issue1666807\n')
        sys.stderr.write('-------------------------------------------------------------------------------\n')
        sys.stderr.flush()
        NORM_SEARCH_CACHE = {}
        initial_norm_paths = _NormPaths

        def _NormPaths(filename):
            try:
                return NORM_SEARCH_CACHE[filename]
            except KeyError:
                abs_path, real_path = initial_norm_paths(filename)
                if not exists(real_path):
                    for path in sys.path:
                        abs_path, real_path = initial_norm_paths(join(path, filename))
                        if exists(real_path):
                            break
                    else:
                        sys.stderr.write('pydev debugger: Unable to find real location for: %s\n' % (filename,))
                        abs_path = filename
                        real_path = filename

                NORM_SEARCH_CACHE[filename] = (abs_path, real_path)
                return (abs_path, real_path)


except:
    traceback.print_exc()

norm_file_to_client = _AbsFile
norm_file_to_server = _NormFile

def setup_client_server_paths(paths):
    """paths is the same format as PATHS_FROM_ECLIPSE_TO_PYTHON"""
    global PATHS_FROM_ECLIPSE_TO_PYTHON
    global norm_file_to_server
    global NORM_FILENAME_TO_SERVER_CONTAINER
    global norm_file_to_client
    global NORM_FILENAME_TO_CLIENT_CONTAINER
    NORM_FILENAME_TO_SERVER_CONTAINER = {}
    NORM_FILENAME_TO_CLIENT_CONTAINER = {}
    PATHS_FROM_ECLIPSE_TO_PYTHON = paths[:]
    if not PATHS_FROM_ECLIPSE_TO_PYTHON:
        norm_file_to_client = _AbsFile
        norm_file_to_server = _NormFile
        return
    else:
        eclipse_sep = None
        python_sep = None
        for eclipse_prefix, server_prefix in PATHS_FROM_ECLIPSE_TO_PYTHON:
            if eclipse_sep is not None and python_sep is not None:
                break
            if eclipse_sep is None:
                for c in eclipse_prefix:
                    if c in ('/', '\\'):
                        eclipse_sep = c
                        break

            if python_sep is None:
                for c in server_prefix:
                    if c in ('/', '\\'):
                        python_sep = c
                        break

        if eclipse_sep == python_sep or eclipse_sep is None or python_sep is None:
            eclipse_sep = python_sep = None

        def _norm_file_to_server(filename):
            try:
                return NORM_FILENAME_TO_SERVER_CONTAINER[filename]
            except KeyError:
                translated = normcase(filename)
                for eclipse_prefix, server_prefix in PATHS_FROM_ECLIPSE_TO_PYTHON:
                    if translated.startswith(eclipse_prefix):
                        if DEBUG_CLIENT_SERVER_TRANSLATION:
                            sys.stderr.write('pydev debugger: replacing to server: %s\n' % (translated,))
                        translated = translated.replace(eclipse_prefix, server_prefix)
                        if DEBUG_CLIENT_SERVER_TRANSLATION:
                            sys.stderr.write('pydev debugger: sent to server: %s\n' % (translated,))
                        break
                else:
                    if DEBUG_CLIENT_SERVER_TRANSLATION:
                        sys.stderr.write('pydev debugger: to server: unable to find matching prefix for: %s in %s\n' % (translated, [ x[0] for x in PATHS_FROM_ECLIPSE_TO_PYTHON ]))

                if eclipse_sep is not None:
                    translated = translated.replace(eclipse_sep, python_sep)
                translated = _NormFile(translated)
                NORM_FILENAME_TO_SERVER_CONTAINER[filename] = translated
                return translated

            return

        def _norm_file_to_client(filename):
            try:
                return NORM_FILENAME_TO_CLIENT_CONTAINER[filename]
            except KeyError:
                translated = _NormFile(filename)
                for eclipse_prefix, python_prefix in PATHS_FROM_ECLIPSE_TO_PYTHON:
                    if translated.startswith(python_prefix):
                        if DEBUG_CLIENT_SERVER_TRANSLATION:
                            sys.stderr.write('pydev debugger: replacing to client: %s\n' % (translated,))
                        translated = translated.replace(python_prefix, eclipse_prefix)
                        if DEBUG_CLIENT_SERVER_TRANSLATION:
                            sys.stderr.write('pydev debugger: sent to client: %s\n' % (translated,))
                        break
                else:
                    if DEBUG_CLIENT_SERVER_TRANSLATION:
                        sys.stderr.write('pydev debugger: to client: unable to find matching prefix for: %s in %s\n' % (translated, [ x[1] for x in PATHS_FROM_ECLIPSE_TO_PYTHON ]))

                if eclipse_sep is not None:
                    translated = translated.replace(python_sep, eclipse_sep)
                NORM_FILENAME_TO_CLIENT_CONTAINER[filename] = translated
                return translated

            return

        norm_file_to_server = _norm_file_to_server
        norm_file_to_client = _norm_file_to_client
        return


setup_client_server_paths(PATHS_FROM_ECLIPSE_TO_PYTHON)

def get_abs_path_real_path_and_base_from_file(f):
    try:
        return NORM_PATHS_AND_BASE_CONTAINER[f]
    except:
        abs_path, real_path = _NormPaths(f)
        base = basename(real_path)
        ret = (abs_path, real_path, base)
        NORM_PATHS_AND_BASE_CONTAINER[f] = ret
        return ret


def get_abs_path_real_path_and_base_from_frame(frame):
    try:
        return NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename]
    except:
        f = frame.f_code.co_filename
        if f is not None and f.startswith('build/bdist.'):
            f = frame.f_globals['__file__']
            if f.endswith('.pyc'):
                f = f[:-1]
        ret = get_abs_path_real_path_and_base_from_file(f)
        NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename] = ret
        return ret

    return