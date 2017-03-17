# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_stackless.py
from __future__ import nested_scopes
import weakref
import sys
from _pydevd_bundle.pydevd_comm import get_global_debugger
from _pydevd_bundle.pydevd_constants import threading, dict_contains, call_only_once
from _pydevd_bundle.pydevd_constants import dict_items
from _pydevd_bundle.pydevd_custom_frames import update_custom_frame, remove_custom_frame, add_custom_frame
from _pydevd_bundle.pydevd_dont_trace_files import DONT_TRACE
from pydevd_file_utils import get_abs_path_real_path_and_base_from_frame
from pydevd_tracing import SetTrace
import stackless

class TaskletToLastId:
    """
    So, why not a WeakKeyDictionary?
    The problem is that removals from the WeakKeyDictionary will create a new tasklet (as it adds a callback to
    remove the key when it's garbage-collected), so, we can get into a recursion.
    """

    def __init__(self):
        self.tasklet_ref_to_last_id = {}
        self._i = 0

    def get(self, tasklet):
        return self.tasklet_ref_to_last_id.get(weakref.ref(tasklet))

    def __setitem__(self, tasklet, last_id):
        self.tasklet_ref_to_last_id[weakref.ref(tasklet)] = last_id
        self._i += 1
        if self._i % 100 == 0:
            for tasklet_ref in list(self.tasklet_ref_to_last_id.keys()):
                if tasklet_ref() is None:
                    del self.tasklet_ref_to_last_id[tasklet_ref]

        return


_tasklet_to_last_id = TaskletToLastId()

class _TaskletInfo:
    _last_id = 0

    def __init__(self, tasklet_weakref, tasklet):
        self.frame_id = None
        self.tasklet_weakref = tasklet_weakref
        last_id = _tasklet_to_last_id.get(tasklet)
        if last_id is None:
            _TaskletInfo._last_id += 1
            last_id = _TaskletInfo._last_id
            _tasklet_to_last_id[tasklet] = last_id
        self._tasklet_id = last_id
        self.update_name()
        return

    def update_name(self):
        tasklet = self.tasklet_weakref()
        if tasklet:
            if tasklet.blocked:
                state = 'blocked'
            elif tasklet.paused:
                state = 'paused'
            elif tasklet.scheduled:
                state = 'scheduled'
            else:
                state = '<UNEXPECTED>'
            try:
                name = tasklet.name
            except AttributeError:
                if tasklet.is_main:
                    name = 'MainTasklet'
                else:
                    name = 'Tasklet-%s' % (self._tasklet_id,)

            thread_id = tasklet.thread_id
            if thread_id != -1:
                for thread in threading.enumerate():
                    if thread.ident == thread_id:
                        if thread.name:
                            thread_name = 'of %s' % (thread.name,)
                        else:
                            thread_name = 'of Thread-%s' % (thread.name or str(thread_id),)
                        break
                else:
                    thread_name = 'of Thread-%s' % (str(thread_id),)

                thread = None
            else:
                thread_name = 'without thread'
            tid = id(tasklet)
            tasklet = None
        else:
            state = 'dead'
            name = 'Tasklet-%s' % (self._tasklet_id,)
            thread_name = ''
            tid = '-'
        self.tasklet_name = '%s %s %s (%s)' % (state,
         name,
         thread_name,
         tid)
        return

    if not hasattr(stackless.tasklet, 'trace_function'):

        def update_name(self):
            tasklet = self.tasklet_weakref()
            if tasklet:
                try:
                    name = tasklet.name
                except AttributeError:
                    if tasklet.is_main:
                        name = 'MainTasklet'
                    else:
                        name = 'Tasklet-%s' % (self._tasklet_id,)

                thread_id = tasklet.thread_id
                for thread in threading.enumerate():
                    if thread.ident == thread_id:
                        if thread.name:
                            thread_name = 'of %s' % (thread.name,)
                        else:
                            thread_name = 'of Thread-%s' % (thread.name or str(thread_id),)
                        break
                else:
                    thread_name = 'of Thread-%s' % (str(thread_id),)

                thread = None
                tid = id(tasklet)
                tasklet = None
            else:
                name = 'Tasklet-%s' % (self._tasklet_id,)
                thread_name = ''
                tid = '-'
            self.tasklet_name = '%s %s (%s)' % (name, thread_name, tid)
            return


_weak_tasklet_registered_to_info = {}

def get_tasklet_info(tasklet):
    return register_tasklet_info(tasklet)


def register_tasklet_info(tasklet):
    r = weakref.ref(tasklet)
    info = _weak_tasklet_registered_to_info.get(r)
    if info is None:
        info = _weak_tasklet_registered_to_info[r] = _TaskletInfo(r, tasklet)
    return info


_application_set_schedule_callback = None

def _schedule_callback(prev, next):
    """
    Called when a context is stopped or a new context is made runnable.
    """
    global _application_set_schedule_callback
    try:
        if not prev and not next:
            return
        current_frame = sys._getframe()
        if next:
            register_tasklet_info(next)
            debugger = get_global_debugger()
            if debugger is not None:
                next.trace_function = debugger.trace_dispatch
                frame = next.frame
                if frame is current_frame:
                    frame = frame.f_back
                if hasattr(frame, 'f_trace'):
                    frame.f_trace = debugger.trace_dispatch
            debugger = None
        if prev:
            register_tasklet_info(prev)
        try:
            for tasklet_ref, tasklet_info in dict_items(_weak_tasklet_registered_to_info):
                tasklet = tasklet_ref()
                if tasklet is None or not tasklet.alive:
                    try:
                        del _weak_tasklet_registered_to_info[tasklet_ref]
                    except KeyError:
                        pass

                    if tasklet_info.frame_id is not None:
                        remove_custom_frame(tasklet_info.frame_id)
                else:
                    is_running = stackless.get_thread_info(tasklet.thread_id)[1] is tasklet
                    if tasklet is prev or tasklet is not next and not is_running:
                        frame = tasklet.frame
                        if frame is current_frame:
                            frame = frame.f_back
                        if frame is not None:
                            base = get_abs_path_real_path_and_base_from_frame(frame)[-1]
                            is_file_to_ignore = dict_contains(DONT_TRACE, base)
                            if not is_file_to_ignore:
                                tasklet_info.update_name()
                                if tasklet_info.frame_id is None:
                                    tasklet_info.frame_id = add_custom_frame(frame, tasklet_info.tasklet_name, tasklet.thread_id)
                                else:
                                    update_custom_frame(tasklet_info.frame_id, frame, tasklet.thread_id, name=tasklet_info.tasklet_name)
                    elif tasklet is next or is_running:
                        if tasklet_info.frame_id is not None:
                            remove_custom_frame(tasklet_info.frame_id)
                            tasklet_info.frame_id = None

        finally:
            tasklet = None
            tasklet_info = None
            frame = None

    except:
        import traceback
        traceback.print_exc()

    if _application_set_schedule_callback is not None:
        return _application_set_schedule_callback(prev, next)
    else:
        return


if not hasattr(stackless.tasklet, 'trace_function'):

    def _schedule_callback(prev, next):
        """
        Called when a context is stopped or a new context is made runnable.
        """
        try:
            if not prev and not next:
                return
            if next:
                register_tasklet_info(next)
                debugger = get_global_debugger()
                if debugger is not None and next.frame:
                    if hasattr(next.frame, 'f_trace'):
                        next.frame.f_trace = debugger.trace_dispatch
                debugger = None
            if prev:
                register_tasklet_info(prev)
            try:
                for tasklet_ref, tasklet_info in dict_items(_weak_tasklet_registered_to_info):
                    tasklet = tasklet_ref()
                    if tasklet is None or not tasklet.alive:
                        try:
                            del _weak_tasklet_registered_to_info[tasklet_ref]
                        except KeyError:
                            pass

                        if tasklet_info.frame_id is not None:
                            remove_custom_frame(tasklet_info.frame_id)
                    elif tasklet.paused or tasklet.blocked or tasklet.scheduled:
                        if tasklet.frame and tasklet.frame.f_back:
                            f_back = tasklet.frame.f_back
                            base = get_abs_path_real_path_and_base_from_frame(f_back)[-1]
                            is_file_to_ignore = dict_contains(DONT_TRACE, base)
                            if not is_file_to_ignore:
                                if tasklet_info.frame_id is None:
                                    tasklet_info.frame_id = add_custom_frame(f_back, tasklet_info.tasklet_name, tasklet.thread_id)
                                else:
                                    update_custom_frame(tasklet_info.frame_id, f_back, tasklet.thread_id)
                    elif tasklet.is_current:
                        if tasklet_info.frame_id is not None:
                            remove_custom_frame(tasklet_info.frame_id)
                            tasklet_info.frame_id = None

            finally:
                tasklet = None
                tasklet_info = None
                f_back = None

        except:
            import traceback
            traceback.print_exc()

        if _application_set_schedule_callback is not None:
            return _application_set_schedule_callback(prev, next)
        else:
            return


    _original_setup = stackless.tasklet.setup

    def setup(self, *args, **kwargs):
        """
        Called to run a new tasklet: rebind the creation so that we can trace it.
        """
        f = self.tempval

        def new_f(old_f, args, kwargs):
            debugger = get_global_debugger()
            if debugger is not None:
                SetTrace(debugger.trace_dispatch)
            debugger = None
            self.tempval = old_f
            register_tasklet_info(self)
            return old_f(*args, **kwargs)

        self.tempval = new_f
        return _original_setup(self, f, args, kwargs)


    def __call__(self, *args, **kwargs):
        """
        Called to run a new tasklet: rebind the creation so that we can trace it.
        """
        return setup(self, *args, **kwargs)


    _original_run = stackless.run

    def run(*args, **kwargs):
        debugger = get_global_debugger()
        if debugger is not None:
            SetTrace(debugger.trace_dispatch)
        debugger = None
        return _original_run(*args, **kwargs)


def patch_stackless():
    """
    This function should be called to patch the stackless module so that new tasklets are properly tracked in the
    debugger.
    """
    global _application_set_schedule_callback
    _application_set_schedule_callback = stackless.set_schedule_callback(_schedule_callback)

    def set_schedule_callback(callable):
        global _application_set_schedule_callback
        old = _application_set_schedule_callback
        _application_set_schedule_callback = callable
        return old

    def get_schedule_callback():
        return _application_set_schedule_callback

    set_schedule_callback.__doc__ = stackless.set_schedule_callback.__doc__
    if hasattr(stackless, 'get_schedule_callback'):
        get_schedule_callback.__doc__ = stackless.get_schedule_callback.__doc__
    stackless.set_schedule_callback = set_schedule_callback
    stackless.get_schedule_callback = get_schedule_callback
    if not hasattr(stackless.tasklet, 'trace_function'):
        __call__.__doc__ = stackless.tasklet.__call__.__doc__
        stackless.tasklet.__call__ = __call__
        setup.__doc__ = stackless.tasklet.setup.__doc__
        stackless.tasklet.setup = setup
        run.__doc__ = stackless.run.__doc__
        stackless.run = run


patch_stackless = call_only_once(patch_stackless)