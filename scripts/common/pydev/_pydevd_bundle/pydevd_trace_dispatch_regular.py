# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_trace_dispatch_regular.py
import traceback
from _pydev_bundle.pydev_is_thread_alive import is_thread_alive
from _pydev_imps import _pydev_threading as threading
from _pydevd_bundle.pydevd_constants import get_thread_id
from _pydevd_bundle.pydevd_dont_trace_files import DONT_TRACE
from _pydevd_bundle.pydevd_kill_all_pydevd_threads import kill_all_pydev_threads
from pydevd_file_utils import get_abs_path_real_path_and_base_from_frame, NORM_PATHS_AND_BASE_CONTAINER
from _pydevd_bundle.pydevd_tracing import SetTrace
from _pydevd_bundle.pydevd_additional_thread_info import PyDBAdditionalThreadInfo
threadingCurrentThread = threading.currentThread
get_file_type = DONT_TRACE.get

def trace_dispatch(py_db, frame, event, arg):
    t = threadingCurrentThread()
    if getattr(t, 'pydev_do_not_trace', None):
        return
    else:
        try:
            additional_info = t.additional_info
            if additional_info is None:
                raise AttributeError()
        except:
            additional_info = t.additional_info = PyDBAdditionalThreadInfo()

        thread_tracer = ThreadTracer((py_db, t, additional_info))
        SetTrace(thread_tracer.__call__)
        return thread_tracer.__call__(frame, event, arg)


class ThreadTracer:

    def __init__(self, args):
        self._args = args

    def __call__(self, frame, event, arg):
        """ This is the callback used when we enter some context in the debugger.
        
        We also decorate the thread we are in with info about the debugging.
        The attributes added are:
            pydev_state
            pydev_step_stop
            pydev_step_cmd
            pydev_notify_kill
        
        :param PyDB py_db:
            This is the global debugger (this method should actually be added as a method to it).
        """
        py_db, t, additional_info = self._args
        try:
            if py_db._finish_debugging_session:
                if not py_db._termination_event_set:
                    try:
                        if py_db.output_checker is None:
                            kill_all_pydev_threads()
                    except:
                        traceback.print_exc()

                    py_db._termination_event_set = True
                return
            if not is_thread_alive(t):
                py_db._process_thread_not_alive(get_thread_id(t))
                return
            try:
                abs_path_real_path_and_base = NORM_PATHS_AND_BASE_CONTAINER[frame.f_code.co_filename]
            except:
                abs_path_real_path_and_base = get_abs_path_real_path_and_base_from_frame(frame)

            if py_db.thread_analyser is not None:
                py_db.thread_analyser.log_event(frame)
            if py_db.asyncio_analyser is not None:
                py_db.asyncio_analyser.log_event(frame)
            file_type = get_file_type(abs_path_real_path_and_base[-1])
            if file_type is not None:
                if file_type == 1:
                    if py_db.not_in_scope(abs_path_real_path_and_base[1]):
                        return
                else:
                    return
            if additional_info.pydev_step_cmd != -1:
                if py_db.is_filter_enabled and py_db.is_ignored_by_filters(abs_path_real_path_and_base[1]):
                    return
                if py_db.is_filter_libraries and py_db.not_in_scope(abs_path_real_path_and_base[1]):
                    return
            if additional_info.is_tracing:
                return
            return additional_info.create_db_frame((py_db,
             abs_path_real_path_and_base[1],
             additional_info,
             t,
             frame)).trace_dispatch(frame, event, arg)
        except SystemExit:
            return
        except Exception:
            if py_db._finish_debugging_session:
                return
            try:
                if traceback is not None:
                    traceback.print_exc()
            except:
                pass

            return

        return