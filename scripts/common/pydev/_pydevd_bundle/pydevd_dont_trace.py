# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_dont_trace.py
"""
Support for a tag that allows skipping over functions while debugging.
"""
import linecache
import re
from _pydevd_bundle.pydevd_constants import dict_contains
DONT_TRACE_TAG = '@DontTrace'
RE_DECORATOR = re.compile('^\\s*@')
_filename_to_ignored_lines = {}

def default_should_trace_hook(frame, filename):
    """
    Return True if this frame should be traced, False if tracing should be blocked.
    """
    ignored_lines = _filename_to_ignored_lines.get(filename)
    if ignored_lines is None:
        ignored_lines = {}
        lines = linecache.getlines(filename)
        i_line = 0
        for line in lines:
            j = line.find('#')
            if j >= 0:
                comment = line[j:]
                if DONT_TRACE_TAG in comment:
                    ignored_lines[i_line] = 1
                    k = i_line - 1
                    while k >= 0:
                        if RE_DECORATOR.match(lines[k]):
                            ignored_lines[k] = 1
                            k -= 1
                        else:
                            break

                    k = i_line + 1
                    while k <= len(lines):
                        if RE_DECORATOR.match(lines[k]):
                            ignored_lines[k] = 1
                            k += 1
                        else:
                            break

            i_line += 1

        _filename_to_ignored_lines[filename] = ignored_lines
    func_line = frame.f_code.co_firstlineno - 1
    return not (dict_contains(ignored_lines, func_line - 1) or dict_contains(ignored_lines, func_line))


should_trace_hook = None

def clear_trace_filter_cache():
    """
    Clear the trace filter cache.
    Call this after reloading.
    """
    global should_trace_hook
    try:
        old_hook = should_trace_hook
        should_trace_hook = None
        linecache.clearcache()
        _filename_to_ignored_lines.clear()
    finally:
        should_trace_hook = old_hook

    return


def trace_filter(mode):
    """
    Set the trace filter mode.
    
    mode: Whether to enable the trace hook.
      True: Trace filtering on (skipping methods tagged @DontTrace)
      False: Trace filtering off (trace methods tagged @DontTrace)
      None/default: Toggle trace filtering.
    """
    global should_trace_hook
    if mode is None:
        mode = should_trace_hook is None
    if mode:
        should_trace_hook = default_should_trace_hook
    else:
        should_trace_hook = None
    return mode