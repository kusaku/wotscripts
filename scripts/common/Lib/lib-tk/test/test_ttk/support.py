# Embedded file name: scripts/common/Lib/lib-tk/test/test_ttk/support.py
import Tkinter

def get_tk_root():
    try:
        root = Tkinter._default_root
    except AttributeError:
        root = None

    if root is None:
        root = Tkinter.Tk()
    return root


def root_deiconify():
    root = get_tk_root()
    root.deiconify()


def root_withdraw():
    root = get_tk_root()
    root.withdraw()


def simulate_mouse_click(widget, x, y):
    """Generate proper events to click at the x, y position (tries to act
    like an X server)."""
    widget.event_generate('<Enter>', x=0, y=0)
    widget.event_generate('<Motion>', x=x, y=y)
    widget.event_generate('<ButtonPress-1>', x=x, y=y)
    widget.event_generate('<ButtonRelease-1>', x=x, y=y)