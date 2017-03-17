# Embedded file name: scripts/common/pydev/_pydevd_bundle/pydevd_save_locals.py
"""
Utility for saving locals.
"""
import sys

def is_save_locals_available():
    try:
        if '__pypy__' in sys.builtin_module_names:
            import __pypy__
            save_locals = __pypy__.locals_to_fast
            return True
    except:
        pass

    try:
        import ctypes
    except:
        return False

    try:
        func = ctypes.pythonapi.PyFrame_LocalsToFast
    except:
        return False

    return True


def save_locals(frame):
    """
    Copy values from locals_dict into the fast stack slots in the given frame.
    
    Note: the 'save_locals' branch had a different approach wrapping the frame (much more code, but it gives ideas
    on how to save things partially, not the 'whole' locals).
    """
    from _pydevd_bundle import pydevd_vars
    if not isinstance(frame, pydevd_vars.frame_type):
        return
    try:
        if '__pypy__' in sys.builtin_module_names:
            import __pypy__
            save_locals = __pypy__.locals_to_fast
            save_locals(frame)
            return
    except:
        pass

    try:
        import ctypes
    except:
        return

    try:
        func = ctypes.pythonapi.PyFrame_LocalsToFast
    except:
        return

    func(ctypes.py_object(frame), ctypes.c_int(0))