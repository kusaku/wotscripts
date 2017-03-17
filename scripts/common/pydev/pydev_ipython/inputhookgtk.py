# Embedded file name: scripts/common/pydev/pydev_ipython/inputhookgtk.py
"""
Enable pygtk to be used interacive by setting PyOS_InputHook.

Authors: Brian Granger
"""
import gtk, gobject

def _main_quit(*args, **kwargs):
    gtk.main_quit()
    return False


def create_inputhook_gtk(stdin_file):

    def inputhook_gtk():
        gobject.io_add_watch(stdin_file, gobject.IO_IN, _main_quit)
        gtk.main()
        return 0

    return inputhook_gtk