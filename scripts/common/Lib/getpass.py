# Embedded file name: scripts/common/Lib/getpass.py
"""Utilities to get a password and/or the current user name.

getpass(prompt[, stream]) - Prompt for a password, with echo turned off.
getuser() - Get the user name from the environment or password database.

GetPassWarning - This UserWarning is issued when getpass() cannot prevent
                 echoing of the password contents while reading.

On Windows, the msvcrt module will be used.
On the Mac EasyDialogs.AskPassword is used, if available.

"""
import os, sys, warnings
__all__ = ['getpass', 'getuser', 'GetPassWarning']

class GetPassWarning(UserWarning):
    pass


def unix_getpass(prompt = 'Password: ', stream = None):
    """Prompt for a password, with echo turned off.
    
    Args:
      prompt: Written on stream to ask for the input.  Default: 'Password: '
      stream: A writable file object to display the prompt.  Defaults to
              the tty.  If no tty is available defaults to sys.stderr.
    Returns:
      The seKr3t input.
    Raises:
      EOFError: If our input tty or stdin was closed.
      GetPassWarning: When we were unable to turn echo off on the input.
    
    Always restores terminal settings before returning.
    """
    fd = None
    tty = None
    try:
        fd = os.open('/dev/tty', os.O_RDWR | os.O_NOCTTY)
        tty = os.fdopen(fd, 'w+', 1)
        input = tty
        if not stream:
            stream = tty
    except EnvironmentError as e:
        try:
            fd = sys.stdin.fileno()
        except (AttributeError, ValueError):
            passwd = fallback_getpass(prompt, stream)

        input = sys.stdin
        if not stream:
            stream = sys.stderr

    if fd is not None:
        passwd = None
        try:
            old = termios.tcgetattr(fd)
            new = old[:]
            new[3] &= ~termios.ECHO
            tcsetattr_flags = termios.TCSAFLUSH
            if hasattr(termios, 'TCSASOFT'):
                tcsetattr_flags |= termios.TCSASOFT
            try:
                termios.tcsetattr(fd, tcsetattr_flags, new)
                passwd = _raw_input(prompt, stream, input=input)
            finally:
                termios.tcsetattr(fd, tcsetattr_flags, old)
                stream.flush()

        except termios.error as e:
            if passwd is not None:
                raise
            del input
            del tty
            passwd = fallback_getpass(prompt, stream)

    stream.write('\n')
    return passwd


def win_getpass--- This code section failed: ---

0	LOAD_GLOBAL       'sys'
3	LOAD_ATTR         'stdin'
6	LOAD_GLOBAL       'sys'
9	LOAD_ATTR         '__stdin__'
12	COMPARE_OP        'is not'
15	POP_JUMP_IF_FALSE '31'

18	LOAD_GLOBAL       'fallback_getpass'
21	LOAD_FAST         'prompt'
24	LOAD_FAST         'stream'
27	CALL_FUNCTION_2   None
30	RETURN_END_IF     None

31	LOAD_CONST        -1
34	LOAD_CONST        None
37	IMPORT_NAME       'msvcrt'
40	STORE_FAST        'msvcrt'

43	SETUP_LOOP        '73'
46	LOAD_FAST         'prompt'
49	GET_ITER          None
50	FOR_ITER          '72'
53	STORE_FAST        'c'

56	LOAD_FAST         'msvcrt'
59	LOAD_ATTR         'putch'
62	LOAD_FAST         'c'
65	CALL_FUNCTION_1   None
68	POP_TOP           None
69	JUMP_BACK         '50'
72	POP_BLOCK         None
73_0	COME_FROM         '43'

73	LOAD_CONST        ''
76	STORE_FAST        'pw'

79	SETUP_LOOP        '182'

82	LOAD_FAST         'msvcrt'
85	LOAD_ATTR         'getch'
88	CALL_FUNCTION_0   None
91	STORE_FAST        'c'

94	LOAD_FAST         'c'
97	LOAD_CONST        '\r'
100	COMPARE_OP        '=='
103	POP_JUMP_IF_TRUE  '118'
106	LOAD_FAST         'c'
109	LOAD_CONST        '\n'
112	COMPARE_OP        '=='
115_0	COME_FROM         '103'
115	POP_JUMP_IF_FALSE '122'

118	BREAK_LOOP        None
119	JUMP_FORWARD      '122'
122_0	COME_FROM         '119'

122	LOAD_FAST         'c'
125	LOAD_CONST        '\x03'
128	COMPARE_OP        '=='
131	POP_JUMP_IF_FALSE '143'

134	LOAD_GLOBAL       'KeyboardInterrupt'
137	RAISE_VARARGS_1   None
140	JUMP_FORWARD      '143'
143_0	COME_FROM         '140'

143	LOAD_FAST         'c'
146	LOAD_CONST        '\x08'
149	COMPARE_OP        '=='
152	POP_JUMP_IF_FALSE '168'

155	LOAD_FAST         'pw'
158	LOAD_CONST        -1
161	SLICE+2           None
162	STORE_FAST        'pw'
165	JUMP_BACK         '82'

168	LOAD_FAST         'pw'
171	LOAD_FAST         'c'
174	BINARY_ADD        None
175	STORE_FAST        'pw'
178	JUMP_BACK         '82'
181	POP_BLOCK         None
182_0	COME_FROM         '79'

182	LOAD_FAST         'msvcrt'
185	LOAD_ATTR         'putch'
188	LOAD_CONST        '\r'
191	CALL_FUNCTION_1   None
194	POP_TOP           None

195	LOAD_FAST         'msvcrt'
198	LOAD_ATTR         'putch'
201	LOAD_CONST        '\n'
204	CALL_FUNCTION_1   None
207	POP_TOP           None

208	LOAD_FAST         'pw'
211	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 181


def fallback_getpass(prompt = 'Password: ', stream = None):
    warnings.warn('Can not control echo on the terminal.', GetPassWarning, stacklevel=2)
    if not stream:
        stream = sys.stderr
    print >> stream, 'Warning: Password input may be echoed.'
    return _raw_input(prompt, stream)


def _raw_input(prompt = '', stream = None, input = None):
    if not stream:
        stream = sys.stderr
    if not input:
        input = sys.stdin
    prompt = str(prompt)
    if prompt:
        stream.write(prompt)
        stream.flush()
    line = input.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line


def getuser():
    """Get the username from the environment or password database.
    
    First try various environment variables, then the password
    database.  This works on Windows as long as USERNAME is set.
    
    """
    import os
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user

    import pwd
    return pwd.getpwuid(os.getuid())[0]


try:
    import termios
    (termios.tcgetattr, termios.tcsetattr)
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        try:
            from EasyDialogs import AskPassword
        except ImportError:
            getpass = fallback_getpass
        else:
            getpass = AskPassword

    else:
        getpass = win_getpass

else:
    getpass = unix_getpass