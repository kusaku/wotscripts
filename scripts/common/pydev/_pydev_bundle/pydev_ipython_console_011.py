# Embedded file name: scripts/common/pydev/_pydev_bundle/pydev_ipython_console_011.py
"""Interface to TerminalInteractiveShell for PyDev Interactive Console frontend
   for IPython 0.11 to 1.0+.
"""
from __future__ import print_function
import os
import codeop
from IPython.core.error import UsageError
from IPython.core.completer import IPCompleter
from IPython.core.interactiveshell import InteractiveShell, InteractiveShellABC
from IPython.core.usage import default_banner_parts
from IPython.utils.strdispatch import StrDispatch
import IPython.core.release as IPythonRelease
try:
    from IPython.terminal.interactiveshell import TerminalInteractiveShell
except ImportError:
    from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell

try:
    from traitlets import CBool, Unicode
except ImportError:
    from IPython.utils.traitlets import CBool, Unicode

from IPython.core import release
from _pydev_bundle.pydev_imports import xmlrpclib
default_pydev_banner_parts = default_banner_parts
default_pydev_banner = ''.join(default_pydev_banner_parts)

def show_in_pager(self, strng, *args, **kwargs):
    """ Run a string through pager """
    print(strng)


def create_editor_hook(pydev_host, pydev_client_port):

    def call_editor(filename, line = 0, wait = True):
        """ Open an editor in PyDev """
        if line is None:
            line = 0
        filename = os.path.abspath(filename)
        server = xmlrpclib.Server('http://%s:%s' % (pydev_host, pydev_client_port))
        server.IPythonEditor(filename, str(line))
        if wait:
            try:
                raw_input('Press Enter when done editing:')
            except NameError:
                input('Press Enter when done editing:')

        return

    return call_editor


class PyDevIPCompleter(IPCompleter):

    def __init__(self, *args, **kwargs):
        """ Create a Completer that reuses the advanced completion support of PyDev
        in addition to the completion support provided by IPython """
        IPCompleter.__init__(self, *args, **kwargs)
        self.matchers.remove(self.python_matches)


class PyDevTerminalInteractiveShell(TerminalInteractiveShell):
    banner1 = Unicode(default_pydev_banner, config=True, help='The part of the banner to be printed before the profile')
    term_title = CBool(False)
    readline_use = CBool(False)
    autoindent = CBool(False)
    colors_force = CBool(True)
    colors = Unicode('NoColor')

    @staticmethod
    def enable_gui(gui = None, app = None):
        """Switch amongst GUI input hooks by name.
        """
        from pydev_ipython.inputhook import enable_gui as real_enable_gui
        try:
            return real_enable_gui(gui, app)
        except ValueError as e:
            raise UsageError('%s' % e)

    def init_hooks(self):
        super(PyDevTerminalInteractiveShell, self).init_hooks()
        self.set_hook('show_in_pager', show_in_pager)

    def showtraceback(self, exc_tuple = None, filename = None, tb_offset = None, exception_only = False):
        import traceback
        traceback.print_exc()

    def _new_completer_011(self):
        return PyDevIPCompleter(self, self.user_ns, self.user_global_ns, self.readline_omit__names, self.alias_manager.alias_table, self.has_readline)

    def _new_completer_012(self):
        completer = PyDevIPCompleter(shell=self, namespace=self.user_ns, global_namespace=self.user_global_ns, alias_table=self.alias_manager.alias_table, use_readline=self.has_readline, config=self.config)
        self.configurables.append(completer)
        return completer

    def _new_completer_100(self):
        completer = PyDevIPCompleter(shell=self, namespace=self.user_ns, global_namespace=self.user_global_ns, alias_table=self.alias_manager.alias_table, use_readline=self.has_readline, parent=self)
        self.configurables.append(completer)
        return completer

    def _new_completer_200(self):
        completer = PyDevIPCompleter(shell=self, namespace=self.user_ns, global_namespace=self.user_global_ns, use_readline=self.has_readline, parent=self)
        self.configurables.append(completer)
        return completer

    def init_completer(self):
        """Initialize the completion machinery.
        
        This creates a completer that provides the completions that are
        IPython specific. We use this to supplement PyDev's core code
        completions.
        """
        from IPython.core.completerlib import magic_run_completer, cd_completer
        try:
            from IPython.core.completerlib import reset_completer
        except ImportError:
            reset_completer = None

        if IPythonRelease._version_major >= 2:
            self.Completer = self._new_completer_200()
        elif IPythonRelease._version_major >= 1:
            self.Completer = self._new_completer_100()
        elif IPythonRelease._version_minor >= 12:
            self.Completer = self._new_completer_012()
        else:
            self.Completer = self._new_completer_011()
        sdisp = self.strdispatchers.get('complete_command', StrDispatch())
        self.strdispatchers['complete_command'] = sdisp
        self.Completer.custom_completers = sdisp
        self.set_hook('complete_command', magic_run_completer, str_key='%run')
        self.set_hook('complete_command', cd_completer, str_key='%cd')
        if reset_completer:
            self.set_hook('complete_command', reset_completer, str_key='%reset')
        if self.has_readline:
            self.set_readline_completer()
        return

    def init_alias(self):
        InteractiveShell.init_alias(self)

    def ask_exit(self):
        """ Ask the shell to exit. Can be overiden and used as a callback. """
        super(PyDevTerminalInteractiveShell, self).ask_exit()
        print('To exit the PyDev Console, terminate the console within IDE.')

    def init_magics(self):
        super(PyDevTerminalInteractiveShell, self).init_magics()


InteractiveShellABC.register(PyDevTerminalInteractiveShell)

class _PyDevFrontEnd:
    version = release.__version__

    def __init__(self, show_banner = True):
        self.ipython = PyDevTerminalInteractiveShell.instance()
        if show_banner:
            self.ipython.show_banner()
        self._curr_exec_line = 0
        self._curr_exec_lines = []

    def update(self, globals, locals):
        ns = self.ipython.user_ns
        for ind in ['_oh',
         '_ih',
         '_dh',
         '_sh',
         'In',
         'Out',
         'get_ipython',
         'exit',
         'quit']:
            locals[ind] = ns[ind]

        self.ipython.user_global_ns.clear()
        self.ipython.user_global_ns.update(globals)
        self.ipython.user_ns = locals
        if hasattr(self.ipython, 'history_manager') and hasattr(self.ipython.history_manager, 'save_thread'):
            self.ipython.history_manager.save_thread.pydev_do_not_trace = True

    def complete(self, string):
        try:
            if string:
                return self.ipython.complete(None, line=string, cursor_pos=string.__len__())
            return self.ipython.complete(string, string, 0)
        except:
            pass

        return None

    def is_complete(self, string):
        if string in ('', '\n'):
            return True
        else:
            try:
                clean_string = string.rstrip('\n')
                if not clean_string.endswith('\\'):
                    clean_string += '\n\n'
                is_complete = codeop.compile_command(clean_string, '<string>', 'exec')
            except Exception:
                is_complete = True

            return is_complete

    def getCompletions(self, text, act_tok):
        try:
            TYPE_IPYTHON = '11'
            TYPE_IPYTHON_MAGIC = '12'
            _line, ipython_completions = self.complete(text)
            from _pydev_bundle._pydev_completer import Completer
            completer = Completer(self.get_namespace(), None)
            ret = completer.complete(act_tok)
            append = ret.append
            ip = self.ipython
            pydev_completions = set([ f[0] for f in ret ])
            for ipython_completion in ipython_completions:
                if ipython_completion not in pydev_completions:
                    pydev_completions.add(ipython_completion)
                    inf = ip.object_inspect(ipython_completion)
                    if inf['type_name'] == 'Magic function':
                        pydev_type = TYPE_IPYTHON_MAGIC
                    else:
                        pydev_type = TYPE_IPYTHON
                    pydev_doc = inf['docstring']
                    if pydev_doc is None:
                        pydev_doc = ''
                    append((ipython_completion,
                     pydev_doc,
                     '',
                     pydev_type))

            return ret
        except:
            import traceback
            traceback.print_exc()
            return []

        return

    def get_namespace(self):
        return self.ipython.user_ns

    def clear_buffer(self):
        del self._curr_exec_lines[:]

    def add_exec(self, line):
        if self._curr_exec_lines:
            self._curr_exec_lines.append(line)
            buf = '\n'.join(self._curr_exec_lines)
            if self.is_complete(buf):
                self._curr_exec_line += 1
                self.ipython.run_cell(buf)
                del self._curr_exec_lines[:]
                return False
            return True
        elif not self.is_complete(line):
            self._curr_exec_lines.append(line)
            return True
        else:
            self._curr_exec_line += 1
            self.ipython.run_cell(line, store_history=True)
            return False

    def is_automagic(self):
        return self.ipython.automagic

    def get_greeting_msg(self):
        return 'PyDev console: using IPython %s\n' % self.version


import IPython.lib.inputhook
import pydev_ipython.inputhook
IPython.lib.inputhook.enable_gui = pydev_ipython.inputhook.enable_gui
for name in pydev_ipython.inputhook.__all__:
    setattr(IPython.lib.inputhook, name, getattr(pydev_ipython.inputhook, name))

class _PyDevFrontEndContainer:
    _instance = None
    _last_host_port = None


def get_pydev_frontend(pydev_host, pydev_client_port, show_banner = True):
    if _PyDevFrontEndContainer._instance is None:
        _PyDevFrontEndContainer._instance = _PyDevFrontEnd(show_banner=show_banner)
    if _PyDevFrontEndContainer._last_host_port != (pydev_host, pydev_client_port):
        _PyDevFrontEndContainer._last_host_port = (pydev_host, pydev_client_port)
        _PyDevFrontEndContainer._instance.ipython.hooks['editor'] = create_editor_hook(pydev_host, pydev_client_port)
    return _PyDevFrontEndContainer._instance