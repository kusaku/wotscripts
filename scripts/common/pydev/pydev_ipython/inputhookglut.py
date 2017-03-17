# Embedded file name: scripts/common/pydev/pydev_ipython/inputhookglut.py
"""
GLUT Inputhook support functions
"""
import os
import sys
from _pydev_imps import _pydev_time as time
import signal
import OpenGL.GLUT as glut
import OpenGL.platform as platform
from timeit import default_timer as clock
from pydev_ipython.inputhook import stdin_ready
glut_fps = 60
glut_display_mode = glut.GLUT_DOUBLE | glut.GLUT_RGBA | glut.GLUT_DEPTH
glutMainLoopEvent = None
if sys.platform == 'darwin':
    try:
        glutCheckLoop = platform.createBaseFunction('glutCheckLoop', dll=platform.GLUT, resultType=None, argTypes=[], doc='glutCheckLoop(  ) -> None', argNames=())
    except AttributeError:
        raise RuntimeError('Your glut implementation does not allow interactive sessionsConsider installing freeglut.')

    glutMainLoopEvent = glutCheckLoop
elif glut.HAVE_FREEGLUT:
    glutMainLoopEvent = glut.glutMainLoopEvent
else:
    raise RuntimeError('Your glut implementation does not allow interactive sessions. Consider installing freeglut.')

def glut_display():
    pass


def glut_idle():
    pass


def glut_close():
    glut.glutHideWindow()
    glutMainLoopEvent()


def glut_int_handler(signum, frame):
    signal.signal(signal.SIGINT, signal.default_int_handler)
    print '\nKeyboardInterrupt'


def inputhook_glut():
    """Run the pyglet event loop by processing pending events only.
    
    This keeps processing pending events until stdin is ready.  After
    processing all pending events, a call to time.sleep is inserted.  This is
    needed, otherwise, CPU usage is at 100%.  This sleep time should be tuned
    though for best performance.
    """
    signal.signal(signal.SIGINT, glut_int_handler)
    try:
        t = clock()
        if glut.glutGetWindow() == 0:
            glut.glutSetWindow(1)
            glutMainLoopEvent()
            return 0
        while not stdin_ready():
            glutMainLoopEvent()
            used_time = clock() - t
            if used_time > 10.0:
                time.sleep(1.0)
            elif used_time > 0.1:
                time.sleep(0.05)
            else:
                time.sleep(0.001)

    except KeyboardInterrupt:
        pass

    return 0