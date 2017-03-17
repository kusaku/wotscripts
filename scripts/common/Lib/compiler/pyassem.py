# Embedded file name: scripts/common/Lib/compiler/pyassem.py
"""A flow graph representation for Python bytecode"""
import dis
import types
import sys
from compiler import misc
from compiler.consts import CO_OPTIMIZED, CO_NEWLOCALS, CO_VARARGS, CO_VARKEYWORDS

class FlowGraph():

    def __init__(self):
        self.current = self.entry = Block()
        self.exit = Block('exit')
        self.blocks = misc.Set()
        self.blocks.add(self.entry)
        self.blocks.add(self.exit)

    def startBlock(self, block):
        if self._debug:
            if self.current:
                print 'end', repr(self.current)
                print '    next', self.current.next
                print '    prev', self.current.prev
                print '   ', self.current.get_children()
            print repr(block)
        self.current = block

    def nextBlock(self, block = None):
        if block is None:
            block = self.newBlock()
        self.current.addNext(block)
        self.startBlock(block)
        return

    def newBlock(self):
        b = Block()
        self.blocks.add(b)
        return b

    def startExitBlock(self):
        self.startBlock(self.exit)

    _debug = 0

    def _enable_debug(self):
        self._debug = 1

    def _disable_debug(self):
        self._debug = 0

    def emit(self, *inst):
        if self._debug:
            print '\t', inst
        if len(inst) == 2 and isinstance(inst[1], Block):
            self.current.addOutEdge(inst[1])
        self.current.emit(inst)

    def getBlocksInOrder(self):
        """Return the blocks in reverse postorder
        
        i.e. each node appears before all of its successors
        """
        order = order_blocks(self.entry, self.exit)
        return order

    def getBlocks(self):
        return self.blocks.elements()

    def getRoot(self):
        """Return nodes appropriate for use with dominator"""
        return self.entry

    def getContainedGraphs(self):
        l = []
        for b in self.getBlocks():
            l.extend(b.getContainedGraphs())

        return l


def order_blocks--- This code section failed: ---

0	BUILD_LIST_0      None
3	STORE_FAST        'order'

6	LOAD_GLOBAL       'set'
9	CALL_FUNCTION_0   None
12	STORE_DEREF       'remaining'

15	LOAD_FAST         'start_block'
18	BUILD_LIST_1      None
21	STORE_FAST        'todo'

24	SETUP_LOOP        '131'
27	LOAD_FAST         'todo'
30	POP_JUMP_IF_FALSE '130'

33	LOAD_FAST         'todo'
36	LOAD_ATTR         'pop'
39	CALL_FUNCTION_0   None
42	STORE_FAST        'b'

45	LOAD_FAST         'b'
48	LOAD_DEREF        'remaining'
51	COMPARE_OP        'in'
54	POP_JUMP_IF_FALSE '63'

57	CONTINUE          '27'
60	JUMP_FORWARD      '63'
63_0	COME_FROM         '60'

63	LOAD_DEREF        'remaining'
66	LOAD_ATTR         'add'
69	LOAD_FAST         'b'
72	CALL_FUNCTION_1   None
75	POP_TOP           None

76	SETUP_LOOP        '127'
79	LOAD_FAST         'b'
82	LOAD_ATTR         'get_children'
85	CALL_FUNCTION_0   None
88	GET_ITER          None
89	FOR_ITER          '126'
92	STORE_FAST        'c'

95	LOAD_FAST         'c'
98	LOAD_DEREF        'remaining'
101	COMPARE_OP        'not in'
104	POP_JUMP_IF_FALSE '89'

107	LOAD_FAST         'todo'
110	LOAD_ATTR         'append'
113	LOAD_FAST         'c'
116	CALL_FUNCTION_1   None
119	POP_TOP           None
120	JUMP_BACK         '89'
123	JUMP_BACK         '89'
126	POP_BLOCK         None
127_0	COME_FROM         '76'
127	JUMP_BACK         '27'
130	POP_BLOCK         None
131_0	COME_FROM         '24'

131	BUILD_MAP         None
134	STORE_DEREF       'dominators'

137	SETUP_LOOP        '341'
140	LOAD_DEREF        'remaining'
143	GET_ITER          None
144	FOR_ITER          '340'
147	STORE_FAST        'b'

150	LOAD_GLOBAL       '__debug__'
153	POP_JUMP_IF_FALSE '215'
156	LOAD_FAST         'b'
159	LOAD_ATTR         'next'
162_0	COME_FROM         '153'
162	POP_JUMP_IF_FALSE '215'

165	LOAD_FAST         'b'
168	LOAD_FAST         'b'
171	LOAD_ATTR         'next'
174	LOAD_CONST        0
177	BINARY_SUBSCR     None
178	LOAD_ATTR         'prev'
181	LOAD_CONST        0
184	BINARY_SUBSCR     None
185	COMPARE_OP        'is'
188	POP_JUMP_IF_TRUE  '215'
191	LOAD_ASSERT       'AssertionError'
194	LOAD_FAST         'b'
197	LOAD_FAST         'b'
200	LOAD_ATTR         'next'
203	BUILD_TUPLE_2     None
206	CALL_FUNCTION_1   None
209	RAISE_VARARGS_1   None
212	JUMP_FORWARD      '215'
215_0	COME_FROM         '212'

215	LOAD_DEREF        'dominators'
218	LOAD_ATTR         'setdefault'
221	LOAD_FAST         'b'
224	LOAD_GLOBAL       'set'
227	CALL_FUNCTION_0   None
230	CALL_FUNCTION_2   None
233	POP_TOP           None

234	SETUP_LOOP        '337'
237	LOAD_FAST         'b'
240	LOAD_ATTR         'get_followers'
243	CALL_FUNCTION_0   None
246	GET_ITER          None
247	FOR_ITER          '336'
250	STORE_FAST        'c'

253	SETUP_LOOP        '333'

256	LOAD_DEREF        'dominators'
259	LOAD_ATTR         'setdefault'
262	LOAD_FAST         'c'
265	LOAD_GLOBAL       'set'
268	CALL_FUNCTION_0   None
271	CALL_FUNCTION_2   None
274	LOAD_ATTR         'add'
277	LOAD_FAST         'b'
280	CALL_FUNCTION_1   None
283	POP_TOP           None

284	LOAD_FAST         'c'
287	LOAD_ATTR         'prev'
290	POP_JUMP_IF_FALSE '328'
293	LOAD_FAST         'c'
296	LOAD_ATTR         'prev'
299	LOAD_CONST        0
302	BINARY_SUBSCR     None
303	LOAD_FAST         'b'
306	COMPARE_OP        'is not'
309_0	COME_FROM         '290'
309	POP_JUMP_IF_FALSE '328'

312	LOAD_FAST         'c'
315	LOAD_ATTR         'prev'
318	LOAD_CONST        0
321	BINARY_SUBSCR     None
322	STORE_FAST        'c'
325	JUMP_BACK         '256'

328	BREAK_LOOP        None
329	JUMP_BACK         '256'
332	POP_BLOCK         None
333_0	COME_FROM         '253'
333	JUMP_BACK         '247'
336	POP_BLOCK         None
337_0	COME_FROM         '234'
337	JUMP_BACK         '144'
340	POP_BLOCK         None
341_0	COME_FROM         '137'

341	LOAD_CLOSURE      'dominators'
344	LOAD_CLOSURE      'remaining'
350	LOAD_CONST        '<code_object find_next>'
353	MAKE_CLOSURE_0    None
356	STORE_FAST        'find_next'

359	LOAD_FAST         'start_block'
362	STORE_FAST        'b'

365	SETUP_LOOP        '486'

368	LOAD_FAST         'order'
371	LOAD_ATTR         'append'
374	LOAD_FAST         'b'
377	CALL_FUNCTION_1   None
380	POP_TOP           None

381	LOAD_DEREF        'remaining'
384	LOAD_ATTR         'discard'
387	LOAD_FAST         'b'
390	CALL_FUNCTION_1   None
393	POP_TOP           None

394	LOAD_FAST         'b'
397	LOAD_ATTR         'next'
400	POP_JUMP_IF_FALSE '422'

403	LOAD_FAST         'b'
406	LOAD_ATTR         'next'
409	LOAD_CONST        0
412	BINARY_SUBSCR     None
413	STORE_FAST        'b'

416	CONTINUE          '368'
419	JUMP_FORWARD      '463'

422	LOAD_FAST         'b'
425	LOAD_FAST         'exit_block'
428	COMPARE_OP        'is not'
431	POP_JUMP_IF_FALSE '463'
434	LOAD_FAST         'b'
437	LOAD_ATTR         'has_unconditional_transfer'
440	CALL_FUNCTION_0   None
443	UNARY_NOT         None
444_0	COME_FROM         '431'
444	POP_JUMP_IF_FALSE '463'

447	LOAD_FAST         'order'
450	LOAD_ATTR         'append'
453	LOAD_FAST         'exit_block'
456	CALL_FUNCTION_1   None
459	POP_TOP           None
460	JUMP_FORWARD      '463'
463_0	COME_FROM         '419'
463_1	COME_FROM         '460'

463	LOAD_DEREF        'remaining'
466	POP_JUMP_IF_TRUE  '473'

469	BREAK_LOOP        None
470	JUMP_FORWARD      '473'
473_0	COME_FROM         '470'

473	LOAD_FAST         'find_next'
476	CALL_FUNCTION_0   None
479	STORE_FAST        'b'
482	JUMP_BACK         '368'
485	POP_BLOCK         None
486_0	COME_FROM         '365'

486	LOAD_FAST         'order'
489	RETURN_VALUE      None
-1	RETURN_LAST       None

Syntax error at or near `POP_BLOCK' token at offset 332


class Block():
    _count = 0

    def __init__(self, label = ''):
        self.insts = []
        self.outEdges = set()
        self.label = label
        self.bid = Block._count
        self.next = []
        self.prev = []
        Block._count = Block._count + 1

    def __repr__(self):
        if self.label:
            return '<block %s id=%d>' % (self.label, self.bid)
        else:
            return '<block id=%d>' % self.bid

    def __str__(self):
        insts = map(str, self.insts)
        return '<block %s %d:\n%s>' % (self.label, self.bid, '\n'.join(insts))

    def emit(self, inst):
        op = inst[0]
        self.insts.append(inst)

    def getInstructions(self):
        return self.insts

    def addOutEdge(self, block):
        self.outEdges.add(block)

    def addNext(self, block):
        self.next.append(block)
        raise len(self.next) == 1 or AssertionError(map(str, self.next))
        block.prev.append(self)
        raise len(block.prev) == 1 or AssertionError(map(str, block.prev))

    _uncond_transfer = ('RETURN_VALUE', 'RAISE_VARARGS', 'JUMP_ABSOLUTE', 'JUMP_FORWARD', 'CONTINUE_LOOP')

    def has_unconditional_transfer(self):
        """Returns True if there is an unconditional transfer to an other block
        at the end of this block. This means there is no risk for the bytecode
        executer to go past this block's bytecode."""
        try:
            op, arg = self.insts[-1]
        except (IndexError, ValueError):
            return

        return op in self._uncond_transfer

    def get_children(self):
        return list(self.outEdges) + self.next

    def get_followers(self):
        """Get the whole list of followers, including the next block."""
        followers = set(self.next)
        for inst in self.insts:
            if inst[0] in PyFlowGraph.hasjrel:
                followers.add(inst[1])

        return followers

    def getContainedGraphs(self):
        """Return all graphs contained within this block.
        
        For example, a MAKE_FUNCTION block will contain a reference to
        the graph for the function body.
        """
        contained = []
        for inst in self.insts:
            if len(inst) == 1:
                continue
            op = inst[1]
            if hasattr(op, 'graph'):
                contained.append(op.graph)

        return contained


RAW = 'RAW'
FLAT = 'FLAT'
CONV = 'CONV'
DONE = 'DONE'

class PyFlowGraph(FlowGraph):
    super_init = FlowGraph.__init__

    def __init__(self, name, filename, args = (), optimized = 0, klass = None):
        self.super_init()
        self.name = name
        self.filename = filename
        self.docstring = None
        self.args = args
        self.argcount = getArgCount(args)
        self.klass = klass
        if optimized:
            self.flags = CO_OPTIMIZED | CO_NEWLOCALS
        else:
            self.flags = 0
        self.consts = []
        self.names = []
        self.freevars = []
        self.cellvars = []
        self.closure = []
        self.varnames = list(args) or []
        for i in range(len(self.varnames)):
            var = self.varnames[i]
            if isinstance(var, TupleArg):
                self.varnames[i] = var.getName()

        self.stage = RAW
        return

    def setDocstring(self, doc):
        self.docstring = doc

    def setFlag(self, flag):
        self.flags = self.flags | flag
        if flag == CO_VARARGS:
            self.argcount = self.argcount - 1

    def checkFlag(self, flag):
        if self.flags & flag:
            return 1

    def setFreeVars(self, names):
        self.freevars = list(names)

    def setCellVars(self, names):
        self.cellvars = names

    def getCode(self):
        """Get a Python code object"""
        raise self.stage == RAW or AssertionError
        self.computeStackDepth()
        self.flattenGraph()
        raise self.stage == FLAT or AssertionError
        self.convertArgs()
        raise self.stage == CONV or AssertionError
        self.makeByteCode()
        raise self.stage == DONE or AssertionError
        return self.newCodeObject()

    def dump(self, io = None):
        if io:
            save = sys.stdout
            sys.stdout = io
        pc = 0
        for t in self.insts:
            opname = t[0]
            if opname == 'SET_LINENO':
                print
            if len(t) == 1:
                print '\t', '%3d' % pc, opname
                pc = pc + 1
            else:
                print '\t', '%3d' % pc, opname, t[1]
                pc = pc + 3

        if io:
            sys.stdout = save

    def computeStackDepth(self):
        """Compute the max stack depth.
        
        Approach is to compute the stack effect of each basic block.
        Then find the path through the code with the largest total
        effect.
        """
        depth = {}
        exit = None
        for b in self.getBlocks():
            depth[b] = findDepth(b.getInstructions())

        seen = {}

        def max_depth(b, d):
            if b in seen:
                return d
            seen[b] = 1
            d = d + depth[b]
            children = b.get_children()
            if children:
                return max([ max_depth(c, d) for c in children ])
            elif not b.label == 'exit':
                return max_depth(self.exit, d)
            else:
                return d

        self.stacksize = max_depth(self.entry, 0)
        return

    def flattenGraph(self):
        """Arrange the blocks in order and resolve jumps"""
        raise self.stage == RAW or AssertionError
        self.insts = insts = []
        pc = 0
        begin = {}
        end = {}
        for b in self.getBlocksInOrder():
            begin[b] = pc
            for inst in b.getInstructions():
                insts.append(inst)
                if len(inst) == 1:
                    pc = pc + 1
                elif inst[0] != 'SET_LINENO':
                    pc = pc + 3

            end[b] = pc

        pc = 0
        for i in range(len(insts)):
            inst = insts[i]
            if len(inst) == 1:
                pc = pc + 1
            elif inst[0] != 'SET_LINENO':
                pc = pc + 3
            opname = inst[0]
            if opname in self.hasjrel:
                oparg = inst[1]
                offset = begin[oparg] - pc
                insts[i] = (opname, offset)
            elif opname in self.hasjabs:
                insts[i] = (opname, begin[inst[1]])

        self.stage = FLAT

    hasjrel = set()
    for i in dis.hasjrel:
        hasjrel.add(dis.opname[i])

    hasjabs = set()
    for i in dis.hasjabs:
        hasjabs.add(dis.opname[i])

    def convertArgs(self):
        """Convert arguments from symbolic to concrete form"""
        raise self.stage == FLAT or AssertionError
        self.consts.insert(0, self.docstring)
        self.sort_cellvars()
        for i in range(len(self.insts)):
            t = self.insts[i]
            if len(t) == 2:
                opname, oparg = t
                conv = self._converters.get(opname, None)
                if conv:
                    self.insts[i] = (opname, conv(self, oparg))

        self.stage = CONV
        return

    def sort_cellvars(self):
        """Sort cellvars in the order of varnames and prune from freevars.
        """
        cells = {}
        for name in self.cellvars:
            cells[name] = 1

        self.cellvars = [ name for name in self.varnames if name in cells ]
        for name in self.cellvars:
            del cells[name]

        self.cellvars = self.cellvars + cells.keys()
        self.closure = self.cellvars + self.freevars

    def _lookupName(self, name, list):
        """Return index of name in list, appending if necessary
        
        This routine uses a list instead of a dictionary, because a
        dictionary can't store two different keys if the keys have the
        same value but different types, e.g. 2 and 2L.  The compiler
        must treat these two separately, so it does an explicit type
        comparison before comparing the values.
        """
        t = type(name)
        for i in range(len(list)):
            if t == type(list[i]) and list[i] == name:
                return i

        end = len(list)
        list.append(name)
        return end

    _converters = {}

    def _convert_LOAD_CONST(self, arg):
        if hasattr(arg, 'getCode'):
            arg = arg.getCode()
        return self._lookupName(arg, self.consts)

    def _convert_LOAD_FAST(self, arg):
        self._lookupName(arg, self.names)
        return self._lookupName(arg, self.varnames)

    _convert_STORE_FAST = _convert_LOAD_FAST
    _convert_DELETE_FAST = _convert_LOAD_FAST

    def _convert_LOAD_NAME(self, arg):
        if self.klass is None:
            self._lookupName(arg, self.varnames)
        return self._lookupName(arg, self.names)

    def _convert_NAME(self, arg):
        if self.klass is None:
            self._lookupName(arg, self.varnames)
        return self._lookupName(arg, self.names)

    _convert_STORE_NAME = _convert_NAME
    _convert_DELETE_NAME = _convert_NAME
    _convert_IMPORT_NAME = _convert_NAME
    _convert_IMPORT_FROM = _convert_NAME
    _convert_STORE_ATTR = _convert_NAME
    _convert_LOAD_ATTR = _convert_NAME
    _convert_DELETE_ATTR = _convert_NAME
    _convert_LOAD_GLOBAL = _convert_NAME
    _convert_STORE_GLOBAL = _convert_NAME
    _convert_DELETE_GLOBAL = _convert_NAME

    def _convert_DEREF(self, arg):
        self._lookupName(arg, self.names)
        self._lookupName(arg, self.varnames)
        return self._lookupName(arg, self.closure)

    _convert_LOAD_DEREF = _convert_DEREF
    _convert_STORE_DEREF = _convert_DEREF

    def _convert_LOAD_CLOSURE(self, arg):
        self._lookupName(arg, self.varnames)
        return self._lookupName(arg, self.closure)

    _cmp = list(dis.cmp_op)

    def _convert_COMPARE_OP(self, arg):
        return self._cmp.index(arg)

    for name, obj in locals().items():
        if name[:9] == '_convert_':
            opname = name[9:]
            _converters[opname] = obj

    del name
    del obj
    del opname

    def makeByteCode(self):
        raise self.stage == CONV or AssertionError
        self.lnotab = lnotab = LineAddrTable()
        for t in self.insts:
            opname = t[0]
            if len(t) == 1:
                lnotab.addCode(self.opnum[opname])
            else:
                oparg = t[1]
                if opname == 'SET_LINENO':
                    lnotab.nextLine(oparg)
                    continue
                hi, lo = twobyte(oparg)
                try:
                    lnotab.addCode(self.opnum[opname], lo, hi)
                except ValueError:
                    print opname, oparg
                    print self.opnum[opname], lo, hi
                    raise

        self.stage = DONE

    opnum = {}
    for num in range(len(dis.opname)):
        opnum[dis.opname[num]] = num

    del num

    def newCodeObject(self):
        if not self.stage == DONE:
            raise AssertionError
            if self.flags & CO_NEWLOCALS == 0:
                nlocals = 0
            else:
                nlocals = len(self.varnames)
            argcount = self.argcount
            argcount = self.flags & CO_VARKEYWORDS and argcount - 1
        return types.CodeType(argcount, nlocals, self.stacksize, self.flags, self.lnotab.getCode(), self.getConsts(), tuple(self.names), tuple(self.varnames), self.filename, self.name, self.lnotab.firstline, self.lnotab.getTable(), tuple(self.freevars), tuple(self.cellvars))

    def getConsts(self):
        """Return a tuple for the const slot of the code object
        
        Must convert references to code (MAKE_FUNCTION) to code
        objects recursively.
        """
        l = []
        for elt in self.consts:
            if isinstance(elt, PyFlowGraph):
                elt = elt.getCode()
            l.append(elt)

        return tuple(l)


def isJump(opname):
    if opname[:4] == 'JUMP':
        return 1


class TupleArg():
    """Helper for marking func defs with nested tuples in arglist"""

    def __init__(self, count, names):
        self.count = count
        self.names = names

    def __repr__(self):
        return 'TupleArg(%s, %s)' % (self.count, self.names)

    def getName(self):
        return '.%d' % self.count


def getArgCount(args):
    argcount = len(args)
    if args:
        for arg in args:
            if isinstance(arg, TupleArg):
                numNames = len(misc.flatten(arg.names))
                argcount = argcount - numNames

    return argcount


def twobyte(val):
    """Convert an int argument into high and low bytes"""
    raise isinstance(val, int) or AssertionError
    return divmod(val, 256)


class LineAddrTable():
    """lnotab
    
    This class builds the lnotab, which is documented in compile.c.
    Here's a brief recap:
    
    For each SET_LINENO instruction after the first one, two bytes are
    added to lnotab.  (In some cases, multiple two-byte entries are
    added.)  The first byte is the distance in bytes between the
    instruction for the last SET_LINENO and the current SET_LINENO.
    The second byte is offset in line numbers.  If either offset is
    greater than 255, multiple two-byte entries are added -- see
    compile.c for the delicate details.
    """

    def __init__(self):
        self.code = []
        self.codeOffset = 0
        self.firstline = 0
        self.lastline = 0
        self.lastoff = 0
        self.lnotab = []

    def addCode(self, *args):
        for arg in args:
            self.code.append(chr(arg))

        self.codeOffset = self.codeOffset + len(args)

    def nextLine(self, lineno):
        if self.firstline == 0:
            self.firstline = lineno
            self.lastline = lineno
        else:
            addr = self.codeOffset - self.lastoff
            line = lineno - self.lastline
            if line >= 0:
                push = self.lnotab.append
                while addr > 255:
                    push(255)
                    push(0)
                    addr -= 255

                while line > 255:
                    push(addr)
                    push(255)
                    line -= 255
                    addr = 0

                if addr > 0 or line > 0:
                    push(addr)
                    push(line)
                self.lastline = lineno
                self.lastoff = self.codeOffset

    def getCode(self):
        return ''.join(self.code)

    def getTable(self):
        return ''.join(map(chr, self.lnotab))


class StackDepthTracker():

    def findDepth(self, insts, debug = 0):
        depth = 0
        maxDepth = 0
        for i in insts:
            opname = i[0]
            if debug:
                print i,
            delta = self.effect.get(opname, None)
            if delta is not None:
                depth = depth + delta
            else:
                for pat, pat_delta in self.patterns:
                    if opname[:len(pat)] == pat:
                        delta = pat_delta
                        depth = depth + delta
                        break

                if delta is None:
                    meth = getattr(self, opname, None)
                    if meth is not None:
                        depth = depth + meth(i[1])
            if depth > maxDepth:
                maxDepth = depth
            if debug:
                print depth, maxDepth

        return maxDepth

    effect = {'POP_TOP': -1,
     'DUP_TOP': 1,
     'LIST_APPEND': -1,
     'SET_ADD': -1,
     'MAP_ADD': -2,
     'SLICE+1': -1,
     'SLICE+2': -1,
     'SLICE+3': -2,
     'STORE_SLICE+0': -1,
     'STORE_SLICE+1': -2,
     'STORE_SLICE+2': -2,
     'STORE_SLICE+3': -3,
     'DELETE_SLICE+0': -1,
     'DELETE_SLICE+1': -2,
     'DELETE_SLICE+2': -2,
     'DELETE_SLICE+3': -3,
     'STORE_SUBSCR': -3,
     'DELETE_SUBSCR': -2,
     'PRINT_ITEM': -1,
     'RETURN_VALUE': -1,
     'YIELD_VALUE': -1,
     'EXEC_STMT': -3,
     'BUILD_CLASS': -2,
     'STORE_NAME': -1,
     'STORE_ATTR': -2,
     'DELETE_ATTR': -1,
     'STORE_GLOBAL': -1,
     'BUILD_MAP': 1,
     'COMPARE_OP': -1,
     'STORE_FAST': -1,
     'IMPORT_STAR': -1,
     'IMPORT_NAME': -1,
     'IMPORT_FROM': 1,
     'LOAD_ATTR': 0,
     'SETUP_EXCEPT': 3,
     'SETUP_FINALLY': 3,
     'FOR_ITER': 1,
     'WITH_CLEANUP': -1}
    patterns = [('BINARY_', -1), ('LOAD_', 1)]

    def UNPACK_SEQUENCE(self, count):
        return count - 1

    def BUILD_TUPLE(self, count):
        return -count + 1

    def BUILD_LIST(self, count):
        return -count + 1

    def BUILD_SET(self, count):
        return -count + 1

    def CALL_FUNCTION(self, argc):
        hi, lo = divmod(argc, 256)
        return -(lo + hi * 2)

    def CALL_FUNCTION_VAR(self, argc):
        return self.CALL_FUNCTION(argc) - 1

    def CALL_FUNCTION_KW(self, argc):
        return self.CALL_FUNCTION(argc) - 1

    def CALL_FUNCTION_VAR_KW(self, argc):
        return self.CALL_FUNCTION(argc) - 2

    def MAKE_FUNCTION(self, argc):
        return -argc

    def MAKE_CLOSURE(self, argc):
        return -argc

    def BUILD_SLICE(self, argc):
        if argc == 2:
            return -1
        if argc == 3:
            return -2

    def DUP_TOPX(self, argc):
        return argc


findDepth = StackDepthTracker().findDepth