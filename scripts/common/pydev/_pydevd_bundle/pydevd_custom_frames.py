# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_custom_frames.py
from _pydevd_bundle.pydevd_constants import *
from pydevd_file_utils import get_abs_path_real_path_and_base_from_frame
from _pydev_imps import _pydev_thread
threadingCurrentThread = threading.currentThread
DEBUG = False

class CustomFramesContainer:
    custom_frames_lock = None
    custom_frames = None
    _next_frame_id = None
    _py_db_command_thread_event = None


def custom_frames_container_init():
    CustomFramesContainer.custom_frames_lock = _pydev_thread.allocate_lock()
    CustomFramesContainer.custom_frames = {}
    CustomFramesContainer._next_frame_id = 0
    CustomFramesContainer._py_db_command_thread_event = Null()


custom_frames_container_init()

class CustomFrame:

    def __init__(self, name, frame, thread_id):
        self.name = name
        self.frame = frame
        self.mod_time = 0
        self.thread_id = thread_id


def add_custom_frame(frame, name, thread_id):
    CustomFramesContainer.custom_frames_lock.acquire()
    try:
        curr_thread_id = get_thread_id(threadingCurrentThread())
        next_id = CustomFramesContainer._next_frame_id = CustomFramesContainer._next_frame_id + 1
        frame_id = '__frame__:%s|%s' % (next_id, curr_thread_id)
        if DEBUG:
            sys.stderr.write('add_custom_frame: %s (%s) %s %s\n' % (frame_id,
             get_abs_path_real_path_and_base_from_frame(frame)[-1],
             frame.f_lineno,
             frame.f_code.co_name))
        CustomFramesContainer.custom_frames[frame_id] = CustomFrame(name, frame, thread_id)
        CustomFramesContainer._py_db_command_thread_event.set()
        return frame_id
    finally:
        CustomFramesContainer.custom_frames_lock.release()


addCustomFrame = add_custom_frame

def update_custom_frame(frame_id, frame, thread_id, name = None):
    CustomFramesContainer.custom_frames_lock.acquire()
    try:
        if DEBUG:
            sys.stderr.write('update_custom_frame: %s\n' % frame_id)
        try:
            old = CustomFramesContainer.custom_frames[frame_id]
            if name is not None:
                old.name = name
            old.mod_time += 1
            old.thread_id = thread_id
        except:
            sys.stderr.write('Unable to get frame to replace: %s\n' % (frame_id,))
            import traceback
            traceback.print_exc()

        CustomFramesContainer._py_db_command_thread_event.set()
    finally:
        CustomFramesContainer.custom_frames_lock.release()

    return


def get_custom_frame(thread_id, frame_id):
    """
    :param thread_id: This should actually be the frame_id which is returned by add_custom_frame.
    :param frame_id: This is the actual id() of the frame
    """
    CustomFramesContainer.custom_frames_lock.acquire()
    try:
        frame_id = int(frame_id)
        f = CustomFramesContainer.custom_frames[thread_id].frame
        while f is not None:
            if id(f) == frame_id:
                return f
            f = f.f_back

    finally:
        f = None
        CustomFramesContainer.custom_frames_lock.release()

    return


def remove_custom_frame(frame_id):
    CustomFramesContainer.custom_frames_lock.acquire()
    try:
        if DEBUG:
            sys.stderr.write('remove_custom_frame: %s\n' % frame_id)
        dict_pop(CustomFramesContainer.custom_frames, frame_id, None)
        CustomFramesContainer._py_db_command_thread_event.set()
    finally:
        CustomFramesContainer.custom_frames_lock.release()

    return


removeCustomFrame = remove_custom_frame