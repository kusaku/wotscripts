# Embedded file name: scripts/common/Lib/idlelib/SearchEngine.py
import re
from Tkinter import *
import tkMessageBox

def get(root):
    if not hasattr(root, '_searchengine'):
        root._searchengine = SearchEngine(root)
    return root._searchengine


class SearchEngine:

    def __init__(self, root):
        self.root = root
        self.patvar = StringVar(root)
        self.revar = BooleanVar(root)
        self.casevar = BooleanVar(root)
        self.wordvar = BooleanVar(root)
        self.wrapvar = BooleanVar(root)
        self.wrapvar.set(1)
        self.backvar = BooleanVar(root)

    def getpat(self):
        return self.patvar.get()

    def setpat(self, pat):
        self.patvar.set(pat)

    def isre(self):
        return self.revar.get()

    def iscase(self):
        return self.casevar.get()

    def isword(self):
        return self.wordvar.get()

    def iswrap(self):
        return self.wrapvar.get()

    def isback(self):
        return self.backvar.get()

    def getcookedpat(self):
        pat = self.getpat()
        if not self.isre():
            pat = re.escape(pat)
        if self.isword():
            pat = '\\b%s\\b' % pat
        return pat

    def getprog(self):
        pat = self.getpat()
        if not pat:
            self.report_error(pat, 'Empty regular expression')
            return None
        else:
            pat = self.getcookedpat()
            flags = 0
            if not self.iscase():
                flags = flags | re.IGNORECASE
            try:
                prog = re.compile(pat, flags)
            except re.error as what:
                try:
                    msg, col = what
                except:
                    msg = str(what)
                    col = -1

                self.report_error(pat, msg, col)
                return None

            return prog

    def report_error(self, pat, msg, col = -1):
        msg = 'Error: ' + str(msg)
        if pat:
            msg = msg + '\np\\Pattern: ' + str(pat)
        if col >= 0:
            msg = msg + '\nOffset: ' + str(col)
        tkMessageBox.showerror('Regular expression error', msg, master=self.root)

    def setcookedpat(self, pat):
        if self.isre():
            pat = re.escape(pat)
        self.setpat(pat)

    def search_text(self, text, prog = None, ok = 0):
        """Search a text widget for the pattern.
        
        If prog is given, it should be the precompiled pattern.
        Return a tuple (lineno, matchobj); None if not found.
        
        This obeys the wrap and direction (back) settings.
        
        The search starts at the selection (if there is one) or
        at the insert mark (otherwise).  If the search is forward,
        it starts at the right of the selection; for a backward
        search, it starts at the left end.  An empty match exactly
        at either end of the selection (or at the insert mark if
        there is no selection) is ignored  unless the ok flag is true
        -- this is done to guarantee progress.
        
        If the search is allowed to wrap around, it will return the
        original selection if (and only if) it is the only match.
        
        """
        if not prog:
            prog = self.getprog()
            if not prog:
                return None
        wrap = self.wrapvar.get()
        first, last = get_selection(text)
        if self.isback():
            if ok:
                start = last
            else:
                start = first
            line, col = get_line_col(start)
            res = self.search_backward(text, prog, line, col, wrap, ok)
        else:
            if ok:
                start = first
            else:
                start = last
            line, col = get_line_col(start)
            res = self.search_forward(text, prog, line, col, wrap, ok)
        return res

    def search_forward(self, text, prog, line, col, wrap, ok = 0):
        wrapped = 0
        startline = line
        chars = text.get('%d.0' % line, '%d.0' % (line + 1))
        while chars:
            m = prog.search(chars[:-1], col)
            if m:
                if ok or m.end() > col:
                    return (line, m)
            line = line + 1
            if wrapped and line > startline:
                break
            col = 0
            ok = 1
            chars = text.get('%d.0' % line, '%d.0' % (line + 1))
            if not chars and wrap:
                wrapped = 1
                wrap = 0
                line = 1
                chars = text.get('1.0', '2.0')

        return None

    def search_backward--- This code section failed: ---

0	LOAD_CONST        0
3	STORE_FAST        'wrapped'

6	LOAD_FAST         'line'
9	STORE_FAST        'startline'

12	LOAD_FAST         'text'
15	LOAD_ATTR         'get'
18	LOAD_CONST        '%d.0'
21	LOAD_FAST         'line'
24	BINARY_MODULO     None
25	LOAD_CONST        '%d.0'
28	LOAD_FAST         'line'
31	LOAD_CONST        1
34	BINARY_ADD        None
35	BINARY_MODULO     None
36	CALL_FUNCTION_2   None
39	STORE_FAST        'chars'

42	SETUP_LOOP        '280'

45	LOAD_GLOBAL       'search_reverse'
48	LOAD_FAST         'prog'
51	LOAD_FAST         'chars'
54	LOAD_CONST        -1
57	SLICE+2           None
58	LOAD_FAST         'col'
61	CALL_FUNCTION_3   None
64	STORE_FAST        'm'

67	LOAD_FAST         'm'
70	POP_JUMP_IF_FALSE '110'

73	LOAD_FAST         'ok'
76	POP_JUMP_IF_TRUE  '97'
79	LOAD_FAST         'm'
82	LOAD_ATTR         'start'
85	CALL_FUNCTION_0   None
88	LOAD_FAST         'col'
91	COMPARE_OP        '<'
94_0	COME_FROM         '76'
94	POP_JUMP_IF_FALSE '110'

97	LOAD_FAST         'line'
100	LOAD_FAST         'm'
103	BUILD_TUPLE_2     None
106	RETURN_END_IF     None
107	JUMP_FORWARD      '110'
110_0	COME_FROM         '107'

110	LOAD_FAST         'line'
113	LOAD_CONST        1
116	BINARY_SUBTRACT   None
117	STORE_FAST        'line'

120	LOAD_FAST         'wrapped'
123	POP_JUMP_IF_FALSE '142'
126	LOAD_FAST         'line'
129	LOAD_FAST         'startline'
132	COMPARE_OP        '<'
135_0	COME_FROM         '123'
135	POP_JUMP_IF_FALSE '142'

138	BREAK_LOOP        None
139	JUMP_FORWARD      '142'
142_0	COME_FROM         '139'

142	LOAD_CONST        1
145	STORE_FAST        'ok'

148	LOAD_FAST         'line'
151	LOAD_CONST        0
154	COMPARE_OP        '<='
157	POP_JUMP_IF_FALSE '230'

160	LOAD_FAST         'wrap'
163	POP_JUMP_IF_TRUE  '170'

166	BREAK_LOOP        None
167	JUMP_FORWARD      '170'
170_0	COME_FROM         '167'

170	LOAD_CONST        1
173	STORE_FAST        'wrapped'

176	LOAD_CONST        0
179	STORE_FAST        'wrap'

182	LOAD_FAST         'text'
185	LOAD_ATTR         'index'
188	LOAD_CONST        'end-1c'
191	CALL_FUNCTION_1   None
194	STORE_FAST        'pos'

197	LOAD_GLOBAL       'map'
200	LOAD_GLOBAL       'int'
203	LOAD_FAST         'pos'
206	LOAD_ATTR         'split'
209	LOAD_CONST        '.'
212	CALL_FUNCTION_1   None
215	CALL_FUNCTION_2   None
218	UNPACK_SEQUENCE_2 None
221	STORE_FAST        'line'
224	STORE_FAST        'col'
227	JUMP_FORWARD      '230'
230_0	COME_FROM         '227'

230	LOAD_FAST         'text'
233	LOAD_ATTR         'get'
236	LOAD_CONST        '%d.0'
239	LOAD_FAST         'line'
242	BINARY_MODULO     None
243	LOAD_CONST        '%d.0'
246	LOAD_FAST         'line'
249	LOAD_CONST        1
252	BINARY_ADD        None
253	BINARY_MODULO     None
254	CALL_FUNCTION_2   None
257	STORE_FAST        'chars'

260	LOAD_GLOBAL       'len'
263	LOAD_FAST         'chars'
266	CALL_FUNCTION_1   None
269	LOAD_CONST        1
272	BINARY_SUBTRACT   None
273	STORE_FAST        'col'
276	JUMP_BACK         '45'
279	POP_BLOCK         None
280_0	COME_FROM         '42'

280	LOAD_CONST        None
283	RETURN_VALUE      None

Syntax error at or near `POP_BLOCK' token at offset 279


def search_reverse(prog, chars, col):
    m = prog.search(chars)
    if not m:
        return
    else:
        found = None
        i, j = m.span()
        while i < col and j <= col:
            found = m
            if i == j:
                j = j + 1
            m = prog.search(chars, j)
            if not m:
                break
            i, j = m.span()

        return found


def get_selection(text):
    try:
        first = text.index('sel.first')
        last = text.index('sel.last')
    except TclError:
        first = last = None

    if not first:
        first = text.index('insert')
    if not last:
        last = first
    return (first, last)


def get_line_col(index):
    line, col = map(int, index.split('.'))
    return (line, col)