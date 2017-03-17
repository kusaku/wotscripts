# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_frame.py
import linecache
import os.path
import re
import sys
import traceback
from _pydev_bundle import pydev_log
from _pydevd_bundle import pydevd_dont_trace
from _pydevd_bundle import pydevd_vars
from _pydevd_bundle.pydevd_breakpoints import get_exception_breakpoint
from _pydevd_bundle.pydevd_comm import CMD_STEP_CAUGHT_EXCEPTION, CMD_STEP_RETURN, CMD_STEP_OVER, CMD_SET_BREAK, CMD_STEP_INTO, CMD_SMART_STEP_INTO, CMD_RUN_TO_LINE, CMD_SET_NEXT_STATEMENT, CMD_STEP_INTO_MY_CODE
from _pydevd_bundle.pydevd_constants import STATE_SUSPEND, dict_contains, get_thread_id, STATE_RUN, dict_iter_values
from _pydevd_bundle.pydevd_frame_utils import add_exception_to_frame, just_raised
from pydevd_file_utils import get_abs_path_real_path_and_base_from_frame
try:
    from inspect import CO_GENERATOR
except:
    CO_GENERATOR = 0

try:
    from _pydevd_bundle.pydevd_signature import send_signature_call_trace
except ImportError:

    def send_signature_call_trace(*args, **kwargs):
        pass


basename = os.path.basename
IGNORE_EXCEPTION_TAG = re.compile('[^#]*#.*@IgnoreException')
DEBUG_START = ('pydevd.py', 'run')
DEBUG_START_PY3K = ('_pydev_execfile.py', 'execfile')
TRACE_PROPERTY = 'pydevd_traceproperty.py'

class PyDBFrame:
    """This makes the tracing for a given frame, so, the trace_dispatch
    is used initially when we enter into a new context ('call') and then
    is reused for the entire context.
    """
    filename_to_lines_where_exceptions_are_ignored = {}
    filename_to_stat_info = {}
    should_skip = -1

    def __init__(self, args):
        self._args = args[:-1]

    def set_suspend(self, *args, **kwargs):
        self._args[0].set_suspend(*args, **kwargs)

    def do_wait_suspend(self, *args, **kwargs):
        self._args[0].do_wait_suspend(*args, **kwargs)

    def trace_exception(self, frame, event, arg):
        if event == 'exception':
            flag, frame = self.should_stop_on_exception(frame, event, arg)
            if flag:
                self.handle_exception(frame, event, arg)
                return self.trace_dispatch
        return self.trace_exception

    def should_stop_on_exception(self, frame, event, arg):
        main_debugger = self._args[0]
        info = self._args[2]
        flag = False
        if info.pydev_state != STATE_SUSPEND:
            exception, value, trace = arg
            if trace is not None:
                exception_breakpoint = get_exception_breakpoint(exception, main_debugger.break_on_caught_exceptions)
                if exception_breakpoint is not None:
                    if exception_breakpoint.ignore_libraries:
                        if exception_breakpoint.notify_on_first_raise_only:
                            if main_debugger.first_appearance_in_scope(trace):
                                add_exception_to_frame(frame, (exception, value, trace))
                                try:
                                    info.pydev_message = exception_breakpoint.qname
                                except:
                                    info.pydev_message = exception_breakpoint.qname.encode('utf-8')

                                flag = True
                            else:
                                pydev_log.debug('Ignore exception %s in library %s' % (exception, frame.f_code.co_filename))
                                flag = False
                    elif not exception_breakpoint.notify_on_first_raise_only or just_raised(trace):
                        add_exception_to_frame(frame, (exception, value, trace))
                        try:
                            info.pydev_message = exception_breakpoint.qname
                        except:
                            info.pydev_message = exception_breakpoint.qname.encode('utf-8')

                        flag = True
                    else:
                        flag = False
                else:
                    try:
                        if main_debugger.plugin is not None:
                            result = main_debugger.plugin.exception_break(main_debugger, self, frame, self._args, arg)
                            if result:
                                flag, frame = result
                    except:
                        flag = False

        return (flag, frame)

    def handle_exception(self, frame, event, arg):
        try:
            trace_obj = arg[2]
            main_debugger = self._args[0]
            if not hasattr(trace_obj, 'tb_next'):
                return
            initial_trace_obj = trace_obj
            if trace_obj.tb_next is None and trace_obj.tb_frame is frame:
                if main_debugger.break_on_exceptions_thrown_in_same_context:
                    return
            else:
                while trace_obj.tb_next is not None:
                    trace_obj = trace_obj.tb_next

            if main_debugger.ignore_exceptions_thrown_in_lines_with_ignore_exception:
                for check_trace_obj in (initial_trace_obj, trace_obj):
                    filename = get_abs_path_real_path_and_base_from_frame(check_trace_obj.tb_frame)[1]
                    filename_to_lines_where_exceptions_are_ignored = self.filename_to_lines_where_exceptions_are_ignored
                    lines_ignored = filename_to_lines_where_exceptions_are_ignored.get(filename)
                    if lines_ignored is None:
                        lines_ignored = filename_to_lines_where_exceptions_are_ignored[filename] = {}
                    try:
                        curr_stat = os.stat(filename)
                        curr_stat = (curr_stat.st_size, curr_stat.st_mtime)
                    except:
                        curr_stat = None

                    last_stat = self.filename_to_stat_info.get(filename)
                    if last_stat != curr_stat:
                        self.filename_to_stat_info[filename] = curr_stat
                        lines_ignored.clear()
                        try:
                            linecache.checkcache(filename)
                        except:
                            linecache.checkcache()

                    from_user_input = main_debugger.filename_to_lines_where_exceptions_are_ignored.get(filename)
                    if from_user_input:
                        merged = {}
                        merged.update(lines_ignored)
                        merged.update(from_user_input)
                    else:
                        merged = lines_ignored
                    exc_lineno = check_trace_obj.tb_lineno
                    if not dict_contains(merged, exc_lineno):
                        try:
                            line = linecache.getline(filename, exc_lineno, check_trace_obj.tb_frame.f_globals)
                        except:
                            line = linecache.getline(filename, exc_lineno)

                        if IGNORE_EXCEPTION_TAG.match(line) is not None:
                            lines_ignored[exc_lineno] = 1
                            return
                        lines_ignored[exc_lineno] = 0
                    elif merged.get(exc_lineno, 0):
                        return

            thread = self._args[3]
            try:
                frame_id_to_frame = {}
                frame_id_to_frame[id(frame)] = frame
                f = trace_obj.tb_frame
                while f is not None:
                    frame_id_to_frame[id(f)] = f
                    f = f.f_back

                f = None
                thread_id = get_thread_id(thread)
                pydevd_vars.add_additional_frame_by_id(thread_id, frame_id_to_frame)
                try:
                    main_debugger.send_caught_exception_stack(thread, arg, id(frame))
                    self.set_suspend(thread, CMD_STEP_CAUGHT_EXCEPTION)
                    self.do_wait_suspend(thread, frame, event, arg)
                    main_debugger.send_caught_exception_stack_proceeded(thread)
                finally:
                    pydevd_vars.remove_additional_frame_by_id(thread_id)

            except:
                traceback.print_exc()

            main_debugger.set_trace_for_frame_and_parents(frame)
        finally:
            trace_obj = None
            initial_trace_obj = None
            check_trace_obj = None
            f = None
            frame_id_to_frame = None
            main_debugger = None
            thread = None

        return

    def trace_dispatch(self, frame, event, arg):
        main_debugger, filename, info, thread = self._args
        try:
            info.is_tracing = True
            if main_debugger._finish_debugging_session:
                return
            if event == 'call' and main_debugger.signature_factory:
                send_signature_call_trace(main_debugger, frame, filename)
            plugin_manager = main_debugger.plugin
            is_exception_event = event == 'exception'
            has_exception_breakpoints = main_debugger.break_on_caught_exceptions or main_debugger.has_plugin_exception_breaks
            if is_exception_event:
                if has_exception_breakpoints:
                    flag, frame = self.should_stop_on_exception(frame, event, arg)
                    if flag:
                        self.handle_exception(frame, event, arg)
                        return self.trace_dispatch
            elif event not in ('line', 'call', 'return'):
                return
            stop_frame = info.pydev_step_stop
            step_cmd = info.pydev_step_cmd
            if is_exception_event:
                breakpoints_for_file = None
                if stop_frame and stop_frame is not frame and step_cmd == CMD_STEP_OVER and arg[0] in (StopIteration, GeneratorExit) and arg[2] is None:
                    info.pydev_step_cmd = CMD_STEP_INTO
                    info.pydev_step_stop = None
            else:
                if stop_frame is frame and event == 'return' and step_cmd in (CMD_STEP_RETURN, CMD_STEP_OVER):
                    if not frame.f_code.co_flags & CO_GENERATOR:
                        info.pydev_step_cmd = CMD_STEP_INTO
                        info.pydev_step_stop = None
                breakpoints_for_file = main_debugger.breakpoints.get(filename)
                can_skip = False
                if info.pydev_state == STATE_RUN:
                    can_skip = step_cmd == -1 and stop_frame is None or step_cmd in (CMD_STEP_RETURN, CMD_STEP_OVER) and stop_frame is not frame
                if can_skip and plugin_manager is not None and main_debugger.has_plugin_line_breaks:
                    can_skip = not plugin_manager.can_not_skip(main_debugger, self, frame)
                if not breakpoints_for_file:
                    if can_skip:
                        if has_exception_breakpoints:
                            return self.trace_exception
                        else:
                            return
                else:
                    curr_func_name = frame.f_code.co_name
                    if curr_func_name in ('?', '<module>'):
                        curr_func_name = ''
                    for breakpoint in dict_iter_values(breakpoints_for_file):
                        if breakpoint.func_name in ('None', curr_func_name):
                            break
                    else:
                        if can_skip:
                            if has_exception_breakpoints:
                                return self.trace_exception
                            else:
                                return

            try:
                line = frame.f_lineno
                flag = False
                stop_info = {}
                breakpoint = None
                exist_result = False
                stop = False
                bp_type = None
                if not flag and event != 'return' and info.pydev_state != STATE_SUSPEND and breakpoints_for_file is not None and dict_contains(breakpoints_for_file, line):
                    breakpoint = breakpoints_for_file[line]
                    new_frame = frame
                    stop = True
                    if step_cmd == CMD_STEP_OVER and stop_frame is frame and event in ('line', 'return'):
                        stop = False
                elif plugin_manager is not None and main_debugger.has_plugin_line_breaks:
                    result = plugin_manager.get_breakpoint(main_debugger, self, frame, event, self._args)
                    if result:
                        exist_result = True
                        flag, breakpoint, new_frame, bp_type = result
                if breakpoint:
                    if stop or exist_result:
                        condition = breakpoint.condition
                        if condition is not None:
                            try:
                                val = eval(condition, new_frame.f_globals, new_frame.f_locals)
                                if not val:
                                    return self.trace_dispatch
                            except:
                                if type(condition) != type(''):
                                    if hasattr(condition, 'encode'):
                                        condition = condition.encode('utf-8')
                                msg = 'Error while evaluating expression: %s\n' % (condition,)
                                sys.stderr.write(msg)
                                traceback.print_exc()
                                if not main_debugger.suspend_on_breakpoint_exception:
                                    return self.trace_dispatch
                                stop = True
                                try:
                                    etype, value, tb = sys.exc_info()
                                    try:
                                        error = ''.join(traceback.format_exception_only(etype, value))
                                        stack = traceback.extract_stack(f=tb.tb_frame.f_back)
                                        info.conditional_breakpoint_exception = ('Condition:\n' + condition + '\n\nError:\n' + error, stack)
                                    finally:
                                        etype, value, tb = (None, None, None)

                                except:
                                    traceback.print_exc()

                        if breakpoint.expression is not None:
                            try:
                                val = eval(breakpoint.expression, new_frame.f_globals, new_frame.f_locals)
                            except:
                                val = sys.exc_info()[1]
                            finally:
                                if val is not None:
                                    info.pydev_message = str(val)

                        if not main_debugger.first_breakpoint_reached:
                            if event == 'call':
                                if hasattr(frame, 'f_back'):
                                    back = frame.f_back
                                    if back is not None:
                                        _, back_filename, base = get_abs_path_real_path_and_base_from_frame(back)
                                        if base == DEBUG_START[0] and back.f_code.co_name == DEBUG_START[1] or base == DEBUG_START_PY3K[0] and back.f_code.co_name == DEBUG_START_PY3K[1]:
                                            stop = False
                                            main_debugger.first_breakpoint_reached = True
                elif step_cmd != -1:
                    if main_debugger.is_filter_enabled and main_debugger.is_ignored_by_filters(filename):
                        return self.trace_dispatch
                    if main_debugger.is_filter_libraries and main_debugger.not_in_scope(filename):
                        return self.trace_dispatch
                if stop:
                    self.set_suspend(thread, CMD_SET_BREAK)
                elif flag and plugin_manager is not None:
                    result = plugin_manager.suspend(main_debugger, thread, frame, bp_type)
                    if result:
                        frame = result
                if info.pydev_state == STATE_SUSPEND:
                    self.do_wait_suspend(thread, frame, event, arg)
                    return self.trace_dispatch
            except:
                traceback.print_exc()
                raise

            try:
                should_skip = 0
                if pydevd_dont_trace.should_trace_hook is not None:
                    if self.should_skip == -1:
                        if not pydevd_dont_trace.should_trace_hook(frame, filename):
                            should_skip = self.should_skip = 1
                        else:
                            should_skip = self.should_skip = 0
                    else:
                        should_skip = self.should_skip
                plugin_stop = False
                if should_skip:
                    stop = False
                elif step_cmd == CMD_STEP_INTO:
                    stop = event in ('line', 'return')
                    if plugin_manager is not None:
                        result = plugin_manager.cmd_step_into(main_debugger, frame, event, self._args, stop_info, stop)
                        if result:
                            stop, plugin_stop = result
                elif step_cmd == CMD_STEP_INTO_MY_CODE:
                    if not main_debugger.not_in_scope(frame.f_code.co_filename):
                        stop = event == 'line'
                elif step_cmd == CMD_STEP_OVER:
                    stop = stop_frame is frame and event in ('line', 'return')
                    if frame.f_code.co_flags & CO_GENERATOR:
                        if event == 'return':
                            stop = False
                    if plugin_manager is not None:
                        result = plugin_manager.cmd_step_over(main_debugger, frame, event, self._args, stop_info, stop)
                        if result:
                            stop, plugin_stop = result
                elif step_cmd == CMD_SMART_STEP_INTO:
                    stop = False
                    if info.pydev_smart_step_stop is frame:
                        info.pydev_func_name = '.invalid.'
                        info.pydev_smart_step_stop = None
                    if event == 'line' or event == 'exception':
                        curr_func_name = frame.f_code.co_name
                        if curr_func_name in ('?', '<module>') or curr_func_name is None:
                            curr_func_name = ''
                        if curr_func_name == info.pydev_func_name:
                            stop = True
                elif step_cmd == CMD_STEP_RETURN:
                    stop = event == 'return' and stop_frame is frame
                elif step_cmd == CMD_RUN_TO_LINE or step_cmd == CMD_SET_NEXT_STATEMENT:
                    stop = False
                    if event == 'line' or event == 'exception':
                        curr_func_name = frame.f_code.co_name
                        if curr_func_name in ('?', '<module>'):
                            curr_func_name = ''
                        if curr_func_name == info.pydev_func_name:
                            line = info.pydev_next_line
                            if frame.f_lineno == line:
                                stop = True
                            else:
                                if frame.f_trace is None:
                                    frame.f_trace = self.trace_dispatch
                                frame.f_lineno = line
                                frame.f_trace = None
                                stop = True
                else:
                    stop = False
                if plugin_stop:
                    stopped_on_plugin = plugin_manager.stop(main_debugger, frame, event, self._args, stop_info, arg, step_cmd)
                elif stop:
                    if event == 'line':
                        self.set_suspend(thread, step_cmd)
                        self.do_wait_suspend(thread, frame, event, arg)
                    else:
                        back = frame.f_back
                        if back is not None:
                            _, back_filename, base = get_abs_path_real_path_and_base_from_frame(back)
                            if base == DEBUG_START[0] and back.f_code.co_name == DEBUG_START[1]:
                                back = None
                            else:
                                if base == TRACE_PROPERTY:
                                    return
                                if pydevd_dont_trace.should_trace_hook is not None:
                                    if not pydevd_dont_trace.should_trace_hook(back, back_filename):
                                        main_debugger.set_trace_for_frame_and_parents(back, overwrite_prev_trace=True)
                                        return
                        if back is not None:
                            self.set_suspend(thread, step_cmd)
                            self.do_wait_suspend(thread, back, event, arg)
                        else:
                            info.pydev_step_stop = None
                            info.pydev_step_cmd = -1
                            info.pydev_state = STATE_RUN
            except KeyboardInterrupt:
                raise
            except:
                try:
                    traceback.print_exc()
                    info.pydev_step_cmd = -1
                except:
                    return

            retVal = None
            if not main_debugger.quitting:
                retVal = self.trace_dispatch
            return retVal
        finally:
            info.is_tracing = False

        return