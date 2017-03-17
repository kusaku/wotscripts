# Embedded file name: scripts/common/Lib/code.py
"""Utilities needed to emulate Python's interactive interpreter.

"""
import sys
import traceback
from codeop import CommandCompiler, compile_command
__all__ = ['InteractiveInterpreter',
 'InteractiveConsole',
 'interact',
 'compile_command']

def softspace(file, newvalue):
    oldvalue = 0
    try:
        oldvalue = file.softspace
    except AttributeError:
        pass

    try:
        file.softspace = newvalue
    except (AttributeError, TypeError):
        pass

    return oldvalue


class InteractiveInterpreter:
    """Base class for InteractiveConsole.
    
    This class deals with parsing and interpreter state (the user's
    namespace); it doesn't deal with input buffering or prompting or
    input file naming (the filename is always passed in explicitly).
    
    """

    def __init__(self, locals = None):
        """Constructor.
        
        The optional 'locals' argument specifies the dictionary in
        which code will be executed; it defaults to a newly created
        dictionary with key "__name__" set to "__console__" and key
        "__doc__" set to None.
        
        """
        if locals is None:
            locals = {'__name__': '__console__',
             '__doc__': None}
        self.locals = locals
        self.compile = CommandCompiler()
        return

    def runsource(self, source, filename = '<input>', symbol = 'single'):
        """Compile and run some source in the interpreter.
        
        Arguments are as for compile_command().
        
        One several things can happen:
        
        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed by calling the showsyntaxerror() method.
        
        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.
        
        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).
        
        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.
        
        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            self.showsyntaxerror(filename)
            return False

        if code is None:
            return True
        else:
            self.runcode(code)
            return False

    def runcode(self, code):
        """Execute a code object.
        
        When an exception occurs, self.showtraceback() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which is reraised.
        
        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.
        
        """
        try:
            exec code in self.locals
        except SystemExit:
            raise
        except:
            self.showtraceback()
        else:
            if softspace(sys.stdout, 0):
                print

    def showsyntaxerror(self, filename = None):
        """Display the syntax error that just occurred.
        
        This doesn't display a stack trace because there isn't one.
        
        If a filename is given, it is stuffed in the exception instead
        of what was there before (because Python's parser always uses
        "<string>" when reading from a string).
        
        The output is written by self.write(), below.
        
        """
        type, value, sys.last_traceback = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        if filename and type is SyntaxError:
            try:
                msg, (dummy_filename, lineno, offset, line) = value
            except:
                pass
            else:
                value = SyntaxError(msg, (filename,
                 lineno,
                 offset,
                 line))
                sys.last_value = value

        list = traceback.format_exception_only(type, value)
        map(self.write, list)

    def showtraceback(self):
        """Display the exception that just occurred.
        
        We remove the first stack item because it is our own code.
        
        The output is written by self.write(), below.
        
        """
        try:
            type, value, tb = sys.exc_info()
            sys.last_type = type
            sys.last_value = value
            sys.last_traceback = tb
            tblist = traceback.extract_tb(tb)
            del tblist[:1]
            list = traceback.format_list(tblist)
            if list:
                list.insert(0, 'Traceback (most recent call last):\n')
            list[len(list):] = traceback.format_exception_only(type, value)
        finally:
            tblist = tb = None

        map(self.write, list)
        return

    def write(self, data):
        """Write a string.
        
        The base implementation writes to sys.stderr; a subclass may
        replace this with a different implementation.
        
        """
        sys.stderr.write(data)


class InteractiveConsole(InteractiveInterpreter):
    """Closely emulate the behavior of the interactive Python interpreter.
    
    This class builds on InteractiveInterpreter and adds prompting
    using the familiar sys.ps1 and sys.ps2, and input buffering.
    
    """

    def __init__(self, locals = None, filename = '<console>'):
        """Constructor.
        
        The optional locals argument will be passed to the
        InteractiveInterpreter base class.
        
        The optional filename argument should specify the (file)name
        of the input stream; it will show up in tracebacks.
        
        """
        InteractiveInterpreter.__init__(self, locals)
        self.filename = filename
        self.resetbuffer()

    def resetbuffer(self):
        """Reset the input buffer."""
        self.buffer = []

    def interact--- This code section failed: ---

0	SETUP_EXCEPT      '14'

3	LOAD_GLOBAL       'sys'
6	LOAD_ATTR         'ps1'
9	POP_TOP           None
10	POP_BLOCK         None
11	JUMP_FORWARD      '40'
14_0	COME_FROM         '0'

14	DUP_TOP           None
15	LOAD_GLOBAL       'AttributeError'
18	COMPARE_OP        'exception match'
21	POP_JUMP_IF_FALSE '39'
24	POP_TOP           None
25	POP_TOP           None
26	POP_TOP           None

27	LOAD_CONST        '>>> '
30	LOAD_GLOBAL       'sys'
33	STORE_ATTR        'ps1'
36	JUMP_FORWARD      '40'
39	END_FINALLY       None
40_0	COME_FROM         '11'
40_1	COME_FROM         '39'

40	SETUP_EXCEPT      '54'

43	LOAD_GLOBAL       'sys'
46	LOAD_ATTR         'ps2'
49	POP_TOP           None
50	POP_BLOCK         None
51	JUMP_FORWARD      '80'
54_0	COME_FROM         '40'

54	DUP_TOP           None
55	LOAD_GLOBAL       'AttributeError'
58	COMPARE_OP        'exception match'
61	POP_JUMP_IF_FALSE '79'
64	POP_TOP           None
65	POP_TOP           None
66	POP_TOP           None

67	LOAD_CONST        '... '
70	LOAD_GLOBAL       'sys'
73	STORE_ATTR        'ps2'
76	JUMP_FORWARD      '80'
79	END_FINALLY       None
80_0	COME_FROM         '51'
80_1	COME_FROM         '79'

80	LOAD_CONST        'Type "help", "copyright", "credits" or "license" for more information.'
83	STORE_FAST        'cprt'

86	LOAD_FAST         'banner'
89	LOAD_CONST        None
92	COMPARE_OP        'is'
95	POP_JUMP_IF_FALSE '142'

98	LOAD_FAST         'self'
101	LOAD_ATTR         'write'
104	LOAD_CONST        'Python %s on %s\n%s\n(%s)\n'

107	LOAD_GLOBAL       'sys'
110	LOAD_ATTR         'version'
113	LOAD_GLOBAL       'sys'
116	LOAD_ATTR         'platform'
119	LOAD_FAST         'cprt'

122	LOAD_FAST         'self'
125	LOAD_ATTR         '__class__'
128	LOAD_ATTR         '__name__'
131	BUILD_TUPLE_4     None
134	BINARY_MODULO     None
135	CALL_FUNCTION_1   None
138	POP_TOP           None
139	JUMP_FORWARD      '165'

142	LOAD_FAST         'self'
145	LOAD_ATTR         'write'
148	LOAD_CONST        '%s\n'
151	LOAD_GLOBAL       'str'
154	LOAD_FAST         'banner'
157	CALL_FUNCTION_1   None
160	BINARY_MODULO     None
161	CALL_FUNCTION_1   None
164	POP_TOP           None
165_0	COME_FROM         '139'

165	LOAD_CONST        0
168	STORE_FAST        'more'

171	SETUP_LOOP        '387'

174	SETUP_EXCEPT      '337'

177	LOAD_FAST         'more'
180	POP_JUMP_IF_FALSE '195'

183	LOAD_GLOBAL       'sys'
186	LOAD_ATTR         'ps2'
189	STORE_FAST        'prompt'
192	JUMP_FORWARD      '204'

195	LOAD_GLOBAL       'sys'
198	LOAD_ATTR         'ps1'
201	STORE_FAST        'prompt'
204_0	COME_FROM         '192'

204	SETUP_EXCEPT      '287'

207	LOAD_FAST         'self'
210	LOAD_ATTR         'raw_input'
213	LOAD_FAST         'prompt'
216	CALL_FUNCTION_1   None
219	STORE_FAST        'line'

222	LOAD_GLOBAL       'getattr'
225	LOAD_GLOBAL       'sys'
228	LOAD_ATTR         'stdin'
231	LOAD_CONST        'encoding'
234	LOAD_CONST        None
237	CALL_FUNCTION_3   None
240	STORE_FAST        'encoding'

243	LOAD_FAST         'encoding'
246	POP_JUMP_IF_FALSE '283'
249	LOAD_GLOBAL       'isinstance'
252	LOAD_FAST         'line'
255	LOAD_GLOBAL       'unicode'
258	CALL_FUNCTION_2   None
261	UNARY_NOT         None
262_0	COME_FROM         '246'
262	POP_JUMP_IF_FALSE '283'

265	LOAD_FAST         'line'
268	LOAD_ATTR         'decode'
271	LOAD_FAST         'encoding'
274	CALL_FUNCTION_1   None
277	STORE_FAST        'line'
280	JUMP_FORWARD      '283'
283_0	COME_FROM         '280'
283	POP_BLOCK         None
284	JUMP_FORWARD      '318'
287_0	COME_FROM         '204'

287	DUP_TOP           None
288	LOAD_GLOBAL       'EOFError'
291	COMPARE_OP        'exception match'
294	POP_JUMP_IF_FALSE '317'
297	POP_TOP           None
298	POP_TOP           None
299	POP_TOP           None

300	LOAD_FAST         'self'
303	LOAD_ATTR         'write'
306	LOAD_CONST        '\n'
309	CALL_FUNCTION_1   None
312	POP_TOP           None

313	BREAK_LOOP        None
314	JUMP_FORWARD      '333'
317	END_FINALLY       None
318_0	COME_FROM         '284'

318	LOAD_FAST         'self'
321	LOAD_ATTR         'push'
324	LOAD_FAST         'line'
327	CALL_FUNCTION_1   None
330	STORE_FAST        'more'
333_0	COME_FROM         '317'
333	POP_BLOCK         None
334	JUMP_BACK         '174'
337_0	COME_FROM         '174'

337	DUP_TOP           None
338	LOAD_GLOBAL       'KeyboardInterrupt'
341	COMPARE_OP        'exception match'
344	POP_JUMP_IF_FALSE '382'
347	POP_TOP           None
348	POP_TOP           None
349	POP_TOP           None

350	LOAD_FAST         'self'
353	LOAD_ATTR         'write'
356	LOAD_CONST        '\nKeyboardInterrupt\n'
359	CALL_FUNCTION_1   None
362	POP_TOP           None

363	LOAD_FAST         'self'
366	LOAD_ATTR         'resetbuffer'
369	CALL_FUNCTION_0   None
372	POP_TOP           None

373	LOAD_CONST        0
376	STORE_FAST        'more'
379	JUMP_BACK         '174'
382	END_FINALLY       None
383_0	COME_FROM         '382'
383	JUMP_BACK         '174'
386	POP_BLOCK         None
387_0	COME_FROM         '171'
387	LOAD_CONST        None
390	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 386

    def push(self, line):
        """Push a line to the interpreter.
        
        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is 1 if more input is required, 0 if the line was dealt
        with in some way (this is the same as runsource()).
        
        """
        self.buffer.append(line)
        source = '\n'.join(self.buffer)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetbuffer()
        return more

    def raw_input(self, prompt = ''):
        """Write a prompt and read a line.
        
        The returned line does not include the trailing newline.
        When the user enters the EOF key sequence, EOFError is raised.
        
        The base implementation uses the built-in function
        raw_input(); a subclass may replace this with a different
        implementation.
        
        """
        return raw_input(prompt)


def interact(banner = None, readfunc = None, local = None):
    """Closely emulate the interactive Python interpreter.
    
    This is a backwards compatible interface to the InteractiveConsole
    class.  When readfunc is not specified, it attempts to import the
    readline module to enable GNU readline if it is available.
    
    Arguments (all optional, all default to None):
    
    banner -- passed to InteractiveConsole.interact()
    readfunc -- if not None, replaces InteractiveConsole.raw_input()
    local -- passed to InteractiveInterpreter.__init__()
    
    """
    console = InteractiveConsole(local)
    if readfunc is not None:
        console.raw_input = readfunc
    else:
        try:
            import readline
        except ImportError:
            pass

    console.interact(banner)
    return


if __name__ == '__main__':
    interact()