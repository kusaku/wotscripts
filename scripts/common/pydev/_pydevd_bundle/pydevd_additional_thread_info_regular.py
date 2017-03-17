# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_additional_thread_info_regular.py
import sys
import weakref
from _pydev_imps import _pydev_thread
from _pydevd_bundle.pydevd_constants import STATE_RUN, PYTHON_SUSPEND, dict_iter_items
from _pydevd_bundle.pydevd_frame import PyDBFrame

class PyDBAdditionalThreadInfo(object):
    __slots__ = ['pydev_state',
     'pydev_step_stop',
     'pydev_step_cmd',
     'pydev_notify_kill',
     'pydev_smart_step_stop',
     'pydev_django_resolve_frame',
     'pydev_call_from_jinja2',
     'pydev_call_inside_jinja2',
     'is_tracing',
     'conditional_breakpoint_exception',
     'pydev_message',
     'suspend_type',
     'pydev_next_line',
     'pydev_func_name']

    def __init__(self):
        self.pydev_state = STATE_RUN
        self.pydev_step_stop = None
        self.pydev_step_cmd = -1
        self.pydev_notify_kill = False
        self.pydev_smart_step_stop = None
        self.pydev_django_resolve_frame = False
        self.pydev_call_from_jinja2 = None
        self.pydev_call_inside_jinja2 = None
        self.is_tracing = False
        self.conditional_breakpoint_exception = None
        self.pydev_message = ''
        self.suspend_type = PYTHON_SUSPEND
        self.pydev_next_line = -1
        self.pydev_func_name = '.invalid.'
        return

    def iter_frames(self, t):
        current_frames = sys._current_frames()
        v = current_frames.get(t.ident)
        if v is not None:
            return [v]
        else:
            return []

    create_db_frame = PyDBFrame

    def __str__(self):
        return 'State:%s Stop:%s Cmd: %s Kill:%s' % (self.pydev_state,
         self.pydev_step_stop,
         self.pydev_step_cmd,
         self.pydev_notify_kill)


PyDBAdditionalThreadInfoOriginal = PyDBAdditionalThreadInfo

class PyDBAdditionalThreadInfoWithoutCurrentFramesSupport(PyDBAdditionalThreadInfoOriginal):

    def __init__(self):
        PyDBAdditionalThreadInfoOriginal.__init__(self)
        self.lock = _pydev_thread.allocate_lock()
        self._acquire_lock = self.lock.acquire
        self._release_lock = self.lock.release
        d = {}
        self.pydev_existing_frames = d
        try:
            self._iter_frames = d.iterkeys
        except AttributeError:
            self._iter_frames = d.keys

    def _OnDbFrameCollected(self, ref):
        """
            Callback to be called when a given reference is garbage-collected.
        """
        self._acquire_lock()
        try:
            del self.pydev_existing_frames[ref]
        finally:
            self._release_lock()

    def _AddDbFrame(self, db_frame):
        self._acquire_lock()
        try:
            r = weakref.ref(db_frame, self._OnDbFrameCollected)
            self.pydev_existing_frames[r] = r
        finally:
            self._release_lock()

    def create_db_frame(self, args):
        db_frame = PyDBFrame(args)
        db_frame.frame = args[-1]
        self._AddDbFrame(db_frame)
        return db_frame

    def iter_frames(self, t):
        self._acquire_lock()
        try:
            ret = []
            for weak_db_frame in self._iter_frames():
                try:
                    ret.append(weak_db_frame().frame)
                except AttributeError:
                    pass

            return ret
        finally:
            self._release_lock()

    def __str__(self):
        return 'State:%s Stop:%s Cmd: %s Kill:%s Frames:%s' % (self.pydev_state,
         self.pydev_step_stop,
         self.pydev_step_cmd,
         self.pydev_notify_kill,
         len(self.iter_frames(None)))


if not hasattr(sys, '_current_frames'):
    try:
        import threadframe
        sys._current_frames = threadframe.dict
        raise sys._current_frames is threadframe.dict or AssertionError
    except:
        PyDBAdditionalThreadInfo = PyDBAdditionalThreadInfoWithoutCurrentFramesSupport