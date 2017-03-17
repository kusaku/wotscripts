# Embedded file name: scripts/common/pydev/pydev_ipython/inputhookgtk3.py
"""
Enable Gtk3 to be used interacive by IPython.

Authors: Thomi Richards
"""
from gi.repository import Gtk, GLib

def _main_quit(*args, **kwargs):
    Gtk.main_quit()
    return False


def create_inputhook_gtk3(stdin_file):

    def inputhook_gtk3():
        GLib.io_add_watch(stdin_file, GLib.IO_IN, _main_quit)
        Gtk.main()
        return 0

    return inputhook_gtk3